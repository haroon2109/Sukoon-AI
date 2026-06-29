"use client"

import { useRef } from "react"
import { CheckCircle, AlertTriangle, XCircle, Link as LinkIcon, Share2, Download } from "lucide-react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { toJpeg } from "html-to-image"

export type VerdictType = "🟢 Verified" | "🟡 Needs Context" | "🟠 Misleading" | "🔴 False" | "⚪ Unable to Verify" | "verified" | "misleading" | "false" | "unverified"

interface TruthCardProps {
  verdict: VerdictType
  confidenceScore: number
  claimSummary: string
  evidenceFound: string
  aiExplanation: string
  sourceCitations: string[]
}

const themeConfig: Record<string, any> = {
  "🟢 Verified": {
    bg: "bg-[#F9FAFB]",
    border: "border-teal-100/50",
    text: "text-teal-900",
    icon: <CheckCircle className="w-5 h-5 text-teal-700" />,
    badgeBg: "bg-teal-50",
    badgeText: "text-teal-800",
    label: "Verified True",
  },
  "🟡 Needs Context": {
    bg: "bg-[#F9FAFB]",
    border: "border-amber-100/50",
    text: "text-amber-900",
    icon: <AlertTriangle className="w-5 h-5 text-amber-700" />,
    badgeBg: "bg-amber-50",
    badgeText: "text-amber-800",
    label: "Needs Context",
  },
  "🟠 Misleading": {
    bg: "bg-[#F9FAFB]",
    border: "border-amber-100/50",
    text: "text-amber-900",
    icon: <AlertTriangle className="w-5 h-5 text-amber-700" />,
    badgeBg: "bg-amber-50",
    badgeText: "text-amber-800",
    label: "Misleading",
  },
  "🔴 False": {
    bg: "bg-[#F9FAFB]",
    border: "border-rose-100/50",
    text: "text-rose-900",
    icon: <XCircle className="w-5 h-5 text-rose-700" />,
    badgeBg: "bg-rose-50",
    badgeText: "text-rose-800",
    label: "False Information",
  },
  "⚪ Unable to Verify": {
    bg: "bg-[#F9FAFB]",
    border: "border-slate-100/50",
    text: "text-slate-900",
    icon: <AlertTriangle className="w-5 h-5 text-slate-700" />,
    badgeBg: "bg-slate-50",
    badgeText: "text-slate-800",
    label: "Unable to Verify",
  },
}

// Map legacy string formats to the correct UI theme
themeConfig["verified"] = themeConfig["🟢 Verified"]
themeConfig["misleading"] = themeConfig["🟠 Misleading"]
themeConfig["false"] = themeConfig["🔴 False"]
themeConfig["unverified"] = themeConfig["⚪ Unable to Verify"]

export function TruthCard({
  verdict,
  confidenceScore,
  claimSummary,
  evidenceFound,
  aiExplanation,
  sourceCitations,
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
        {/* 1. Claim Summary */}
        <div className="mb-6">
          <h3 className={`text-[10px] font-bold uppercase tracking-widest mb-2 text-slate-400`}>Claim</h3>
          <p className="text-slate-800 font-bold text-xl leading-relaxed border-l-4 border-slate-200 pl-4">
            &quot;{claimSummary}&quot;
          </p>
        </div>

        {/* 2. Evidence Found */}
        <div className="mb-6 bg-slate-50 p-4 rounded-xl border border-slate-100">
          <h3 className={`text-[10px] font-bold uppercase tracking-widest mb-2 text-slate-500`}>Evidence Found</h3>
          <p className="text-slate-600 text-sm leading-relaxed font-mono overflow-y-auto max-h-32">
            {evidenceFound || "No evidence was found in the database."}
          </p>
        </div>
        
        {/* 3. AI Explanation */}
        <div className="mb-6 bg-white p-4 rounded-xl border border-slate-100 shadow-sm">
          <h3 className={`text-[10px] font-bold uppercase tracking-widest mb-2 text-teal-600`}>AI Explanation</h3>
          <p className="text-slate-700 text-sm leading-loose font-medium">
            {aiExplanation}
          </p>
        </div>

        {/* 4. Source Citations */}
        <div className="mb-8">
          <h3 className={`text-[10px] font-bold uppercase tracking-widest mb-3 text-slate-400`}>Sources</h3>
          <div className="flex flex-wrap gap-2">
            {sourceCitations && sourceCitations.length > 0 ? sourceCitations.map((source, idx) => (
              <span key={idx} className="inline-flex items-center gap-1.5 text-[11px] font-medium text-slate-500 bg-stone-50 border border-stone-100 px-3 py-1.5 rounded-md tracking-wide break-all">
                <LinkIcon className="w-3 h-3 text-slate-400 shrink-0" /> {source}
              </span>
            )) : (
              <span className="text-xs text-slate-400 italic">No direct sources</span>
            )}
          </div>
        </div>
        
        {/* 5. Verdict & Confidence */}
        <div className={`p-5 rounded-2xl border flex items-center justify-between ${theme.bg} ${theme.border}`}>
          <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-xl ${theme.badgeBg} ${theme.badgeText} text-sm font-black uppercase tracking-wider shadow-sm`}>
            {theme.icon}
            {theme.label}
          </div>
          <div className="flex flex-col items-end">
            <span className={`text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-0.5`}>
              Confidence
            </span>
            <span className="text-xl font-black text-slate-700">
              {confidenceScore}%
            </span>
          </div>
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
