"use client"

import Link from "next/link"
import { useState, useEffect } from "react"
import { ShieldCheck, ShieldAlert, Users, Target, ChevronDown, MoreVertical, Scan, Wind } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"
import { AnimatedCounter } from "@/components/AnimatedCounter"

// SVG Map of India (Simplified representation)
const IndiaMap = () => (
  <svg viewBox="0 0 800 900" className="w-full h-full drop-shadow-sm">
    <path d="M230,200 L260,150 L320,100 L380,120 L400,100 L440,150 L500,160 L540,240 L500,280 L520,320 L580,350 L640,320 L720,340 L700,420 L660,460 L600,450 L580,500 L500,560 L450,650 L400,800 L350,850 L300,800 L280,680 L200,600 L150,500 L80,480 L100,420 L150,380 L180,300 L180,240 Z" fill="#F8FAFC" stroke="#E2E8F0" strokeWidth="2" />
    <path d="M260,150 L320,100 L380,120 L400,100 L440,150 L350,220 Z" fill="#F1F5F9" /> 
    <path d="M500,280 L520,320 L580,350 L640,320 L720,340 L700,420 L660,460 L600,450 L500,380 Z" fill="#F1F5F9" /> 
    <path d="M150,500 L80,480 L100,420 L150,380 L180,300 L220,400 Z" fill="#F1F5F9" /> 
    <path d="M280,680 L200,600 L150,500 L250,550 Z" fill="#F1F5F9" /> 
    <path d="M400,800 L350,850 L300,800 L280,680 L400,700 Z" fill="#F1F5F9" /> 
    
    {/* Pulse of Peace Activity Spots */}
    <motion.circle cx="620" cy="380" r="15" fill="#34D399" animate={{ opacity: [0.1, 0.6, 0.1], r: [10, 30, 10] }} transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }} />
    <motion.circle cx="250" cy="550" r="10" fill="#34D399" animate={{ opacity: [0.1, 0.5, 0.1], r: [8, 20, 8] }} transition={{ duration: 3.5, repeat: Infinity, ease: "easeInOut", delay: 1 }} />
    <motion.circle cx="350" cy="220" r="12" fill="#34D399" animate={{ opacity: [0.2, 0.8, 0.2], r: [10, 25, 10] }} transition={{ duration: 5, repeat: Infinity, ease: "easeInOut", delay: 0.5 }} />
  </svg>
)

const ProcessingVerificationItem = () => {
   const [step, setStep] = useState(0)
   const steps = ["Extracting entities...", "Querying AltNews API...", "Cross-referencing PIB...", "Synthesizing truth..."]
   
   useEffect(() => {
      const interval = setInterval(() => {
         setStep(s => (s + 1) % steps.length)
      }, 1500)
      return () => clearInterval(interval)
   }, [])

   return (
      <div className="flex items-center p-3 rounded-xl border border-emerald-100 bg-emerald-50/50 relative overflow-hidden shadow-sm">
         <motion.div 
            animate={{ top: ["0%", "100%", "0%"] }} 
            transition={{ duration: 2.5, repeat: Infinity, ease: "linear" }}
            className="absolute left-0 right-0 h-[1px] bg-emerald-400 shadow-[0_0_8px_#34D399] z-10"
         />
         <div className="w-10 h-10 rounded-full bg-white border border-emerald-100 flex items-center justify-center shrink-0 shadow-sm relative z-20">
            <motion.div animate={{ rotate: 360 }} transition={{ duration: 3, repeat: Infinity, ease: "linear" }}>
               <Scan strokeWidth={1.5} className="w-4 h-4 text-emerald-500" />
            </motion.div>
         </div>
         <div className="flex-1 min-w-0 ml-3 relative z-20">
            <div className="flex items-center gap-2 mb-0.5">
               <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
               <p className="text-[11px] font-bold text-slate-800 truncate">PROCESSING ANALYSIS</p>
            </div>
            <p className="text-[9px] text-emerald-600 font-medium tracking-wide uppercase">
               {steps[step]}
            </p>
         </div>
      </div>
   )
}

