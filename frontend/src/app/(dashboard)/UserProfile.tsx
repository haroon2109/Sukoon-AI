"use client"

import { useState, useEffect, useRef } from "react"
import { ChevronDown, LogOut, Settings, User } from "lucide-react"

export default function UserProfile() {
  const [userName, setUserName] = useState("Aman Verma")
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const storedName = localStorage.getItem('sukoon_name')
    if (storedName) {
      setUserName(storedName)
    }

    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  const handleLogout = async () => {
    const Cookies = (await import('js-cookie')).default
    Cookies.remove('sukoon_token')
    localStorage.removeItem('sukoon_name')
    localStorage.removeItem('sukoon_email')
    window.location.href = "/login"
  }

  return (
    <div className="relative" ref={dropdownRef}>
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-3 hover:bg-slate-50 p-1.5 rounded-full pr-3 transition-colors"
      >
         <div className="w-10 h-10 rounded-full bg-slate-100 overflow-hidden shadow-sm flex items-center justify-center text-slate-500 font-bold text-lg bg-gradient-to-br from-emerald-100 to-teal-50 shrink-0">
            {userName.charAt(0).toUpperCase()}
         </div>
         <div className="flex items-center gap-1.5">
            <span className="text-[13px] font-bold text-slate-800 text-left max-w-[100px] leading-tight">{userName}</span>
            <ChevronDown className={`w-4 h-4 text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
         </div>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-[0_8px_30px_rgb(0,0,0,0.08)] border border-slate-100 py-1 z-50 animate-in fade-in slide-in-from-top-2 duration-200">
          <div className="px-4 py-3 border-b border-slate-50">
            <p className="text-sm font-bold text-slate-800 truncate">{userName}</p>
            <p className="text-[11px] font-medium text-slate-500 mt-0.5">Verified User</p>
          </div>
          
          <div className="py-1">
            <button className="w-full text-left px-4 py-2.5 text-[13px] font-bold text-slate-700 hover:bg-slate-50 hover:text-emerald-600 flex items-center gap-3 transition-colors" onClick={() => window.location.href = '/profile'}>
              <User className="w-4 h-4" /> My Profile
            </button>
            <button className="w-full text-left px-4 py-2.5 text-[13px] font-bold text-slate-700 hover:bg-slate-50 hover:text-emerald-600 flex items-center gap-3 transition-colors" onClick={() => window.location.href = '/settings'}>
              <Settings className="w-4 h-4" /> Account Settings
            </button>
          </div>
          
          <div className="border-t border-slate-50 py-1">
            <button 
              onClick={handleLogout}
              className="w-full text-left px-4 py-2.5 text-[13px] font-bold text-red-600 hover:bg-red-50 flex items-center gap-3 transition-colors"
            >
              <LogOut className="w-4 h-4" /> Log out
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
