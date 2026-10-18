import React from 'react';
import { Navigate, Outlet, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useLanguage } from '../hooks/useLanguage';
import Navbar from '../components/Navbar';
import { 
  FiHome, 
  FiActivity, 
  FiSun, 
  FiTrendingUp, 
  FiAward, 
  FiMessageSquare, 
  FiMic, 
  FiBarChart2 
} from 'react-icons/fi';

const DashboardLayout = () => {
  const { isAuthenticated, loading } = useAuth();
  const { t, isMarathi } = useLanguage();
  const location = useLocation();

  const navigationItems = [
    { 
      name: isMarathi ? 'डॅशबोर्ड' : 'Dashboard', 
      path: '/dashboard', 
      icon: FiHome 
    },
    { 
      name: isMarathi ? 'पिक रोग निदान' : 'Crop Disease AI', 
      path: '/disease-detection', 
      icon: FiActivity 
    },
    { 
      name: isMarathi ? 'हवामान अंदाज' : 'Weather Forecast', 
      path: '/weather', 
      icon: FiSun 
    },
    { 
      name: isMarathi ? 'बाजार भाव' : 'Mandi Prices', 
      path: '/market-prices', 
      icon: FiTrendingUp 
    },
    { 
      name: isMarathi ? 'उत्पादन अंदाज' : 'Yield Prediction', 
      path: '/yield-prediction', 
      icon: FiBarChart2 
    },
    { 
      name: isMarathi ? 'सरकारी योजना' : 'Govt Schemes', 
      path: '/schemes', 
      icon: FiAward 
    },
    { 
      name: isMarathi ? 'Agro AI सल्लागार' : 'AgroChat AI', 
      path: '/chatbot', 
      icon: FiMessageSquare 
    },
    { 
      name: isMarathi ? 'व्हॉईस सहाय्यक' : 'Voice Assistant', 
      path: '/voice-assistant', 
      icon: FiMic 
    },
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-amber-50/20 flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-amber-300 border-t-amber-500 rounded-full animate-spin"></div>
          <p className="text-slate-500 text-xs font-semibold tracking-wider">
            {isMarathi ? 'लोड होत आहे...' : 'Loading AgroGen...'}
          </p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-50/40 text-slate-800">
      <Navbar />

      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        <aside className="hidden md:flex flex-col w-64 bg-white border-r border-amber-200/70 p-4 space-y-1">
          <div className="text-[11px] font-bold text-amber-800/80 uppercase tracking-wider px-3 mb-2 flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
            {isMarathi ? 'शेती सेवा' : 'Agro Services'}
          </div>
          {navigationItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                  isActive
                    ? 'bg-amber-100 text-amber-950 border border-amber-300 shadow-sm'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-amber-50/80'
                }`}
              >
                <Icon className={`text-base ${isActive ? 'text-amber-600' : 'text-slate-400'}`} />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </aside>

        {/* Content Area */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