export default function Dashboard() {
  const [userName, setUserName] = useState("Aman")
  const [stats, setStats] = useState<any>(null)
  const [recentVerifications, setRecentVerifications] = useState<any[]>([])
  const [dateRange, setDateRange] = useState(7)

  useEffect(() => {
    const storedName = localStorage.getItem('sukoon_name')
    if (storedName) {
      setUserName(storedName.split(' ')[0])
    }

    const fetchDashboardData = async () => {
      try {
        const [statsRes, historyRes] = await Promise.all([
          fetch(`/api/v1/dashboard/stats?days=${dateRange}`),
          fetch("/api/v1/history")
        ])
        if (statsRes.ok) setStats(await statsRes.json())
        if (historyRes.ok) {
           const historyData = await historyRes.json()
           setRecentVerifications((historyData || []).slice(0, 5))
        }
      } catch (error) {
        console.error("Failed to fetch dashboard data", error)
      }
    }
    fetchDashboardData()
  }, [dateRange])

  // Helper to generate SVG path
  const generatePath = (dataKey: string) => {
    if (!stats || !stats.daily_stats || stats.daily_stats.length === 0) return ""
    const points = stats.daily_stats.map((day: any, i: number) => {
      // Find max value to scale the graph (max 10, min 1 just to show some lines if 0)
      const maxVal = Math.max(10, ...stats.daily_stats.map((d: any) => Math.max(d.analyzed, d.false_claims, d.hate_speech, d.misleading)))
      const x = 100 + (i * 110)
      const y = 250 - ((day[dataKey] / maxVal) * 200)
      return `${x},${y}`
    })
    return `M ${points.join(' L ')}`
  }

  return (
    <div className="max-w-[1400px] mx-auto space-y-6 pb-10">
      
      {/* Hero Section */}
      <div className="flex flex-col md:flex-row items-center justify-between bg-white rounded-[2rem] border border-slate-100 p-8 md:pl-10 relative overflow-hidden shadow-sm">
         <div className="z-10 max-w-full md:max-w-[60%] relative">
            <h1 className="text-3xl font-bold text-slate-800 font-serif mb-2 flex items-center gap-2 flex-wrap">
               Good morning, {userName} <span className="text-2xl">👋</span>
            </h1>
            <p className="text-slate-500 font-medium text-sm">Here's what's happening with your verification shield today.</p>
         </div>
         <div className="w-[300px] h-[160px] md:absolute md:-right-4 md:-bottom-2 z-0 mt-6 md:mt-0 opacity-90 md:opacity-100">
            <img src="/man_laptop.png" alt="Man with laptop" className="w-full h-full object-contain mix-blend-multiply" />
         </div>
      </div>

      {/* The Serene Dropzone */}
      <Link href="/analyze-reel" className="block w-full">
         <motion.div 
           whileHover="hover"
           className="w-full bg-slate-50/50 rounded-[2rem] p-10 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] border-2 border-dashed border-slate-200 flex flex-col items-center justify-center cursor-pointer transition-colors hover:bg-emerald-50/50 hover:border-emerald-200 group"
         >
           <motion.div 
              variants={{ hover: { scale: 1.1, rotate: 90, borderColor: '#34D399', backgroundColor: '#ECFDF5' } }}
              transition={{ duration: 0.3 }}
              className="w-16 h-16 rounded-full bg-white border border-slate-100 flex items-center justify-center text-slate-400 mb-4 shadow-sm"
           >
              <Scan strokeWidth={1.5} className="w-8 h-8 group-hover:text-emerald-500 transition-colors" />
           </motion.div>
           <h3 className="text-sm font-bold text-slate-700 tracking-[0.3em] uppercase font-serif mb-2">Drop content to verify</h3>
           <p className="text-xs text-slate-500 font-medium">Drag and drop images, videos, or paste a link here for instant forensic analysis.</p>
         </motion.div>
      </Link>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
         <div className="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm flex flex-col gap-4">
           <div className="w-12 h-12 rounded-full bg-emerald-50 flex items-center justify-center text-emerald-600 mb-2">
              <ShieldCheck className="w-6 h-6" />
           </div>
           <div>
              <p className="text-[11px] font-bold text-slate-500 mb-1">Content Analyzed</p>
              <div className="flex items-baseline gap-3">
                 <h2 className="text-[28px] font-black text-slate-800 leading-none">
                   <AnimatedCounter value={stats?.total_analyzed ?? 0} />
                 </h2>
                 <span className="text-xs font-bold text-slate-400 flex items-center gap-0.5">
                    -
                 </span>
              </div>
              <p className="text-[9px] text-slate-400 font-medium mt-1">vs yesterday</p>
           </div>
        </div>

        <div className="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm flex flex-col gap-4">
           <div className="w-12 h-12 rounded-full bg-red-50 flex items-center justify-center text-red-500 mb-2">
              <ShieldAlert className="w-6 h-6" />
           </div>
           <div>
              <p className="text-[11px] font-bold text-slate-500 mb-1">False Claims Detected</p>
              <div className="flex items-baseline gap-3">
                 <h2 className="text-[28px] font-black text-slate-800 leading-none">
                   <AnimatedCounter value={stats?.false_claims ?? 0} />
                 </h2>
                 <span className="text-xs font-bold text-slate-400 flex items-center gap-0.5">
                    -
                 </span>
              </div>
              <p className="text-[9px] text-slate-400 font-medium mt-1">vs yesterday</p>
           </div>
        </div>

        <div className="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm flex flex-col gap-4">
           <div className="w-12 h-12 rounded-full bg-amber-50 flex items-center justify-center text-amber-500 mb-2">
              <Users className="w-6 h-6" />
           </div>
           <div>
              <p className="text-[11px] font-bold text-slate-500 mb-1">Hate Speech Intercepted</p>
              <div className="flex items-baseline gap-3">
                 <h2 className="text-[28px] font-black text-slate-800 leading-none">
                   <AnimatedCounter value={stats?.hate_speech ?? 0} />
                 </h2>
                 <span className="text-xs font-bold text-slate-400 flex items-center gap-0.5">
                    -
                 </span>
              </div>
              <p className="text-[9px] text-slate-400 font-medium mt-1">vs yesterday</p>
           </div>
        </div>

        <div className="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm flex flex-col gap-4">
           <div className="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center text-blue-500 mb-2">
              <Target className="w-6 h-6" />
           </div>
           <div>
              <p className="text-[11px] font-bold text-slate-500 mb-1">Verification Accuracy</p>
              <div className="flex items-baseline gap-3">
                 <h2 className="text-[28px] font-black text-slate-800 leading-none">
                   {stats ? <AnimatedCounter value={stats.verification_accuracy} suffix="%" /> : '-'}
                 </h2>
                 <span className="text-xs font-bold text-slate-400 flex items-center gap-0.5">
                    -
                 </span>
              </div>
              <p className="text-[9px] text-slate-400 font-medium mt-1">vs last 7 days</p>
           </div>
        </div>
      </div>

      {/* Middle Row: Line Chart & Recent Verifications */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
         {/* Line Chart */}
         <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-100 shadow-sm p-6 flex flex-col">
            <div className="flex justify-between items-center mb-6">
               <h3 className="text-sm font-bold text-slate-800">Verification Overview <span className="text-slate-400 font-normal ml-1">ⓘ</span></h3>
               <div className="relative">
                 <select 
                   value={dateRange} 
                   aria-label="Select date range"
                   onChange={(e) => setDateRange(Number(e.target.value))} 
                   className="flex items-center gap-2 text-xs font-semibold text-slate-600 border border-slate-200 rounded-lg pl-3 pr-8 py-1.5 hover:bg-slate-50 outline-none cursor-pointer appearance-none bg-transparent relative z-10"
                 >
                   <option value={7}>Last 7 Days</option>
                   <option value={14}>Last 14 Days</option>
                   <option value={30}>Last 30 Days</option>
                 </select>
                 <ChevronDown className="w-3 h-3 absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 z-0 pointer-events-none" />
               </div>
            </div>
            
            <div className="flex-1 relative min-h-[250px] w-full">
               {/* Custom SVG Line Chart */}
               <svg viewBox="0 0 800 300" className="w-full h-full" preserveAspectRatio="none">
                  {/* Grid Lines */}
                  {[0, 1, 2, 3, 4].map((i) => (
                    <g key={i}>
                       <line x1="40" y1={250 - i*60} x2="800" y2={250 - i*60} stroke="#F1F5F9" strokeWidth="1" />
                       <text x="30" y={254 - i*60} fontSize="10" fill="#94A3B8" textAnchor="end">{i*200}</text>
                    </g>
                  ))}
                  
                  {/* X Axis Labels */}
                  {(stats?.daily_stats || []).map((day: any, i: number) => (
                    <text key={day.date} x={100 + i*110} y="270" fontSize="10" fill="#94A3B8" textAnchor="middle">{day.date}</text>
                  ))}
                  {(!stats || stats.daily_stats.length === 0) && ['May 14', 'May 15', 'May 16', 'May 17', 'May 18', 'May 19', 'May 20'].map((label, i) => (
                    <text key={label} x={100 + i*110} y="270" fontSize="10" fill="#94A3B8" textAnchor="middle">{label}</text>
                  ))}

                  {/* Lines & Points */}
                  {/* Total Analyzed (Green) */}
                  <path d={stats ? generatePath("analyzed") : ""} fill="none" stroke="#10B981" strokeWidth="2.5" />
                  
                  {/* False Claims (Red) */}
                  <path d={stats ? generatePath("false_claims") : ""} fill="none" stroke="#F43F5E" strokeWidth="2.5" />
                  
                  {/* Hate Speech (Yellow) */}
                  <path d={stats ? generatePath("hate_speech") : ""} fill="none" stroke="#FBBF24" strokeWidth="2.5" />
                  
                  {/* Misleading (Blue) */}
                  <path d={stats ? generatePath("misleading") : ""} fill="none" stroke="#60A5FA" strokeWidth="2.5" />
                  
               </svg>
            </div>
            
            {/* Chart Legend */}
            <div className="flex items-center justify-center gap-6 mt-6 pt-6 border-t border-slate-50">
               <div className="flex items-center gap-2"><div className="w-3 h-1.5 rounded-full bg-emerald-500"></div><span className="text-[11px] font-semibold text-slate-700">Total Analyzed</span></div>
               <div className="flex items-center gap-2"><div className="w-3 h-1.5 rounded-full bg-rose-500"></div><span className="text-[11px] font-semibold text-slate-700">False Claims</span></div>
               <div className="flex items-center gap-2"><div className="w-3 h-1.5 rounded-full bg-amber-400"></div><span className="text-[11px] font-semibold text-slate-700">Hate Speech</span></div>
               <div className="flex items-center gap-2"><div className="w-3 h-1.5 rounded-full bg-blue-400"></div><span className="text-[11px] font-semibold text-slate-700">Misleading</span></div>
            </div>
         </div>

         {/* Recent Verifications */}
         <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 flex flex-col">
            <div className="flex justify-between items-center mb-6">
               <h3 className="text-sm font-bold text-slate-800">Recent Verifications</h3>
               <Link href="/history" className="text-[11px] font-bold text-emerald-600 hover:text-emerald-700">View All</Link>
            </div>
            
            <div className="flex flex-col gap-5 flex-1">

                {recentVerifications.length > 0 ? (
                  recentVerifications.map((item) => (
                    <div key={item.id} className="flex items-center hover:bg-slate-50 p-2 rounded-xl transition-colors border border-transparent">
                      <div className="w-10 h-10 rounded-full bg-slate-50 border border-slate-200 flex items-center justify-center shrink-0 shadow-sm overflow-hidden text-emerald-500 font-bold text-xs uppercase">
                         {item.platform ? item.platform.substring(0, 2) : "WEB"}
                      </div>
                      <div className="flex-1 min-w-0 ml-3">
                         <p className="text-[11px] font-bold text-slate-800 truncate mb-0.5">{item.claim?.extracted_claim || item.claim?.raw_content || "Unknown content"}</p>
                         <p className="text-[9px] text-slate-500 font-medium">
                           {item.verdict || "Unverified"} • {item.confidence_score || 0}% Confidence
                         </p>
                      </div>
                      <button aria-label="More options" className="text-slate-400 hover:text-slate-600"><MoreVertical className="w-4 h-4" /></button>
                    </div>
                  ))
                ) : (
                  <motion.div 
                     animate={{ scale: [0.98, 1.02, 0.98], opacity: [0.7, 1, 0.7] }} 
                     transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                     className="flex flex-col items-center justify-center flex-1 py-10 text-emerald-700/50"
                  >
                     <Wind strokeWidth={1} className="w-12 h-12 mb-3" />
                     <p className="text-[11px] font-bold tracking-widest uppercase font-serif">All Clear</p>
                     <p className="text-[9px] font-medium text-slate-400 mt-1">No active misinformation threats detected.</p>
                  </motion.div>
                )}
             </div>
         </div>
      </div>

      {/* Bottom Row: Platforms, Map, Quote */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
         {/* Top Platforms */}
         <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6">
            <div className="flex justify-between items-center mb-6">
               <h3 className="text-sm font-bold text-slate-800">Top Platforms</h3>
               <div className="relative">
                 <select 
                   value={dateRange} 
                   aria-label="Select date range for platforms"
                   onChange={(e) => setDateRange(Number(e.target.value))} 
                   className="flex items-center gap-2 text-[10px] font-bold text-slate-500 bg-slate-50 border border-slate-100 rounded pl-2 pr-6 py-1 hover:bg-slate-100 outline-none cursor-pointer appearance-none relative z-10"
                 >
                   <option value={7}>Last 7 Days</option>
                   <option value={14}>Last 14 Days</option>
                   <option value={30}>Last 30 Days</option>
                 </select>
                 <ChevronDown className="w-3 h-3 absolute right-1.5 top-1/2 -translate-y-1/2 text-slate-400 z-0 pointer-events-none" />
               </div>
            </div>
            
            <div className="flex items-center justify-between gap-4 mt-8">
               <div className="w-24 h-24 relative shrink-0">
                 <svg viewBox="0 0 100 100" className="w-full h-full transform -rotate-90 drop-shadow-sm">
                   <circle cx="50" cy="50" r="42" fill="transparent" stroke="#F1F5F9" strokeWidth="6" />
                   <motion.circle 
                     cx="50" cy="50" r="42" fill="transparent" stroke="#10B981" strokeWidth="6"
                     strokeLinecap="round" strokeDasharray="264"
                     initial={{ strokeDashoffset: 264 }}
                     animate={{ strokeDashoffset: 264 - (264 * ((stats?.platform_stats?.[0]?.percentage ?? 0) / 100)) }}
                     transition={{ duration: 1.5, ease: "easeOut" }}
                   />
                   <motion.circle 
                     cx="50" cy="50" r="42" fill="transparent" stroke="#F43F5E" strokeWidth="6"
                     strokeLinecap="round" strokeDasharray="264"
                     initial={{ strokeDashoffset: 264 }}
                     animate={{ strokeDashoffset: 264 - (264 * ((stats?.platform_stats?.[1]?.percentage ?? 0) / 100)) }}
                     transition={{ duration: 1.5, ease: "easeOut", delay: 0.2 }}
                     style={{ transform: `rotate(${360 * ((stats?.platform_stats?.[0]?.percentage ?? 0) / 100)}deg)`, transformOrigin: '50% 50%' }}
                   />
                 </svg>
                 <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-2xl font-black text-slate-800 font-serif leading-none">
                       {stats ? <AnimatedCounter value={stats.verification_accuracy} suffix="%" /> : '-'}
                    </span>
                    <span className="text-[7px] font-bold text-slate-400 uppercase tracking-widest mt-1">ACCURACY</span>
                 </div>
               </div>
               
               <div className="flex-1 space-y-4 opacity-50">
                  <div className="flex items-center justify-between">
                     <div className="flex items-center gap-2">
                        <div className="w-5 h-5 rounded-full bg-[#25D366] flex items-center justify-center"><div className="w-2.5 h-2.5 bg-white rounded-full"></div></div>
                        <span className="text-[11px] font-semibold text-slate-700">WhatsApp</span>
                     </div>
                     <span className="text-[11px] font-bold text-slate-800">{stats?.platform_stats?.[0]?.percentage ?? 0}%</span>
                  </div>
                  <div className="flex items-center justify-between">
                     <div className="flex items-center gap-2">
                        <div className="w-5 h-5 rounded-full bg-gradient-to-tr from-[#FD1D1D] to-[#833AB4] flex items-center justify-center"><div className="w-2.5 h-2.5 border border-white rounded-lg"></div></div>
                        <span className="text-[11px] font-semibold text-slate-700">Instagram</span>
                     </div>
                     <span className="text-[11px] font-bold text-slate-800">{stats?.platform_stats?.[1]?.percentage ?? 0}%</span>
                  </div>
                  <div className="flex items-center justify-between">
                     <div className="flex items-center gap-2">
                        <div className="w-5 h-5 rounded-full bg-black flex items-center justify-center"><span className="text-white text-[8px] font-bold">X</span></div>
                        <span className="text-[11px] font-semibold text-slate-700">X (Twitter)</span>
                     </div>
                     <span className="text-[11px] font-bold text-slate-800">{stats?.platform_stats?.[2]?.percentage ?? 0}%</span>
                  </div>
               </div>
            </div>
         </div>
         
         {/* Quote Banner */}
         <div className="bg-emerald-50/70 rounded-2xl border border-emerald-100/50 p-6 relative overflow-hidden flex items-center">
            <div className="relative z-10 w-[60%]">
               <h1 className="text-4xl text-emerald-300 font-serif mb-2 leading-none">“</h1>
               <p className="text-[13px] font-bold text-slate-800 leading-relaxed font-serif pr-4">
                  In a world of noise, Sukoon AI brings truth, so communities can live in peace.
               </p>
            </div>
            <div className="absolute right-0 bottom-0 w-[140px] h-full z-0 flex items-end justify-center">
               <img src="/meditating_woman.png" alt="Meditating" className="w-full h-full object-contain mix-blend-multiply opacity-90 object-bottom" />
            </div>
         </div>
      </div>
      
    </div>
  )
}
