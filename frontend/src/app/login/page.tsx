"use client"
import Link from "next/link"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { Lock, Mail, ChevronRight, User, ShieldCheck, Bell, Users } from "lucide-react"

// Custom Lotus SVG Logo
const LotusIcon = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" fill="currentColor" className={className} xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C12 2 10 6 10 10C10 14 12 18 12 18C12 18 14 14 14 10C14 6 12 2 12 2Z" opacity="0.6"/>
    <path d="M12 22C12 22 16 19 19 15C22 11 22 7 22 7C22 7 18 8 14 11C11.5 12.8 12 22 12 22Z" opacity="0.8"/>
    <path d="M12 22C12 22 8 19 5 15C2 11 2 7 2 7C2 7 6 8 10 11C12.5 12.8 12 22 12 22Z" />
  </svg>
)

export default function LoginPage() {
  const router = useRouter()
  const [identifier, setIdentifier] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!identifier.trim() || !password.trim()) {
      setError("Please enter both your email/phone and password.")
      return
    }

    // In a real app, this would be an API call to verify credentials.
    // For now, we'll just log them in to the dashboard directly.
    setError("")
    router.push('/dashboard')
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col md:flex-row font-sans">
       
       {/* Left Column (Information) - Cloned from Onboarding */}
       <div className="w-full md:w-[45%] lg:w-[40%] bg-[#F8FAFC] p-8 lg:p-12 xl:p-16 flex flex-col min-h-screen border-r border-slate-200">
          
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 mb-16 hover:opacity-90 transition-opacity w-fit">
            <LotusIcon className="w-8 h-8 text-emerald-600" />
            <div className="flex flex-col">
              <span className="text-[17px] font-semibold tracking-tight text-slate-800 leading-none">Sukoon <span className="font-bold text-emerald-600">AI</span></span>
              <span className="text-[8px] text-slate-500 font-medium tracking-wide mt-1">Verified Peace. Digital Harmony.</span>
            </div>
          </Link>

          {/* Heading */}
          <div className="mb-10">
             <h1 className="text-[32px] lg:text-[40px] font-bold text-slate-800 leading-[1.15] mb-4">
                Welcome back<br/>to your peace
             </h1>
             <p className="text-[13px] text-slate-500 font-medium leading-relaxed max-w-[320px]">
                Sign in to manage your alerts and verify the truth within your community.
             </p>
          </div>

          {/* Illustration Area */}
          <div className="relative w-full max-w-[340px] h-[220px] mb-8 mx-auto md:mx-0 flex items-center justify-center">
             <img src="/man_laptop.png" alt="Onboarding Hero" className="w-[120%] h-[120%] object-contain -ml-8 mix-blend-multiply" />
             <div className="absolute top-10 right-4 w-12 h-12 bg-white rounded-full shadow-lg border border-slate-100 flex items-center justify-center text-emerald-600 z-10 hidden sm:flex">
                <User className="w-6 h-6" />
             </div>
          </div>

          {/* Feature Highlight Box */}
          <div className="bg-[#f0fdf4] rounded-2xl p-6 border border-[#dcfce7] mb-auto">
             <div className="space-y-5">
                <div className="flex items-start gap-4">
                   <div className="w-8 h-8 rounded-full bg-white text-emerald-600 flex items-center justify-center shrink-0 shadow-sm border border-emerald-50">
                      <ShieldCheck className="w-4 h-4" />
                   </div>
                   <div>
                      <h4 className="text-[12px] font-bold text-slate-800 mb-0.5">Personalized Experience</h4>
                      <p className="text-[10px] font-medium text-slate-500 leading-relaxed">Get alerts and insights relevant to you.</p>
                   </div>
                </div>

                <div className="flex items-start gap-4">
                   <div className="w-8 h-8 rounded-full bg-white text-emerald-600 flex items-center justify-center shrink-0 shadow-sm border border-emerald-50">
                      <Bell className="w-4 h-4" />
                   </div>
                   <div>
                      <h4 className="text-[12px] font-bold text-slate-800 mb-0.5">Timely Alerts</h4>
                      <p className="text-[10px] font-medium text-slate-500 leading-relaxed">Stay informed about harmful content.</p>
                   </div>
                </div>

                <div className="flex items-start gap-4">
                   <div className="w-8 h-8 rounded-full bg-white text-emerald-600 flex items-center justify-center shrink-0 shadow-sm border border-emerald-50">
                      <Users className="w-4 h-4" />
                   </div>
                   <div>
                      <h4 className="text-[12px] font-bold text-slate-800 mb-0.5">Safer Community</h4>
                      <p className="text-[10px] font-medium text-slate-500 leading-relaxed">Together, we build a peaceful digital world.</p>
                   </div>
                </div>
             </div>
          </div>

          {/* Footer Note */}
          <div className="mt-8 flex items-start gap-3">
             <Lock className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
             <p className="text-[11px] font-medium text-slate-500 leading-relaxed">
                Your information is secure and<br/>never shared with anyone.
             </p>
          </div>
       </div>

       {/* Right Column (Form) */}
       <div className="flex-1 p-4 sm:p-8 md:p-12 flex items-center justify-center bg-slate-50">
          <div className="w-full max-w-[480px] bg-white rounded-[2rem] shadow-sm border border-slate-200 p-8 sm:p-10">
             
             {/* Form Header */}
             <div className="flex items-center gap-5 mb-8">
                <div className="w-14 h-14 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
                   <User className="w-6 h-6 stroke-[2]" />
                </div>
                <div>
                   <h2 className="text-[22px] font-bold text-slate-800 mb-1">Welcome Back</h2>
                   <p className="text-[13px] text-slate-500 font-medium">Please enter your details to sign in.</p>
                </div>
             </div>

             {/* Google OAuth Button */}
             <button type="button" onClick={() => router.push('/dashboard')} className="w-full mt-6 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-[13px] font-bold py-3.5 rounded-xl flex items-center justify-center gap-3 transition-colors shadow-sm mb-8">
                <svg viewBox="0 0 24 24" className="w-5 h-5">
                   <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                   <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                   <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                   <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                </svg>
                Sign in with Google
             </button>

             {/* OAuth Divider */}
             <div className="relative mb-8">
                <div className="absolute inset-0 flex items-center">
                   <div className="w-full border-t border-slate-200"></div>
                </div>
                <div className="relative flex justify-center text-[11px] font-bold">
                   <span className="bg-white px-3 text-slate-400 tracking-wider">OR CONTINUE WITH</span>
                </div>
             </div>

             {/* Form */}
             <form onSubmit={handleLogin} className="space-y-6">
                
                {/* Email / Phone */}
                <div className="space-y-2">
                   <label className="text-[12px] font-bold text-slate-800 block">Email or Phone Number</label>
                   <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                         <Mail className="w-4 h-4 text-slate-400" />
                      </div>
                      <input 
                        type="text" 
                        value={identifier}
                        onChange={(e) => setIdentifier(e.target.value)}
                        placeholder="Enter your email or phone" 
                        className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-[12px] font-medium text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-colors" 
                      />
                   </div>
                </div>

                {/* Password */}
                <div className="space-y-2">
                   <div className="flex items-center justify-between">
                      <label className="text-[12px] font-bold text-slate-800 block">Password</label>
                      <Link href="#" className="text-[11px] font-bold text-emerald-600 hover:text-emerald-700">Forgot password?</Link>
                   </div>
                   <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                         <Lock className="w-4 h-4 text-slate-400" />
                      </div>
                      <input 
                        type="password" 
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="••••••••" 
                        className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-[12px] font-medium text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-colors" 
                      />
                   </div>
                </div>

                {/* Error Message */}
                {error && (
                  <div className="bg-red-50 text-red-500 text-[12px] font-bold p-3 rounded-lg text-center border border-red-100">
                    {error}
                  </div>
                )}

                {/* Action Button */}
                <button type="submit" className="w-full bg-[#059669] hover:bg-[#047857] text-white text-[13px] font-bold py-3.5 rounded-xl flex items-center justify-center gap-2 transition-colors shadow-md shadow-emerald-600/20">
                   Sign In <ChevronRight className="w-4 h-4" />
                </button>
                
             </form>

             {/* Footer link */}
             <div className="mt-8 text-center">
                <p className="text-[12px] font-medium text-slate-500">
                   Don&apos;t have an account? <Link href="/onboarding" className="font-bold text-emerald-600 hover:text-emerald-700">Sign up</Link>
                </p>
             </div>

          </div>
       </div>
    </div>
  )
}
