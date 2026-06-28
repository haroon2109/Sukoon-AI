"use client";
import Link from "next/link";
import { motion, useInView } from "framer-motion";
import { useRef, useEffect, useState } from "react";
import { ShieldCheck, Play, ArrowRight, Upload, Brain, Shield, CheckCircle2, LayoutDashboard, Search, History, Bell, Settings, Send, Users, Globe, Quote } from "lucide-react";
import { ThemeToggle } from "@/components/ThemeToggle";
import { AnimatedCounter } from "@/components/AnimatedCounter";

// Helper components for Icons used in the illustration
const WhatsAppIcon = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" className={className || "w-8 h-8 text-white"} fill="currentColor">
    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.888-.788-1.487-1.761-1.66-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/>
  </svg>
);

const InstagramIconCustom = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" className={className || "w-8 h-8"} fill="url(#instagram-gradient)">
    <defs>
      <linearGradient id="instagram-gradient" x1="0%" y1="100%" x2="100%" y2="0%">
        <stop offset="0%" stopColor="#f09433" />
        <stop offset="25%" stopColor="#e6683c" />
        <stop offset="50%" stopColor="#dc2743" />
        <stop offset="75%" stopColor="#cc2366" />
        <stop offset="100%" stopColor="#bc1888" />
      </linearGradient>
    </defs>
    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/>
  </svg>
);

const XIconCustom = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" className={className || "w-8 h-8 text-white"} fill="currentColor">
    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
  </svg>
);

