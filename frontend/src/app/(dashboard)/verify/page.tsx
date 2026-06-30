"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { UploadCloud, Link as LinkIcon, FileText, Loader2 } from "lucide-react"
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
  
  const handleVerify = async () => {
    if (inputType !== "media" && !textContent.trim()) return;
    if (inputType === "media" && !selectedFile) return;

    setStep("processing")
    setProcessingStage("Connecting to Sukoon AI backend...")
    
    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || ""
      let response;

      if (inputType === "media") {
        setProcessingStage("Uploading media and running OCR...")
        const formData = new FormData()
        formData.append("file", selectedFile!)
        if (textContent) {
            formData.append("content", textContent)
        }
        
        response = await fetch(`${baseUrl}/api/v1/verify/media`, {
          method: "POST",
          body: formData
        })
      } else {
        setProcessingStage("Extracting claims and retrieving RAG evidence...")
        response = await fetch(`${baseUrl}/api/verify`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ content: textContent })
        })
      }
      
      setProcessingStage("Analyzing reasoning and generating peace verdict...")
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || "Verification failed")
      }

      const data = await response.json()
      
      if (data.status === "success") {
        // Map backend output to frontend TruthCard props
        setResultData({
          id: `v_${Date.now()}`,
          verdict: data.data.verdict,
          confidenceScore: data.data.confidence_score,
          claimSummary: data.data.claimSummary || textContent,
          evidenceFound: data.data.evidenceFound,
          aiExplanation: data.data.aiExplanation || data.data.explanation,
          sourceCitations: data.data.sourceCitations || []
        })
        setStep("result")
      } else {
        throw new Error(data.message)
      }
      
    } catch (error: unknown) {
      console.error("API error:", error)
      alert(error instanceof Error ? error.message : "An unknown error occurred")
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
