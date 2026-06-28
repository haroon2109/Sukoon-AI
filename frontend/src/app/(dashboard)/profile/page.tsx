"use client"
import { useState, useEffect } from "react"
import { User, Mail, Shield, Building, Edit2, ShieldCheck, Phone, MapPin, Globe, Calendar } from "lucide-react"

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
  <svg viewBox="0 0 24 24" className={className || "w-8 h-8"} fill="currentColor">
    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
  </svg>
);

export default function ProfilePage() {
  const [userName, setUserName] = useState("")
  const [userEmail, setUserEmail] = useState("")
  const [userMobile, setUserMobile] = useState("")
  const [userCity, setUserCity] = useState("")
  const [userLanguage, setUserLanguage] = useState("")
  const [userAge, setUserAge] = useState("")
  const [userInsta, setUserInsta] = useState("")
  const [userX, setUserX] = useState("")

  useEffect(() => {
    const storedName = localStorage.getItem('sukoon_name')
    if (storedName) setUserName(storedName)
    const storedEmail = localStorage.getItem('sukoon_email')
    if (storedEmail) setUserEmail(storedEmail)
    const storedMobile = localStorage.getItem('sukoon_mobile')
    if (storedMobile) setUserMobile(storedMobile)
    const storedCity = localStorage.getItem('sukoon_city')
    if (storedCity) setUserCity(storedCity)
    const storedLanguage = localStorage.getItem('sukoon_language')
    if (storedLanguage) setUserLanguage(storedLanguage)
    const storedAge = localStorage.getItem('sukoon_age')
    if (storedAge) setUserAge(storedAge)
    const storedInsta = localStorage.getItem('sukoon_insta')
    if (storedInsta) setUserInsta(storedInsta)
    const storedX = localStorage.getItem('sukoon_x')
    if (storedX) setUserX(storedX)
  }, [])

  return (
    <div className="max-w-[1000px] mx-auto space-y-8 pb-10">
      <div className="flex items-center justify-between mb-8">
         <h1 className="text-3xl font-bold text-slate-800 font-serif">My Profile</h1>
      </div>

      <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
         {/* Banner */}
         <div className="h-32 bg-gradient-to-r from-emerald-500 to-teal-500 relative"></div>
         
         <div className="px-8 pb-8 relative">
            {/* Avatar */}
            <div className="w-24 h-24 rounded-full border-4 border-white bg-slate-100 flex items-center justify-center text-3xl font-bold text-slate-400 absolute -top-12 shadow-md bg-gradient-to-br from-emerald-100 to-teal-50">
               {userName ? userName.charAt(0).toUpperCase() : "U"}
               <button title="Edit Profile" aria-label="Edit Profile" className="absolute bottom-0 right-0 w-8 h-8 bg-white rounded-full border border-slate-200 flex items-center justify-center text-slate-500 hover:text-emerald-600 transition-colors shadow-sm">
                  <Edit2 className="w-4 h-4" />
               </button>
            </div>

            <div className="pt-16">
               <div className="flex justify-between items-start mb-8">
                  <div>
                     <h2 className="text-2xl font-bold text-slate-800">{userName || "User"}</h2>
                     <p className="text-slate-500 font-medium">{userEmail || "No email provided"}</p>
                  </div>
                  <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-50 border border-emerald-100 text-emerald-700 text-[11px] font-bold">
                     <ShieldCheck className="w-4 h-4" /> Verified Peace Builder
                  </div>
               </div>

               <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-6">
                     <h3 className="text-sm font-bold text-slate-800 border-b border-slate-100 pb-2">Personal Information</h3>
                     
                     <div className="space-y-4">
                        <div>
                           <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wide">Full Name</label>
                           <div className="flex items-center gap-3 mt-1 p-3 bg-slate-50 border border-slate-200 rounded-xl">
                              <User className="w-4 h-4 text-slate-400" />
                              <span className="text-[13px] font-bold text-slate-800">{userName || "Not provided"}</span>
                           </div>
                        </div>

                        <div>
                           <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wide">Email Address</label>
                           <div className="flex items-center gap-3 mt-1 p-3 bg-slate-50 border border-slate-200 rounded-xl">
                              <Mail className="w-4 h-4 text-slate-400" />
                              <span className="text-[13px] font-bold text-slate-800">{userEmail || "Not provided"}</span>
                           </div>
                        </div>
                        
                        <div>
                           <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wide">Age</label>
                           <div className="flex items-center gap-3 mt-1 p-3 bg-slate-50 border border-slate-200 rounded-xl">
                              <Calendar className="w-4 h-4 text-slate-400" />
                              <span className="text-[13px] font-bold text-slate-800">{userAge || "Not provided"}</span>
                           </div>
                        </div>

                        <div>
                           <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wide">Mobile Number</label>
                           <div className="flex items-center gap-3 mt-1 p-3 bg-slate-50 border border-slate-200 rounded-xl">
                              <Phone className="w-4 h-4 text-slate-400" />
                              <span className="text-[13px] font-bold text-slate-800">{userMobile || "Not provided"}</span>
                           </div>
                        </div>
                        
                        <div>
                           <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wide">City</label>
                           <div className="flex items-center gap-3 mt-1 p-3 bg-slate-50 border border-slate-200 rounded-xl">
                              <MapPin className="w-4 h-4 text-slate-400" />
                              <span className="text-[13px] font-bold text-slate-800">{userCity || "Not provided"}</span>
                           </div>
                        </div>
                        
                        <div>
                           <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wide">Preferred Language</label>
                           <div className="flex items-center gap-3 mt-1 p-3 bg-slate-50 border border-slate-200 rounded-xl">
                              <Globe className="w-4 h-4 text-slate-400" />
                              <span className="text-[13px] font-bold text-slate-800">{userLanguage || "Not provided"}</span>
                           </div>
                        </div>

                        <div>
                           <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wide">Instagram ID (Optional)</label>
                           <div className="flex items-center gap-3 mt-1 p-3 bg-slate-50 border border-slate-200 rounded-xl">
                              <InstagramIconCustom className="w-4 h-4 text-slate-400" />
                              <span className="text-[13px] font-bold text-slate-800">{userInsta || "Not provided"}</span>
                           </div>
                        </div>

                        <div>
                           <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wide">X / Twitter ID (Optional)</label>
                           <div className="flex items-center gap-3 mt-1 p-3 bg-slate-50 border border-slate-200 rounded-xl">
                              <XIconCustom className="w-4 h-4 text-slate-400" />
                              <span className="text-[13px] font-bold text-slate-800">{userX || "Not provided"}</span>
                           </div>
                        </div>
                     </div>
                  </div>

                  <div className="space-y-6">
                     <h3 className="text-sm font-bold text-slate-800 border-b border-slate-100 pb-2">Account Status</h3>
                     
                     <div className="bg-emerald-50/50 border border-emerald-100 rounded-2xl p-5 flex flex-col items-center text-center">
                        <Shield className="w-10 h-10 text-emerald-500 mb-3" />
                        <h4 className="text-[15px] font-bold text-slate-800 mb-1">Account is Secure</h4>
                        <p className="text-[11px] text-slate-500 font-medium mb-4">Your account is fully verified and actively participating in the Sukoon AI network.</p>
                        <button className="w-full py-2 bg-white border border-emerald-200 text-emerald-700 text-xs font-bold rounded-xl hover:bg-emerald-50 transition-colors">
                           Manage Security Settings
                        </button>
                     </div>
                  </div>
               </div>
            </div>
         </div>
      </div>
    </div>
  )
}
