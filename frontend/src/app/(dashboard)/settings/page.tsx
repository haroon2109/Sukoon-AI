"use client"
import { User, Bell, ShieldCheck, Globe, Moon, Download, Trash2, ChevronRight, ChevronDown, Headset, Crown } from "lucide-react"
import { useState, useEffect } from "react"
import Link from "next/link"

export default function SettingsPage() {
  const [userName, setUserName] = useState("Aman Verma")
  const [notificationsEnabled, setNotificationsEnabled] = useState(true)
  const [language, setLanguage] = useState("English")
  const [isLanguageMenuOpen, setIsLanguageMenuOpen] = useState(false)
  const languages = ["Bengali", "English", "Hindi", "Kannada", "Malayalam", "Marathi", "Tamil", "Telugu", "Urdu"]
  const [appearance, setAppearance] = useState("Light")
  const [joinDate, setJoinDate] = useState("...")

  useEffect(() => {
    const storedName = localStorage.getItem('sukoon_name')
    if (storedName) {
      setUserName(storedName)
    }

    const storedLanguage = localStorage.getItem('sukoon_language')
    if (storedLanguage) {
      setLanguage(storedLanguage)
    }

    let storedDate = localStorage.getItem('sukoon_join_date')
    if (!storedDate) {
      const today = new Date();
      storedDate = today.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
      localStorage.setItem('sukoon_join_date', storedDate);
    }
    setJoinDate(storedDate)
  }, [])

  const handleLanguageChange = (lang: string) => {
    setLanguage(lang)
    setIsLanguageMenuOpen(false)
    localStorage.setItem('sukoon_language', lang)
    // Reload page to trigger Google Translate widget with new cookie
    window.location.reload()
  }

  const handleDeleteAccount = async () => {
    if (confirm("Are you sure you want to delete your account? This action cannot be undone.")) {
      const Cookies = (await import('js-cookie')).default
      Cookies.remove('sukoon_token')
      localStorage.clear()
      window.location.href = '/'
    }
  }

  const handleExport = () => {
    alert("Your data export has started. You will receive an email when it is ready.")
  }
  return (
    <div className="max-w-[1400px] mx-auto space-y-6 pb-10">
       {/* Hero Section */}
       <div className="flex flex-col md:flex-row items-center justify-between mb-10 bg-white rounded-2xl border border-slate-100 shadow-sm p-8">
          <div className="max-w-xl pr-6">
             <h1 className="text-3xl font-bold text-slate-800 font-serif mb-2">Settings</h1>
             <p className="text-slate-500 font-medium text-sm">Manage your preferences and account settings.</p>
          </div>
          <div className="hidden md:block w-[280px] shrink-0">
             <img src="/settings_hero.png" alt="Settings hero" className="w-full h-auto object-contain mix-blend-multiply" />
          </div>
       </div>

       <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content Area (Left Column) */}
          <div className="lg:col-span-2 space-y-6">
             
             {/* Settings List */}
             <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden p-2">
                 <div className="flex flex-col gap-0">
                    
                    {/* Profile Information */}
                    <div className="flex items-center p-4 px-5 hover:bg-slate-50 transition-colors gap-5">
                       <div className="w-10 h-10 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
                          <User className="w-5 h-5" />
                       </div>
                       <div className="flex-1 min-w-0">
                          <h3 className="text-[13px] font-bold text-slate-800 mb-0.5">Profile Information</h3>
                          <p className="text-[11px] text-slate-500 font-medium">View and update your personal information.</p>
                       </div>
                       <div className="shrink-0">
                          <button className="flex items-center justify-center gap-1.5 text-[11px] font-bold text-slate-600 border border-slate-200 rounded-lg px-4 py-2 hover:bg-white transition-colors w-[85px]" onClick={() => window.location.href = '/profile'}>
                             Edit <ChevronRight className="w-3.5 h-3.5 ml-0.5 text-slate-400" />
                          </button>
                       </div>
                    </div>

                    <hr className="border-slate-50 mx-5" />

                    {/* Notifications */}
                    <div className="flex items-center p-4 px-5 hover:bg-slate-50 transition-colors gap-5 cursor-pointer" onClick={() => setNotificationsEnabled(!notificationsEnabled)}>
                       <div className="w-10 h-10 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
                          <Bell className="w-5 h-5" />
                       </div>
                       <div className="flex-1 min-w-0">
                          <h3 className="text-[13px] font-bold text-slate-800 mb-0.5">Notifications</h3>
                          <p className="text-[11px] text-slate-500 font-medium">Manage how you receive alerts and updates.</p>
                       </div>
                       <div className="shrink-0 flex justify-end w-[85px]">
                          <div className={`w-11 h-6 rounded-full flex items-center p-0.5 transition-colors ${notificationsEnabled ? 'bg-emerald-600' : 'bg-slate-300'}`}>
                             <div className={`w-5 h-5 bg-white rounded-full shadow-sm transition-transform ${notificationsEnabled ? 'translate-x-5' : 'translate-x-0'}`}></div>
                          </div>
                       </div>
                    </div>



                    <hr className="border-slate-50 mx-5" />

                    {/* Language */}
                    <div className="flex items-center p-4 px-5 hover:bg-slate-50 transition-colors gap-5">
                       <div className="w-10 h-10 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
                          <Globe className="w-5 h-5" />
                       </div>
                       <div className="flex-1 min-w-0">
                          <h3 className="text-[13px] font-bold text-slate-800 mb-0.5">Language</h3>
                          <p className="text-[11px] text-slate-500 font-medium">Choose your preferred language.</p>
                       </div>
                       <div className="shrink-0 relative">
                          <button className="flex items-center justify-between gap-1.5 text-[11px] font-bold text-slate-600 border border-slate-200 rounded-lg px-4 py-2 hover:bg-white transition-colors w-[100px]" onClick={() => setIsLanguageMenuOpen(!isLanguageMenuOpen)}>
                             {language} <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                          </button>
                          {isLanguageMenuOpen && (
                             <div className="absolute right-0 top-full mt-1 w-[100px] bg-white border border-slate-200 rounded-lg shadow-lg overflow-hidden z-10">
                                {languages.map((lang) => (
                                   <button key={lang} className="w-full text-left px-4 py-2 text-[11px] font-bold text-slate-600 hover:bg-slate-50 transition-colors" onClick={() => handleLanguageChange(lang)}>
                                      {lang}
                                   </button>
                                ))}
                             </div>
                          )}
                       </div>
                    </div>



                    <hr className="border-slate-50 mx-5" />

                    {/* Data & Export */}
                    <div className="flex items-center p-4 px-5 hover:bg-slate-50 transition-colors gap-5">
                       <div className="w-10 h-10 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
                          <Download className="w-5 h-5" />
                       </div>
                       <div className="flex-1 min-w-0">
                          <h3 className="text-[13px] font-bold text-slate-800 mb-0.5">Data & Export</h3>
                          <p className="text-[11px] text-slate-500 font-medium">Download or export your data and reports.</p>
                       </div>
                       <div className="shrink-0">
                          <button className="flex items-center justify-center gap-1.5 text-[11px] font-bold text-slate-600 border border-slate-200 rounded-lg px-4 py-2 hover:bg-white transition-colors w-[85px]" onClick={handleExport}>
                             Export <ChevronRight className="w-3.5 h-3.5 ml-0.5 text-slate-400" />
                          </button>
                       </div>
                    </div>

                    <hr className="border-slate-50 mx-5" />

                    {/* Delete Account */}
                    <div className="flex items-center p-4 px-5 hover:bg-red-50/50 transition-colors gap-5">
                       <div className="w-10 h-10 rounded-full bg-red-50 text-red-500 flex items-center justify-center shrink-0">
                          <Trash2 className="w-5 h-5" />
                       </div>
                       <div className="flex-1 min-w-0">
                          <h3 className="text-[13px] font-bold text-slate-800 mb-0.5">Delete Account</h3>
                          <p className="text-[11px] text-slate-500 font-medium">Permanently delete your account and all data.</p>
                       </div>
                       <div className="shrink-0">
                          <button className="flex items-center justify-center gap-1.5 text-[11px] font-bold text-red-500 border border-red-200 rounded-lg px-4 py-2 hover:bg-red-50 transition-colors w-[85px]" onClick={handleDeleteAccount}>
                             Delete
                          </button>
                       </div>
                    </div>

                 </div>
             </div>
          </div>

          {/* Right Column Cards */}
          <div className="space-y-6">
             
             {/* Account Overview */}
             <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6">
                <h3 className="text-[13px] font-bold text-slate-800 mb-6">Account Overview</h3>
                
                <div className="flex items-center gap-4 mb-6">
                   <div className="w-12 h-12 rounded-full overflow-hidden bg-slate-200 shrink-0 flex items-center justify-center text-slate-500 font-bold text-xl bg-gradient-to-br from-emerald-100 to-teal-50">
                      {userName.charAt(0).toUpperCase()}
                   </div>
                   <div>
                      <h4 className="text-[14px] font-bold text-slate-800 leading-none mb-1.5">{userName}</h4>
                      <p className="text-[11px] font-medium text-slate-500">{userName.toLowerCase().replace(/\s+/g, '')}@example.com</p>
                   </div>
                </div>

                <div className="space-y-4 mb-6">
                   <div>
                      <p className="text-[10px] font-medium text-slate-500 mb-1">Member since</p>
                      <h4 className="text-[12px] font-bold text-slate-700">{joinDate}</h4>
                   </div>
                   <div>
                      <p className="text-[10px] font-medium text-slate-500 mb-1">Plan</p>
                      <span className="bg-[#f0fdf4] text-emerald-700 border border-[#dcfce7] text-[10px] font-bold px-2 py-0.5 rounded-md inline-block">Free Plan</span>
                   </div>
                </div>

             </div>

             {/* Need Help */}
             <div className="bg-[#F8FAFC] rounded-2xl border border-slate-100 p-6 flex flex-col items-center text-center">
                <div className="w-12 h-12 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center mb-4">
                   <Headset className="w-6 h-6" />
                </div>
                <h3 className="text-[13px] font-bold text-slate-800 mb-2 leading-tight">Need Help?</h3>
                <p className="text-[10px] font-medium text-slate-500 mb-6 leading-relaxed">
                   If you&apos;re facing any issues or have questions, we&apos;re here to help.
                </p>
                <Link href="/support" className="bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 text-[11px] font-bold py-2 px-4 rounded-lg flex items-center justify-center gap-1.5 transition-colors shadow-sm">
                   Contact Support <ChevronRight className="w-3 h-3 text-slate-400" />
                </Link>
             </div>
          </div>
       </div>

    </div>
  )
}
