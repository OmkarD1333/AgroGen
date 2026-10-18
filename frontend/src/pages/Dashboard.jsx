import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useLanguage } from '../hooks/useLanguage';
import { 
  FiActivity, 
  FiSun, 
  FiTrendingUp, 
  FiAward, 
  FiMessageSquare, 
  FiMic, 
  FiArrowRight, 
  FiCheckCircle 
} from 'react-icons/fi';

const Dashboard = () => {
  const { user } = useAuth();
  const { t, isMarathi } = useLanguage();

  const services = [
    {
      title: t('svcDiseaseTitle'),
      desc: t('svcDiseaseDesc'),
      link: '/disease-detection',
      icon: FiActivity,
      badge: isMarathi ? 'AI मॉडेल' : 'AI Powered',
      cardStyle: 'bg-white border-amber-200/90 hover:border-amber-300',
      iconBg: 'bg-amber-100 text-amber-700',
    },
    {
      title: t('svcWeatherTitle'),
      desc: t('svcWeatherDesc'),
      link: '/weather',
      icon: FiSun,
      badge: isMarathi ? 'ताजे अपडेट्स' : 'Live Radar',
      cardStyle: 'bg-white border-amber-200/90 hover:border-amber-300',
      iconBg: 'bg-amber-100 text-amber-700',
    },
    {
      title: t('svcMarketTitle'),
      desc: t('svcMarketDesc'),
      link: '/market-prices',
      icon: FiTrendingUp,
      badge: isMarathi ? 'APMC दर' : 'APMC Mandi',
      cardStyle: 'bg-white border-amber-200/90 hover:border-amber-300',
      iconBg: 'bg-amber-100 text-amber-700',
    },
    {
      title: t('svcSchemesTitle'),
      desc: t('svcSchemesDesc'),
      link: '/schemes',
      icon: FiAward,
      badge: isMarathi ? 'सरकारी अनुदान' : 'Subsidies',
      cardStyle: 'bg-white border-emerald-200/90 hover:border-emerald-300',
      iconBg: 'bg-emerald-100 text-emerald-700',
    },
    {
      title: t('svcChatTitle'),
      desc: t('svcChatDesc'),
      link: '/chatbot',
      icon: FiMessageSquare,
      badge: isMarathi ? '२४/७ उपलब्ध' : '24/7 AgroBot',
      cardStyle: 'bg-white border-amber-200/90 hover:border-amber-300',
      iconBg: 'bg-amber-100 text-amber-700',
    },
    {
      title: t('svcVoiceTitle'),
      desc: t('svcVoiceDesc'),
      link: '/voice-assistant',
      icon: FiMic,
      badge: isMarathi ? 'व्हॉईस AI' : 'Voice AI',
      cardStyle: 'bg-white border-emerald-200/90 hover:border-emerald-300',
      iconBg: 'bg-emerald-100 text-emerald-700',
    },
  ];

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Welcome Banner: White background with Warm Yellow glow and subtle Green accents */}
      <div className="relative overflow-hidden rounded-2xl bg-white border border-amber-200 p-6 sm:p-8 shadow-warm">
        <div className="absolute top-0 right-0 w-80 h-80 bg-amber-200/30 rounded-full blur-3xl pointer-events-none -mr-16 -mt-16"></div>
        <div className="absolute bottom-0 left-1/3 w-60 h-60 bg-emerald-100/40 rounded-full blur-2xl pointer-events-none"></div>

        <div className="relative z-10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 text-xs font-bold px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300 mb-2">
              <FiCheckCircle className="text-emerald-600" />
              <span>{t('verifiedBadge')}</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              {t('greeting')}, {user?.full_name || t('farmerFriend')}! 👋
            </h1>
            <p className="text-slate-600 text-sm mt-1.5 max-w-xl leading-relaxed">
              {t('welcomeDesc')}
            </p>
          </div>

          <div className="flex flex-col text-right bg-amber-50/80 border border-amber-200 px-4 py-3 rounded-xl">
            <span className="text-xs text-amber-800 font-semibold">{user?.email}</span>
            <span className="text-xs font-bold text-emerald-700 mt-0.5">
              {isMarathi ? 'भाषा: मराठी' : 'Language: English'}
            </span>
          </div>
        </div>
      </div>

      {/* Grid of features */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-amber-500"></span>
            {isMarathi ? 'उपलब्ध शेती सेवा' : 'Available Agricultural Services'}
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {services.map((svc) => {
            const Icon = svc.icon;
            return (
              <Link
                key={svc.title}
                to={svc.link}
                className={`group p-5 rounded-2xl border transition-all duration-200 hover:-translate-y-1 hover:shadow-warm ${svc.cardStyle}`}
              >
                <div className="flex items-center justify-between mb-3">
                  <div className={`w-11 h-11 rounded-xl flex items-center justify-center ${svc.iconBg} shadow-sm`}>
                    <Icon className="text-xl" />
                  </div>
                  <span className="text-[11px] font-bold text-slate-600 bg-slate-100 px-2.5 py-1 rounded-full border border-slate-200">
                    {svc.badge}
                  </span>
                </div>
                <h3 className="font-bold text-slate-900 text-base group-hover:text-amber-700 transition-colors">
                  {svc.title}
                </h3>
                <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
                  {svc.desc}
                </p>
                <div className="mt-4 flex items-center gap-1.5 text-xs font-bold text-emerald-700 group-hover:text-emerald-800">
                  <span>{isMarathi ? 'माहिती पहा' : 'Explore'}</span>
                  <FiArrowRight className="group-hover:translate-x-1 transition-transform" />
                </div>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
