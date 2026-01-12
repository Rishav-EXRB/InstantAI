
import React from 'react';
import { MOCK_METRICS } from '../constants';
import { 
  ArrowUpRight, 
  ArrowDownRight, 
  Search, 
  Filter, 
  Download,
  MoreHorizontal,
  PlusCircle,
  Zap,
  TrendingUp,
  AlertTriangle,
  Lightbulb
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';

const data = [
  { name: 'Mon', revenue: 4000, users: 2400 },
  { name: 'Tue', revenue: 3000, users: 1398 },
  { name: 'Wed', revenue: 2000, users: 9800 },
  { name: 'Thu', revenue: 2780, users: 3908 },
  { name: 'Fri', revenue: 1890, users: 4800 },
  { name: 'Sat', revenue: 2390, users: 3800 },
  { name: 'Sun', revenue: 3490, users: 4300 },
];

const Dashboard: React.FC = () => {
  return (
    <div className="p-8 space-y-8 animate-in fade-in duration-500">
      <div className="flex items-end justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Executive Brief</h1>
          <p className="text-slate-500 mt-1">What changed in your business today and why.</p>
        </div>
        <div className="flex gap-2">
          <button className="flex items-center gap-2 px-4 py-2 border border-slate-200 rounded-lg text-sm font-medium hover:bg-white transition-all">
            <Download size={16} /> Export
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 shadow-md shadow-blue-200 transition-all">
            <Filter size={16} /> Filters
          </button>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {MOCK_METRICS.map((metric) => (
          <div key={metric.id} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-all group cursor-pointer">
            <div className="flex justify-between items-start mb-4">
              <span className="text-sm font-medium text-slate-500">{metric.name}</span>
              <button className="p-1 hover:bg-slate-50 rounded text-slate-400">
                <MoreHorizontal size={16} />
              </button>
            </div>
            <div className="flex items-end gap-3">
              <span className="text-2xl font-bold">{typeof metric.value === 'number' && metric.id === 'm1' ? `$${(metric.value / 1000000).toFixed(1)}M` : metric.value}{metric.id === 'm2' || metric.id === 'm3' || metric.id === 'm4' ? '%' : ''}</span>
              <div className={`flex items-center text-xs font-bold mb-1 px-1.5 py-0.5 rounded-full ${
                metric.trend === 'up' ? 'text-emerald-600 bg-emerald-50' : 'text-rose-600 bg-rose-50'
              }`}>
                {metric.trend === 'up' ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
                {metric.change}%
              </div>
            </div>
            <div className="mt-4 h-12 w-full opacity-50 group-hover:opacity-100 transition-opacity">
               <ResponsiveContainer width="100%" height="100%">
                 <AreaChart data={data}>
                   <Area type="monotone" dataKey="revenue" stroke={metric.trend === 'up' ? '#10b981' : '#f43f5e'} fill={metric.trend === 'up' ? '#ecfdf5' : '#fff1f2'} strokeWidth={2} />
                 </AreaChart>
               </ResponsiveContainer>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Chart */}
        <div className="lg:col-span-2 bg-white p-8 rounded-3xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-lg font-bold">Revenue Performance</h2>
              <p className="text-xs text-slate-400 uppercase tracking-widest mt-1">Real-time across regions</p>
            </div>
            <div className="flex gap-2">
               <div className="flex items-center gap-2 text-xs font-medium px-3 py-1.5 bg-slate-50 rounded-lg">
                 <div className="w-2 h-2 rounded-full bg-blue-600"></div> Revenue
               </div>
               <div className="flex items-center gap-2 text-xs font-medium px-3 py-1.5 bg-slate-50 rounded-lg">
                 <div className="w-2 h-2 rounded-full bg-indigo-300"></div> Projected
               </div>
            </div>
          </div>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data}>
                <defs>
                  <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.1}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#94a3b8'}} dy={10} />
                <YAxis axisLine={false} tickLine={false} tick={{fontSize: 12, fill: '#94a3b8'}} />
                <Tooltip 
                  contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)' }}
                />
                <Area type="monotone" dataKey="revenue" stroke="#3b82f6" fillOpacity={1} fill="url(#colorRev)" strokeWidth={3} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Actionable Insights */}
        <div className="space-y-6">
          <div className="bg-slate-900 rounded-3xl p-6 text-white overflow-hidden relative group">
            <div className="absolute -right-8 -top-8 w-32 h-32 bg-blue-600 rounded-full blur-[60px] opacity-40 group-hover:opacity-60 transition-opacity"></div>
            <div className="flex items-center gap-2 mb-6">
              <Zap className="text-blue-400" size={20} />
              <h3 className="font-bold">Agentic Alerts</h3>
            </div>
            <div className="space-y-4">
               <div className="bg-white/10 p-4 rounded-2xl border border-white/10 hover:bg-white/15 transition-all cursor-pointer">
                 <div className="flex items-center gap-2 mb-2">
                   <AlertTriangle className="text-amber-400" size={14} />
                   <span className="text-xs font-semibold text-amber-400">Inventory Alert</span>
                 </div>
                 <p className="text-sm font-medium leading-tight">Stockout risk for SKU-904 in Bengaluru hub. Estimated impact: $12k.</p>
                 <button className="mt-3 text-[10px] uppercase font-bold tracking-widest text-blue-400 hover:text-blue-300">Investigate root cause</button>
               </div>
               <div className="bg-white/10 p-4 rounded-2xl border border-white/10 hover:bg-white/15 transition-all cursor-pointer">
                 <div className="flex items-center gap-2 mb-2">
                   <TrendingUp className="text-emerald-400" size={14} />
                   <span className="text-xs font-semibold text-emerald-400">Opportunity</span>
                 </div>
                 <p className="text-sm font-medium leading-tight">Retention in "Power Users" cohort is up 15%. Suggest expansion campaign.</p>
                 <button className="mt-3 text-[10px] uppercase font-bold tracking-widest text-blue-400 hover:text-blue-300">Draft Campaign</button>
               </div>
            </div>
            <button className="w-full mt-6 py-2.5 bg-blue-600 rounded-xl text-xs font-bold hover:bg-blue-700 transition-all flex items-center justify-center gap-2 shadow-lg shadow-blue-900/40">
              <PlusCircle size={14} /> Create New Action
            </button>
          </div>

          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
            <div className="flex items-center gap-2 mb-4">
              <Lightbulb className="text-blue-600" size={18} />
              <h3 className="font-bold text-sm">Recommended Investigation</h3>
            </div>
            <p className="text-xs text-slate-500 mb-4 leading-relaxed">
              Why did the "Home Office" category see a 4% margin drop despite increased sales volume?
            </p>
            <div className="space-y-2">
              <div className="w-full bg-slate-50 p-2 rounded-lg text-[11px] font-medium text-slate-600 border border-slate-100 flex items-center justify-between">
                <span>Analyze vendor pricing changes</span>
                <ChevronRight size={12} />
              </div>
              <div className="w-full bg-slate-50 p-2 rounded-lg text-[11px] font-medium text-slate-600 border border-slate-100 flex items-center justify-between">
                <span>Compare shipping costs by region</span>
                <ChevronRight size={12} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const ChevronRight = ({ size }: { size: number }) => <ArrowUpRight size={size} />;

export default Dashboard;
