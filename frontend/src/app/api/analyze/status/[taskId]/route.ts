import { NextRequest, NextResponse } from "next/server";

export const dynamic = 'force-dynamic';

export async function GET(req: NextRequest, { params }: { params: { taskId: string } }) {
  try {
    const { taskId } = params;
    
    let backendUrl = process.env.BACKEND_API_URL || "http://127.0.0.1:8000";
    backendUrl = backendUrl.replace(/\/$/, "");
    
    const targetUrl = `${backendUrl}/api/v1/verify/status/${taskId}`;
    
    const response = await fetch(targetUrl, {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    });

    if (!response.ok) {
      return NextResponse.json(
        { success: false, error: "Failed to fetch task status" },
        { status: response.status === 404 ? 404 : 502 }
      );
    }

    const result = await response.json();
    return NextResponse.json(result);

  } catch (globalError: any) {
    console.error("Unhandled exception in status route proxy:", globalError);
    return NextResponse.json(
      { success: false, error: `Internal serverless runtime failure: ${globalError.message || globalError}` },
      { status: 500 }
    );
  }
}
