"use client";
import Link from "next/link";
import { ArrowLeft, Shield, CheckCircle2 } from "lucide-react";
import { motion } from "framer-motion";
import { mockVerifications } from "@/lib/mockData";

export default function ExampleCardsPage() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 pb-20">
      <nav className="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-[1400px] mx-auto px-6 h-16 flex items-center">
          <Link href="/" className="flex items-center gap-2 text-slate-600 hover:text-emerald-600 font-medium transition-colors">
            <ArrowLeft className="w-4 h-4" /> Back to Home
          </Link>
        </div>
      </nav>

      <div className="max-w-[1400px] mx-auto px-6 pt-12">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h1 className="text-4xl font-bold font-serif text-slate-900 mb-4">Truth Cards Gallery</h1>
          <p className="text-lg text-slate-600 font-medium">
            Explore examples of how Sukoon AI debunks rumors, verifies facts, and delivers peaceful clarity in a highly shareable format.
          </p>
        </div>

        <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-10">
          {mockVerifications.slice(0, 9).map((verification, i) => (
            <motion.div 
              key={verification.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              whileHover={{ scale: 1.03, y: -10, rotateX: 2, rotateY: 2 }}
              className="bg-white rounded-3xl shadow-lg border border-slate-100 overflow-hidden flex flex-col h-full cursor-pointer"
            >
              <div className={`absolute top-0 right-0 px-4 py-2 text-white font-black rounded-bl-xl text-sm tracking-widest flex items-center gap-1 z-10 ${
                verification.verdict === 'false' ? 'bg-red-500' :
                verification.verdict === 'misleading' ? 'bg-amber-500' : 'bg-emerald-500'
              }`}>
                {verification.verdict === 'false' || verification.verdict === 'misleading' ? (
                  <Shield className="w-4 h-4 fill-white opacity-80" />
                ) : (
                  <CheckCircle2 className="w-4 h-4" />
                )}
                {verification.verdict.toUpperCase()}
              </div>
              
              <div className="p-8 pb-4 mt-4 flex-grow">
                 <div className="flex justify-between items-start mb-6">
                    <div className="pr-12">
                       <span className={`text-xs font-bold uppercase tracking-wider mb-2 block ${
                          verification.verdict === 'false' ? 'text-red-500' :
                          verification.verdict === 'misleading' ? 'text-amber-500' : 'text-emerald-600'
                       }`}>CLAIM</span>
                       <h4 className="text-lg font-bold text-slate-800 leading-tight">"{verification.claimSummary}"</h4>
                    </div>
                 </div>

                 <div className="w-full h-48 bg-slate-100 rounded-xl relative overflow-hidden mb-6 flex items-center justify-center border border-slate-200 group">
                    {verification.mediaType === 'image' && verification.mediaUrl ? (
                      /* eslint-disable-next-line @next/next/no-img-element */
                      <img src={verification.mediaUrl} alt={verification.claimSummary} className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" />
                    ) : (
                      <div className="text-slate-300 font-mono text-sm tracking-widest">NO MEDIA</div>
                    )}
                 </div>

                 <div>
                    <span className="text-xs font-bold text-emerald-600 uppercase tracking-wider mb-2 block">TRUTH</span>
                    <p className="text-[14px] font-medium text-slate-700 leading-relaxed">
                      {verification.actualFacts}
                    </p>
                 </div>
              </div>

              <div className="px-8 py-4 bg-slate-50 border-t border-slate-100">
                 <span className="text-[10px] font-bold text-slate-400 block mb-2 uppercase">Verified Sources:</span>
                 <div className="flex flex-wrap gap-2 items-center">
                    {verification.sourceCitations.map((source, idx) => (
                      <span key={idx} className="text-[10px] font-bold text-slate-500 bg-white border border-slate-200 px-2 py-1 rounded">
                        {source}
                      </span>
                    ))}
                 </div>
              </div>
              
              <div className="p-4 bg-emerald-50 text-center border-t border-emerald-100 mt-auto">
                 <p className="text-[11px] font-bold text-emerald-700 mb-1">{verification.peaceMessage}</p>
                 <p className="text-[10px] font-medium text-emerald-600 uppercase tracking-widest">Verify before you share. 🌿</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
