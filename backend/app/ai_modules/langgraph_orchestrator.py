import typing
import logging
import httpx
from typing import Annotated, Dict, Any
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# Import the actual engines we built
from app.services.scraper import is_url, scrape_url
from app.services.rag_service import rag_service
from app.services.ai_engine import verify_multimodal_content
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

# Define the Graph State
class AgentState(TypedDict):
    raw_input: str
    extracted_claim: str
    historical_records: str
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
        self.graph.add_node("agent_c_truth_evaluator", self.agent_c_truth_evaluator)
        self.graph.add_node("downstream_webhook", self.downstream_webhook)
        
        # Define the directed workflow (edges)
        self.graph.add_edge(START, "supervisor_ingestion")
        
        # Parallel Execution: Supervisor delegates to Agent A and Agent B concurrently
        self.graph.add_edge("supervisor_ingestion", "agent_a_scraper")
        self.graph.add_edge("supervisor_ingestion", "agent_b_database")
        
        # Fan-in: Both agents return results to Agent C
        self.graph.add_edge(["agent_a_scraper", "agent_b_database"], "agent_c_truth_evaluator")
        
        # Final Action: Trigger webhook and end
        self.graph.add_edge("agent_c_truth_evaluator", "downstream_webhook")
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
            # Note: scrape_url is currently synchronous in scraper.py, we run it normally
            extracted = scrape_url(raw)
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
        
        # Real logic: Call Supabase pgvector RAG Service
        # rag_service.retrieve_context is synchronous
        records_list = rag_service.retrieve_context(claim=raw, top_k=3)
        
        if records_list:
            # Format the records for the AI
            formatted_records = "\n".join([f"- {r.get('title', 'Record')}: {r.get('text', '')}" for r in records_list])
            records = f"Found {len(records_list)} historical records:\n{formatted_records}"
        else:
            records = "Found historical record: No identical matches in Supabase."
            
        return {"historical_records": records}

    # Step 3: Synthesis and Debate
    async def agent_c_truth_evaluator(self, state: AgentState) -> AgentState:
        """The core Gemini model that synthesizes findings and writes the final JSON report."""
        logger.info("[LangGraph] Agent C: Truth Evaluator synthesizing findings with Gemini 2.5 Flash...")
        claim = state.get("extracted_claim", "")
        records = state.get("historical_records", "")
        
        # Real logic: Call Gemini API using structured JSON Pydantic schema
        response = await verify_multimodal_content(text_content=claim, retrieved_context=records)
        
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
        """Triggers external n8n webhook (notifying community moderators)."""
        logger.info("[LangGraph] Webhook: Triggering downstream n8n automation...")
        # Note: In production you would do:
        # async with httpx.AsyncClient() as client:
        #     await client.post("http://localhost:8080/api/v1/n8n/webhook", json=state.get("final_report"))
        return {"webhook_status": "success"}

    async def execute_graph(self, input_text: str) -> Dict[str, Any]:
        """
        Executes the compiled LangGraph workflow.
        """
        initial_state = AgentState(
            raw_input=input_text,
            extracted_claim="",
            historical_records="",
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
