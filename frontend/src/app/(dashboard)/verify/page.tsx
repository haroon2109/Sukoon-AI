"use client"

import { useState, useEffect, useRef } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { UploadCloud, Link as LinkIcon, FileText, Loader2, PlayCircle, ShieldAlert, CheckCircle2 } from "lucide-react"
import { TruthCard } from "@/components/shared/TruthCard"
import { motion, AnimatePresence } from "framer-motion"
import { VerificationRecord, getRandomVerification } from "@/lib/mockData"

export default function VerifyPage() {
  const [step, setStep] = useState<"input" | "processing" | "result">("input")
  const [inputType, setInputType] = useState<"media" | "url" | "text">("media")
  const [resultData, setResultData] = useState<VerificationRecord | null>(null)
  
  // WebSocket State
  const [processingStage, setProcessingStage] = useState<string>("Initializing pipeline...")
  const wsRef = useRef<WebSocket | null>(null)
  
  const handleSimulateUpload = async () => {
    setStep("processing")
    setProcessingStage("Connecting to server...")
    
    try {
      // Create actual backend task
      const response = await fetch("/api/v1/verify/media", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ raw_content: "Simulated upload payload", language: "en" })
      })
      
      const data = await response.json()
      const taskId = data.id || data.task_id || `task-${Date.now()}` // Fallback if needed
      
      // Connect to our FastAPI WebSocket endpoint
      const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const ws = new WebSocket(`${wsProtocol}//${window.location.host}/api/v1/verify/ws/${taskId}`)
      wsRef.current = ws

      ws.onmessage = (event) => {
        const payload = JSON.parse(event.data)
        setProcessingStage(payload.message)
        if (payload.step === "completed") {
          setTimeout(() => {
            setResultData(payload.data || getRandomVerification())
            setStep("result")
            ws.close()
          }, 1000)
        }
      }
      
      ws.onerror = (error) => {
        console.error("WebSocket error:", error)
        setProcessingStage("Falling back to standard connection...")
        setTimeout(() => {
          setResultData(getRandomVerification())
          setStep("result")
        }, 2500)
      }
    } catch (error) {
      console.error("API error:", error)
      setProcessingStage("Failed to connect. Using offline mode...")
      setTimeout(() => {
        setResultData(getRandomVerification())
        setStep("result")
      }, 2000)
    }
  }

  // Cleanup WebSocket on unmount
  useEffect(() => {
    return () => {
      if (wsRef.current) wsRef.current.close()
    }
  }, [])

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

              <div className="bg-white rounded-3xl p-12 text-center hover:bg-stone-50 transition-colors cursor-pointer group shadow-[0_8px_30px_rgb(0,0,0,0.04)]" onClick={handleSimulateUpload}>
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} className="w-20 h-20 bg-[#F9FAFB] text-slate-400 border border-slate-100 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:text-teal-600 transition-colors">
                  {inputType === "media" ? <UploadCloud className="w-8 h-8" /> : inputType === "url" ? <LinkIcon className="w-8 h-8" /> : <FileText className="w-8 h-8" />}
                </motion.div>
                <h3 className="text-xl font-semibold text-slate-800 mb-2 tracking-tight">Click to browse or drag and drop</h3>
                <p className="text-slate-400 text-sm font-light">Supports WhatsApp Audio, Video, Images, or text snippets.</p>
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
                {/* Calm pulsing glow instead of aggressive ping */}
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
              <Button variant="outline" onClick={() => setStep("input")} className="rounded-full">Verify Another</Button>
            </div>
            
            <div className="flex justify-center">
              <TruthCard 
                verdict={resultData.verdict}
                confidenceScore={resultData.confidenceScore}
                claimSummary={resultData.claimSummary}
                actualFacts={resultData.actualFacts}
                sourceCitations={resultData.sourceCitations}
                peaceMessage={resultData.peaceMessage}
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
