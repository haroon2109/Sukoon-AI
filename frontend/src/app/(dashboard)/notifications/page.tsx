"use client"
import { useState } from "react"
import { Bell, Check, CheckCircle2, AlertTriangle, TrendingUp, Users, ShieldCheck, Star, MoreVertical, ChevronLeft, ChevronRight } from "lucide-react"

export default function NotificationsPage() {
  const [activeTab, setActiveTab] = useState("all")
  const [isAllRead, setIsAllRead] = useState(false)
  const [preferences, setPreferences] = useState({
    verificationUpdates: true,
    misinformationAlerts: true,
    reportsInsights: true,
    communityUpdates: true
  })
  
  const togglePreference = (key: keyof typeof preferences) => {
    setPreferences(prev => ({ ...prev, [key]: !prev[key] }))
  }

  const allNotifications = [
    {
      id: 1,
      type: 'alerts',
      title: "Viral False Claim Detected",
      message: "A trending video regarding recent elections has been marked as FALSE. See the truth card.",
      time: "2 hours ago",
      icon: AlertTriangle,
      iconColor: "text-red-500",
      bgColor: "bg-red-50",
    },
    {
      id: 2,
      type: 'alerts',
      title: "Hate Speech Warning",
      message: "High volume of hate speech detected in a newly verified reel.",
      time: "5 hours ago",
      icon: ShieldCheck,
      iconColor: "text-amber-500",
      bgColor: "bg-amber-50",
    },
    {
      id: 3,
      type: 'updates',
      title: "Weekly Peace Report",
      message: "Your weekly verification report is ready! You have helped stop 45 rumors this week.",
      time: "1 day ago",
      icon: TrendingUp,
      iconColor: "text-emerald-600",
      bgColor: "bg-emerald-50",
    },
    {
      id: 4,
      type: 'updates',
      title: "New Feature Available",
      message: "You can now verify text articles alongside images and videos.",
      time: "2 days ago",
      icon: Star,
      iconColor: "text-blue-500",
      bgColor: "bg-blue-50",
    },
    {
      id: 5,
      type: 'updates',
      title: "Community Milestone",
      message: "Sukoon AI just crossed 50K verified claims. Thanks for being a peace builder!",
      time: "3 days ago",
      icon: Users,
      iconColor: "text-purple-500",
      bgColor: "bg-purple-50",
    }
  ]

  const displayedNotifications = allNotifications.filter(n => {
    if (activeTab === 'all' || activeTab === 'unread') return true;
    return n.type === activeTab;
  })

  const handleMarkAllAsRead = () => {
    setIsAllRead(true)
  }

  return (
    <div className="max-w-[1400px] mx-auto space-y-6 pb-10">
       
       {/* Header Section */}
       <div className="flex items-start justify-between mt-6 mb-8">
          <div className="flex items-center gap-4">
             <div className="w-12 h-12 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
                <Bell className="w-6 h-6 stroke-[2]" />
             </div>
             <div>
                <h1 className="text-2xl font-bold text-slate-800 font-serif mb-1">Notification Center</h1>
                <p className="text-slate-500 font-medium text-[13px]">
                   All important updates, alerts and activities in one place.
                </p>
             </div>
          </div>
          <button 
             onClick={handleMarkAllAsRead}
             disabled={isAllRead}
             className={`flex items-center gap-1.5 text-[12px] font-bold transition-colors mt-2 ${isAllRead ? 'text-slate-400 cursor-default' : 'text-emerald-600 hover:text-emerald-700'}`}>
             <Check className="w-4 h-4" /> <Check className="w-4 h-4 -ml-2.5" /> {isAllRead ? 'Marked as read' : 'Mark all as read'}
          </button>
       </div>

       <div className="grid grid-cols-1 lg:grid-cols-[1fr_340px] gap-6">
          
          {/* Main Content Area (Left Column) */}
          <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6 flex flex-col min-h-[600px]">
             
             {/* Tabs Bar */}
             <div className="flex items-center gap-3 mb-6 pb-6 border-b border-slate-100 overflow-x-auto no-scrollbar">
                <button 
                  onClick={() => setActiveTab("all")}
                  className={`flex items-center gap-2 px-4 py-2 rounded-full text-[12px] font-bold whitespace-nowrap shrink-0 transition-colors ${activeTab === 'all' ? 'bg-emerald-50 border border-emerald-100 text-emerald-700' : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 hover:text-slate-900'}`}>
                   All <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[9px] ${activeTab === 'all' ? 'bg-emerald-600 text-white' : 'bg-slate-100 text-slate-500'}`}>{isAllRead ? 0 : 5}</span>
                </button>
                <button 
                  onClick={() => setActiveTab("unread")}
                  className={`flex items-center gap-2 px-4 py-2 rounded-full text-[12px] font-bold whitespace-nowrap shrink-0 transition-colors ${activeTab === 'unread' ? 'bg-emerald-50 border border-emerald-100 text-emerald-700' : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 hover:text-slate-900'}`}>
                   Unread <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[9px] ${activeTab === 'unread' ? 'bg-emerald-600 text-white' : 'bg-slate-100 text-slate-500'}`}>{isAllRead ? 0 : 5}</span>
                </button>
                <button 
                  onClick={() => setActiveTab("alerts")}
                  className={`flex items-center gap-2 px-4 py-2 rounded-full text-[12px] font-bold whitespace-nowrap shrink-0 transition-colors ${activeTab === 'alerts' ? 'bg-emerald-50 border border-emerald-100 text-emerald-700' : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 hover:text-slate-900'}`}>
                   Alerts <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[9px] ${activeTab === 'alerts' ? 'bg-emerald-600 text-white' : 'bg-slate-100 text-slate-500'}`}>{isAllRead ? 0 : 2}</span>
                </button>
                <button 
                  onClick={() => setActiveTab("updates")}
                  className={`flex items-center gap-2 px-4 py-2 rounded-full text-[12px] font-bold whitespace-nowrap shrink-0 transition-colors ${activeTab === 'updates' ? 'bg-emerald-50 border border-emerald-100 text-emerald-700' : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 hover:text-slate-900'}`}>
                   Updates <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[9px] ${activeTab === 'updates' ? 'bg-emerald-600 text-white' : 'bg-slate-100 text-slate-500'}`}>{isAllRead ? 0 : 3}</span>
                </button>
                <button 
                  onClick={() => setActiveTab("community")}
                  className={`flex items-center gap-2 px-4 py-2 rounded-full text-[12px] font-bold whitespace-nowrap shrink-0 transition-colors ${activeTab === 'community' ? 'bg-emerald-50 border border-emerald-100 text-emerald-700' : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 hover:text-slate-900'}`}>
                   Community <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[9px] ${activeTab === 'community' ? 'bg-emerald-600 text-white' : 'bg-slate-100 text-slate-500'}`}>0</span>
                </button>
             </div>

             {/* Notification List */}
             <div className="space-y-0 flex-1">
                {isAllRead || (activeTab === 'community') ? (
                  <div className="flex flex-col items-center justify-center py-12 text-center opacity-70">
                     <img src="/quiet_mountain_empty.png" alt="Empty Notifications" className="w-48 h-48 object-contain mb-6 rounded-3xl shadow-sm mix-blend-multiply" />
                     <h4 className="text-lg font-bold text-slate-700 mb-2">No new notifications</h4>
                     <p className="text-sm text-slate-500 max-w-sm leading-relaxed">You're all caught up! Enjoy the quiet view from the top while we monitor for important updates.</p>
                  </div>
                ) : (
                  <div className="flex flex-col">
                    {displayedNotifications.map((notification, idx) => (
                      <div key={notification.id} className={`flex items-start gap-4 p-5 transition-colors border-b border-slate-50 hover:bg-slate-50 ${idx === 0 ? 'rounded-t-2xl' : ''}`}>
                         <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${notification.bgColor} ${notification.iconColor}`}>
                            <notification.icon className="w-5 h-5" />
                         </div>
                         <div className="flex-1">
                            <div className="flex items-center justify-between mb-1">
                               <h4 className="text-sm font-bold text-slate-800">{notification.title}</h4>
                               <span className="text-[10px] font-bold text-slate-400">{notification.time}</span>
                            </div>
                            <p className="text-xs font-medium text-slate-600 leading-relaxed mb-2">{notification.message}</p>
                            <div className="flex items-center gap-3">
                               <button className="text-[10px] font-bold text-emerald-600 hover:text-emerald-700">View Details</button>
                               <span className="w-1 h-1 rounded-full bg-slate-300"></span>
                               <button className="text-[10px] font-bold text-slate-500 hover:text-slate-700">Dismiss</button>
                            </div>
                         </div>
                         <div className="w-2 h-2 rounded-full bg-emerald-500 mt-1.5 shrink-0"></div>
                      </div>
                    ))}
                  </div>
                )}
             </div>
          </div>

          {/* Right Column Cards */}
          <div className="space-y-6">
             
             {/* Notification Preferences */}
             <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-6">
                <h3 className="text-[14px] font-bold text-slate-800 mb-1">Notification Preferences</h3>
                <p className="text-[11px] text-slate-500 font-medium mb-6">Choose what you want to be notified about.</p>

                <div className="space-y-5">
                   
                   {/* Option 1 */}
                   <div className="flex items-center justify-between">
                      <div className="flex items-start gap-3">
                         <div className="w-8 h-8 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0 border border-emerald-100">
                            <ShieldCheck className="w-4 h-4" />
                         </div>
                         <div>
                            <h4 className="text-[12px] font-bold text-slate-800 mb-0.5">Verification Updates</h4>
                            <p className="text-[10px] text-slate-500 font-medium">Get notified when your content is verified.</p>
                         </div>
                      </div>
                      <div 
                        onClick={() => togglePreference('verificationUpdates')}
                        className={`w-8 h-4 rounded-full relative cursor-pointer ml-4 shrink-0 transition-colors ${preferences.verificationUpdates ? 'bg-emerald-600' : 'bg-slate-300'}`}>
                         <div className={`absolute top-0.5 w-3 h-3 bg-white rounded-full shadow-sm transition-all ${preferences.verificationUpdates ? 'right-0.5' : 'left-0.5'}`}></div>
                      </div>
                   </div>

                   {/* Option 2 */}
                   <div className="flex items-center justify-between">
                      <div className="flex items-start gap-3">
                         <div className="w-8 h-8 rounded-full bg-orange-50 text-orange-600 flex items-center justify-center shrink-0 border border-orange-100">
                            <AlertTriangle className="w-4 h-4" />
                         </div>
                         <div>
                            <h4 className="text-[12px] font-bold text-slate-800 mb-0.5">Misinformation Alerts</h4>
                            <p className="text-[10px] text-slate-500 font-medium">Receive alerts about trending misinformation.</p>
                         </div>
                      </div>
                      <div 
                        onClick={() => togglePreference('misinformationAlerts')}
                        className={`w-8 h-4 rounded-full relative cursor-pointer ml-4 shrink-0 transition-colors ${preferences.misinformationAlerts ? 'bg-emerald-600' : 'bg-slate-300'}`}>
                         <div className={`absolute top-0.5 w-3 h-3 bg-white rounded-full shadow-sm transition-all ${preferences.misinformationAlerts ? 'right-0.5' : 'left-0.5'}`}></div>
                      </div>
                   </div>

                   {/* Option 3 */}
                   <div className="flex items-center justify-between">
                      <div className="flex items-start gap-3">
                         <div className="w-8 h-8 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center shrink-0 border border-blue-100">
                            <TrendingUp className="w-4 h-4" />
                         </div>
                         <div>
                            <h4 className="text-[12px] font-bold text-slate-800 mb-0.5">Reports & Insights</h4>
                            <p className="text-[10px] text-slate-500 font-medium">Weekly reports and insights from Sukoon AI.</p>
                         </div>
                      </div>
                      <div 
                        onClick={() => togglePreference('reportsInsights')}
                        className={`w-8 h-4 rounded-full relative cursor-pointer ml-4 shrink-0 transition-colors ${preferences.reportsInsights ? 'bg-emerald-600' : 'bg-slate-300'}`}>
                         <div className={`absolute top-0.5 w-3 h-3 bg-white rounded-full shadow-sm transition-all ${preferences.reportsInsights ? 'right-0.5' : 'left-0.5'}`}></div>
                      </div>
                   </div>

                   {/* Option 4 */}
                   <div className="flex items-center justify-between">
                      <div className="flex items-start gap-3">
                         <div className="w-8 h-8 rounded-full bg-purple-50 text-purple-600 flex items-center justify-center shrink-0 border border-purple-100">
                            <Users className="w-4 h-4" />
                         </div>
                         <div>
                            <h4 className="text-[12px] font-bold text-slate-800 mb-0.5">Community Updates</h4>
                            <p className="text-[10px] text-slate-500 font-medium">Updates on community actions and contributions.</p>
                         </div>
                      </div>
                      <div 
                        onClick={() => togglePreference('communityUpdates')}
                        className={`w-8 h-4 rounded-full relative cursor-pointer ml-4 shrink-0 transition-colors ${preferences.communityUpdates ? 'bg-emerald-600' : 'bg-slate-300'}`}>
                         <div className={`absolute top-0.5 w-3 h-3 bg-white rounded-full shadow-sm transition-all ${preferences.communityUpdates ? 'right-0.5' : 'left-0.5'}`}></div>
                      </div>
                   </div>

                </div>


             </div>

             {/* Promotional Card */}
             <div className="bg-[#f8fafc] rounded-2xl border border-[#f1f5f9] p-6 text-center flex flex-col items-center">
                <div className="relative w-32 h-24 mb-4 flex items-center justify-center">
                   {/* Using smart_alert_track.png as a placeholder for the envelope illustration */}
                   <img src="/smart_alert_track.png" alt="Never miss what matters" className="w-full h-full object-contain mix-blend-multiply" />
                   <div className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-red-500 text-white flex items-center justify-center text-[9px] font-bold border-2 border-white">1</div>
                </div>
                <h3 className="text-[14px] font-bold text-emerald-800 mb-2">Never miss what matters.</h3>
                <p className="text-[11px] text-slate-500 font-medium px-2 leading-relaxed">
                   We'll keep you updated so you can help build a safer digital world.
                </p>
             </div>

          </div>
       </div>

    </div>
  )
}
