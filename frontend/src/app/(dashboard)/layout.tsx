"use client"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { useState } from "react"
import { ThemeToggle } from "@/components/ThemeToggle"
import UserProfile from "./UserProfile"
import { Shield, Home, Search, History, Settings, Bell, Bookmark, BarChart3, HelpCircle, User, Moon, Sun, ChevronDown, Users, ChevronRight, Headset, Menu, X, Heart } from "lucide-react"

// A custom Lotus SVG icon that perfectly matches the logo style
const LotusIcon = ({ className }: { className?: string }) => (
  <svg viewBox="0 0 24 24" fill="currentColor" className={className} xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C12 2 10 6 10 10C10 14 12 18 12 18C12 18 14 14 14 10C14 6 12 2 12 2Z" opacity="0.6"/>
    <path d="M12 22C12 22 16 19 19 15C22 11 22 7 22 7C22 7 18 8 14 11C11.5 12.8 12 22 12 22Z" opacity="0.8"/>
    <path d="M12 22C12 22 8 19 5 15C2 11 2 7 2 7C2 7 6 8 10 11C12.5 12.8 12 22 12 22Z" />
  </svg>
)

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [isDesktopSidebarCollapsed, setIsDesktopSidebarCollapsed] = useState(false)
  const [isNotificationSlidebarOpen, setIsNotificationSlidebarOpen] = useState(false)
  const [hasNotifications, setHasNotifications] = useState(false)

  const navLinks: { name: string; href: string; icon: any; badge?: string | number }[] = [
    { name: "Dashboard", href: "/dashboard", icon: Home },
    { name: "Analyze Content", href: "/analyze-reel", icon: Search },
    { name: "History", href: "/history", icon: History },
    { name: "Alerts", href: "/alerts", icon: Bell },
    { name: "Saved", href: "/saved", icon: Bookmark },
    { name: "Notification Center", href: "/notifications", icon: Bell },
    { name: "Universal Harmony", href: "/peace-quotes", icon: Heart },
  ]

  const bottomLinks = [
    { name: "Settings", href: "/settings", icon: Settings },
    { name: "Help & Support", href: "/support", icon: HelpCircle },
  ]

  return (
    <div className="flex min-h-screen bg-slate-50 dark:bg-[#f4f7f5] transition-colors duration-0 relative overflow-hidden">
      {/* NSA Grid overlay (only visible in dark mode) */}
      <div className="absolute inset-0 z-0 hidden dark:block opacity-[0.15] pointer-events-none bg-[linear-gradient(to_right,rgba(16,185,129,0.5)_1px,transparent_1px),linear-gradient(to_bottom,rgba(16,185,129,0.5)_1px,transparent_1px)] bg-[size:40px_40px]">
         <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_0%,#f4f7f5_100%)]"></div>
      </div>
      {/* Mobile Sidebar Overlay */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-slate-900/50 z-40 md:hidden"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Sidebar Navigation */}
      <aside className={`fixed inset-y-0 left-0 z-50 bg-white dark:bg-white/80 dark:backdrop-blur-md border-r border-slate-100 dark:border-emerald-100 flex flex-col transform transition-all duration-300 md:relative md:translate-x-0 ${isDesktopSidebarCollapsed ? 'w-[88px]' : 'w-[280px]'} ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className={`h-[88px] flex items-center ${isDesktopSidebarCollapsed ? 'justify-center px-0' : 'justify-between px-8'} shrink-0`}>
          <Link className="flex flex-col justify-center" href="/">
             <div className="flex items-center gap-2">
                <LotusIcon className="w-7 h-7 text-emerald-600" />
                {!isDesktopSidebarCollapsed && (
                  <span className="font-bold text-[22px] tracking-tight text-slate-800 dark:text-emerald-950 font-serif">
                    Sukoon AI
                  </span>
                )}
             </div>
             {!isDesktopSidebarCollapsed && <span className="text-[10px] text-slate-500 dark:text-emerald-700/80 font-medium tracking-wide mt-0.5 ml-9">Verified Peace. Digital Harmony.</span>}
          </Link>
          <button aria-label="Close sidebar" className="md:hidden p-1 text-slate-400" onClick={() => setIsSidebarOpen(false)}>
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Desktop Toggle Button */}
        <div className={`hidden md:flex border-y border-slate-50 shrink-0 ${isDesktopSidebarCollapsed ? 'justify-center' : 'justify-center'} py-2 bg-slate-50/50`}>
           <button 
             aria-label="Toggle sidebar"
             className="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-white rounded-lg transition-all w-full flex justify-center mx-4" 
             onClick={() => setIsDesktopSidebarCollapsed(!isDesktopSidebarCollapsed)}
           >
             <Menu className="w-4 h-4" />
           </button>
        </div>

        <nav className="flex-1 px-4 py-8 space-y-1 overflow-y-auto">
          {navLinks.map((link) => {
            const isActive = pathname === link.href
            return (
              <Link 
                key={link.name} 
                href={link.href} 
                className={`flex items-center ${isDesktopSidebarCollapsed ? 'justify-center' : 'justify-between'} px-4 py-3 rounded-xl transition-colors ${
                  isActive 
                    ? 'bg-emerald-50 dark:bg-emerald-100 text-emerald-700 dark:text-emerald-800' 
                    : 'text-slate-600 dark:text-emerald-700 hover:bg-slate-50 dark:hover:bg-emerald-50/50 hover:text-slate-900 dark:hover:text-emerald-900'
                }`}
                title={isDesktopSidebarCollapsed ? link.name : undefined}
              >
                <div className={`flex items-center ${isDesktopSidebarCollapsed ? 'justify-center' : 'gap-3'}`}>
                  <link.icon className="w-4 h-4 stroke-[2]" />
                  {!isDesktopSidebarCollapsed && <span className="font-semibold text-[13px]">{link.name}</span>}
                </div>
                {!isDesktopSidebarCollapsed && link.badge && (
                  <div className="w-5 h-5 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center text-[10px] font-bold">
                    {link.badge}
                  </div>
                )}
              </Link>
            )
          })}
          
          <div className="pt-6 pb-2"></div>
          
          {bottomLinks.map((link) => {
            const isActive = pathname === link.href
            return (
              <Link 
                key={link.name} 
                href={link.href} 
                className={`flex items-center ${isDesktopSidebarCollapsed ? 'justify-center' : 'gap-3'} px-4 py-3 rounded-xl transition-colors ${
                  isActive 
                    ? 'bg-emerald-50 dark:bg-emerald-100 text-emerald-700 dark:text-emerald-800' 
                    : 'text-slate-600 dark:text-emerald-700 hover:bg-slate-50 dark:hover:bg-emerald-50/50 hover:text-slate-900 dark:hover:text-emerald-900'
                }`}
                title={isDesktopSidebarCollapsed ? link.name : undefined}
              >
                <link.icon className="w-4 h-4 stroke-[2]" />
                {!isDesktopSidebarCollapsed && <span className="font-semibold text-[13px]">{link.name}</span>}
              </Link>
            )
          })}
        </nav>
        
        {/* Bottom CTA Card */}
        {!isDesktopSidebarCollapsed && (
          <div className="p-4 shrink-0 pb-6">
             <div className="rounded-2xl relative overflow-hidden flex flex-col items-center">
                 <img src="/uploaded_quote.png" alt="Inspirational Quote" className="w-full h-auto object-contain rounded-xl mix-blend-multiply border border-slate-100" />
             </div>
          </div>
        )}
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden relative w-full z-10">
        <header className="h-[88px] flex items-center justify-between gap-6 md:gap-10 px-4 md:px-8 bg-transparent shrink-0">
          
          <div className="flex items-center gap-4 flex-1">
            <button aria-label="Open sidebar" className="md:hidden p-2 text-slate-600 bg-white border border-slate-200 rounded-xl shadow-sm" onClick={() => setIsSidebarOpen(true)}>
              <Menu className="w-5 h-5" />
            </button>
            {/* Top Search Bar (Hidden on mobile) */}
            <div className="hidden md:block w-full max-w-[400px]">
               <div className="relative">
                  <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 dark:text-emerald-600/60" />
                  <input 
                    type="text" 

                    placeholder="Search anything..." 
                    className="w-full h-11 pl-11 pr-12 bg-white dark:bg-white border border-slate-200 dark:border-emerald-200 rounded-xl text-sm outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-all placeholder:text-slate-400 dark:placeholder:text-emerald-600/50 font-medium text-slate-700 dark:text-emerald-950 shadow-sm dark:shadow-emerald-900/5"
                  />
                  <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center justify-center bg-slate-50 dark:bg-emerald-50 border border-slate-200 dark:border-emerald-200 rounded text-[10px] text-slate-500 dark:text-emerald-700 px-1.5 py-0.5 font-bold">
                     ⌘ /
                  </div>
               </div>
            </div>
          </div>
          
          <div className="flex items-center gap-2 md:gap-5">
            <ThemeToggle />
            <button 
               className="p-2 text-slate-400 hover:text-slate-600 transition-colors relative"
               onClick={() => setIsNotificationSlidebarOpen(true)}
            >
              <Bell className="w-5 h-5" />
              {hasNotifications && (
                 <div className="absolute top-1 right-2 w-2 h-2 rounded-full bg-red-500 ring-4 ring-[#F8FAFC]"></div>
              )}
            </button>
            
            <div className="hidden md:block h-8 w-px bg-slate-200 mx-2"></div>
            
            <UserProfile />
          </div>
        </header>
        
        <div className="flex-1 overflow-auto p-4 md:p-8 pt-0">
          {children}
        </div>
      </main>

      {/* Notification Slidebar */}
      {isNotificationSlidebarOpen && (
        <div 
          className="fixed inset-0 bg-slate-900/20 z-50 transition-opacity backdrop-blur-sm"
          onClick={() => setIsNotificationSlidebarOpen(false)}
        />
      )}
      <div className={`fixed inset-y-0 right-0 z-50 w-full md:w-[380px] bg-white shadow-2xl border-l border-slate-100 flex flex-col transform transition-transform duration-300 ${isNotificationSlidebarOpen ? 'translate-x-0' : 'translate-x-full'}`}>
         <div className="h-[88px] flex items-center justify-between px-6 border-b border-slate-50 shrink-0">
            <div>
               <h3 className="font-bold text-lg text-slate-800 font-serif">Notifications</h3>
               <p className="text-[11px] text-slate-500 font-medium">You have 0 unread alerts.</p>
            </div>
            <button aria-label="Close notifications" className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-50 rounded-full transition-colors" onClick={() => setIsNotificationSlidebarOpen(false)}>
              <X className="w-5 h-5" />
            </button>
         </div>
         <div className="flex-1 overflow-y-auto p-6 space-y-4">
            <div className="flex flex-col items-center justify-center h-full text-center p-6 opacity-50">
               <Bell className="w-12 h-12 text-slate-300 mb-4" />
               <h4 className="text-sm font-bold text-slate-700 mb-1">No new notifications</h4>
               <p className="text-xs text-slate-500">You're all caught up! We'll alert you here when there are updates.</p>
            </div>
         </div>
         <div className="p-4 border-t border-slate-50 shrink-0">
            <button 
               onClick={() => setHasNotifications(false)}
               disabled={!hasNotifications}
               className={`w-full py-3 font-bold text-sm rounded-xl transition-colors ${!hasNotifications ? 'bg-slate-50 text-slate-400 cursor-default' : 'bg-slate-50 hover:bg-slate-100 text-slate-700'}`}>
               {!hasNotifications ? 'Marked as read' : 'Mark all as read'}
            </button>
         </div>
      </div>
      {/* Floating Action Button (Support) */}
      <Link href="/support" className="fixed bottom-6 right-6 z-40 flex items-center justify-center w-12 h-12 bg-emerald-600 text-white rounded-full shadow-lg shadow-emerald-500/30 hover:bg-emerald-700 hover:scale-110 transition-all duration-300 group">
         <Headset className="w-5 h-5" />
         {/* Tooltip */}
         <div className="absolute right-full mr-3 top-1/2 -translate-y-1/2 px-3 py-1.5 bg-slate-800 text-white text-[11px] font-bold rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
            Get Help & Support
         </div>
         {/* Ping animation */}
         <div className="absolute inset-0 rounded-full border-2 border-emerald-500 animate-ping opacity-20"></div>
      </Link>
    </div>
  )
}
