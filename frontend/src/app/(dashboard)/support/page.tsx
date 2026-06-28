"use client"
import { Search, FileText, ShieldCheck, HelpCircle, PlaySquare, Mail, MessageSquare, Ticket, ExternalLink, ChevronDown, ArrowRight, ChevronRight } from "lucide-react"
import Link from "next/link"

import { useState } from "react"

export default function SupportPage() {
  const [showAllFaqs, setShowAllFaqs] = useState(false)
  return (
    <div className="max-w-[1400px] mx-auto space-y-6 pb-10">
       {/* Hero Section */}
       <div className="flex flex-col md:flex-row items-center justify-between mb-10 bg-white rounded-2xl border border-slate-100 shadow-sm p-8">
          <div className="max-w-xl pr-6">
             <h1 className="text-3xl font-bold text-slate-800 font-serif mb-2">Help & Support</h1>
             <p className="text-slate-500 font-medium text-sm max-w-md leading-relaxed">
               We're here to help you. Find answers, guides and support to make your experience better.
             </p>
          </div>
          <div className="hidden md:block w-[320px] shrink-0">
             <img src="/support_hero.png" alt="Support hero" className="w-full h-auto object-contain mix-blend-multiply" />
          </div>
       </div>

       <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content Area (Left Column) */}
          <div className="lg:col-span-2 space-y-6">
             
             {/* Search Section */}
             <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6">
                <h3 className="text-[14px] font-bold text-slate-800 mb-4">How can we help you today?</h3>
                <div className="relative">
                   <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                   <input 
                      type="text" 
                      placeholder="Search for help topics, guides or questions..." 
                      className="w-full bg-slate-50 border border-slate-200 text-slate-800 text-[13px] rounded-xl pl-11 pr-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-all placeholder:text-slate-400"
                   />
                </div>
             </div>

             {/* Quick Help Grid */}
             <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6">
                <h3 className="text-[14px] font-bold text-slate-800 mb-5">Quick Help</h3>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                   {/* Card 1 */}
                   <Link href="/dashboard" className="border border-slate-100 rounded-xl p-5 hover:border-emerald-100 hover:bg-emerald-50/30 transition-colors group cursor-pointer flex flex-col h-full">
                      <div className="w-10 h-10 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center mb-4">
                         <FileText className="w-5 h-5" />
                      </div>
                      <h4 className="text-[13px] font-bold text-slate-800 mb-1.5">Getting Started</h4>
                      <p className="text-[10px] text-slate-500 font-medium leading-relaxed mb-4 flex-grow">
                         Learn the basics and set up your account.
                      </p>
                      <span className="text-[11px] font-bold text-emerald-600 flex items-center gap-1 group-hover:text-emerald-700">
                         View Guide <ArrowRight className="w-3.5 h-3.5" />
                      </span>
                   </Link>

                   {/* Card 2 */}
                   <Link href="/analyze-reel" className="border border-slate-100 rounded-xl p-5 hover:border-emerald-100 hover:bg-emerald-50/30 transition-colors group cursor-pointer flex flex-col h-full">
                      <div className="w-10 h-10 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center mb-4">
                         <ShieldCheck className="w-5 h-5" />
                      </div>
                      <h4 className="text-[13px] font-bold text-slate-800 mb-1.5">How it Works</h4>
                      <p className="text-[10px] text-slate-500 font-medium leading-relaxed mb-4 flex-grow">
                         Understand how Sukoon AI analyzes content.
                      </p>
                      <span className="text-[11px] font-bold text-emerald-600 flex items-center gap-1 group-hover:text-emerald-700">
                         View Guide <ArrowRight className="w-3.5 h-3.5" />
                      </span>
                   </Link>

                   {/* Card 3 */}
                   <Link href="#faqs" className="border border-slate-100 rounded-xl p-5 hover:border-emerald-100 hover:bg-emerald-50/30 transition-colors group cursor-pointer flex flex-col h-full">
                      <div className="w-10 h-10 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center mb-4">
                         <HelpCircle className="w-5 h-5" />
                      </div>
                      <h4 className="text-[13px] font-bold text-slate-800 mb-1.5">FAQs</h4>
                      <p className="text-[10px] text-slate-500 font-medium leading-relaxed mb-4 flex-grow">
                         Find answers to commonly asked questions.
                      </p>
                      <span className="text-[11px] font-bold text-emerald-600 flex items-center gap-1 group-hover:text-emerald-700">
                         View FAQs <ArrowRight className="w-3.5 h-3.5" />
                      </span>
                   </Link>

                   {/* Card 4 */}
                   <Link href="#" className="border border-slate-100 rounded-xl p-5 hover:border-emerald-100 hover:bg-emerald-50/30 transition-colors group cursor-pointer flex flex-col h-full">
                      <div className="w-10 h-10 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center mb-4">
                         <PlaySquare className="w-5 h-5" />
                      </div>
                      <h4 className="text-[13px] font-bold text-slate-800 mb-1.5">Video Tutorials</h4>
                      <p className="text-[10px] text-slate-500 font-medium leading-relaxed mb-4 flex-grow">
                         Watch step-by-step video guides.
                      </p>
                      <span className="text-[11px] font-bold text-emerald-600 flex items-center gap-1 group-hover:text-emerald-700">
                         Watch Now <ArrowRight className="w-3.5 h-3.5" />
                      </span>
                   </Link>
                </div>
             </div>

             {/* Popular Questions */}
             <div id="faqs" className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6">
                <h3 className="text-[14px] font-bold text-slate-800 mb-5">Popular Questions</h3>
                
                <div className="space-y-0 border border-slate-100 rounded-xl overflow-hidden">
                   <details className="group border-b border-slate-100">
                      <summary className="flex items-center justify-between p-4 px-5 hover:bg-slate-50 cursor-pointer list-none [&::-webkit-details-marker]:hidden">
                         <span className="text-[12px] font-bold text-slate-700">What is Sukoon AI and how does it work?</span>
                         <ChevronDown className="w-4 h-4 text-slate-400 transition-transform group-open:rotate-180" />
                      </summary>
                      <div className="px-5 pb-4 text-[11px] text-slate-500 leading-relaxed bg-slate-50/50">
                         Sukoon AI is a verification platform that uses advanced AI to analyze text, images, and videos. It cross-references claims against trusted sources to determine if the content is true, false, misleading, or hate speech.
                      </div>
                   </details>
                   <details className="group border-b border-slate-100">
                      <summary className="flex items-center justify-between p-4 px-5 hover:bg-slate-50 cursor-pointer list-none [&::-webkit-details-marker]:hidden">
                         <span className="text-[12px] font-bold text-slate-700">What types of content can I analyze?</span>
                         <ChevronDown className="w-4 h-4 text-slate-400 transition-transform group-open:rotate-180" />
                      </summary>
                      <div className="px-5 pb-4 text-[11px] text-slate-500 leading-relaxed bg-slate-50/50">
                         You can analyze text messages, links to social media posts, images, and audio/video forwards (like those from WhatsApp). Our AI extracts claims from all these formats and verifies them.
                      </div>
                   </details>
                   <details className="group border-b border-slate-100">
                      <summary className="flex items-center justify-between p-4 px-5 hover:bg-slate-50 cursor-pointer list-none [&::-webkit-details-marker]:hidden">
                         <span className="text-[12px] font-bold text-slate-700">How accurate is the analysis?</span>
                         <ChevronDown className="w-4 h-4 text-slate-400 transition-transform group-open:rotate-180" />
                      </summary>
                      <div className="px-5 pb-4 text-[11px] text-slate-500 leading-relaxed bg-slate-50/50">
                         Our analysis is highly accurate as it relies on real-time cross-referencing with verified news databases and semantic vector search. However, as an AI tool, it should be used as a guide alongside critical thinking.
                      </div>
                   </details>
                   <details className="group border-b border-slate-100">
                      <summary className="flex items-center justify-between p-4 px-5 hover:bg-slate-50 cursor-pointer list-none [&::-webkit-details-marker]:hidden">
                         <span className="text-[12px] font-bold text-slate-700">How do I report a false result?</span>
                         <ChevronDown className="w-4 h-4 text-slate-400 transition-transform group-open:rotate-180" />
                      </summary>
                      <div className="px-5 pb-4 text-[11px] text-slate-500 leading-relaxed bg-slate-50/50">
                         If you believe an analysis result is incorrect, you can click the "Flag as incorrect" button at the bottom of the result card. This helps our team review the claim and improve the AI model.
                      </div>
                   </details>
                   <details className="group border-b border-slate-100">
                      <summary className="flex items-center justify-between p-4 px-5 hover:bg-slate-50 cursor-pointer list-none [&::-webkit-details-marker]:hidden">
                         <span className="text-[12px] font-bold text-slate-700">Is my data secure and private?</span>
                         <ChevronDown className="w-4 h-4 text-slate-400 transition-transform group-open:rotate-180" />
                      </summary>
                      <div className="px-5 pb-4 text-[11px] text-slate-500 leading-relaxed bg-slate-50/50">
                         Yes. We do not store personal identifiable information alongside your queries. Any media uploaded is strictly used for analysis and is periodically purged from our servers to ensure privacy.
                      </div>
                   </details>
                </div>

                {showAllFaqs && (
                   <div className="space-y-0 border border-slate-100 rounded-xl overflow-hidden mt-0 border-t-0 rounded-t-none">
                         <details className="group border-b border-slate-100">
                            <summary className="flex items-center justify-between p-4 px-5 hover:bg-slate-50 cursor-pointer list-none [&::-webkit-details-marker]:hidden">
                               <span className="text-[12px] font-bold text-slate-700">What languages are supported?</span>
                               <ChevronDown className="w-4 h-4 text-slate-400 transition-transform group-open:rotate-180" />
                            </summary>
                            <div className="px-5 pb-4 text-[11px] text-slate-500 leading-relaxed bg-slate-50/50">
                               Currently, Sukoon AI primarily supports English, Hindi, and several regional Indian languages for text and audio analysis. We are continuously adding support for more languages.
                            </div>
                         </details>
                         <details className="group border-b border-slate-100">
                            <summary className="flex items-center justify-between p-4 px-5 hover:bg-slate-50 cursor-pointer list-none [&::-webkit-details-marker]:hidden">
                               <span className="text-[12px] font-bold text-slate-700">Is there a mobile app?</span>
                               <ChevronDown className="w-4 h-4 text-slate-400 transition-transform group-open:rotate-180" />
                            </summary>
                            <div className="px-5 pb-4 text-[11px] text-slate-500 leading-relaxed bg-slate-50/50">
                               At this moment, Sukoon AI is accessible via our responsive web platform. A dedicated mobile application is currently in development and will be released soon.
                            </div>
                         </details>
                         <details className="group border-b border-slate-100">
                            <summary className="flex items-center justify-between p-4 px-5 hover:bg-slate-50 cursor-pointer list-none [&::-webkit-details-marker]:hidden">
                               <span className="text-[12px] font-bold text-slate-700">Can I use Sukoon AI for commercial purposes?</span>
                               <ChevronDown className="w-4 h-4 text-slate-400 transition-transform group-open:rotate-180" />
                            </summary>
                            <div className="px-5 pb-4 text-[11px] text-slate-500 leading-relaxed bg-slate-50/50">
                               Yes! We offer enterprise APIs and commercial plans for businesses that need to verify high volumes of content. Please contact our sales team for more information.
                            </div>
                         </details>
                   </div>
                )}

                {!showAllFaqs && (
                   <div className="mt-4 flex justify-center">
                      <span onClick={() => setShowAllFaqs(true)} className="text-[11px] font-bold text-emerald-600 flex items-center gap-1 hover:text-emerald-700 cursor-pointer">
                         View All FAQs <ArrowRight className="w-3.5 h-3.5" />
                      </span>
                   </div>
                )}
             </div>
          </div>

          {/* Right Column Cards */}
          <div className="space-y-6">
             
             {/* Contact Support */}
             <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6">
                <h3 className="text-[13px] font-bold text-slate-800 mb-1">Contact Support</h3>
                <p className="text-[11px] text-slate-500 font-medium mb-5">
                   Can't find what you're looking for? <br/>Our support team is ready to help you.
                </p>
                
                <div className="space-y-2 mb-4">
                   {/* Email */}
                   <a href="https://mail.google.com/mail/?view=cm&fs=1&to=justimaginary21@gmail.com" target="_blank" rel="noopener noreferrer" className="flex items-center gap-4 p-3 rounded-xl bg-emerald-50/50 hover:bg-emerald-50 border border-transparent hover:border-emerald-100 transition-colors cursor-pointer group">
                      <div className="w-8 h-8 rounded-full bg-white border border-emerald-100 text-emerald-600 flex items-center justify-center shrink-0">
                         <Mail className="w-4 h-4" />
                      </div>
                      <div className="flex-1">
                         <h4 className="text-[12px] font-bold text-slate-800 leading-none mb-1">Email Support</h4>
                         <p className="text-[10px] font-medium text-slate-500">justimaginary21@gmail.com</p>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-emerald-600 transition-colors" />
                   </a>

                   {/* Live Chat */}
                   <a href="https://wa.me/917305090806" target="_blank" rel="noopener noreferrer" className="flex items-center gap-4 p-3 rounded-xl bg-emerald-50/50 hover:bg-emerald-50 border border-transparent hover:border-emerald-100 transition-colors cursor-pointer group">
                      <div className="w-8 h-8 rounded-full bg-white border border-emerald-100 text-emerald-600 flex items-center justify-center shrink-0">
                         <MessageSquare className="w-4 h-4" />
                      </div>
                      <div className="flex-1">
                         <h4 className="text-[12px] font-bold text-slate-800 leading-none mb-1">Live Chat</h4>
                         <p className="text-[10px] font-medium text-slate-500">Chat with our team</p>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-emerald-600 transition-colors" />
                   </a>
                </div>

                <div className="flex items-center gap-2 text-[10px] text-slate-500 font-medium justify-center">
                   <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" /> We usually respond within 24 hours.
                </div>
             </div>

             {/* System Status */}
             <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5 flex flex-col justify-center">
                <div className="flex items-center justify-between mb-2">
                   <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                      <span className="text-[12px] font-bold text-slate-800">System Status</span>
                   </div>
                   <span className="bg-[#f0fdf4] text-emerald-700 border border-[#dcfce7] text-[10px] font-bold px-2 py-0.5 rounded-md">All Systems Operational</span>
                </div>
                <p className="text-[9px] font-medium text-slate-400 ml-4">Last updated: Just now</p>
             </div>
          </div>
       </div>

    </div>
  )
}
