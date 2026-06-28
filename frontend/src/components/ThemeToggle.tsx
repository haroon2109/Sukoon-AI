"use client"

import * as React from "react"
import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"

export function ThemeToggle() {
  const [mounted, setMounted] = React.useState(false)
  const { setTheme, theme, resolvedTheme } = useTheme()

  React.useEffect(() => {
    // eslint-disable-next-line
    setMounted(true)
  }, [])

  if (!mounted) {
    return <div className="hidden sm:flex w-[130px] h-[34px] rounded-full bg-slate-100 border border-slate-200"></div>
  }

  const currentTheme = theme === 'system' ? resolvedTheme : theme;
  const isDark = currentTheme === 'dark';

  const toggleTheme = (e: React.MouseEvent) => {
    const isAppearanceTransition = 'startViewTransition' in document
      && !window.matchMedia('(prefers-reduced-motion: reduce)').matches

    if (!isAppearanceTransition) {
      setTheme(isDark ? 'light' : 'dark')
      return
    }

    const x = e.clientX
    const y = e.clientY
    const endRadius = Math.hypot(
      Math.max(x, innerWidth - x),
      Math.max(y, innerHeight - y)
    )
    // startViewTransition is now supported
    const transition = document.startViewTransition(() => {
      return import('react-dom').then(({ flushSync }) => {
        flushSync(() => {
          setTheme(isDark ? 'light' : 'dark')
        })
      })
    })

    transition.ready.then(() => {
      const clipPath = [
        `circle(0px at ${x}px ${y}px)`,
        `circle(${endRadius}px at ${x}px ${y}px)`
      ]
      document.documentElement.animate(
        {
          clipPath: !isDark ? clipPath : [...clipPath].reverse()
        },
        {
          duration: 600,
          easing: 'cubic-bezier(0.87, 0, 0.13, 1)',
          pseudoElement: !isDark ? '::view-transition-new(root)' : '::view-transition-old(root)'
        }
      )
    })
  }

  return (
    <button 
      onClick={toggleTheme}
      className={`hidden sm:flex px-3 py-1.5 items-center gap-2 rounded-full font-bold text-[11px] transition-all border ${
        isDark 
          ? 'bg-emerald-50 border-emerald-200 text-emerald-700 hover:bg-emerald-100 hover:border-emerald-300 shadow-[0_0_15px_rgba(16,185,129,0.15)]' 
          : 'bg-slate-100 border-slate-200 text-slate-600 hover:bg-slate-200'
      }`}
      title={isDark ? "Switch to standard mode" : "Enable Serene Mode"}
    >
      {isDark ? <Sun className="w-3.5 h-3.5 text-emerald-600" /> : <Moon className="w-3.5 h-3.5" />}
      {isDark ? 'Standard Mode' : 'Serene Mode'}
    </button>
  )
}
