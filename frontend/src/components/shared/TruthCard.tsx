"use client"

import { useRef } from "react"
import { CheckCircle, AlertTriangle, XCircle, Link as LinkIcon, Share2, Download } from "lucide-react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { toJpeg } from "html-to-image"

type VerdictType = "verified" | "misleading" | "false"

interface TruthCardProps {
  verdict: VerdictType
  confidenceScore: number
  claimSummary: string
  actualFacts: string
  sourceCitations: string[]
  peaceMessage: string
  toxicityScore?: number
  factualityScore?: number
}

const themeConfig = {
  verified: {
    bg: "bg-[#F9FAFB]",
    border: "border-teal-100/50",
    text: "text-teal-900",
    icon: <CheckCircle className="w-5 h-5 text-teal-700" />,
    badgeBg: "bg-teal-50",
    badgeText: "text-teal-800",
    label: "Verified True",
  },
  misleading: {
    bg: "bg-[#F9FAFB]",
    border: "border-amber-100/50",
    text: "text-amber-900",
    icon: <AlertTriangle className="w-5 h-5 text-amber-700" />,
    badgeBg: "bg-amber-50",
    badgeText: "text-amber-800",
    label: "Misleading Context",
  },
  false: {
    bg: "bg-[#F9FAFB]",
    border: "border-rose-100/50",
    text: "text-rose-900",
    icon: <XCircle className="w-5 h-5 text-rose-700" />,
    badgeBg: "bg-rose-50",
    badgeText: "text-rose-800",
    label: "False Information",
  },
}

export function TruthCard({
  verdict,
  confidenceScore,
  claimSummary,
  actualFacts,
  sourceCitations,
  peaceMessage,
  toxicityScore,
  factualityScore,
}: TruthCardProps) {
  const cardRef = useRef<HTMLDivElement>(null)
  const theme = themeConfig[verdict]

  const handleDownload = () => {
    if (cardRef.current === null) return
    
    // Generate heavily compressed JPEG to hit the sub-150KB WhatsApp target
    toJpeg(cardRef.current, { quality: 0.8, pixelRatio: 1.5 })
      .then((dataUrl) => {
        const link = document.createElement("a")
        link.download = `Sukoon-FactCheck-${Date.now()}.jpg`
        link.href = dataUrl
        link.click()
      })
      .catch((err) => {
        console.error("Oops, something went wrong!", err)
        alert("Failed to generate the image. Please try again.")
      })
  }

  return (
    <div className="flex flex-col gap-4 w-full max-w-sm mx-auto">
      {/* The capture area */}
      <div 
        ref={cardRef} 
        className={`relative overflow-hidden rounded-[2rem] border border-stone-200/50 ${theme.bg} p-8 sm:p-10 shadow-[0_8px_30px_rgb(0,0,0,0.04)] bg-white`}
      >
        {/* Header / Status Badge */}
        <div className="flex items-center justify-between mb-8">
          <div className={`inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full ${theme.badgeBg} ${theme.badgeText} text-xs font-bold uppercase tracking-widest border border-stone-100`}>
            {theme.icon}
            {theme.label}
          </div>
          <span className={`text-[10px] font-bold uppercase tracking-widest text-slate-400`}>
            {confidenceScore}% Confidence
          </span>
        </div>

        {/* Claim Summary */}
        <div className="mb-8">
          <h3 className={`text-[10px] font-bold uppercase tracking-widest mb-3 text-slate-400`}>Original Claim</h3>
          <p className="text-slate-800 font-medium text-lg leading-relaxed">
            &quot;{claimSummary}&quot;
          </p>
        </div>

        {/* Actual Facts */}
        <div className="mb-8 bg-stone-50/50 p-5 rounded-2xl border border-stone-100/50">
          <h3 className={`text-[10px] font-bold uppercase tracking-widest mb-3 text-slate-400`}>Forensic Facts</h3>
          <p className="text-slate-600 text-sm leading-loose font-light">
            {actualFacts}
          </p>
        </div>

        {/* Source Citations */}
        <div className="mb-10">
          <h3 className={`text-[10px] font-bold uppercase tracking-widest mb-3 text-slate-400`}>Verified Sources</h3>
          <div className="flex flex-wrap gap-2">
            {sourceCitations.map((source, idx) => (
              <span key={idx} className="inline-flex items-center gap-1.5 text-[11px] font-medium text-slate-500 bg-stone-50 border border-stone-100 px-3 py-1.5 rounded-md tracking-wide">
                <LinkIcon className="w-3 h-3 text-slate-400" /> {source}
              </span>
            ))}
          </div>
        </div>

        {/* Peace Index Metrics (If Available) */}
        {(toxicityScore !== undefined && factualityScore !== undefined) && (
          <div className="mb-8 grid grid-cols-2 gap-4">
            <div className="bg-stone-50/50 p-4 rounded-xl border border-stone-100 flex flex-col items-center justify-center text-center">
              <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1">Toxicity</span>
              <span className={`text-2xl font-black ${toxicityScore > 50 ? 'text-rose-600' : 'text-teal-600'}`}>{toxicityScore}/100</span>
            </div>
            <div className="bg-stone-50/50 p-4 rounded-xl border border-stone-100 flex flex-col items-center justify-center text-center">
              <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1">Factuality</span>
              <span className={`text-2xl font-black ${factualityScore < 50 ? 'text-rose-600' : 'text-teal-600'}`}>{factualityScore}/100</span>
            </div>
          </div>
        )}

        {/* Peace Message */}
        <div className={`p-6 rounded-2xl bg-white shadow-sm border ${theme.border} mt-4`}>
          <p className={`text-sm font-medium italic leading-loose ${theme.text}`}>
            {peaceMessage}
          </p>
        </div>

        {/* Footer Branding for Image export */}
        <div className="mt-8 flex items-center justify-between opacity-40">
          <span className="text-[10px] font-bold text-slate-800 tracking-wider">Sukoon.ai</span>
          <span className="text-[9px] text-slate-500 uppercase tracking-widest font-mono">Verified Audit</span>
        </div>
      </div>

      {/* Action Buttons (Not part of the downloaded image) */}
      <div className="flex flex-col sm:flex-row gap-3 mt-2">
        <Button 
          onClick={handleDownload}
          className="flex-1 rounded-full bg-slate-800 hover:bg-slate-700 text-white h-14 font-medium"
        >
          <Download className="w-4 h-4 mr-2" /> Save Image
        </Button>
        <Button 
          variant="outline"
          className="flex-1 rounded-full border-stone-200 text-slate-600 hover:bg-stone-50 h-14 font-medium"
        >
          <Share2 className="w-4 h-4 mr-2" /> Forward
        </Button>
      </div>
    </div>
  )
}
