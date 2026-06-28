"use client"
import Link from "next/link"
import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { Calendar, Filter, Link as LinkIcon, MoreVertical, Play, ChevronDown, CheckCircle2, XCircle, AlertCircle, HelpCircle, BarChart3, Image as ImageIcon, Loader2 } from "lucide-react"

export default function HistoryPage() {
  const [historyItems, setHistoryItems] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(true)
  
  // Pagination & Filters
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage, setItemsPerPage] = useState(10)
  const [platformFilter, setPlatformFilter] = useState("All")
  const [resultFilter, setResultFilter] = useState("All")
  const [dateFilter, setDateFilter] = useState("")

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch("/api/v1/history")
        if (response.ok) {
          const data = await response.json()
          setHistoryItems(data || [])
        }
      } catch (error) {
        console.error("Failed to fetch history:", error)
      } finally {
        setIsLoading(false)
      }
    }
    fetchHistory()
  }, [])

  const total = historyItems.length
  const counts = historyItems.reduce((acc, item) => {
    const verdict = item.verdict?.toLowerCase()
    if (verdict === 'true') acc.trueCount++
    else if (verdict === 'false') acc.falseCount++
    else if (verdict === 'misleading') acc.misleadingCount++
    else acc.unverifiedCount++
    return acc
  }, { trueCount: 0, falseCount: 0, misleadingCount: 0, unverifiedCount: 0 })

  const filteredItems = historyItems.filter(item => {
    const matchPlatform = platformFilter === "All" || (item.platform && item.platform.toLowerCase() === platformFilter.toLowerCase())
    const matchResult = resultFilter === "All" || (item.verdict && item.verdict.toLowerCase() === resultFilter.toLowerCase())
    
    let matchDate = true;
    if (dateFilter && item.completed_at) {
      const itemDate = new Date(item.completed_at);
      const now = new Date();
      if (dateFilter === "7") {
        const sevenDaysAgo = new Date(now.setDate(now.getDate() - 7));
        matchDate = itemDate >= sevenDaysAgo;
      } else if (dateFilter === "30") {
        const thirtyDaysAgo = new Date(now.setDate(now.getDate() - 30));
        matchDate = itemDate >= thirtyDaysAgo;
      } else if (dateFilter === "year") {
        const startOfYear = new Date(now.getFullYear(), 0, 1);
        matchDate = itemDate >= startOfYear;
      }
    }

    return matchPlatform && matchResult && matchDate
  })

  const totalFiltered = filteredItems.length
  const totalPages = Math.max(1, Math.ceil(totalFiltered / itemsPerPage))
  
  const currentItems = filteredItems.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage)

  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= totalPages) setCurrentPage(page)
  }

  return (
    <div className="max-w-[1400px] mx-auto space-y-6 pb-10">
       {/* Hero Section */}
       <div className="flex flex-col md:flex-row items-center justify-between mb-10 bg-white dark:bg-white/90 rounded-2xl border border-slate-100 dark:border-emerald-100 shadow-sm p-8">
          <div className="max-w-xl pr-6">
             <h1 className="text-3xl font-bold text-slate-800 dark:text-emerald-950 font-serif mb-2">History</h1>
             <p className="text-slate-500 dark:text-emerald-700/80 font-medium text-sm">View and track all your content verification history.</p>
          </div>
          <div className="hidden md:block w-[240px] shrink-0">
             <img src="/history_hero.png" alt="History hero" className="w-full h-auto object-contain mix-blend-multiply" />
          </div>
       </div>

       <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content Area (Left Column) */}
          <div className="lg:col-span-2 space-y-6">
             
              {/* Filter Bar */}
             <div className="flex flex-wrap items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                   <div className="relative flex items-center">
                      <Calendar className="w-3.5 h-3.5 text-slate-400 absolute left-4 pointer-events-none" />
                      <select 
                        aria-label="Filter by date range"
                        value={dateFilter}
                        onChange={(e) => {setDateFilter(e.target.value); setCurrentPage(1)}}
                        className="pl-9 pr-8 py-2 text-[11px] font-bold text-slate-600 dark:text-emerald-700 bg-white dark:bg-white/90 border border-slate-200 dark:border-emerald-100 rounded-xl hover:bg-slate-50 dark:hover:bg-emerald-50 shadow-sm appearance-none outline-none cursor-pointer"
                      >
                         <option value="">Date Range</option>
                         <option value="7">Last 7 Days</option>
                         <option value="30">Last 30 Days</option>
                         <option value="year">This Year</option>
                      </select>
                      <ChevronDown className="w-3 h-3 text-slate-400 absolute right-3 pointer-events-none" />
                   </div>
                   <select 
                      aria-label="Filter by platform"
                      value={platformFilter} 
                      onChange={(e) => {setPlatformFilter(e.target.value); setCurrentPage(1)}}
                      className="flex items-center gap-2 text-[11px] font-bold text-slate-600 dark:text-emerald-700 bg-white dark:bg-white/90 border border-slate-200 dark:border-emerald-100 rounded-xl px-4 py-2 hover:bg-slate-50 dark:hover:bg-emerald-50 shadow-sm outline-none appearance-none cursor-pointer"
                   >
                      <option value="All">All Platforms</option>
                      <option value="WhatsApp">WhatsApp</option>
                      <option value="Instagram">Instagram</option>
                      <option value="X">X (Twitter)</option>
                   </select>
                   <select 
                      aria-label="Filter by result"
                      value={resultFilter} 
                      onChange={(e) => {setResultFilter(e.target.value); setCurrentPage(1)}}
                      className="flex items-center gap-2 text-[11px] font-bold text-slate-600 bg-white border border-slate-200 rounded-xl px-4 py-2 hover:bg-slate-50 shadow-sm outline-none appearance-none cursor-pointer"
                   >
                      <option value="All">All Results</option>
                      <option value="True">True</option>
                      <option value="False">False</option>
                      <option value="Misleading">Misleading</option>
                   </select>
                </div>
                <details className="relative group">
                   <summary className="flex items-center gap-2 text-[11px] font-bold text-slate-600 bg-white border border-slate-200 rounded-xl px-4 py-2 hover:bg-slate-50 shadow-sm list-none cursor-pointer [&::-webkit-details-marker]:hidden">
                      <Filter className="w-3.5 h-3.5 text-slate-400" /> Filters
                   </summary>
                   <div className="absolute top-full right-0 mt-1 w-48 bg-white border border-slate-200 rounded-xl shadow-lg z-[999] p-2">
                      <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2 px-2 pt-1">Filter By</div>
                      <label className="flex items-center gap-2 px-2 py-1.5 hover:bg-slate-50 rounded-lg cursor-pointer">
                         <input type="checkbox" className="accent-emerald-500 rounded-sm" />
                         <span className="text-[11px] font-medium text-slate-700">High Confidence Only</span>
                      </label>
                      <label className="flex items-center gap-2 px-2 py-1.5 hover:bg-slate-50 rounded-lg cursor-pointer">
                         <input type="checkbox" className="accent-emerald-500 rounded-sm" />
                         <span className="text-[11px] font-medium text-slate-700">Has Video</span>
                      </label>
                   </div>
                </details>
             </div>

             {/* History Table List */}
             <div className="bg-white dark:bg-white/90 rounded-2xl border border-slate-100 dark:border-emerald-100 shadow-sm overflow-hidden">
                 <div className="flex flex-col gap-0 p-2">
                    {/* Header */}
                    <div className="flex items-center text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2 px-4 py-3">
                       <div className="flex-1">Content</div>
                       <div className="w-24 text-center">Platform</div>
                       <div className="w-24 text-center">Result</div>
                       <div className="w-20 text-center">Confidence</div>
                       <div className="w-20 text-right">Time</div>
                       <div className="w-8"></div>
                    </div>

                    <hr className="border-slate-50 mx-4 mb-2" />

                    {isLoading ? (
                      <div className="py-12 flex justify-center items-center">
                        <Loader2 className="w-8 h-8 text-emerald-500 animate-spin" />
                      </div>
                    ) : currentItems.length === 0 ? (
                      <div className="py-16 flex flex-col items-center justify-center text-center opacity-70">
                         <img src="/zen_garden_empty.png" alt="Empty History" className="w-48 h-48 object-contain mb-6 rounded-3xl shadow-sm mix-blend-multiply" />
                         <h4 className="text-lg font-bold text-slate-700 mb-2">Your history is clear</h4>
                         <p className="text-sm text-slate-500 max-w-sm leading-relaxed">No verifications found. Start verifying claims to see your history grow like a peaceful garden.</p>
                      </div>
                    ) : (
                      <div className="relative pl-6 py-2 mb-4">
                        {/* The vertical timeline rail */}
                        <div className="absolute top-0 bottom-0 left-[35px] w-0.5 bg-slate-100 dark:bg-emerald-100 z-0"></div>
                        
                        <div className="flex flex-col gap-4 relative z-10">
                          {currentItems.map((item, idx) => (
                            <div key={item.id} className="relative flex items-center group">
                               {/* Timeline Node & Connector */}
                               <div className="absolute -left-6 flex items-center">
                                  <motion.div 
                                    className="w-3 h-3 rounded-full border-2 border-white dark:border-[#f4f7f5] bg-slate-300 dark:bg-emerald-300 group-hover:bg-emerald-500 shadow-sm transition-colors z-10" 
                                    whileHover={{ scale: 1.5 }}
                                  />
                                  <div className="w-4 h-0.5 bg-slate-100 dark:bg-emerald-100 group-hover:bg-emerald-200 dark:group-hover:bg-emerald-400 transition-colors"></div>
                               </div>

                               {/* Holographic 3D Tilt Card */}
                               <motion.div 
                                 whileHover={{ scale: 1.01, rotateX: 2, rotateY: -1, y: -2 }}
                                 transition={{ type: "spring", stiffness: 300, damping: 20 }}
                                 className="flex items-center bg-white dark:bg-white/90 p-3 px-4 rounded-xl transition-all border border-slate-100 dark:border-emerald-100 shadow-sm hover:shadow-[0_10px_40px_-10px_rgba(0,0,0,0.08)] flex-1 ml-4 cursor-pointer relative overflow-hidden"
                               >
                                  {/* Glassmorphic Re-Analyze Overlay on Hover */}
                                  <div className="absolute inset-0 bg-white/40 backdrop-blur-[1px] opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center z-20">
                                     <button className="bg-emerald-600 text-white font-bold text-[11px] px-4 py-1.5 rounded-lg shadow-lg hover:bg-emerald-700 hover:scale-105 transition-all flex items-center gap-2">
                                        <Play className="w-3 h-3" /> Re-Analyze
                                     </button>
                                  </div>

                                  <div className="flex items-center gap-4 flex-1 min-w-0 relative z-10">
                                     <div className="w-14 h-10 rounded-lg bg-slate-50 border border-slate-200 flex flex-col p-1.5 shrink-0 shadow-sm">
                                        <div className="w-full h-1 bg-slate-200 rounded-sm mb-1"></div>
                                        <div className="w-4/5 h-1 bg-slate-200 rounded-sm mb-1"></div>
                                        <div className="w-full h-1 bg-slate-200 rounded-sm mb-1"></div>
                                        <div className="w-3/5 h-1 bg-slate-200 rounded-sm"></div>
                                     </div>
                                     <div className="flex-1 min-w-0">
                                        <p className="text-[11px] font-bold text-slate-800 dark:text-emerald-950 truncate mb-0.5">{item.claim?.extracted_claim || item.claim?.raw_content || "Unknown content"}</p>
                                        <p className="text-[9px] text-slate-500 font-medium">{item.platform || "Web Application"}</p>
                                     </div>
                                  </div>
                                  <div className="w-24 flex justify-center relative z-10">
                                     <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-500"><span className="text-[9px] font-bold">{item.platform ? item.platform.substring(0, 3).toUpperCase() : "WEB"}</span></div>
                                  </div>
                                  <div className="w-24 flex justify-center relative z-10">
                                     <span className={`text-[9px] font-bold px-2.5 py-1 rounded-md uppercase border ${
                                       item.verdict?.toLowerCase() === "false" ? "bg-red-50 text-red-600 border-red-100 group-hover:shadow-[0_0_15px_rgba(244,63,94,0.4)]" :
                                       item.verdict?.toLowerCase() === "misleading" ? "bg-amber-50 text-amber-700 border-amber-100 group-hover:shadow-[0_0_15px_rgba(245,158,11,0.4)]" :
                                       item.verdict?.toLowerCase() === "true" ? "bg-emerald-50 text-emerald-700 border-emerald-100 group-hover:shadow-[0_0_15px_rgba(16,185,129,0.4)]" :
                                       "bg-blue-50 text-blue-600 border-blue-100 group-hover:shadow-[0_0_15px_rgba(59,130,246,0.4)]"
                                     } transition-all duration-300`}>
                                       {item.verdict || "Unverified"}
                                     </span>
                                  </div>
                                  <div className="w-20 text-center relative z-10">
                                     <span className="text-[11px] font-bold text-emerald-600">{item.confidence_score || 0}%</span>
                                  </div>
                                  <div className="w-20 text-right relative z-10">
                                     <span className="text-[10px] font-medium text-slate-400">
                                       {item.completed_at ? new Date(item.completed_at).toLocaleDateString() : "-"}
                                     </span>
                                  </div>
                                  <div className="w-8 flex justify-end pr-1 relative z-10">
                                     <button aria-label="More options" className="text-slate-400 hover:text-slate-600"><MoreVertical className="w-4 h-4" /></button>
                                  </div>
                               </motion.div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                 </div>

                 {/* Pagination Footer */}
                 <div className="border-t border-slate-100 dark:border-emerald-100 p-4 px-6 flex flex-wrap gap-4 items-center justify-between">
                    <span className="text-[11px] font-medium text-slate-500">
                      Showing {Math.min((currentPage - 1) * itemsPerPage + 1, totalFiltered)} to {Math.min(currentPage * itemsPerPage, totalFiltered)} of {totalFiltered} results
                    </span>
                    <div className="flex items-center gap-4">
                       <div className="flex items-center gap-1">
                          <button 
                            disabled={currentPage === 1}
                            onClick={() => handlePageChange(currentPage - 1)}
                            className="w-7 h-7 flex items-center justify-center rounded border border-slate-200 dark:border-slate-800 text-slate-400 dark:text-slate-500 hover:bg-slate-50 dark:hover:bg-slate-800 disabled:opacity-50"
                          >‹</button>
                          
                          {Array.from({ length: totalPages }).map((_, i) => {
                             const page = i + 1;
                             if (page === 1 || page === totalPages || (page >= currentPage - 1 && page <= currentPage + 1)) {
                                return (
                                   <button 
                                     key={page}
                                     onClick={() => handlePageChange(page)}
                                     className={`w-7 h-7 flex items-center justify-center rounded text-[11px] font-bold ${page === currentPage ? 'bg-emerald-50 dark:bg-emerald-100 text-emerald-600 dark:text-emerald-700' : 'hover:bg-slate-50 dark:hover:bg-emerald-50 text-slate-600 dark:text-emerald-700 border border-transparent'}`}
                                   >
                                     {page}
                                   </button>
                                );
                             } else if (page === currentPage - 2 || page === currentPage + 2) {
                                return <span key={`ellipsis-${page}`} className="w-5 text-center text-slate-400 text-xs">...</span>
                             }
                             return null;
                          })}
                          
                          <button 
                            disabled={currentPage === totalPages}
                            onClick={() => handlePageChange(currentPage + 1)}
                            className="w-7 h-7 flex items-center justify-center rounded border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 disabled:opacity-50"
                          >›</button>
                       </div>
                       <select 
                          aria-label="Items per page"
                          value={itemsPerPage}
                          onChange={(e) => {setItemsPerPage(Number(e.target.value)); setCurrentPage(1)}}
                          className="flex items-center gap-2 text-[11px] font-medium text-slate-600 dark:text-emerald-700 border border-slate-200 dark:border-emerald-200 bg-white dark:bg-white/90 rounded-md px-2 py-1 hover:bg-slate-50 dark:hover:bg-emerald-50 outline-none cursor-pointer"
                       >
                          <option value="10">10 / page</option>
                          <option value="25">25 / page</option>
                          <option value="50">50 / page</option>
                       </select>
                    </div>
                 </div>
             </div>
          </div>

          {/* Right Column Cards */}
          <div className="space-y-6">
             {/* History Overview */}
             <div className="bg-white dark:bg-white/90 rounded-2xl border border-slate-100 dark:border-emerald-100 shadow-sm p-6">
                <h3 className="text-[13px] font-bold text-slate-800 dark:text-emerald-950 mb-6">History Overview</h3>
                
                <div className="space-y-4">
                   <div className="flex items-center gap-4 pb-4 border-b border-slate-50">
                      <div className="w-10 h-10 rounded-full bg-emerald-50 flex items-center justify-center shrink-0">
                         <div className="w-5 h-5 bg-emerald-600 rounded-sm flex items-center justify-center clip-shield">
                            <CheckCircle2 className="w-3 h-3 text-white" />
                         </div>
                       </div>
                       <div>
                         <h4 className="text-[16px] font-bold text-slate-800 dark:text-emerald-900 leading-none mb-1">{total}</h4>
                         <p className="text-[10px] font-medium text-slate-500">Total Verifications</p>
                      </div>
                   </div>

                   <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-full bg-emerald-50/50 border border-emerald-100 flex items-center justify-center shrink-0">
                         <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                      </div>
                      <div>
                         <h4 className="text-[14px] font-bold text-slate-800 dark:text-emerald-900 leading-none mb-1">{counts.trueCount}</h4>
                         <p className="text-[10px] font-medium text-slate-500">True</p>
                      </div>
                   </div>

                   <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-full bg-red-50/50 border border-red-100 flex items-center justify-center shrink-0">
                         <XCircle className="w-5 h-5 text-red-500" />
                      </div>
                      <div>
                         <h4 className="text-[14px] font-bold text-slate-800 dark:text-emerald-900 leading-none mb-1">{counts.falseCount}</h4>
                         <p className="text-[10px] font-medium text-slate-500">False</p>
                      </div>
                   </div>

                   <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-full bg-amber-50/50 border border-amber-100 flex items-center justify-center shrink-0">
                         <AlertCircle className="w-5 h-5 text-amber-500" />
                      </div>
                      <div>
                         <h4 className="text-[14px] font-bold text-slate-800 dark:text-emerald-900 leading-none mb-1">{counts.misleadingCount}</h4>
                         <p className="text-[10px] font-medium text-slate-500">Misleading</p>
                      </div>
                   </div>

                   <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-full bg-blue-50/50 border border-blue-100 flex items-center justify-center shrink-0">
                         <HelpCircle className="w-5 h-5 text-blue-500" />
                      </div>
                      <div>
                         <h4 className="text-[14px] font-bold text-slate-800 dark:text-emerald-900 leading-none mb-1">{counts.unverifiedCount}</h4>
                         <p className="text-[10px] font-medium text-slate-500">Unverified</p>
                      </div>
                   </div>
                </div>
             </div>

             {/* Keep track Spread peace */}
             <div className="bg-[#f0fdf4] dark:bg-emerald-50/50 rounded-2xl border border-[#dcfce7] dark:border-emerald-100 p-6 text-center">
                <div className="w-full h-[120px] mb-4 relative flex items-center justify-center">
                   <img src="/history_track.png" alt="Keep track" className="w-[120%] h-[120%] object-contain mix-blend-multiply opacity-90" />
                </div>
                <h3 className="text-[13px] font-bold text-slate-800 dark:text-emerald-950 mb-2">Keep track. Spread peace.</h3>
                <p className="text-[10px] font-medium text-slate-500 mb-6 leading-relaxed">
                   Review your past verifications and help build a safer digital world.
                </p>
                <Link href="/dashboard" className="bg-white dark:bg-white border border-slate-200 dark:border-emerald-200 hover:bg-slate-50 dark:hover:bg-emerald-50 text-slate-700 dark:text-emerald-800 text-[11px] font-bold py-2 px-5 rounded-lg flex items-center justify-center gap-2 transition-colors mx-auto shadow-sm w-fit mt-4">
                   View Reports <BarChart3 className="w-3.5 h-3.5" />
                </Link>
             </div>
          </div>
       </div>

    </div>
  )
}

function ShieldIcon(props: any) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}>
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
    </svg>
  )
}