const LotusIcon = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" fill="currentColor" className={className} xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C12 2 10 6 10 10C10 14 12 18 12 18C12 18 14 14 14 10C14 6 12 2 12 2Z" opacity="0.6"/>
    <path d="M12 22C12 22 16 19 19 15C22 11 22 7 22 7C22 7 18 8 14 11C11.5 12.8 12 22 12 22Z" opacity="0.8"/>
    <path d="M12 22C12 22 8 19 5 15C2 11 2 7 2 7C2 7 6 8 10 11C12.5 12.8 12 22 12 22Z" />
  </svg>
);

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-teal-100 selection:text-teal-900 overflow-x-hidden">
      
      {/* Navigation */}
      <nav className="fixed w-full z-50 bg-white/80 backdrop-blur-xl border-b border-slate-200/50">
        <div className="max-w-[1400px] mx-auto px-6 h-20 flex items-center justify-between">
          {/* Logo Section */}
          <div className="flex items-center gap-2 md:gap-3 shrink-0">
            <div className="text-emerald-600">
               <LotusIcon className="w-7 h-7 md:w-8 md:h-8 text-emerald-600" />
            </div>
            <div className="flex flex-col justify-center">
              <span className="text-lg md:text-xl font-semibold tracking-tight text-slate-800 leading-none whitespace-nowrap">Sukoon <span className="font-bold text-emerald-600">AI</span></span>
              <span className="text-[10px] text-slate-500 font-medium tracking-wide mt-1 whitespace-nowrap">Verified Peace. Digital Harmony.</span>
            </div>
          </div>
          
          {/* Main Navigation Links */}
          <div className="hidden md:flex items-center justify-center gap-4 lg:gap-8 text-sm lg:text-[15px] font-medium text-slate-600 flex-1 px-4">
            <Link href="/" className="text-slate-900 font-semibold whitespace-nowrap">Home</Link>
            <Link href="#how-it-works" className="hover:text-emerald-600 transition-colors whitespace-nowrap">How It Works</Link>
            <Link href="#platforms" className="hover:text-emerald-600 transition-colors whitespace-nowrap">Our Shield Covers</Link>
            <Link href="/cards" className="hover:text-emerald-600 transition-colors whitespace-nowrap">Truth Cards</Link>
            <Link href="#truth-over-rumors" className="hover:text-emerald-600 transition-colors whitespace-nowrap hidden lg:block">Truth Over Rumors</Link>

          </div>
          
          {/* Action Buttons */}
          <div className="flex items-center gap-3 lg:gap-4 shrink-0">
            <ThemeToggle />
            <Link href="/login" className="text-sm lg:text-[15px] font-medium text-slate-700 hover:text-slate-900 px-2 transition-colors whitespace-nowrap">
              Sign In
            </Link>
            <Link href="/onboarding" className="px-4 lg:px-5 py-2 lg:py-2.5 rounded-xl bg-[#2E8C6A] hover:bg-[#257356] text-white text-sm lg:text-[15px] font-medium transition-all shadow-md shadow-emerald-600/20 whitespace-nowrap">
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-16 px-6 relative overflow-hidden bg-slate-50">
        {/* Dynamic Mesh Gradient Background */}
        <div className="absolute inset-0 z-0 overflow-hidden opacity-60">
          <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] rounded-full bg-emerald-200/50 mix-blend-multiply filter blur-[100px] animate-pulse"></div>
          <div className="absolute top-[20%] right-[-10%] w-[40%] h-[60%] rounded-full bg-teal-200/50 mix-blend-multiply filter blur-[100px] animate-pulse" style={{ animationDelay: '2s' }}></div>
          <div className="absolute bottom-[-10%] left-[20%] w-[50%] h-[50%] rounded-full bg-emerald-100/60 mix-blend-multiply filter blur-[100px] animate-pulse" style={{ animationDelay: '4s' }}></div>
        </div>

        <div className="max-w-[1400px] mx-auto grid lg:grid-cols-[1fr_1.1fr] gap-12 items-center relative z-10 min-h-[85vh]">
          {/* Left Content */}
          <div className="space-y-8 md:space-y-10 pl-4 lg:pl-10">
            <div className="flex flex-col items-start gap-4">
              <span className="text-[10px] md:text-xs font-bold text-slate-500 uppercase tracking-[0.3em] font-serif">
                T R U S T &nbsp; I N F R A S T R U C T U R E
              </span>
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-50 border border-slate-200 text-slate-600 text-xs font-semibold tracking-wide shadow-sm">
                <ShieldCheck className="w-4 h-4 text-emerald-600" />
                AI-Powered Trust Shield
              </div>
            </div>
            
            <h1 className="text-5xl md:text-[64px] font-bold tracking-tight text-slate-900 leading-[1.1]">
              Turning Viral Panic<br />
              Into <span className="text-[#2E8C6A]">Verified Peace 🌿</span>
            </h1>
            
            <p className="text-lg md:text-xl text-slate-600 leading-relaxed font-medium max-w-[540px]">
              Sukoon AI helps you verify suspicious content, stop the spread
              of misinformation, and build a calmer, more informed digital world.
            </p>
            
            <div className="flex flex-wrap items-center gap-6 text-sm font-semibold text-slate-700">
               <span className="flex items-center gap-2"><CheckCircle2 className="w-5 h-5 text-emerald-500 bg-emerald-50 rounded-full" /> AI-Powered Verification</span>
               <span className="flex items-center gap-2"><CheckCircle2 className="w-5 h-5 text-emerald-500 bg-emerald-50 rounded-full" /> Multi-Platform Shield</span>
               <span className="flex items-center gap-2"><CheckCircle2 className="w-5 h-5 text-emerald-500 bg-emerald-50 rounded-full" /> Peace-First Approach</span>
            </div>

            <div className="flex flex-col sm:flex-row items-center gap-5 pt-4">
              <Link href="/analyze-reel" className="w-full sm:w-auto px-8 py-4 rounded-full bg-[#2E8C6A] hover:bg-[#257356] text-white font-semibold text-base transition-all flex items-center justify-center gap-2 shadow-lg shadow-emerald-600/30">
                Verify Something Now <ArrowRight className="w-5 h-5" />
              </Link>
              <Link href="#how-it-works" className="w-full sm:w-auto px-8 py-4 rounded-full bg-white text-slate-800 font-semibold hover:bg-slate-50 border border-slate-200 transition-all flex items-center justify-center gap-3 shadow-sm">
                See How It Works <div className="w-6 h-6 rounded-full border border-slate-300 flex items-center justify-center"><Play className="w-3 h-3 text-slate-600 ml-0.5" /></div>
              </Link>
            </div>
          </div>

          {/* Right Hero Illustration V2 */}
          <div className="relative h-full min-h-[600px] w-full flex items-center justify-center pt-10 scale-90 lg:scale-100">
             
             {/* Decorative Background Elements */}
             <div className="absolute top-[10%] right-[20%] text-emerald-200 opacity-50 rotate-45"><Send className="w-12 h-12 fill-emerald-100" /></div>
             <div className="absolute top-[5%] right-[40%] w-3 h-3 rounded-full bg-emerald-300"></div>
             <div className="absolute top-[40%] right-[5%] w-2 h-2 rounded-full bg-yellow-300"></div>
             <div className="absolute bottom-[20%] left-[10%] w-4 h-4 rounded-full bg-emerald-200"></div>

             {/* Web Dashboard Mockup */}
             <motion.div 
               animate={{ y: [0, -15, 0] }}
               transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
               className="absolute z-10 w-[520px] h-[360px] bg-white rounded-2xl shadow-2xl border border-slate-100 overflow-hidden flex transform -translate-x-12 -translate-y-8"
             >
                {/* Sidebar */}
                <div className="w-[140px] bg-white border-r border-slate-100 p-5 flex flex-col gap-4">
                   <div className="flex items-center gap-2 mb-6">
                     <LotusIcon className="w-5 h-5 text-emerald-600" />
                     <span className="text-[13px] font-bold text-slate-800 font-serif">Sukoon AI</span>
                   </div>
                   <div className="flex items-center gap-3 text-slate-400 pl-2"><LayoutDashboard className="w-3.5 h-3.5" /> <span className="text-[11px] font-medium">Dashboard</span></div>
                   <div className="flex items-center gap-3 text-emerald-700 bg-emerald-50 px-2 py-2 rounded-lg -ml-2"><Search className="w-3.5 h-3.5" /> <span className="text-[11px] font-bold">Analyze</span></div>
                   <div className="flex items-center gap-3 text-slate-400 pl-2"><History className="w-3.5 h-3.5" /> <span className="text-[11px] font-medium">History</span></div>
                   <div className="flex items-center gap-3 text-slate-400 pl-2"><Bell className="w-3.5 h-3.5" /> <span className="text-[11px] font-medium">Alerts</span></div>
                </div>
                {/* Main Content */}
                <div className="flex-1 p-8 flex flex-col relative bg-white">
                   <div className="flex items-center gap-4 mb-8 bg-emerald-50/80 p-4 rounded-xl border border-emerald-100/50">
                      <div className="w-8 h-8 rounded-full bg-emerald-100/80 border border-emerald-200 flex items-center justify-center text-emerald-600 shrink-0"><CheckCircle2 className="w-4 h-4" /></div>
                      <div>
                         <h5 className="text-sm font-bold text-slate-800 font-serif">Verification Complete</h5>
                         <p className="text-[11px] text-slate-500">We've verified the content and found the truth.</p>
                      </div>
                   </div>

                   <div className="space-y-6">
                      <div>
                         <span className="text-[9px] font-bold text-red-500 uppercase tracking-widest mb-1 block">CLAIM</span>
                         <p className="text-sm font-bold text-slate-800 font-serif leading-tight pr-10">This video shows violence in Bihar today.</p>
                      </div>
                      <div>
                         <span className="text-[9px] font-bold text-emerald-600 uppercase tracking-widest mb-1 block">TRUTH</span>
                         <p className="text-xs font-medium text-slate-600 leading-relaxed pr-10">This video is from a protest in Bangladesh in 2022.</p>
                      </div>
                   </div>

                   {/* Progress Bar */}
                   <div className="absolute bottom-8 left-8 right-8">
                      <span className="text-[10px] font-bold text-slate-500 mb-2 block font-serif">Confidence Score</span>
                      <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                         <div className="h-full bg-emerald-500 w-[92%] rounded-full"></div>
                      </div>
                   </div>
                </div>

                {/* Bottom Left Badge */}
                <div className="absolute bottom-0 left-0 z-30 w-24 h-24 bg-gradient-to-br from-[#2E8C6A] to-[#1E624A] rounded-tr-[2rem] flex items-center justify-center shadow-lg border-t-4 border-r-4 border-white">
                   <LotusIcon className="w-10 h-10 text-white/90" />
                </div>
             </motion.div>

             {/* Mobile Mockup */}
             <motion.div 
               animate={{ y: [0, 10, 0] }}
               transition={{ duration: 5, repeat: Infinity, ease: "easeInOut", delay: 1 }}
               className="absolute z-20 w-[220px] h-[450px] bg-white rounded-[2.5rem] shadow-2xl border-[6px] border-slate-100 overflow-hidden transform translate-x-32 translate-y-4 flex flex-col"
             >
                {/* Notch */}
                <div className="w-20 h-5 bg-slate-100 rounded-b-xl mx-auto absolute top-0 left-0 right-0 z-10"></div>
                
                {/* Header */}
                <div className="pt-10 pb-4 px-4 flex items-center justify-center gap-2 bg-white">
                   <LotusIcon className="w-5 h-5 text-emerald-600" />
                   <span className="text-xs font-bold text-slate-800 font-serif">Sukoon AI</span>
                </div>

                {/* Body */}
                <div className="flex-1 bg-slate-50/50 flex flex-col items-center justify-center p-5">
                   <div className="w-full bg-white rounded-[1.5rem] shadow-[0_10px_40px_-10px_rgba(0,0,0,0.1)] border border-slate-100 p-5 flex flex-col items-center text-center relative overflow-hidden">
                      <div className="absolute top-0 right-0 bg-red-500 text-white text-[9px] font-black tracking-widest px-3 py-1.5 rounded-bl-xl">FALSE</div>
                      
                      <div className="mt-6 mb-4">
                         <Shield className="w-10 h-10 text-red-500 stroke-[1.5]" />
                      </div>
                      <span className="text-[9px] font-bold text-slate-400 uppercase tracking-widest mb-2 font-serif">CONFIDENCE</span>
                      <span className="text-4xl font-black text-slate-800 mb-6 font-serif tracking-tight">92%</span>
                      
                      <button className="w-full py-2.5 bg-slate-100 text-slate-700 text-[10px] font-bold rounded-xl hover:bg-slate-200 transition-colors">
                         View Details
                      </button>
                   </div>
                </div>
             </motion.div>
          </div>
        </div>
      </section>

      {/* Trust Logos */}
      <section className="py-12 bg-white border-y border-slate-100 overflow-hidden">
        <div className="max-w-[1400px] mx-auto px-6 text-center">
          <p className="text-sm font-semibold text-slate-400 mb-8">Trusted by individuals and organizations across India</p>
          <div className="flex flex-wrap justify-center items-center gap-10 md:gap-20 opacity-50 grayscale hover:grayscale-0 transition-all duration-500">
             <span className="text-2xl font-black tracking-tighter text-slate-800">ALT NEWS</span>
             <span className="text-2xl font-bold font-serif text-slate-800">BOOM LIVE</span>
             <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-full border-2 border-slate-800 flex items-center justify-center"><span className="text-[10px] font-bold">PIB</span></div>
                <span className="text-lg font-bold leading-none text-slate-800">PIB Fact<br/>Check</span>
             </div>
             <span className="text-2xl font-serif font-medium text-slate-800 uppercase">The Hindu</span>
             <span className="text-2xl font-bold text-slate-800 uppercase tracking-wide">India Today</span>
             <span className="text-2xl font-black text-slate-800">DD NEWS</span>
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section id="how-it-works" className="py-24 px-6 bg-slate-50 overflow-hidden">
        <motion.div 
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.7 }}
          className="max-w-6xl mx-auto"
        >
          <div className="text-center mb-16">
            <h2 className="text-[10px] md:text-xs font-bold tracking-[0.3em] text-slate-400 uppercase mb-3 font-serif">HOW SUKOON WORKS</h2>
            <h3 className="text-4xl md:text-[44px] font-bold text-slate-900 font-serif">Verify in 3 Simple Steps</h3>
          </div>

          <div className="grid md:grid-cols-3 gap-8 relative z-10">
            {/* Step 1 */}
            <div className="bg-white rounded-3xl p-10 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] border border-slate-100 flex flex-col items-center text-center relative">
              <div className="absolute -top-4 right-8 text-6xl font-black text-slate-50 opacity-50 z-0">01</div>
              <div className="w-20 h-20 rounded-full bg-emerald-50 border-8 border-white shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] flex items-center justify-center text-emerald-500 mb-8 relative z-10">
                <Upload className="w-8 h-8" strokeWidth={1.5} />
              </div>
              <h4 className="text-xl font-bold text-slate-800 mb-4 relative z-10">Share the Content</h4>
              <p className="text-slate-500 leading-relaxed font-medium relative z-10">
                Forward a message, paste a link, or upload media from WhatsApp, Instagram, or X.
              </p>
            </div>

            {/* Step 2 */}
            <div className="bg-white rounded-3xl p-10 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] border border-slate-100 flex flex-col items-center text-center relative mt-0 md:mt-12">
              <div className="absolute -top-4 right-8 text-6xl font-black text-slate-50 opacity-50 z-0">02</div>
              <div className="w-20 h-20 rounded-full bg-blue-50 border-8 border-white shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] flex items-center justify-center text-blue-500 mb-8 relative z-10">
                <Brain className="w-8 h-8" strokeWidth={1.5} />
              </div>
              <h4 className="text-xl font-bold text-slate-800 mb-4 relative z-10">AI Analyzes & Verifies</h4>
              <p className="text-slate-500 leading-relaxed font-medium relative z-10">
                Our AI checks the facts, scans sources, detects manipulation, and analyzes the context.
              </p>
            </div>

            {/* Step 3 */}
            <div className="bg-white rounded-3xl p-10 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] border border-slate-100 flex flex-col items-center text-center relative mt-0 md:mt-24">
              <div className="absolute -top-4 right-8 text-6xl font-black text-slate-50 opacity-50 z-0">03</div>
              <div className="w-20 h-20 rounded-full bg-purple-50 border-8 border-white shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] flex items-center justify-center text-purple-500 mb-8 relative z-10">
                <ShieldCheck className="w-8 h-8" strokeWidth={1.5} />
              </div>
              <h4 className="text-xl font-bold text-slate-800 mb-4 relative z-10">Get Peaceful Clarity</h4>
              <p className="text-slate-500 leading-relaxed font-medium relative z-10">
                Receive a clear truth card with verified facts and a calm response meant to reduce panic.
              </p>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Where Misinformation Spreads */}
      <section id="platforms" className="py-24 px-6 bg-white overflow-hidden">
        <motion.div 
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.7 }}
          className="max-w-[1400px] mx-auto"
        >
          <div className="mb-16">
            <h2 className="text-[10px] md:text-xs font-bold tracking-[0.3em] text-slate-400 uppercase mb-3 font-serif">OUR SHIELD COVERS</h2>
            <h3 className="text-4xl md:text-[44px] font-bold text-slate-900 leading-tight max-w-xl font-serif">
              Where Misinformation Spreads, Sukoon Protects
            </h3>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {/* WhatsApp */}
            <div className="bg-white border border-slate-100 rounded-3xl p-10 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] hover:shadow-lg transition-shadow group flex flex-col h-full">
              <div className="w-16 h-16 rounded-full bg-emerald-50 border border-emerald-100 flex items-center justify-center mb-8">
                 <WhatsAppIcon className="w-8 h-8 text-emerald-600" />
              </div>
              <h4 className="text-2xl font-bold text-slate-800 mb-4">WhatsApp</h4>
              <p className="text-slate-500 font-medium leading-relaxed mb-10 flex-grow">
                Forward suspicious messages, audios, images or videos to our verified number and get instant truth checks.
              </p>
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-green-50 text-green-700 text-sm font-bold mt-auto self-start border border-green-100">
                <WhatsAppIcon className="w-4 h-4 text-green-600" /> WhatsApp Tipline
              </div>
            </div>

            {/* Instagram */}
            <div className="bg-white border border-slate-100 rounded-3xl p-10 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] hover:shadow-lg transition-shadow group flex flex-col h-full">
              <div className="w-16 h-16 rounded-3xl bg-rose-50 border border-rose-100 flex items-center justify-center mb-8">
                 <InstagramIconCustom className="w-8 h-8" />
              </div>
              <h4 className="text-2xl font-bold text-slate-800 mb-4">Instagram</h4>
              <p className="text-slate-500 font-medium leading-relaxed mb-10 flex-grow">
                Paste any Reel link and we'll analyze the content, audio, frames, and context for you.
              </p>
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-pink-50 text-pink-700 text-sm font-bold mt-auto self-start border border-pink-100">
                <InstagramIconCustom className="w-4 h-4 text-pink-600" /> Reel Analyzer
              </div>
            </div>

            {/* X */}
            <div className="bg-white border border-slate-100 rounded-3xl p-10 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] hover:shadow-lg transition-shadow group flex flex-col h-full">
              <div className="w-16 h-16 rounded-full bg-slate-50 border border-slate-200 flex items-center justify-center mb-8">
                 <XIconCustom className="w-7 h-7 text-slate-700" />
              </div>
              <h4 className="text-2xl font-bold text-slate-800 mb-4">X (Twitter)</h4>
              <p className="text-slate-500 font-medium leading-relaxed mb-10 flex-grow">
                Mention @SukoonAI_Bot in a tweet and our bot will reply with verified facts to de-escalate misinformation.
              </p>
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-100 text-slate-800 text-sm font-bold mt-auto self-start border border-slate-200">
                <XIconCustom className="w-4 h-4 text-slate-700" /> De-escalation Bot
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Truth Over Rumors */}
      <section id="truth-over-rumors" className="py-24 px-6 bg-slate-50 overflow-hidden">
        <motion.div 
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.7 }}
          className="max-w-[1400px] mx-auto grid lg:grid-cols-2 gap-20 items-center"
        >
          <div className="space-y-10 pl-4 lg:pl-10">
            <div>
              <h2 className="text-[10px] md:text-xs font-bold tracking-[0.3em] text-slate-400 uppercase mb-3 font-serif">TRUTH OVER RUMORS</h2>
              <h3 className="text-4xl md:text-5xl font-bold text-slate-900 font-serif leading-tight">
                Clear. Calm. Shareable.
              </h3>
            </div>
            
            <p className="text-xl text-slate-600 leading-relaxed font-medium max-w-lg">
              Our Truth Cards are designed to be easy to understand, easy to share, and impossible to ignore.
            </p>
            
            <div className="grid sm:grid-cols-2 gap-y-4 gap-x-8 text-slate-700 font-semibold">
               <span className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-[#2E8C6A] fill-[#2E8C6A]/10" /> Simple Visuals</span>
               <span className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-[#2E8C6A] fill-[#2E8C6A]/10" /> Peace-First Messaging</span>
               <span className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-[#2E8C6A] fill-[#2E8C6A]/10" /> Verified Sources</span>
               <span className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-[#2E8C6A] fill-[#2E8C6A]/10" /> Share Anywhere</span>
            </div>

            <div className="pt-4">
              <Link href="/cards" className="inline-flex items-center gap-2 px-8 py-4 rounded-full bg-[#2E8C6A] hover:bg-[#257356] text-white font-semibold transition-all shadow-lg shadow-emerald-600/20">
                See Example Cards <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </div>

          <div className="relative h-[600px] flex items-center justify-center scale-90 md:scale-100">
             {/* Background stacked cards to give 3D effect */}
             <div className="absolute w-[400px] h-[500px] bg-yellow-50 rounded-3xl border border-yellow-100 rotate-6 translate-x-12 opacity-60 shadow-xl"></div>
             <div className="absolute w-[400px] h-[500px] bg-orange-50 rounded-3xl border border-orange-100 -rotate-3 -translate-x-12 opacity-80 shadow-xl"></div>
             
             {/* Main Card */}
             <div className="relative z-10 w-[440px] bg-white rounded-3xl shadow-2xl border border-slate-100 overflow-hidden flex flex-col">
                <div className="absolute top-0 right-0 px-4 py-2 bg-red-500 text-white font-black rounded-bl-xl text-sm tracking-widest flex items-center gap-1">
                   <Shield className="w-4 h-4 fill-white text-red-500" /> FALSE
                </div>
                
                <div className="p-8 pb-4 mt-4">
                   <div className="flex justify-between items-start mb-6">
                      <div>
                         <span className="text-xs font-bold text-red-500 uppercase tracking-wider mb-1 block">CLAIM</span>
                         <h4 className="text-xl font-bold text-slate-800 pr-4">A viral video shows Sachin Tendulkar promoting a gaming app that guarantees quick money.</h4>
                      </div>
                      <div className="text-right shrink-0">
                         <span className="text-[10px] font-bold text-slate-400 block">Confidence</span>
                         <span className="text-2xl font-black text-slate-800">99%</span>
                      </div>
                   </div>

                   {/* Mock Image Area */}
                   <div className="w-full h-40 bg-slate-900 rounded-xl relative overflow-hidden mb-6 flex items-center justify-center border border-slate-200 shadow-inner">
                      <div 
                        className="absolute inset-0 bg-cover bg-center opacity-60" 
                        style={{ backgroundImage: "url('https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Sachin_Tendulkar_at_MRF_Promotion_Event.jpg/800px-Sachin_Tendulkar_at_MRF_Promotion_Event.jpg')" }}
                      ></div>
                      <div className="relative z-10 w-12 h-12 bg-white/20 backdrop-blur rounded-full flex items-center justify-center">
                         <Play className="w-5 h-5 text-white ml-1" />
                      </div>
                      <div className="absolute bottom-2 left-2 px-2 py-1 bg-black/50 backdrop-blur rounded text-[10px] text-white font-mono">
                         AI DEEPFAKE
                      </div>
                   </div>

                   <div>
                      <span className="text-xs font-bold text-emerald-600 uppercase tracking-wider mb-1 block">TRUTH</span>
                      <p className="text-[14px] font-medium text-slate-700 leading-relaxed mb-3">
                        This is an AI-generated deepfake. Sachin Tendulkar confirmed the video is fake, and NDTV reported his voice was cloned for a financial scam.
                      </p>
                      <a href="https://www.ndtv.com/india-news/sachin-tendulkar-deepfake-video-promotes-gaming-app-cricket-legend-says-disturbing-4863339" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-600 hover:text-emerald-700 transition-colors bg-emerald-50 px-3 py-1.5 rounded-lg border border-emerald-100">
                        Read Full Article <ArrowRight className="w-3 h-3" />
                      </a>
                   </div>
                </div>

                <div className="px-8 py-4 bg-slate-50 border-t border-slate-100 mt-auto">
                   <span className="text-[10px] font-bold text-slate-400 block mb-2">Sources:</span>
                   <div className="flex gap-4 items-center">
                     <span className="text-lg font-black text-slate-400">NDTV</span>
                     <span className="text-sm font-bold text-slate-400">PTI</span>
                     <span className="text-sm font-serif font-bold text-slate-400">THE HINDU</span>
                   </div>
                </div>
                
                <div className="p-4 bg-emerald-50 text-center border-t border-emerald-100">
                   <p className="text-xs font-bold text-emerald-700">Let's keep our communities peaceful.</p>
                   <p className="text-xs font-medium text-emerald-600">Verify before you share. 🌿</p>
                </div>
              </div>
           </div>
        </motion.div>
      </section>

      {/* Quote Banner */}
      <section className="py-20 px-6 bg-white overflow-hidden border-t border-slate-100">
        <motion.div 
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.7 }}
          className="max-w-[1200px] mx-auto bg-emerald-50/70 rounded-[2.5rem] p-10 md:p-16 relative flex flex-col md:flex-row items-center gap-10 border border-emerald-100/50 shadow-sm"
        >
           <div className="flex-1 relative z-10">
              <Quote className="w-12 h-12 text-emerald-300 mb-6 rotate-180" />
              <h3 className="text-3xl md:text-[40px] font-bold text-slate-800 font-serif leading-tight mb-4">
                 Peace begins with <span className="text-emerald-600">clarity.</span>
              </h3>
              <p className="text-lg text-slate-600 font-medium leading-relaxed max-w-lg">
                 In a world of noise, Sukoon AI brings truth, so communities can live in peace.
              </p>
           </div>
           <div className="w-full md:w-[400px] h-[250px] relative shrink-0">
              {/* Image Illustration of Meditating Figure */}
              <div className="absolute inset-0 flex justify-center items-center">
                 <img 
                   src="/meditating_woman.png" 
                   alt="Woman meditating in lotus position" 
                   className="w-[110%] h-[110%] object-contain scale-[1.3] -translate-y-4 mix-blend-multiply opacity-90 drop-shadow-md"
                 />
              </div>
           </div>
        </motion.div>
      </section>




      {/* Footer Banner - Solid Green Full Width */}
      <section className="bg-gradient-to-r from-[#2E8C6A] to-emerald-600 pt-20 pb-20 relative overflow-hidden">
        {/* Background decorative lotus */}
        <div className="absolute -bottom-20 left-0 w-[400px] h-[400px] text-white opacity-[0.05] z-0 pointer-events-none">
          <LotusIcon className="w-full h-full" />
        </div>

        <div className="max-w-[1400px] mx-auto px-6 relative z-10 flex flex-col items-center justify-center gap-10">
          <div className="flex items-center gap-6 max-w-2xl text-center">
            <div className="w-20 h-20 hidden md:flex items-center justify-center bg-white/10 rounded-full shrink-0 border border-white/20 backdrop-blur-sm">
               <LotusIcon className="w-10 h-10 text-white" />
            </div>
            <div className="space-y-3 text-left">
               <h3 className="text-3xl md:text-4xl font-bold text-white font-serif tracking-tight">
                 Be a Part of the Peace Movement
               </h3>
               <p className="text-emerald-100 font-medium text-lg">
                 Together, we can build a digital world where truth prevails and peace is the norm.
               </p>
            </div>
          </div>
          
          <div className="flex flex-col sm:flex-row gap-4 w-full md:w-auto mt-4 shrink-0 justify-center">
            <Link href="/onboarding" className="px-8 py-4 rounded-xl bg-white text-emerald-700 font-bold hover:bg-emerald-50 transition-all text-center shadow-lg">
              Get Started for Free
            </Link>
            <Link href="#how-it-works" className="px-8 py-4 rounded-xl border-2 border-emerald-400 text-white font-bold hover:bg-emerald-600/50 transition-all text-center">
              Read More
            </Link>
          </div>
        </div>
      </section>

      {/* Minimal Footer */}
      <footer className="py-8 bg-slate-900 border-t border-slate-800 text-center px-6">
         <p className="text-slate-400 text-sm font-medium">© 2026 Sukoon AI. All rights reserved.</p>
      </footer>
    </div>
  )
}
