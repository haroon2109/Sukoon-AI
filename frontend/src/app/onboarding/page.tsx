"use client"
import Link from "next/link"
import { useState } from "react"
import { useRouter } from "next/navigation"
import { ShieldCheck, User, Calendar, Camera, Phone, Mail, MapPin, Map, Globe, ChevronDown, Lock, Bell, Users, ChevronRight } from "lucide-react"

// Custom Lotus SVG Logo
const LotusIcon = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" fill="currentColor" className={className} xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C12 2 10 6 10 10C10 14 12 18 12 18C12 18 14 14 14 10C14 6 12 2 12 2Z" opacity="0.6"/>
    <path d="M12 22C12 22 16 19 19 15C22 11 22 7 22 7C22 7 18 8 14 11C11.5 12.8 12 22 12 22Z" opacity="0.8"/>
    <path d="M12 22C12 22 8 19 5 15C2 11 2 7 2 7C2 7 6 8 10 11C12.5 12.8 12 22 12 22Z" />
  </svg>
)

export default function OnboardingPage() {
  const router = useRouter()
  const [fullName, setFullName] = useState("")
  const [age, setAge] = useState("")
  const [mobile, setMobile] = useState("")
  const [city, setCity] = useState("")
  const [password, setPassword] = useState("")
  const [language, setLanguage] = useState("English")
  const [error, setError] = useState("")

  const handleContinue = () => {
    if (!fullName.trim() || !age.trim() || !mobile.trim() || !city.trim() || !password.trim()) {
      setError("Please fill in all mandatory fields to continue.")
      return
    }
    setError("")
    localStorage.setItem('sukoon_name', fullName.trim())
    localStorage.setItem('sukoon_age', age.trim())
    localStorage.setItem('sukoon_mobile', mobile.trim())
    localStorage.setItem('sukoon_city', city.trim())
    localStorage.setItem('sukoon_language', language)
    router.push('/dashboard')
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col md:flex-row font-sans">
       
       {/* Left Column (Information) */}
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
                Let's get to<br/>know you better
             </h1>
             <p className="text-[13px] text-slate-500 font-medium leading-relaxed max-w-[320px]">
                Help us personalize your experience and keep you informed about what matters most.
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
          <div className="w-full max-w-[640px] bg-white rounded-[2rem] shadow-sm border border-slate-200 p-8 sm:p-10">
             
             {/* Form Header */}
             <div className="flex items-center gap-5 mb-8">
                <div className="w-14 h-14 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
                   <User className="w-6 h-6 stroke-[2]" />
                </div>
                <div>
                   <h2 className="text-[22px] font-bold text-slate-800 mb-1">Create Your Profile</h2>
                   <p className="text-[13px] text-slate-500 font-medium">Just a few details to get you started.</p>
                </div>
             </div>

             {/* Google OAuth */}
             <button type="button" onClick={() => { localStorage.setItem('sukoon_name', 'Google User'); router.push('/dashboard') }} className="w-full bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-[13px] font-bold py-3.5 rounded-xl flex items-center justify-center gap-3 transition-colors shadow-sm mb-8">
                <svg viewBox="0 0 24 24" className="w-5 h-5">
                   <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                   <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                   <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                   <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                </svg>
                Sign up with Google
             </button>

             {/* OAuth Divider */}
             <div className="relative mb-8">
                <div className="absolute inset-0 flex items-center">
                   <div className="w-full border-t border-slate-200"></div>
                </div>
                <div className="relative flex justify-center text-[11px] font-bold">
                   <span className="bg-white px-3 text-slate-400 tracking-wider">OR REGISTER WITH EMAIL</span>
                </div>
             </div>

             {/* Form Fields */}
             <div className="space-y-6">
                
                {/* Row 1: Name & Age */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                   <div className="space-y-2">
                      <label className="text-[12px] font-bold text-slate-800 block">Full Name <span className="text-red-500">*</span></label>
                      <div className="relative">
                         <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                            <User className="w-4 h-4 text-slate-400" />
                         </div>
                         <input 
                           type="text" 
                           value={fullName}
                           onChange={(e) => setFullName(e.target.value)}
                           placeholder="Enter your full name" 
                           className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-[12px] font-medium text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-colors" 
                         />
                      </div>
                   </div>
                   <div className="space-y-2">
                      <label className="text-[12px] font-bold text-slate-800 block">Age <span className="text-red-500">*</span></label>
                      <div className="relative">
                         <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                            <Calendar className="w-4 h-4 text-slate-400" />
                         </div>
                         <input 
                           type="text" 
                           value={age}
                           onChange={(e) => setAge(e.target.value)}
                           placeholder="Enter your age" 
                           className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-[12px] font-medium text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-colors" 
                         />
                      </div>
                   </div>
                </div>

                {/* Profile Picture Upload */}
                <div className="space-y-2">
                   <label className="text-[12px] font-bold text-slate-800 block">Profile Picture</label>
                   <div className="flex items-center gap-5">
                      <div className="w-20 h-20 rounded-2xl bg-slate-50 border border-slate-200 border-dashed flex items-center justify-center text-slate-400 shrink-0 hover:bg-slate-100 transition-colors cursor-pointer">
                         <Camera className="w-6 h-6" />
                      </div>
                      <div>
                         <h4 className="text-[12px] font-bold text-slate-800 mb-1">Upload a profile picture</h4>
                         <p className="text-[10px] text-slate-500 font-medium mb-3">JPG, PNG or WEBP. Max size 2MB.</p>
                         <button className="px-4 py-1.5 rounded-md border border-emerald-600 text-emerald-600 text-[11px] font-bold hover:bg-emerald-50 transition-colors">
                            Choose File
                         </button>
                      </div>
                   </div>
                </div>

                {/* Row 2: Mobile & Email */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                   <div className="space-y-2">
                      <label className="text-[12px] font-bold text-slate-800 block">Mobile Number <span className="text-red-500">*</span></label>
                      <div className="relative">
                         <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                            <Phone className="w-4 h-4 text-slate-400" />
                         </div>
                         <input 
                           type="text" 
                           value={mobile}
                           onChange={(e) => setMobile(e.target.value)}
                           placeholder="Enter your mobile number" 
                           className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-[12px] font-medium text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-colors" 
                         />
                      </div>
                   </div>
                   <div className="space-y-2">
                      <label className="text-[12px] font-bold text-slate-800 block">Email (Optional)</label>
                      <div className="relative">
                         <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                            <Mail className="w-4 h-4 text-slate-400" />
                         </div>
                         <input type="email" placeholder="Enter your email address" className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-[12px] font-medium text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-colors" />
                      </div>
                   </div>
                </div>

                {/* Password */}
                <div className="space-y-2">
                   <label className="text-[12px] font-bold text-slate-800 block">Create Password <span className="text-red-500">*</span></label>
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

                {/* Row 3: City & State */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                   <div className="space-y-2">
                      <label className="text-[12px] font-bold text-slate-800 block">City <span className="text-red-500">*</span></label>
                      <div className="relative">
                         <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                            <MapPin className="w-4 h-4 text-slate-400" />
                         </div>
                         <input 
                           type="text" 
                           value={city}
                           onChange={(e) => setCity(e.target.value)}
                           placeholder="Enter your city" 
                           className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-[12px] font-medium text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-colors" 
                         />
                      </div>
                   </div>
                   <div className="space-y-2">
                      <label className="text-[12px] font-bold text-slate-800 block">State / Province (Optional)</label>
                      <div className="relative">
                         <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                            <Map className="w-4 h-4 text-slate-400" />
                         </div>
                         <input type="text" placeholder="Enter your state or province" className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-[12px] font-medium text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-colors" />
                      </div>
                   </div>
                </div>

                {/* Language Dropdown */}
                <div className="space-y-2">
                   <label className="text-[12px] font-bold text-slate-800 block">Preferred Language</label>
                   <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                         <Globe className="w-4 h-4 text-slate-500" />
                      </div>
                      <select 
                         aria-label="Preferred Language"
                         value={language}
                         onChange={(e) => setLanguage(e.target.value)}
                         className="w-full pl-10 pr-10 py-3 bg-white border border-slate-200 rounded-xl text-[12px] font-bold text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-colors appearance-none cursor-pointer"
                      >
                         <option value="Bengali">Bengali</option>
                         <option value="English">English</option>
                         <option value="Hindi">Hindi</option>
                         <option value="Kannada">Kannada</option>
                         <option value="Malayalam">Malayalam</option>
                         <option value="Marathi">Marathi</option>
                         <option value="Tamil">Tamil</option>
                         <option value="Telugu">Telugu</option>
                         <option value="Urdu">Urdu</option>
                      </select>
                      <div className="absolute inset-y-0 right-0 pr-3.5 flex items-center pointer-events-none">
                         <ChevronDown className="w-4 h-4 text-slate-400" />
                      </div>
                   </div>
                </div>

                {/* Privacy Banner */}
                <div className="bg-[#f0fdf4] rounded-xl p-4 border border-[#dcfce7] flex items-start gap-4 mt-8">
                   <div className="w-8 h-8 rounded-full bg-white text-emerald-600 flex items-center justify-center shrink-0 shadow-sm border border-emerald-50">
                      <ShieldCheck className="w-4 h-4" />
                   </div>
                   <div>
                      <h4 className="text-[12px] font-bold text-emerald-800 mb-1">Your privacy matters</h4>
                      <p className="text-[10px] font-medium text-slate-500 leading-relaxed pr-4">
                         We only use your information to personalize your experience and keep you safe. You can change this anytime in settings.
                      </p>
                   </div>
                </div>

                {/* Action Area */}
                <div className="pt-4 flex flex-col items-center">
                   {error && (
                     <div className="text-red-500 text-xs font-bold mb-3">{error}</div>
                   )}
                   <button onClick={handleContinue} className="w-full max-w-[400px] bg-[#059669] hover:bg-[#047857] text-white text-[13px] font-bold py-3.5 rounded-xl flex items-center justify-center gap-2 transition-colors shadow-md shadow-emerald-600/20">
                      Continue <ChevronRight className="w-4 h-4" />
                   </button>
                   <p className="text-[10px] text-slate-400 font-medium mt-4">
                      You can update these details anytime later.
                   </p>
                </div>

             </div>
          </div>
       </div>
    </div>
  )
}
