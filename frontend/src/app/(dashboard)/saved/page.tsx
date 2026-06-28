"use client"
import { useState, useRef, useEffect } from "react"
import { Bookmark, MoreVertical, ChevronDown, Image as ImageIcon, Link as LinkIcon, FileText, Video, Mic, ChevronRight } from "lucide-react"

export default function SavedPage() {
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);
  
  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = () => setActiveDropdown(null);
    document.addEventListener("click", handleClickOutside);
    return () => document.removeEventListener("click", handleClickOutside);
  }, []);
  return (
    <div className="max-w-[1400px] mx-auto space-y-6 pb-10">
       {/* Hero Section */}
       <div className="flex flex-col md:flex-row items-center justify-between mb-10 bg-white rounded-2xl border border-slate-100 shadow-sm p-8">
          <div className="max-w-xl pr-6 flex items-start gap-4">
             <div className="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-2xl flex items-center justify-center border border-emerald-100 shrink-0">
                <Bookmark className="w-6 h-6 stroke-[2]" />
             </div>
             <div>
                <h1 className="text-3xl font-bold text-slate-800 font-serif mb-2">Saved</h1>
                <p className="text-slate-500 font-medium text-sm">Your saved content for quick access and future reference.</p>
             </div>
          </div>
          <div className="hidden md:block w-[280px] shrink-0">
             <img src="/saved_hero.png" alt="Saved hero" className="w-full h-auto object-contain mix-blend-multiply" />
          </div>
       </div>

       <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content Area (Left Column) */}
          <div className="lg:col-span-2 space-y-6">
             
             {/* Filter Bar */}
             <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 pb-4 relative">
                <div className="flex items-center gap-3">
                   <div className="relative flex items-center">
                      <svg viewBox="0 0 24 24" className="w-3.5 h-3.5 fill-slate-400 absolute left-4 pointer-events-none"><path d="M10 3H4a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1zM9 9H5V5h4v4zm11-6h-6a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1zm-1 6h-4V5h4v4zm-9 4H4a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-6a1 1 0 0 0-1-1zm-1 6H5v-4h4v4zm11-6h-6a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-6a1 1 0 0 0-1-1zm-1 6h-4v-4h4v4z"/></svg> 
                      <select aria-label="Filter by type" className="pl-9 pr-8 py-2 text-[11px] font-bold text-slate-600 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 shadow-sm appearance-none outline-none cursor-pointer">
                         <option>All Types</option>
                         <option>Images</option>
                         <option>Videos</option>
                      </select>
                      <ChevronDown className="w-3 h-3 text-slate-400 absolute right-3 pointer-events-none" />
                   </div>
                   
                   <div className="relative flex items-center">
                      <svg viewBox="0 0 24 24" className="w-3.5 h-3.5 fill-slate-400 absolute left-4 pointer-events-none"><path d="M10 3H4a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1zM9 9H5V5h4v4zm11-6h-6a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1zm-1 6h-4V5h4v4zm-9 4H4a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-6a1 1 0 0 0-1-1zm-1 6H5v-4h4v4zm11-6h-6a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-6a1 1 0 0 0-1-1zm-1 6h-4v-4h4v4z"/></svg>
                      <select aria-label="Filter by platform" className="pl-9 pr-8 py-2 text-[11px] font-bold text-slate-600 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 shadow-sm appearance-none outline-none cursor-pointer">
                         <option>All Platforms</option>
                         <option>WhatsApp</option>
                         <option>Instagram</option>
                         <option>Twitter</option>
                      </select>
                      <ChevronDown className="w-3 h-3 text-slate-400 absolute right-3 pointer-events-none" />
                   </div>
                </div>
                   <div className="relative">
                      <button 
                        onClick={(e) => { e.stopPropagation(); setActiveDropdown(activeDropdown === 'filters' ? null : 'filters'); }}
                        className="flex items-center gap-2 text-[11px] font-bold text-slate-600 bg-white border border-slate-200 rounded-xl px-4 py-2 hover:bg-slate-50 shadow-sm active:scale-95 transition-transform">
                         <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-3.5 h-3.5 text-slate-400"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
                         Filters
                      </button>
                      {activeDropdown === 'filters' && (
                        <div className="absolute top-full right-0 mt-1 w-48 bg-white border border-slate-200 rounded-xl shadow-lg z-50 p-2" onClick={(e) => e.stopPropagation()}>
                           <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2 px-2 pt-1">Sort By</div>
                           <label className="flex items-center gap-2 px-2 py-1.5 hover:bg-slate-50 rounded-lg cursor-pointer">
                              <input type="radio" name="sort" className="accent-emerald-500" defaultChecked />
                              <span className="text-[11px] font-medium text-slate-700">Newest First</span>
                           </label>
                           <label className="flex items-center gap-2 px-2 py-1.5 hover:bg-slate-50 rounded-lg cursor-pointer">
                              <input type="radio" name="sort" className="accent-emerald-500" />
                              <span className="text-[11px] font-medium text-slate-700">Oldest First</span>
                           </label>
                           
                           <div className="w-full h-px bg-slate-100 my-2"></div>
                           
                           <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2 px-2 pt-1">Filter</div>
                           <label className="flex items-center gap-2 px-2 py-1.5 hover:bg-slate-50 rounded-lg cursor-pointer">
                              <input type="checkbox" className="accent-emerald-500 rounded-sm" />
                              <span className="text-[11px] font-medium text-slate-700">Verified Only</span>
                           </label>
                           <label className="flex items-center gap-2 px-2 py-1.5 hover:bg-slate-50 rounded-lg cursor-pointer">
                              <input type="checkbox" className="accent-emerald-500 rounded-sm" />
                              <span className="text-[11px] font-medium text-slate-700">High Confidence</span>
                           </label>
                        </div>
                      )}
                   </div>
             </div>

             {/* Saved List */}
             <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden p-2">
                 <div className="flex flex-col gap-1">
                    <div className="flex flex-col items-center justify-center py-16 text-center opacity-70">
                       <img src="/floating_feather_empty.png" alt="Empty Saved Items" className="w-48 h-48 object-contain mb-6 rounded-3xl shadow-sm mix-blend-multiply" />
                       <h4 className="text-lg font-bold text-slate-700 mb-2">No saved items yet</h4>
                       <p className="text-sm text-slate-500 max-w-sm leading-relaxed">When you find important analyses or reports, you can bookmark them to review later. Let your saved items gently accumulate here.</p>
                    </div>
                 </div>
             </div>
          </div>

          {/* Right Column Cards */}
          <div className="space-y-6">
             {/* Saved Overview */}
             <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6">
                <h3 className="text-[13px] font-bold text-slate-800 mb-6">Saved Overview</h3>
                
                <div className="space-y-4">
                   <div className="flex items-center gap-4 pb-4 border-b border-slate-50">
                      <div className="w-10 h-10 rounded-full bg-emerald-50 flex items-center justify-center shrink-0">
                         <div className="w-5 h-5 bg-emerald-600 rounded-sm flex items-center justify-center clip-shield">
                            <Bookmark className="w-3 h-3 text-white fill-current" />
                         </div>
                      </div>
                      <div>
                         <h4 className="text-[16px] font-bold text-slate-800 leading-none mb-1">0</h4>
                         <p className="text-[10px] font-medium text-slate-500">Total Saved</p>
                      </div>
                   </div>

                   <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-full bg-red-50/50 border border-red-100 flex items-center justify-center shrink-0">
                         <svg viewBox="0 0 24 24" className="w-5 h-5 text-red-500 fill-current"><path d="M21.582 6.186a2.684 2.684 0 0 0-1.884-1.884C18.035 3.84 12 3.84 12 3.84s-6.035 0-7.698.462a2.684 2.684 0 0 0-1.884 1.884C1.956 7.85 1.956 12 1.956 12s0 4.15.462 5.814a2.684 2.684 0 0 0 1.884 1.884C6.035 20.16 12 20.16 12 20.16s6.035 0 7.698-.462a2.684 2.684 0 0 0 1.884-1.884C22.044 16.15 22.044 12 22.044 12s0-4.15-.462-5.814zM9.956 15.27V8.73l6.505 3.27-6.505 3.27z"/></svg>
                      </div>
                      <div>
                         <h4 className="text-[14px] font-bold text-slate-800 leading-none mb-1">0</h4>
                         <p className="text-[10px] font-medium text-slate-500">Videos</p>
                      </div>
                   </div>

                   <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-full bg-amber-50/50 border border-amber-100 flex items-center justify-center shrink-0">
                         <FileText className="w-5 h-5 text-amber-500" />
                      </div>
                      <div>
                         <h4 className="text-[14px] font-bold text-slate-800 leading-none mb-1">0</h4>
                         <p className="text-[10px] font-medium text-slate-500">Texts</p>
                      </div>
                   </div>

                   <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-full bg-emerald-50/50 border border-emerald-100 flex items-center justify-center shrink-0">
                         <Mic className="w-5 h-5 text-emerald-500" />
                      </div>
                      <div>
                         <h4 className="text-[14px] font-bold text-slate-800 leading-none mb-1">0</h4>
                         <p className="text-[10px] font-medium text-slate-500">Audios</p>
                      </div>
                   </div>

                   <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-full bg-blue-50/50 border border-blue-100 flex items-center justify-center shrink-0">
                         <LinkIcon className="w-5 h-5 text-blue-500" />
                      </div>
                      <div>
                         <h4 className="text-[14px] font-bold text-slate-800 leading-none mb-1">0</h4>
                         <p className="text-[10px] font-medium text-slate-500">Links</p>
                      </div>
                   </div>
                </div>
             </div>

             {/* Save today, stay informed tomorrow */}
             <div className="bg-[#f0fdf4] rounded-2xl border border-[#dcfce7] p-6 text-left">
                <div className="w-full h-[140px] mb-4 relative flex items-center justify-center">
                   <img src="/smart_saved_track.png" alt="Smart saved" className="w-full h-full object-contain mix-blend-multiply" />
                </div>
                <h3 className="text-[13px] font-bold text-emerald-800 mb-2 leading-tight">Save today, stay informed<br/>tomorrow.</h3>
                <p className="text-[10px] font-medium text-slate-500 mb-6 leading-relaxed">
                   Bookmark important content to review and share responsibly.
                </p>
             </div>
          </div>
       </div>

    </div>
  )
}
