"use client"
import { useState } from "react"
import { ShieldAlert, AlertCircle, Users, HelpCircle, BarChart3, Settings, ChevronRight, ChevronDown } from "lucide-react"
import Link from "next/link"

export default function AlertsPage() {
  const [activeTab, setActiveTab] = useState("all")
  return (
    <div className="max-w-[1400px] mx-auto space-y-6 pb-10">
       {/* Hero Section */}
       <div className="flex flex-col md:flex-row items-center justify-between mb-10 bg-white rounded-2xl border border-slate-100 shadow-sm p-8">
          <div className="max-w-xl pr-6">
             <h1 className="text-3xl font-bold text-slate-800 font-serif mb-2">Alerts</h1>
             <p className="text-slate-500 font-medium text-sm">Stay informed about critical or trending harmful content.</p>
          </div>
          <div className="hidden md:block w-[240px] shrink-0">
             <img src="/alerts_hero.png" alt="Alerts hero" className="w-full h-auto object-contain mix-blend-multiply" />
          </div>
       </div>

       <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content Area (Left Column) */}
          <div className="lg:col-span-2 space-y-6">
             
             {/* Tabs Bar */}
             <div className="flex items-center gap-6 border-b border-slate-200">
                <button 
                  onClick={() => setActiveTab("all")}
                  className={`text-[13px] font-bold pb-3 flex items-center gap-2 ${activeTab === 'all' ? 'text-emerald-700 border-b-2 border-emerald-500' : 'text-slate-500 hover:text-slate-700'}`}>
                   All Alerts <span className={`${activeTab === 'all' ? 'bg-emerald-100/80 text-emerald-700' : 'bg-slate-100 text-slate-500'} text-[10px] px-1.5 py-0.5 rounded-md`}>0</span>
                </button>
                <button 
                  onClick={() => setActiveTab("false_info")}
                  className={`text-[13px] font-bold pb-3 flex items-center gap-2 ${activeTab === 'false_info' ? 'text-emerald-700 border-b-2 border-emerald-500' : 'text-slate-500 hover:text-slate-700'}`}>
                   False Information <span className={`${activeTab === 'false_info' ? 'bg-emerald-100/80 text-emerald-700' : 'bg-slate-100 text-slate-500'} text-[10px] px-1.5 py-0.5 rounded-md`}>0</span>
                </button>
                <button 
                  onClick={() => setActiveTab("hate_speech")}
                  className={`text-[13px] font-bold pb-3 flex items-center gap-2 ${activeTab === 'hate_speech' ? 'text-emerald-700 border-b-2 border-emerald-500' : 'text-slate-500 hover:text-slate-700'}`}>
                   Hate Speech <span className={`${activeTab === 'hate_speech' ? 'bg-emerald-100/80 text-emerald-700' : 'bg-slate-100 text-slate-500'} text-[10px] px-1.5 py-0.5 rounded-md`}>0</span>
                </button>
                <button 
                  onClick={() => setActiveTab("misleading")}
                  className={`text-[13px] font-bold pb-3 flex items-center gap-2 ${activeTab === 'misleading' ? 'text-emerald-700 border-b-2 border-emerald-500' : 'text-slate-500 hover:text-slate-700'}`}>
                   Misleading <span className={`${activeTab === 'misleading' ? 'bg-emerald-100/80 text-emerald-700' : 'bg-slate-100 text-slate-500'} text-[10px] px-1.5 py-0.5 rounded-md`}>0</span>
                </button>
                <button 
                  onClick={() => setActiveTab("other")}
                  className={`text-[13px] font-bold pb-3 flex items-center gap-2 ${activeTab === 'other' ? 'text-emerald-700 border-b-2 border-emerald-500' : 'text-slate-500 hover:text-slate-700'}`}>
                   Other <span className={`${activeTab === 'other' ? 'bg-emerald-100/80 text-emerald-700' : 'bg-slate-100 text-slate-500'} text-[10px] px-1.5 py-0.5 rounded-md`}>0</span>
                </button>
             </div>

             {/* Alerts List */}
             <div className="space-y-4">
                 <div className="flex flex-col items-center justify-center py-24 text-center opacity-50">
                    <ShieldAlert className="w-16 h-16 text-slate-300 mb-4" />
                    <h4 className="text-lg font-bold text-slate-700 mb-2">No active alerts</h4>
                    <p className="text-sm text-slate-500 max-w-sm">We are monitoring your environment. Important alerts will be listed here.</p>
                 </div>
             </div>
          </div>

          {/* Right Column Cards */}
          <div className="space-y-6">
             {/* Alert Overview */}
             <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6">
                <h3 className="text-[13px] font-bold text-slate-800 mb-6">Alert Overview</h3>
                
                <div className="space-y-4 mb-6">
                   <div className="flex items-center gap-4 border-b border-slate-50 pb-4">
                      <div className="w-10 h-10 rounded-full bg-red-50/50 border border-red-100 flex items-center justify-center shrink-0">
                         <ShieldAlert className="w-5 h-5 text-red-500" />
                      </div>
                      <div>
                         <h4 className="text-[14px] font-bold text-slate-800 leading-none mb-1">0</h4>
                         <p className="text-[10px] font-medium text-slate-500">False Information</p>
                      </div>
                   </div>

                   <div className="flex items-center gap-4 border-b border-slate-50 pb-4">
                      <div className="w-10 h-10 rounded-full bg-amber-50/50 border border-amber-100 flex items-center justify-center shrink-0">
                         <AlertCircle className="w-5 h-5 text-amber-500" />
                      </div>
                      <div>
                         <h4 className="text-[14px] font-bold text-slate-800 leading-none mb-1">0</h4>
                         <p className="text-[10px] font-medium text-slate-500">Misleading</p>
                      </div>
                   </div>

                   <div className="flex items-center gap-4 border-b border-slate-50 pb-4">
                      <div className="w-10 h-10 rounded-full bg-red-50/50 border border-red-100 flex items-center justify-center shrink-0">
                         <Users className="w-5 h-5 text-red-500" />
                      </div>
                      <div>
                         <h4 className="text-[14px] font-bold text-slate-800 leading-none mb-1">0</h4>
                         <p className="text-[10px] font-medium text-slate-500">Hate Speech</p>
                      </div>
                   </div>

                   <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-full bg-blue-50/50 border border-blue-100 flex items-center justify-center shrink-0">
                         <HelpCircle className="w-5 h-5 text-blue-500" />
                      </div>
                      <div>
                         <h4 className="text-[14px] font-bold text-slate-800 leading-none mb-1">0</h4>
                         <p className="text-[10px] font-medium text-slate-500">Unverified</p>
                      </div>
                   </div>
                </div>

                <Link href="/history" className="w-full bg-[#f0fdf4] hover:bg-[#dcfce7] text-emerald-700 text-[11px] font-bold py-2.5 rounded-lg flex items-center justify-center gap-2 transition-colors">
                   View All Reports <BarChart3 className="w-3.5 h-3.5" />
                </Link>
             </div>

             {/* Smart Alert */}
             <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 text-center">
                <h3 className="text-[13px] font-bold text-slate-800 text-left mb-4">Smart Alert</h3>
                <div className="w-full h-[120px] mb-4 relative flex items-center justify-center">
                   <img src="/smart_alert_track.png" alt="Smart alert" className="w-[120%] h-[120%] object-contain mix-blend-multiply" />
                </div>
                <p className="text-[10px] font-medium text-slate-500 mb-6 leading-relaxed text-left">
                   We analyze content 24/7 to keep you and your community safe.
                </p>
                <Link href="/settings" className="bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-[11px] font-bold py-2 px-5 rounded-lg flex items-center justify-center gap-2 transition-colors mr-auto shadow-sm w-fit">
                   Manage Preferences <Settings className="w-3.5 h-3.5" />
                </Link>
             </div>
          </div>
       </div>

    </div>
  )
}
