import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useLanguage } from '../hooks/useLanguage';
import { GiWheat } from 'react-icons/gi';
import { FiLogOut, FiUser } from 'react-icons/fi';
import LanguageToggle from './LanguageToggle';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const { t } = useLanguage();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-amber-200/70 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-10 h-10 rounded-xl bg-amber-400 p-0.5 flex items-center justify-center shadow-sm shadow-amber-400/40 group-hover:scale-105 transition-transform">
              <div className="w-full h-full bg-white rounded-[9px] flex items-center justify-center">
                <GiWheat className="text-amber-600 text-xl" />
              </div>
            </div>
            <div>
              <span className="text-lg font-extrabold text-slate-900 tracking-tight">
                Agro<span className="text-amber-500">Gen</span> <span className="text-emerald-600 text-sm font-bold">AI</span>
              </span>
              <span className="text-[10px] block text-emerald-700 font-semibold -mt-1 tracking-wider uppercase">
                Smart Farming
              </span>
            </div>
          </Link>

          {/* Right Section: Language Toggle & User actions */}
          <div className="flex items-center gap-3">
            <LanguageToggle />

            {isAuthenticated ? (
              <div className="flex items-center gap-2.5 pl-2 border-l border-amber-200">
                <div className="hidden sm:flex flex-col text-right">
                  <span className="text-xs font-bold text-slate-800">
                    {user?.full_name || t('farmerFriend')}
                  </span>
                  <span className="text-[11px] text-slate-500 truncate max-w-[140px]">
                    {user?.email}
                  </span>
                </div>
                <div className="w-9 h-9 rounded-full bg-amber-100 border border-amber-300 text-amber-800 flex items-center justify-center font-bold text-sm shadow-sm">
                  {user?.full_name ? user.full_name[0].toUpperCase() : <FiUser />}
                </div>
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 hover:text-red-700 bg-amber-50 hover:bg-red-50 border border-amber-200 hover:border-red-200 rounded-lg transition-colors ml-1"
                  title="Logout"
                >
                  <FiLogOut className="text-sm" />
                  <span className="hidden md:inline">{t('logout')}</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  to="/login"
                  className="px-3 py-1.5 text-xs font-bold text-slate-700 hover:text-slate-900 transition-colors"
                >
                  {t('loginButton')}
                </Link>
                <Link
                  to="/register"
                  className="px-3.5 py-1.5 text-xs font-bold bg-amber-400 hover:bg-amber-500 text-slate-900 rounded-lg transition-colors shadow-sm"
                >
                  {t('registerButton')}
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
