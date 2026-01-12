
import React from 'react';
import { NAVIGATION_ITEMS } from '../constants';
import { AppType } from '../types';
import { Terminal, Settings, Bell, Search, Zap } from 'lucide-react';
import { UserProfile } from "../types";

interface LayoutProps {
  children: React.ReactNode;
  activeTab?: AppType;
  setActiveTab?: (tab: AppType) => void;
  variant?: "app" | "auth";
  user?: UserProfile;
  onLogout?: () => void;
}

const Layout: React.FC<LayoutProps> = ({ children, activeTab, setActiveTab, variant = "app", user, onLogout }) => {
  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">
      {variant === "app" && (
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col z-20">
        <div className="p-6 flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-lg text-white">
            <Zap size={20} />
          </div>
          <span className="font-bold text-xl tracking-tight">InstantAI</span>
        </div>

        <nav className="flex-1 mt-4 px-3 space-y-1">
          {NAVIGATION_ITEMS.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                activeTab === item.id 
                  ? 'bg-blue-50 text-blue-600' 
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              }`}
            >
              {item.icon}
              {item.label}
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-slate-100 space-y-1">
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-slate-600 hover:bg-slate-50">
            <Settings size={20} />
            Settings
          </button>
          <div onClick={() => setActiveTab?.(AppType.PROFILE)} className="flex items-center gap-3 px-4 py-3 rounded-xl cursor-pointer hover:bg-slate-50 transition-all">
            <div className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center text-xs font-bold">
              JD
            </div>
            <div className="flex flex-col">
              <span className="text-xs font-semibold">Jane Doe</span>
              <span className="text-[10px] text-slate-400 uppercase tracking-widest">
                Admin
              </span>
            </div>
          </div>
        </div>
      </aside>
      )}

      {/* Main Content */}
      <main className="flex-1 flex flex-col relative overflow-hidden">
        {variant === "app" && (
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 z-10">
          <div className="flex items-center gap-4 flex-1">
             <div className="relative max-w-md w-full">
               <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
               <input 
                 type="text" 
                 placeholder="Search insights, metrics, or apps..."
                 className="w-full bg-slate-100 border-none rounded-full py-2 pl-10 pr-4 text-sm focus:ring-2 focus:ring-blue-500 transition-all outline-none"
               />
             </div>
          </div>
          <div className="flex items-center gap-3">
            <button className="p-2 text-slate-500 hover:bg-slate-100 rounded-lg transition-colors">
              <Bell size={20} />
            </button>
            <button className="flex items-center gap-2 bg-slate-900 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-slate-800 transition-all">
              <Terminal size={16} />
              New Inquiry
            </button>
          </div>
        </header>
        )}

        <div className={`flex-1 overflow-y-auto ${
            variant === "auth"
            ? "flex items-center justify-center bg-slate-50"
            : "bg-slate-50/50"
        }`}>
            {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;
