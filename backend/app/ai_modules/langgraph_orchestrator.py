import asyncio
import os
import typing
import logging
import httpx
import operator
from typing import Annotated, Dict, Any, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# Import the actual engines we built
from app.services.scraper import is_url, scrape_url
from app.services.rag_service import rag_service
from app.services.searxng_service import searxng_service
from app.services.ai_engine import verify_multimodal_content
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

def refine_search_query(text: str) -> str:
    """
    Refines conversational or messy raw text into a high-signal search query.
    Removes common filler phrases, punctuation, and selects key terms.
    """
    if not text:
        return ""
    
    # 1. Lowercase and clean known conversational filler phrases
    query = text.lower()
    fillers = [
        "is it true that", "can you verify if", "please check if", "did you hear",
        "is this true", "verification needed for", "verify this:", "fwd:", "forwarded"
    ]
    for filler in fillers:
        query = query.replace(filler, "")
        
    # 2. Clean punctuation
    for char in [".", ",", "?", "!", "\"", "'", "(", ")", "[", "]", "-", "_", ":", ";"]:
        query = query.replace(char, " ")
        
    # 3. Trim whitespace
    words = [w.strip() for w in query.split() if w.strip()]
    
    # 4. Stopwords filtering to prioritize high-signal keywords if query is long
    stopwords = {
        "is", "the", "a", "an", "and", "or", "but", "if", "then", "of", "to", "for", 
        "in", "on", "at", "by", "with", "about", "that", "this", "these", "those"
    }
    
    if len(words) > 6:
        # Filter stopwords to focus search
        filtered_words = [w for w in words if w not in stopwords]
        # Fallback to original words if everything was a stopword
        result_words = filtered_words if filtered_words else words
    else:
        result_words = words
        
    # Take up to 10 key terms to keep the query specific but not too narrow
    refined = " ".join(result_words[:10])
    return refined if refined else text[:100]

# Define the Graph State
class AgentState(TypedDict):
    raw_input: str
    extracted_claim: str
    historical_records: Annotated[List[str], operator.add]
    web_records: Annotated[List[str], operator.add]
    final_report: Dict[str, Any]
    webhook_status: str

