import { NextRequest, NextResponse } from "next/server";

// Set max duration for Vercel Hobby tier (maximum allowable limit)
export const maxDuration = 60;

export async function POST(req: NextRequest) {
  try {
    const contentType = req.headers.get("content-type") || "";
    let backendUrl = process.env.BACKEND_API_URL || "http://127.0.0.1:8000";
    // Ensure URL doesn't have trailing slash
    backendUrl = backendUrl.replace(/\/$/, "");
    
    const targetUrl = `${backendUrl}/api/v1/verify/sync`;
    
    console.log(`Proxying verification request to: ${targetUrl}`);
    
    let response: Response;

    // Proxy the request exactly as received (either JSON or FormData)
    if (contentType.includes("multipart/form-data")) {
      const formData = await req.formData();
      response = await fetch(targetUrl, {
        method: "POST",
        body: formData,
      });
    } else {
      const json = await req.json();
      response = await fetch(targetUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(json)
      });
    }

    if (!response.ok) {
      console.error(`Backend returned status ${response.status}`);
      let errorText = "Unknown error from backend";
      try {
        const errorJson = await response.json();
        errorText = errorJson.detail || errorJson.error || JSON.stringify(errorJson);
      } catch (e) {
        errorText = await response.text();
      }
      return NextResponse.json(
        { success: false, error: `Inference pipeline exhausted: ${errorText}` },
        { status: response.status === 400 ? 400 : 503 }
      );
    }

    const result = await response.json();
    return NextResponse.json(result);

  } catch (globalError: any) {
    console.error("Unhandled exception in analyze route proxy:", globalError);
    return NextResponse.json(
      { success: false, error: `Internal serverless runtime failure: ${globalError.message || globalError}` },
      { status: 500 }
    );
  }
}
