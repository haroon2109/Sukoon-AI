import { NextRequest, NextResponse } from "next/server";

// Set max duration for Vercel Hobby tier (maximum allowable limit)
export const maxDuration = 60;

const SUKOON_PERSONA = `You are the core logic engine of Sukoon AI, an advanced fact-checking and responsible AI verification platform.
Your objective is to evaluate incoming claims, multimodal media (images/video/audio), and search grounding to determine objective truth.

RULES FOR EVALUATION:
1. If the claim matches the context or is objectively true, respond with 'verified'.
2. If the claim is demonstrably false, fabricated, or biased, respond with 'false'.
3. If the claim twists facts or removes critical nuance, respond with 'misleading'.
4. If there is no evidence either way, respond with 'unable_to_verify'.

Provide a strict confidence score (0-100) reflecting the quality of the evidence, and a highly analytical, clinical explanation.`;

const RESPONSE_SCHEMA = {
  type: "OBJECT",
  properties: {
    verdict: {
      type: "STRING",
      description: "Must be exactly one of: 'verified', 'needs_context', 'misleading', 'false', 'unable_to_verify'"
    },
    confidence_score: {
      type: "NUMBER",
      description: "A confidence score between 0 and 100 based on the provided evidence"
    },
    explanation: {
      type: "STRING",
      description: "A concise, neutral, and scientific explanation of why this verdict was reached, citing specific sources or details"
    }
  },
  required: ["verdict", "confidence_score", "explanation"]
};

// Exponential backoff fetch helper
async function fetchWithRetry(url: string, body: any, retries = 3, delay = 1000): Promise<Response> {
  let lastError: any;
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
      });
      
      if (response.ok) {
        return response;
      }
      
      // Retry on rate limit (429) or server errors (5xx)
      if (response.status === 429 || response.status >= 500) {
        console.warn(`Gemini API returned status ${response.status}. Retrying in ${delay}ms...`);
        lastError = new Error(`API returned status ${response.status}`);
      } else {
        // Bad request or authorization failure — return immediately
        return response;
      }
    } catch (e) {
      console.warn(`Network/Fetch error: ${e}. Retrying in ${delay}ms...`);
      lastError = e;
    }
    
    await new Promise(res => setTimeout(res, delay));
    delay *= 2; // Double the delay
  }
  throw lastError || new Error("Inference failed after max retries");
}

export async function POST(req: NextRequest) {
  try {
    const contentType = req.headers.get("content-type") || "";
    let text = "";
    let mediaBase64 = "";
    let mediaMimeType = "";

    // 1. Ingest Payload
    if (contentType.includes("multipart/form-data")) {
      const formData = await req.formData();
      const file = formData.get("file") as File | null;
      const contentText = formData.get("content") as string | null;
      
      if (file) {
        const bytes = await file.arrayBuffer();
        mediaBase64 = Buffer.from(bytes).toString("base64");
        mediaMimeType = file.type;
      }
      text = contentText || "";
    } else {
      const json = await req.json();
      text = json.content || json.url || "";
    }

    if (!text && !mediaBase64) {
      return NextResponse.json(
        { success: false, error: "Empty request. Please provide text, URL, or media." },
        { status: 400 }
      );
    }

    const apiKey = process.env.GEMINI_API_KEY || process.env.NEXT_PUBLIC_GEMINI_API_KEY || "AIzaSyDummyKey_ReplaceMe";
    
    // Construct parts array
    const parts: any[] = [];
    if (mediaBase64 && mediaMimeType) {
      parts.push({
        inlineData: {
          mimeType: mediaMimeType,
          data: mediaBase64
        }
      });
    }
    
    // Add text prompt
    parts.push({
      text: text ? `Please analyze and verify this content:\n\n${text}` : "Please analyze the uploaded media file for truthfulness, manipulation, and context."
    });

    // 2. Prepare Request Configuration with Google Search Grounding
    const requestBody = {
      contents: [
        {
          parts: parts
        }
      ],
      systemInstruction: {
        parts: [
          {
            text: SUKOON_PERSONA
          }
        ]
      },
      tools: [
        {
          googleSearch: {}
        }
      ],
      generationConfig: {
        responseMimeType: "application/json",
        responseSchema: RESPONSE_SCHEMA
      }
    };

    // Define model endpoints
    const primaryUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key=${apiKey}`;
    const fallbackUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;

    let response: Response;
    
    // 3. Fallback Model Sequence Loop
    try {
      console.log("Calling primary heavy inference model (gemini-2.5-pro) with Google Search grounding...");
      response = await fetchWithRetry(primaryUrl, requestBody, 3, 1000);
      
      // If primary model failed due to key permissions/invalid options, throw to fallback
      if (!response.ok) {
        throw new Error(`Primary model failed: ${response.status}`);
      }
    } catch (primaryError) {
      console.warn("Primary model (gemini-2.5-pro) failed or timed out. Falling back to fast model (gemini-2.5-flash) without tools...", primaryError);
      
      // Strip out Google Search grounding tool for the fast fallback to ensure success
      const fallbackRequestBody = {
        ...requestBody,
        tools: undefined
      };
      
      try {
        response = await fetchWithRetry(fallbackUrl, fallbackRequestBody, 3, 500);
        if (!response.ok) {
          throw new Error(`Fallback model failed: ${response.status}`);
        }
      } catch (fallbackError: any) {
        console.error("All inference attempts exhausted.", fallbackError);
        return NextResponse.json(
          { success: false, error: `Inference pipeline exhausted: ${fallbackError.message || fallbackError}` },
          { status: 503 }
        );
      }
    }

    // 4. Parse Structured Result
    const result = await response.json();
    const textResponse = result?.candidates?.[0]?.content?.parts?.[0]?.text;
    
    if (!textResponse) {
      // If we got an empty response but successful status, return descriptive error
      return NextResponse.json(
        { success: false, error: "Empty content returned from the generative model." },
        { status: 502 }
      );
    }

    try {
      const parsedData = JSON.parse(textResponse.trim());
      
      // Extract grounding metadata if available (citations)
      const searchChunks = result?.candidates?.[0]?.groundingMetadata?.groundingChunks || [];
      const citations = searchChunks.map((chunk: any) => ({
        title: chunk?.web?.title || "Web Search Result",
        url: chunk?.web?.uri || "#"
      }));

      return NextResponse.json({
        success: true,
        data: {
          verdict: parsedData.verdict || "unable_to_verify",
          confidenceScore: parsedData.confidence_score ?? 50,
          explanation: parsedData.explanation || "No explanation provided.",
          citations: citations
        }
      });
    } catch (parseError) {
      console.error("JSON parsing error of model output:", parseError, textResponse);
      return NextResponse.json(
        { success: false, error: "Model returned invalid JSON format." },
        { status: 502 }
      );
    }

  } catch (globalError: any) {
    console.error("Unhandled exception in analyze route:", globalError);
    return NextResponse.json(
      { success: false, error: `Internal serverless runtime failure: ${globalError.message || globalError}` },
      { status: 500 }
    );
  }
}