class LangGraphOrchestrator:
    """
    Orchestrates the Sukoon AI verification process using LangGraph's StateGraph.
    This creates a deterministic, directed graph of specialized agents with parallel execution.
    """
    def __init__(self):
        # Initialize the StateGraph with our custom AgentState
        self.graph = StateGraph(AgentState)
        
        # Add the core agents (nodes)
        self.graph.add_node("supervisor_ingestion", self.supervisor_ingestion)
        self.graph.add_node("agent_a_scraper", self.agent_a_scraper)
        self.graph.add_node("agent_b_database", self.agent_b_database)
        self.graph.add_node("agent_c_web_search", self.agent_c_web_search)
        self.graph.add_node("agent_d_truth_evaluator", self.agent_d_truth_evaluator)
        self.graph.add_node("downstream_webhook", self.downstream_webhook)
        
        # Define the directed workflow (edges)
        self.graph.add_edge(START, "supervisor_ingestion")
        
        # Parallel Execution: Supervisor delegates to Agent A, Agent B, and Agent C concurrently
        self.graph.add_edge("supervisor_ingestion", "agent_a_scraper")
        self.graph.add_edge("supervisor_ingestion", "agent_b_database")
        self.graph.add_edge("supervisor_ingestion", "agent_c_web_search")
        
        # Fan-in: All three agents return results to Agent D
        self.graph.add_edge("agent_a_scraper", "agent_d_truth_evaluator")
        self.graph.add_edge("agent_b_database", "agent_d_truth_evaluator")
        self.graph.add_edge("agent_c_web_search", "agent_d_truth_evaluator")
        
        # Final Action: Trigger webhook and end
        self.graph.add_edge("agent_d_truth_evaluator", "downstream_webhook")
        self.graph.add_edge("downstream_webhook", END)
        
        # Compile the state graph into an executable runner
        self.runner = self.graph.compile()

    # Step 1: Task Ingestion & Delegation
    async def supervisor_ingestion(self, state: AgentState) -> AgentState:
        """Intercepts the request and delegates tasks."""
        logger.info("[LangGraph] Supervisor: Request intercepted. Delegating tasks...")
        return state

    # Step 2a: Agent A (The Media Scraper) - Runs in parallel
    async def agent_a_scraper(self, state: AgentState) -> AgentState:
        """Extracts text and metadata from the flagged content."""
        logger.info("[LangGraph] Agent A: Media Scraper analyzing input...")
        raw = state.get("raw_input", "")
        
        # Real logic: If it's a URL, use Playwright/BeautifulSoup hybrid scraper
        if is_url(raw):
            logger.info("[LangGraph] Agent A: URL detected. Firing scraper...")
            # scrape_url is synchronous — run in thread pool to avoid blocking the event loop
            extracted = await asyncio.to_thread(scrape_url, raw)
        else:
            extracted = raw
            
        # Break text into semantically cohesive 500-character chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_text(extracted)
        
        # We can pass the chunks joined by newlines to downstream models, 
        # which helps them process massive articles while retaining semantic meaning.
        chunked_claim = "\n\n".join(chunks)
            
        return {"extracted_claim": chunked_claim}

    # Step 2b: Agent B (The Database Specialist) - Runs in parallel
    async def agent_b_database(self, state: AgentState) -> AgentState:
        """Executes pgvector/Qdrant RAG search over historical records."""
        logger.info("[LangGraph] Agent B: Database Specialist querying vector DB...")
        raw = state.get("raw_input", "")
        
        # rag_service.retrieve_context is synchronous — run in thread pool to avoid blocking the event loop
        records_list = await asyncio.to_thread(rag_service.retrieve_context, raw, 3)
        
        if records_list:
            # Format the records for the AI
            formatted_records = "\n".join([f"- {r.get('title', 'Record')}: {r.get('text', '')}" for r in records_list])
            records = f"Found {len(records_list)} historical records:\n{formatted_records}"
        else:
            records = "Found historical record: No identical matches in Supabase."
            
        return {"historical_records": [records]}
    # Step 2c: Agent C (The Live Web Searcher) - Runs in parallel
    async def agent_c_web_search(self, state: AgentState) -> AgentState:
        """Executes SearXNG search to find live web context."""
        logger.info("[LangGraph] Agent C: Web Searcher querying SearXNG...")
        raw = state.get("raw_input", "")
        
        # Refine conversational text into high-signal search terms
        search_query = refine_search_query(raw)
        logger.info(f"[LangGraph] Agent C: Refined search query to: '{search_query}'")
        
        web_records = await searxng_service.search(query=search_query, top_k=3)
        return {"web_records": [web_records]}

    # Step 3: Synthesis and Debate
    async def agent_d_truth_evaluator(self, state: AgentState) -> AgentState:
        """The core LLM that synthesizes findings and writes the final JSON report."""
        logger.info("[LangGraph] Agent D: Truth Evaluator synthesizing findings...")
        claim = state.get("extracted_claim", "")
        
        historical_list = state.get("historical_records", [])
        web_list = state.get("web_records", [])
        
        historical_records = "\n\n".join(historical_list)
        web_records = "\n\n".join(web_list)
        
        # Combine both historical RAG data and Live Web Search data
        combined_context = f"=== HISTORICAL LOCAL RECORDS ===\n{historical_records}\n\n=== LIVE WEB SEARCH RECORDS ===\n{web_records}"
        
        # Real logic: Call LLM API using structured JSON schema
        response = await verify_multimodal_content(text_content=claim, retrieved_context=combined_context)
        
        if response.get("status") == "success":
            final_report = response.get("data", {})
        else:
            final_report = {
                "verdict": "⚪ Unable to Verify",
                "confidence_score": 0.0,
                "explanation": f"Evaluation failed: {response.get('message', 'Unknown Error')}"
            }
            
        return {"final_report": final_report}

    # Step 4: Downstream Workflow Trigger
    async def downstream_webhook(self, state: AgentState) -> AgentState:
        """
        Triggers external n8n webhook (notifying community moderators).
        Enforces strict timeouts and unique deduplication headers.
        """
        logger.info("[LangGraph] Webhook: Triggering downstream n8n automation...")
        webhook_url = os.getenv("N8N_WEBHOOK_URL", "http://localhost:8080/api/v1/n8n/webhook")
        
        # Resolve a unique task/verification ID for header tracking
        task_id = state.get("final_report", {}).get("verification_id", "unknown")
        if task_id == "unknown":
            import hashlib
            hasher = hashlib.sha256()
            hasher.update(str(state.get("raw_input", "")).encode("utf-8"))
            task_id = hasher.hexdigest()[:32]
            
        import time
        headers = {
            "X-Sukoon-Task-ID": str(task_id),
            "X-Sukoon-Timestamp": str(int(time.time()))
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    webhook_url,
                    json=state.get("final_report", {}),
                    headers=headers,
                    timeout=5.0
                )
                response.raise_for_status()
                logger.info(f"[LangGraph] Webhook: Downstream n8n automation completed with status {response.status_code}")
                return {"webhook_status": "success"}
        except httpx.TimeoutException as e:
            logger.warning(f"[LangGraph] Webhook: Downstream n8n trigger timed out (5s limit): {e}")
            return {"webhook_status": "failed_timeout"}
        except Exception as e:
            logger.error(f"[LangGraph] Webhook: Downstream n8n trigger encountered an error: {e}", exc_info=True)
            return {"webhook_status": "failed_network"}

    async def execute_graph(self, input_text: str) -> Dict[str, Any]:
        """
        Executes the compiled LangGraph workflow.
        """
        initial_state = AgentState(
            raw_input=input_text,
            extracted_claim="",
            historical_records=[],
            web_records=[],
            final_report={},
            webhook_status=""
        )
        
        try:
            # Run the async compiled graph
            final_state = await self.runner.ainvoke(initial_state)
            return final_state.get("final_report", {})
        except Exception as e:
            logger.error(f"LangGraph execution failed: {str(e)}")
            return {"error": "Graph execution failed", "message": str(e)}

# Singleton instance for dependency injection
langgraph_pipeline = LangGraphOrchestrator()
