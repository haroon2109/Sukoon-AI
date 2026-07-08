"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { UploadCloud, Link as LinkIcon, FileText, Loader2 } from "lucide-react"
import { fetchWithAuth } from "@/lib/api"
import { TruthCard } from "@/components/shared/TruthCard"
import { motion, AnimatePresence } from "framer-motion"
import { VerificationRecord } from "@/lib/mockData"

export default function VerifyPage() {
  const [step, setStep] = useState<"input" | "processing" | "result">("input")
  const [inputType, setInputType] = useState<"media" | "url" | "text">("media")
  const [resultData, setResultData] = useState<VerificationRecord | null>(null)
  const [processingStage, setProcessingStage] = useState<string>("Initializing pipeline...")
  const [textContent, setTextContent] = useState("")
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isError, setIsError] = useState(false)
  const [errorMessage, setErrorMessage] = useState("")
  
  const handleVerify = async () => {
    if (inputType !== "media" && !textContent.trim()) return;
    if (inputType === "media" && !selectedFile) return;

    setStep("processing")
    setIsError(false)
    setErrorMessage("")
    setProcessingStage("Connecting to Sukoon AI backend...")
    
    // Simulate stages
    const stages = [
      "Uploading media and running OCR...",
      "Extracting claims and retrieving RAG evidence...",
      "Analyzing reasoning and generating peace verdict..."
    ];
    let stageIdx = 0;
    const stageInterval = setInterval(() => {
      if (stageIdx < stages.length) {
        setProcessingStage(stages[stageIdx]);
        stageIdx++;
      }
    }, 2000);
    
    try {
      let response;

      if (inputType === "media") {
        const formData = new FormData()
        formData.append("file", selectedFile!)
        if (textContent) {
            formData.append("content", textContent)
        }
        
        response = await fetch(`/api/analyze`, {
          method: "POST",
          body: formData
        })
      } else {
        response = await fetch(`/api/analyze`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content: textContent })
        })
      }
      
      clearInterval(stageInterval);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error || "Verification failed")
      }

      const resData = await response.json()
      
      if (resData.success && resData.task_id) {
        // Polling logic
        const taskId = resData.task_id;
        let pollCount = 0;
        const maxPolls = 30; // 30 * 2s = 60s timeout
        
        while (pollCount < maxPolls) {
          await new Promise(resolve => setTimeout(resolve, 2000));
          pollCount++;
          
          const statusRes = await fetch(`/api/analyze/status/${taskId}`);
          if (!statusRes.ok) {
            continue;
          }
          
          const statusData = await statusRes.json();
          
          if (statusData.status === "completed" && statusData.data) {
            setResultData({
              id: Math.random().toString(36).substr(2, 9),
              verdict: statusData.data.verdict,
              confidenceScore: statusData.data.confidenceScore,
              claimSummary: textContent || (selectedFile ? selectedFile.name : "Uploaded media content"),
              evidenceFound: statusData.data.explanation || "Evidence found",
              aiExplanation: statusData.data.explanation,
              sourceCitations: (statusData.data.citations || []).map((s: any) => s.url || s.title || s)
            });
            setStep("result");
            return;
          } else if (statusData.status === "failed") {
            throw new Error(statusData.error || "Backend processing failed");
          }
        }
        throw new Error("Verification timed out waiting for backend.");
      } else {
        throw new Error(resData.error || "Invalid response format from server.")
      }
      
    } catch (error: any) {
      clearInterval(stageInterval);
      console.error("API error:", error)
      setIsError(true)
      setErrorMessage(error instanceof Error ? error.message : "An unknown error occurred")
      setStep("input")
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.files && e.target.files[0]) {
          setSelectedFile(e.target.files[0])
      }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-slate-900 mb-2">Analyze Content</h1>
        <p className="text-slate-500">Submit suspicious forwards or links for instant AI verification.</p>
      </div>

      <AnimatePresence mode="wait">
        {step === "input" && (
          <motion.div 
            key="input"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <Card className="p-8 border-slate-100 shadow-sm rounded-3xl">
              <div className="flex gap-4 mb-8 border-b border-slate-100 pb-4">
                <button 
                  onClick={() => setInputType("media")}
                  className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-colors ${inputType === "media" ? "bg-slate-900 text-white" : "bg-slate-50 text-slate-600 hover:bg-slate-100"}`}
                >
                  <UploadCloud className="w-4 h-4" /> Media Forward
                </button>
                <button 
                  onClick={() => setInputType("url")}
                  className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-colors ${inputType === "url" ? "bg-slate-900 text-white" : "bg-slate-50 text-slate-600 hover:bg-slate-100"}`}
                >
                  <LinkIcon className="w-4 h-4" /> Social Link
                </button>
                <button 
                  onClick={() => setInputType("text")}
                  className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-colors ${inputType === "text" ? "bg-slate-900 text-white" : "bg-slate-50 text-slate-600 hover:bg-slate-100"}`}
                >
                  <FileText className="w-4 h-4" /> Raw Text
                </button>
              </div>

              <div className="bg-white rounded-3xl p-8 text-center transition-colors">
                {inputType === "media" ? (
                  <div className="space-y-4">
                    <label className="block text-slate-700 font-medium text-left">Upload Audio, Video, or Image</label>
                    <input type="file" aria-label="Upload Audio, Video, or Image" onChange={handleFileChange} className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-teal-50 file:text-teal-700 hover:file:bg-teal-100" />
                    <textarea 
                        className="w-full mt-4 p-4 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-teal-500/20" 
                        rows={3} 
                        placeholder="(Optional) Add any caption that came with this forward..."
                        value={textContent}
                        onChange={(e) => setTextContent(e.target.value)}
                    />
                  </div>
                ) : (
                  <div className="space-y-4">
                     <textarea 
                        className="w-full p-4 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-teal-500/20" 
                        rows={6} 
                        placeholder={inputType === "url" ? "Paste a news article or social media link here..." : "Paste the suspicious WhatsApp forward here..."}
                        value={textContent}
                        onChange={(e) => setTextContent(e.target.value)}
                    />
                  </div>
                )}
                
                {/* Non-intrusive Error Banner */}
                 {isError && (
                   <div className="mt-4 p-4 bg-red-50 border border-red-100 rounded-xl flex items-start gap-3 text-red-800 text-left">
                     <svg className="w-5 h-5 text-red-600 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                       <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                     </svg>
                     <div className="flex-1 text-xs">
                       <span className="font-bold block mb-1">Verification Failed</span>
                       <span className="font-medium text-red-600">{errorMessage}</span>
                       <button 
                         onClick={handleVerify} 
                         className="mt-3 block font-bold text-red-800 hover:text-red-900 border border-red-200 bg-white px-3 py-1.5 rounded-lg shadow-sm hover:bg-red-50 transition-colors cursor-pointer"
                       >
                         Retry Verification
                       </button>
                     </div>
                   </div>
                 )}
                 
                 <Button 
                     onClick={handleVerify} 
                     className="mt-6 rounded-full px-8 py-6 text-lg w-full bg-slate-900 hover:bg-slate-800"
                     disabled={inputType === "media" ? !selectedFile : !textContent.trim()}
                 >
                     Run Forensic Verification
                 </Button>
              </div>
            </Card>
          </motion.div>
        )}

        {step === "processing" && (
          <motion.div 
            key="processing"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.4 }}
          >
            <Card className="p-12 border-none shadow-[0_8px_30px_rgb(0,0,0,0.04)] rounded-3xl text-center flex flex-col items-center justify-center min-h-[400px] bg-white">
              <div className="relative mb-10">
                <div className="absolute inset-0 bg-teal-100 rounded-full blur-2xl animate-pulse opacity-50 scale-150"></div>
                <div className="w-20 h-20 bg-stone-50 rounded-full flex items-center justify-center relative z-10 border border-stone-100 shadow-sm">
                  <Loader2 className="w-8 h-8 text-teal-600 animate-spin" />
                </div>
              </div>
              <h2 className="text-2xl font-semibold text-slate-800 mb-4 tracking-tight">Forensic Scan Active</h2>
              
              <div className="bg-[#F9FAFB] rounded-2xl p-5 min-w-[320px] shadow-inner mb-6">
                <motion.p 
                  key={processingStage}
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-slate-500 font-medium font-mono text-xs tracking-wide"
                >
                  {processingStage}
                </motion.p>
              </div>
            </Card>
          </motion.div>
        )}

        {step === "result" && resultData && (
          <motion.div 
            key="result"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, type: "spring" }}
            className="space-y-6"
          >
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-xl font-semibold text-slate-900">Verification Complete</h2>
              <Button variant="outline" onClick={() => {
                  setStep("input")
                  setTextContent("")
                  setSelectedFile(null)
              }} className="rounded-full">Verify Another</Button>
            </div>
            
            <div className="flex justify-center">
              <TruthCard 
                verdict={resultData.verdict}
                confidenceScore={resultData.confidenceScore}
                claimSummary={resultData.claimSummary}
                evidenceFound={resultData.evidenceFound || "No explicit evidence mapped in mock."}
                aiExplanation={resultData.aiExplanation || resultData.actualFacts || "No explanation provided."}
                sourceCitations={resultData.sourceCitations || []}
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
