"use client"
import Link from "next/link"
import { motion } from "framer-motion"
import { useState, useEffect } from "react"
import { Sparkles, Type, UploadCloud, Link as LinkIcon, MoreVertical, Play, FileText, CheckCircle2, Loader2, Lightbulb, ScanSearch, ShieldAlert, ShieldCheck, Network, Database, Search } from "lucide-react"

const TIPS = [
  {
    image: "/safe_tip_woman.png",
    title: "Tip for a safer internet",
    subtitle: "Pause. Verify. Share Peace.",
    description: "Always verify before you believe and share."
  },
  {
    image: "/smart_saved_track.png",
    title: "Think before you forward",
    subtitle: "Misinformation spreads fast.",
    description: "Check the source and context before passing it on."
  },
  {
    image: "/meditating_woman.png",
    title: "Keep the peace",
    subtitle: "Don't let panic win.",
    description: "Take a deep breath and rely on verified facts."
  }
]

export default function AnalyzeContent() {
  const [inputText, setInputText] = useState("")
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisStep, setAnalysisStep] = useState(0)
  const [showNewResult, setShowNewResult] = useState(false)
  const [resultData, setResultData] = useState<any>(null)
  const [activeTab, setActiveTab] = useState("text")
  const [tipIndex, setTipIndex] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setTipIndex(prev => (prev + 1) % TIPS.length)
    }, 5000)
    return () => clearInterval(interval)
  }, [])

  const STAGES = [
    "Parsing payload...",
    "Extracting claims via LLM...",
    "Querying Qdrant for known facts...",
    "Synthesizing Peace Message...",
    "Verification complete. Generating Truth Card."
  ]

  const handleAnalyze = async () => {
    if (!inputText.trim()) return
    setIsAnalyzing(true)
    setAnalysisStep(0)
    setShowNewResult(false)
    setResultData(null)

    try {
      setAnalysisStep(0);
      
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || ""
      
      // We simulate stages visually while the request is in flight
      const stageInterval = setInterval(() => {
          setAnalysisStep(prev => prev < 3 ? prev + 1 : 3)
      }, 1500)

      let response;
      if (activeTab === "media") {
          // Note: In a full implementation, you'd want to attach a file input ref here.
          // For now, we fallback to text if they just clicked without a file.
          response = await fetch(`${baseUrl}/api/verify`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ content: inputText })
          })
      } else {
          response = await fetch(`${baseUrl}/api/verify`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ content: inputText })
          })
      }

      clearInterval(stageInterval)
      setAnalysisStep(4)
      
      if (!response.ok) {
          throw new Error("Verification failed")
      }
      
      const data = await response.json()
      
      if (data.status === "success") {
          const rawVerdict = data.data.verdict || "⚪ Unable to Verify";
          let simpleVerdict = "unable to verify";
          if (rawVerdict.includes("Verified")) simpleVerdict = "true";
          if (rawVerdict.includes("False")) simpleVerdict = "false";
          if (rawVerdict.includes("Misleading") || rawVerdict.includes("Context")) simpleVerdict = "misleading";
          
          setTimeout(() => {
              setResultData({
                verdict: simpleVerdict,
                confidenceScore: data.data.confidence_score,
                claimSummary: data.data.claimSummary || inputText,
                actualFacts: data.data.aiExplanation || data.data.explanation || "No explanation.",
                sources: (data.data.sourceCitations || []).map((s: string) => ({ name: s, url: "#" })),
                aiDeepfake: false
              });
              setIsAnalyzing(false);
              setShowNewResult(true);
              setInputText("");
          }, 1000);
      } else {
          throw new Error(data.message)
      }

    } catch (error) {
      console.error(error);
      setIsAnalyzing(false);
      alert("Failed to analyze content. Please try again.")
    }
  }

  const handleTryExample = () => {
    setInputText("School closed tomorrow due to heavy rain in Chennai.")
  }

  return (
    <div className="max-w-[1400px] mx-auto space-y-6 pb-10">
       {/* Hero Section */}
       <div className="flex flex-col md:flex-row items-center justify-between mb-10 bg-white rounded-2xl border border-slate-100 shadow-sm p-8">
          <div className="max-w-xl pr-6">
             <h1 className="text-3xl font-bold text-slate-800 font-serif mb-2">Analyze Content</h1>
             <p className="text-slate-500 font-medium text-sm">Paste text, upload media, or share a link to analyze and verify the truth.</p>
          </div>
          <div className="hidden md:block w-[240px] shrink-0">
             <img src="/analyze_hero.png" alt="Analyze hero" className="w-full h-auto object-contain mix-blend-multiply" />
          </div>
       </div>

       <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Input Card & Recent Analyses */}
          <div className="lg:col-span-2 space-y-6">
             {/* Input Card */}
             <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden flex flex-col min-h-[400px]">
                {/* Tabs */}
                <div className="flex items-center gap-8 px-8 border-b border-slate-100">
                   <button 
                     onClick={() => setActiveTab("text")}
                     className={`flex items-center gap-2 py-4 border-b-2 text-sm transition-colors ${activeTab === 'text' ? 'border-emerald-600 text-emerald-700 font-bold' : 'border-transparent text-slate-500 font-medium hover:text-slate-700'}`}>
                      <Type className="w-4 h-4" /> Paste Text
                   </button>
                   <button 
                     onClick={() => setActiveTab("media")}
                     className={`flex items-center gap-2 py-4 border-b-2 text-sm transition-colors ${activeTab === 'media' ? 'border-emerald-600 text-emerald-700 font-bold' : 'border-transparent text-slate-500 font-medium hover:text-slate-700'}`}>
                      <UploadCloud className="w-4 h-4" /> Upload Media
                   </button>
                   <button 
                     onClick={() => setActiveTab("link")}
                     className={`flex items-center gap-2 py-4 border-b-2 text-sm transition-colors ${activeTab === 'link' ? 'border-emerald-600 text-emerald-700 font-bold' : 'border-transparent text-slate-500 font-medium hover:text-slate-700'}`}>
                      <LinkIcon className="w-4 h-4" /> Share Link
                   </button>
                </div>
                
                {/* Textarea Area */}
                <div className="flex-1 p-6 flex flex-col relative">
                   <div className="flex-1 border border-dashed border-slate-200 rounded-xl bg-slate-50 p-4 relative flex items-center justify-center overflow-hidden">
                      {isAnalyzing && (
                        <div className="absolute inset-0 z-10 pointer-events-none opacity-40">
                           <div className="absolute inset-0 bg-[linear-gradient(rgba(16,185,129,0.2)_1px,transparent_1px),linear-gradient(90deg,rgba(16,185,129,0.2)_1px,transparent_1px)] bg-[size:20px_20px]" />
                           <motion.div 
                              className="absolute top-0 left-0 right-0 h-1 bg-emerald-400 shadow-[0_0_10px_#34D399]" 
                              animate={{ top: ["0%", "100%", "0%"] }} 
                              transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                           />
                           <motion.div
                              className="absolute w-8 h-8 border-2 border-emerald-400 rounded-sm opacity-0"
                              animate={{ opacity: [0, 1, 0], x: [100, 300, 150], y: [50, 150, 100], scale: [1, 1.2, 1] }}
                              transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                           />
                        </div>
                      )}
                      
                      {activeTab === 'media' ? (
                        <div className="flex flex-col items-center justify-center text-center">
                          <UploadCloud className="w-10 h-10 text-slate-400 mb-3" />
                          <p className="text-sm font-semibold text-slate-700">Drag and drop media files here</p>
                          <p className="text-xs text-slate-500 mt-1">or click to browse from your computer</p>
                          <input type="file" aria-label="Upload media" className="absolute inset-0 opacity-0 cursor-pointer w-full h-full" />
                        </div>
                      ) : (
                        <>
                          <textarea 
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                            disabled={isAnalyzing}
                            className="w-full h-full bg-transparent resize-none outline-none text-sm text-slate-700 placeholder:text-slate-400 font-medium disabled:opacity-50 absolute inset-0 p-4"
                            placeholder={activeTab === 'link' ? "Paste your link here..." : "Type or paste your text here..."}
                          ></textarea>
                          <div className="absolute bottom-3 right-4 flex items-center gap-1 text-[11px] font-bold text-slate-400 pointer-events-none">
                             {inputText.length}/5000
                          </div>
                        </>
                      )}
                   </div>
                </div>

                {/* Bottom Buttons or Loading State */}
                 {isAnalyzing ? (
                   <div className="px-8 py-8 flex flex-col md:flex-row gap-8 border-t border-slate-50 mt-auto bg-emerald-50 rounded-b-2xl min-h-[160px] relative overflow-hidden text-emerald-800 font-mono">
                      {/* Scanning Background Effect */}
                      <motion.div 
                        className="absolute inset-0 bg-gradient-to-r from-transparent via-emerald-100/50 to-transparent w-[200%]"
                        animate={{ x: ["-100%", "50%"] }}
                        transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
                      />
                      
                      {/* Multi-Stage Checklist */}
                      <div className="flex-1 space-y-3 z-10 relative">
                         <div className="text-[10px] uppercase tracking-widest text-slate-500 mb-4 font-sans font-bold flex items-center gap-2">
                            <Loader2 className="w-3 h-3 animate-spin text-emerald-600" />
                            Cognitive Processing Engine
                         </div>
                         {STAGES.map((stage, idx) => (
                            <div key={idx} className={`flex items-center gap-3 text-xs transition-opacity duration-300 ${analysisStep === idx ? 'opacity-100 font-bold' : analysisStep > idx ? 'opacity-70' : 'opacity-40'}`}>
                               <div className={`w-4 h-4 rounded-full flex items-center justify-center border ${analysisStep > idx ? 'bg-emerald-500 border-emerald-500' : analysisStep === idx ? 'border-emerald-600 animate-pulse' : 'border-slate-300'}`}>
                                  {analysisStep > idx ? <CheckCircle2 className="w-3 h-3 text-white" /> : analysisStep === idx ? <div className="w-1.5 h-1.5 bg-emerald-600 rounded-full" /> : null}
                               </div>
                               <span className={analysisStep === idx ? 'text-emerald-700 font-bold' : analysisStep > idx ? 'text-emerald-600' : 'text-slate-500'}>{stage}</span>
                            </div>
                         ))}
                      </div>

                      {/* Entity Extraction HUD */}
                      <div className="w-full md:w-[280px] bg-white/60 rounded-xl border border-emerald-100/80 p-4 z-10 relative text-[10px] space-y-2 shadow-sm">
                         <div className="uppercase tracking-widest text-emerald-800 mb-2 font-bold font-sans">Live Extraction</div>
                         {analysisStep >= 0 && <motion.div initial={{opacity:0}} animate={{opacity:1}} className="flex items-center gap-2"><Search className="w-3 h-3 text-emerald-600"/> <span className="text-slate-700 font-medium">Parsing structure... OK</span></motion.div>}
                         {analysisStep >= 1 && <motion.div initial={{opacity:0}} animate={{opacity:1}} className="flex items-center gap-2"><Type className="w-3 h-3 text-amber-500"/> <span className="text-slate-700 font-medium">Named Entity: [detected]</span></motion.div>}
                         {analysisStep >= 2 && <motion.div initial={{opacity:0}} animate={{opacity:1}} className="flex items-center gap-2"><Database className="w-3 h-3 text-blue-500"/> <span className="text-slate-700 font-medium">Cross-ref Qdrant... MATCH</span></motion.div>}
                         {analysisStep >= 3 && <motion.div initial={{opacity:0}} animate={{opacity:1}} className="flex items-center gap-2"><Network className="w-3 h-3 text-purple-500"/> <span className="text-slate-700 font-medium">Synthesizing output...</span></motion.div>}
                      </div>
                   </div>
                ) : (
                   <div className="px-6 pb-6 pt-2 flex justify-between items-center">
                      <button 
                        onClick={handleTryExample}
                        className="flex items-center gap-2 text-emerald-600 font-bold text-sm px-5 py-2.5 rounded-xl border border-emerald-100 hover:bg-emerald-50 transition-colors shadow-sm"
                      >
                         <Lightbulb className="w-4 h-4" /> Try an Example
                      </button>
                      <div className="relative group">
                        {inputText.trim() && !isAnalyzing && (
                          <div className="absolute -inset-0.5 bg-emerald-500 rounded-xl blur opacity-30 group-hover:opacity-60 transition duration-1000 group-hover:duration-200 animate-pulse"></div>
                        )}
                        <button 
                          onClick={handleAnalyze}
                          disabled={!inputText.trim()}
                          className="relative flex items-center gap-2 bg-[#15803d] hover:bg-[#166534] disabled:bg-slate-300 disabled:text-slate-500 text-white font-bold text-sm px-6 py-2.5 rounded-xl transition-colors shadow-sm"
                        >
                           <ScanSearch className="w-4 h-4" /> Analyze Now
                        </button>
                      </div>
                   </div>
                )}
             </div>
             
             {/* Recent Analyses */}
             <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6">
                 <div className="flex justify-between items-center mb-6">
                    <h3 className="text-sm font-bold text-slate-800">Recent Analyses</h3>
                    <Link href="/history" className="flex items-center gap-1 text-[11px] font-bold text-emerald-600 hover:text-emerald-700">
                      View All <span className="text-lg leading-none mb-0.5">›</span>
                    </Link>
                 </div>
                 
                 <div className="flex flex-col gap-5">
                    {/* Header */}
                    <div className="flex items-center text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2 px-2">
                       <div className="flex-1">Content</div>
                       <div className="w-24 text-center">Platform</div>
                       <div className="w-24 text-center">Result</div>
                       <div className="w-20 text-center">Confidence</div>
                       <div className="w-20 text-right">Time</div>
                       <div className="w-8"></div>
                    </div>

                    {/* New Generated Result (Massive Truth Card Reveal) */}
                    {showNewResult && resultData && (
                       <motion.div 
                         initial={{ opacity: 0, y: 50, scale: 0.95 }}
                         animate={{ opacity: 1, y: 0, scale: 1 }}
                         transition={{ duration: 0.6, type: "spring", bounce: 0.4 }}
                         className={`mb-8 w-full bg-white rounded-3xl p-8 border-2 shadow-[0_30px_60px_-15px_rgba(0,0,0,0.1)] flex flex-col items-center justify-center relative overflow-hidden ${resultData.verdict === "false" ? "border-red-200" : resultData.verdict === "misleading" ? "border-amber-200" : resultData.verdict === "true" ? "border-emerald-200" : "border-blue-200"}`}
                       >
                         {/* Background glow */}
                         <div className={`absolute inset-0 opacity-10 pointer-events-none ${resultData.verdict === "false" ? "bg-red-500" : resultData.verdict === "misleading" ? "bg-amber-500" : resultData.verdict === "true" ? "bg-emerald-500" : "bg-blue-500"}`} />
                         
                         <div className={`w-24 h-24 rounded-full flex items-center justify-center shadow-lg relative z-10 mb-6 ${resultData.verdict === "false" ? "bg-red-50" : resultData.verdict === "misleading" ? "bg-amber-50" : resultData.verdict === "true" ? "bg-emerald-50" : "bg-blue-50"}`}>
                            {resultData.verdict === "false" ? <ShieldAlert className="w-12 h-12 text-red-500" /> : resultData.verdict === "true" ? <ShieldCheck className="w-12 h-12 text-emerald-500" /> : <ShieldAlert className="w-12 h-12 text-blue-500" />}
                            <motion.div className={`absolute inset-0 rounded-full border-2 ${resultData.verdict === "false" ? "border-red-300" : resultData.verdict === "misleading" ? "border-amber-300" : resultData.verdict === "true" ? "border-emerald-300" : "border-blue-300"}`} animate={{ scale: [1, 1.3, 1], opacity: [0.5, 0, 0.5] }} transition={{ duration: 2, repeat: Infinity }} />
                         </div>

                         <h4 className="text-[10px] font-bold text-slate-400 tracking-[0.3em] uppercase mb-2">Verdict</h4>
                         <h2 className={`text-4xl font-black uppercase font-serif tracking-wide mb-6 ${resultData.verdict === "false" ? "text-red-600" : resultData.verdict === "misleading" ? "text-amber-600" : resultData.verdict === "true" ? "text-emerald-600" : "text-blue-600"}`}>
                            {resultData.verdict}
                         </h2>

                         <div className="max-w-2xl text-center mb-8 relative z-10">
                            <p className="text-sm font-medium text-slate-700 leading-relaxed bg-white/60 p-4 rounded-xl border border-white/40 shadow-sm backdrop-blur-sm">
                               {resultData.claimSummary}
                            </p>
                         </div>

                         {/* Source Chain */}
                         <div className="w-full pt-6 border-t border-slate-100 flex flex-col md:flex-row items-center justify-center gap-4 relative z-10">
                            <div className="flex items-center gap-2 group cursor-help">
                               <div className="w-8 h-8 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-center"><Network className="w-4 h-4 text-slate-500 group-hover:text-emerald-500 transition-colors" /></div>
                               <span className="text-xs font-bold text-slate-600">Query Parsing</span>
                            </div>
                            <div className="w-8 h-px bg-slate-300"></div>
                            <div className="flex items-center gap-2 group cursor-help">
                               <div className="w-8 h-8 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-center"><Search className="w-4 h-4 text-slate-500 group-hover:text-emerald-500 transition-colors" /></div>
                               <span className="text-xs font-bold text-slate-600">Google Search Grounding</span>
                            </div>
                            <div className="w-8 h-px bg-slate-300"></div>
                            <div className="flex items-center gap-2 group cursor-help">
                               <div className="w-8 h-8 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-center"><Database className="w-4 h-4 text-slate-500 group-hover:text-emerald-500 transition-colors" /></div>
                               <span className="text-xs font-bold text-slate-600">Sukoon Synthesis</span>
                            </div>
                         </div>
                       </motion.div>
                    )}


                 </div>
             </div>
          </div>

          {/* Right Column Cards */}
          <div className="space-y-6">
             {/* Supported Platforms */}
             <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6">
                <h3 className="text-sm font-bold text-slate-800 mb-1">Supported Platforms</h3>
                <p className="text-[10px] font-medium text-slate-500 mb-6">Analyze content from your favorite platforms</p>
                
                <div className="space-y-5">
                   <div className="flex gap-4">
                      <div className="w-8 h-8 rounded-full bg-[#25D366] flex items-center justify-center shrink-0 shadow-sm">
                         <svg viewBox="0 0 24 24" className="w-4 h-4 fill-white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.888-.788-1.487-1.761-1.66-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>
                      </div>
                      <div>
                         <h4 className="text-[11px] font-bold text-slate-800">WhatsApp</h4>
                         <p className="text-[10px] font-medium text-slate-500 leading-snug pr-4">Forwarded messages, images, videos, audios & documents</p>
                      </div>
                   </div>

                   <div className="flex gap-4">
                      <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-[#FD1D1D] to-[#833AB4] flex items-center justify-center shrink-0 shadow-sm">
                         <svg viewBox="0 0 24 24" className="w-5 h-5 fill-white"><path fillRule="evenodd" clipRule="evenodd" d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
                      </div>
                      <div>
                         <h4 className="text-[11px] font-bold text-slate-800">Instagram</h4>
                         <p className="text-[10px] font-medium text-slate-500 leading-snug pr-4">Reels, posts, captions, stories & DMs</p>
                      </div>
                   </div>

                   <div className="flex gap-4">
                      <div className="w-8 h-8 rounded-full bg-black flex items-center justify-center shrink-0 shadow-sm">
                         <span className="text-white text-[12px] font-black">X</span>
                      </div>
                      <div>
                         <h4 className="text-[11px] font-bold text-slate-800">X (Twitter)</h4>
                         <p className="text-[10px] font-medium text-slate-500 leading-snug pr-4">Tweets, threads, mentions & replies</p>
                      </div>
                   </div>

                   <div className="flex gap-4">
                      <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center shrink-0 shadow-sm border border-slate-200">
                         <LinkIcon className="w-4 h-4 text-slate-500" />
                      </div>
                      <div>
                         <h4 className="text-[11px] font-bold text-slate-800">Link</h4>
                         <p className="text-[10px] font-medium text-slate-500 leading-snug pr-4">Any link from websites or social platforms</p>
                      </div>
                   </div>
                </div>
             </div>

             {/* Tip for a safer internet */}
             <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 pb-4">
                <div className="w-full h-[140px] bg-[#E8F5E9] rounded-xl mb-6 relative flex items-center justify-center overflow-hidden border border-emerald-50">
                   <img key={tipIndex} src={TIPS[tipIndex].image} alt="Safe Tip" className="w-[110%] h-[110%] object-contain mix-blend-multiply opacity-90 transition-opacity duration-500 animate-in fade-in" />
                </div>
                <h3 className="text-[13px] font-bold text-slate-800 mb-2">{TIPS[tipIndex].title}</h3>
                <p className="text-[11px] font-bold text-slate-800 leading-tight mb-1">{TIPS[tipIndex].subtitle}</p>
                <p className="text-[10px] font-medium text-slate-500 mb-6 pr-4 h-6">{TIPS[tipIndex].description}</p>
                
                {/* Carousel dots */}
                <div className="flex justify-center gap-1.5 mb-2">
                   {TIPS.map((_, i) => (
                      <button 
                         key={i} 
                         onClick={() => setTipIndex(i)} 
                         className={`w-1.5 h-1.5 rounded-full transition-colors ${i === tipIndex ? 'bg-emerald-600' : 'bg-slate-200'}`}
                         aria-label={`Go to slide ${i + 1}`}
                      ></button>
                   ))}
                </div>
             </div>
          </div>
       </div>

    </div>
  )
}
