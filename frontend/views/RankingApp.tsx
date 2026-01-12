
import React, { useState } from 'react';
import { 
  BarChart3, 
  Settings2, 
  Search, 
  ChevronDown, 
  Sparkles, 
  ArrowUp, 
  ArrowDown, 
  TrendingUp,
  Target,
  MoreVertical,
  HelpCircle
} from 'lucide-react';

const ENTITIES = [
  { id: 1, name: 'Mumbai Hub', score: 94.2, rank: 1, trend: '+2', metrics: { speed: 98, quality: 92, cost: 91 } },
  { id: 2, name: 'Delhi South', score: 91.8, rank: 2, trend: '-1', metrics: { speed: 88, quality: 95, cost: 93 } },
  { id: 3, name: 'Bengaluru East', score: 88.5, rank: 3, trend: '+4', metrics: { speed: 92, quality: 84, cost: 89 } },
  { id: 4, name: 'Chennai Central', score: 85.1, rank: 4, trend: '0', metrics: { speed: 82, quality: 88, cost: 85 } },
  { id: 5, name: 'Kolkata Port', score: 82.3, rank: 5, trend: '-3', metrics: { speed: 75, quality: 89, cost: 83 } },
];

const RankingApp: React.FC = () => {
  const [activeTab, setActiveTab] = useState('distribution');

  return (
    <div className="p-8 space-y-8 animate-in slide-in-from-bottom-4 duration-500">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Rating & Ranking</h1>
          <p className="text-slate-500 mt-1">Universal comparison engine for business entities.</p>
        </div>
        <div className="flex gap-3">
          <button className="bg-white border border-slate-200 px-4 py-2 rounded-xl text-sm font-semibold flex items-center gap-2 hover:bg-slate-50">
            <Settings2 size={16} /> Configure Rubric
          </button>
          <button className="bg-blue-600 text-white px-4 py-2 rounded-xl text-sm font-semibold flex items-center gap-2 hover:bg-blue-700 shadow-lg shadow-blue-100">
            <Sparkles size={16} /> Agentic Enrichment
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Rubric Config Panel */}
        <div className="lg:col-span-1 bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <h3 className="font-bold text-sm flex items-center gap-2">
            <Target size={18} className="text-blue-600" /> Scoring Weights
          </h3>
          <div className="space-y-4">
            {[
              { label: 'Speed (Turnaround Time)', weight: 40, color: 'bg-blue-500' },
              { label: 'Quality (Audit Score)', weight: 35, color: 'bg-emerald-500' },
              { label: 'Efficiency (Cost/Unit)', weight: 25, color: 'bg-amber-500' },
            ].map(w => (
              <div key={w.label} className="space-y-2">
                <div className="flex justify-between text-xs font-semibold">
                  <span className="text-slate-600">{w.label}</span>
                  <span>{w.weight}%</span>
                </div>
                <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                  <div className={`h-full ${w.color}`} style={{ width: `${w.weight}%` }}></div>
                </div>
              </div>
            ))}
          </div>
          <div className="pt-4 border-t border-slate-100">
             <div className="text-[10px] uppercase font-bold text-slate-400 mb-2">Filters Applied</div>
             <div className="flex flex-wrap gap-2">
               <span className="px-2 py-1 bg-slate-50 rounded text-[10px] font-bold border border-slate-100">REGION: INDIA</span>
               <span className="px-2 py-1 bg-slate-50 rounded text-[10px] font-bold border border-slate-100">TIME: LTM</span>
             </div>
          </div>
        </div>

        {/* Ranking List */}
        <div className="lg:col-span-3 space-y-4">
          <div className="bg-white border border-slate-200 rounded-3xl shadow-sm overflow-hidden">
             <div className="p-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={14} />
                  <input 
                    type="text" 
                    placeholder="Search entities..." 
                    className="bg-white border border-slate-200 rounded-lg py-1.5 pl-8 pr-4 text-xs focus:ring-1 focus:ring-blue-500 outline-none w-64"
                  />
                </div>
                <div className="flex gap-2">
                   <button className="px-3 py-1.5 text-xs font-medium bg-white border border-slate-200 rounded-lg">All Entities</button>
                   <button className="px-3 py-1.5 text-xs font-medium text-slate-500">Top Performers</button>
                </div>
             </div>
             <div className="overflow-x-auto">
               <table className="w-full text-left">
                 <thead>
                   <tr className="border-b border-slate-100">
                     <th className="px-6 py-4 text-[11px] uppercase tracking-wider text-slate-400 font-bold">Rank</th>
                     <th className="px-6 py-4 text-[11px] uppercase tracking-wider text-slate-400 font-bold">Entity</th>
                     <th className="px-6 py-4 text-[11px] uppercase tracking-wider text-slate-400 font-bold">Total Score</th>
                     <th className="px-6 py-4 text-[11px] uppercase tracking-wider text-slate-400 font-bold">Metric Breakdown</th>
                     <th className="px-6 py-4 text-[11px] uppercase tracking-wider text-slate-400 font-bold text-right">Actions</th>
                   </tr>
                 </thead>
                 <tbody className="divide-y divide-slate-50">
                   {ENTITIES.map((entity) => (
                     <tr key={entity.id} className="hover:bg-slate-50/50 transition-colors group">
                       <td className="px-6 py-4">
                         <div className="flex items-center gap-3">
                           <span className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${
                             entity.rank === 1 ? 'bg-amber-100 text-amber-700' : 
                             entity.rank === 2 ? 'bg-slate-100 text-slate-700' :
                             entity.rank === 3 ? 'bg-orange-100 text-orange-700' : 'bg-slate-50 text-slate-400'
                           }`}>
                             {entity.rank}
                           </span>
                           <div className={`flex items-center text-[10px] font-bold ${
                             entity.trend.startsWith('+') ? 'text-emerald-500' : 
                             entity.trend === '0' ? 'text-slate-300' : 'text-rose-500'
                           }`}>
                             {entity.trend.startsWith('+') ? <ArrowUp size={10} /> : 
                              entity.trend.startsWith('-') ? <ArrowDown size={10} /> : null}
                             {entity.trend !== '0' ? entity.trend : ''}
                           </div>
                         </div>
                       </td>
                       <td className="px-6 py-4">
                         <div className="flex flex-col">
                           <span className="font-bold text-slate-900 group-hover:text-blue-600 transition-colors">{entity.name}</span>
                           <span className="text-[10px] text-slate-400">Hub ID: #BIZ-{entity.id}00X</span>
                         </div>
                       </td>
                       <td className="px-6 py-4">
                         <div className="flex items-center gap-2">
                           <span className="font-bold text-lg">{entity.score}</span>
                           <div className="w-12 h-1 bg-slate-100 rounded-full overflow-hidden">
                             <div className="h-full bg-blue-500" style={{ width: `${entity.score}%` }}></div>
                           </div>
                         </div>
                       </td>
                       <td className="px-6 py-4">
                          <div className="flex gap-4">
                            <div className="flex flex-col">
                              <span className="text-[9px] text-slate-400 font-bold">SPD</span>
                              <span className="text-xs font-semibold">{entity.metrics.speed}</span>
                            </div>
                            <div className="flex flex-col">
                              <span className="text-[9px] text-slate-400 font-bold">QLT</span>
                              <span className="text-xs font-semibold text-emerald-600">{entity.metrics.quality}</span>
                            </div>
                            <div className="flex flex-col">
                              <span className="text-[9px] text-slate-400 font-bold">CST</span>
                              <span className="text-xs font-semibold">{entity.metrics.cost}</span>
                            </div>
                          </div>
                       </td>
                       <td className="px-6 py-4 text-right">
                          <button className="p-2 hover:bg-slate-100 rounded-lg text-slate-400">
                            <MoreVertical size={16} />
                          </button>
                       </td>
                     </tr>
                   ))}
                 </tbody>
               </table>
             </div>
          </div>

          <div className="bg-blue-50/50 border border-blue-100 rounded-3xl p-6 flex gap-4 items-start">
            <div className="bg-blue-600 p-2 rounded-xl text-white">
              <Sparkles size={20} />
            </div>
            <div className="flex-1">
              <h4 className="font-bold text-sm text-blue-900">Why did Mumbai Hub take #1?</h4>
              <p className="text-sm text-blue-700 mt-1 leading-relaxed">
                Mumbai improved their turnaround time by 12% following the implementation of the new sorting algorithm, overcoming a slight dip in quality audit scores from last month.
              </p>
              <div className="mt-4 flex gap-2">
                <button className="px-3 py-1.5 bg-blue-600 text-white rounded-lg text-xs font-bold shadow-lg shadow-blue-200">Investigate Drilldown</button>
                <button className="px-3 py-1.5 bg-white text-blue-600 border border-blue-200 rounded-lg text-xs font-bold">View Improvement Plan</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RankingApp;
