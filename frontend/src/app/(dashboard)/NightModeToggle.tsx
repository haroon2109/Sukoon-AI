"use client"

import { useState, useEffect } from "react"
import { Sun, Moon } from "lucide-react"

export default function NightModeToggle() {
  const [isDark, setIsDark] = useState(false)

  useEffect(() => {
    // Check if user has previously set dark mode
    if (localStorage.getItem('theme') === 'dark') {
      setIsDark(true)
      document.documentElement.classList.add('dark-theme')
    }
  }, [])

  const toggleTheme = () => {
    if (isDark) {
      document.documentElement.classList.remove('dark-theme')
      localStorage.setItem('theme', 'light')
      setIsDark(false)
    } else {
      document.documentElement.classList.add('dark-theme')
      localStorage.setItem('theme', 'dark')
      setIsDark(true)
    }
  }

  return (
    <>
      <button 
        onClick={toggleTheme}
        className="p-2 text-slate-400 hover:text-slate-600 transition-colors"
        title="Toggle Night Mode"
      >
        {isDark ? <Moon className="w-5 h-5 text-emerald-500" /> : <Sun className="w-5 h-5" />}
      </button>


    </>
  )
}
