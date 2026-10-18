import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useLanguage } from '../hooks/useLanguage';
import { getErrorMessage } from '../services/api';
import toast from 'react-hot-toast';
import { FiMail, FiLock, FiEye, FiEyeOff, FiArrowRight, FiCheckCircle } from 'react-icons/fi';
import { GiWheat } from 'react-icons/gi';
import LanguageToggle from '../components/LanguageToggle';
import GoogleSignInButton from '../components/auth/GoogleSignInButton';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const { t } = useLanguage();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || '/dashboard';

  useEffect(() => {
    const errorParam = new URLSearchParams(window.location.search).get('error');
    if (errorParam) {
      toast.error(decodeURIComponent(errorParam));
      // Remove query param from URL so toast never repeats
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.email || !formData.password) {
      toast.error(t('fillRequired'));
      return;
    }

    try {
      setLoading(true);
      await login(formData.email.trim(), formData.password);
      toast.success(t('loginSuccess'));
      navigate(from, { replace: true });
    } catch (error) {
      console.error('Login error:', error);
      toast.error(getErrorMessage(error));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center px-4 py-8 relative overflow-hidden bg-gradient-to-b from-white via-amber-50/40 to-emerald-50/30">
      {/* Top Floating Language Switcher Bar */}
      <div className="w-full max-w-md flex justify-between items-center mb-4 px-1">
        <div className="flex items-center gap-1.5 text-xs font-semibold text-emerald-800 bg-emerald-100/70 border border-emerald-300/60 px-3 py-1 rounded-full">
          <span className="w-2 h-2 rounded-full bg-emerald-600 animate-pulse"></span>
          AgroGen Smart AI
        </div>
        <LanguageToggle />
      </div>

      <div className="w-full max-w-md relative z-10">
        {/* Brand Header */}
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-amber-400 p-1 shadow-lg shadow-amber-400/30 mb-3 border-2 border-white">
            <div className="w-full h-full bg-amber-50 rounded-[12px] flex items-center justify-center">
              <GiWheat className="text-amber-600 text-3xl" />
            </div>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-slate-900">
            Agro<span className="text-amber-500">Gen</span> <span className="text-emerald-600 text-2xl font-bold">AI</span>
          </h1>
          <p className="text-slate-600 text-sm font-medium mt-1">
            {t('tagline')}
          </p>
          <p className="text-xs text-emerald-700 font-semibold mt-0.5">
            {t('subTagline')}
          </p>
        </div>

        {/* Auth Card */}
        <div className="white-card p-8 border border-amber-200/80 shadow-warm-lg">
          <div className="mb-6">
            <h2 className="text-xl font-bold text-slate-900">{t('loginTitle')}</h2>
            <p className="text-xs text-slate-500 mt-1">
              {t('loginSubtitle')}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email Field */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                {t('emailLabel')} <span className="text-amber-600">*</span>
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-amber-500">
                  <FiMail className="text-lg" />
                </div>
                <input
                  type="email"
                  name="email"
                  required
                  placeholder={t('emailPlaceholder')}
                  value={formData.email}
                  onChange={handleChange}
                  className="auth-input-light pl-10"
                  autoComplete="email"
                />
              </div>
            </div>

            {/* Password Field */}
            <div>
              <div className="flex justify-between items-center mb-1.5">
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
                  {t('passwordLabel')} <span className="text-amber-600">*</span>
                </label>
                <a
                  href="#forgot"
                  onClick={(e) => {
                    e.preventDefault();
                    toast(t('adminContactTip'), { icon: 'ℹ️' });
                  }}
                  className="text-xs font-semibold text-emerald-700 hover:text-emerald-800 transition-colors"
                >
                  {t('forgotPassword')}
                </a>
              </div>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-amber-500">
                  <FiLock className="text-lg" />
                </div>
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  required
                  placeholder={t('passwordPlaceholder')}
                  value={formData.password}
                  onChange={handleChange}
                  className="auth-input-light pl-10 pr-10"
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-400 hover:text-slate-700 transition-colors"
                  tabIndex="-1"
                >
                  {showPassword ? <FiEyeOff /> : <FiEye />}
                </button>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="btn-yellow flex items-center justify-center gap-2 mt-2"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-slate-900/30 border-t-slate-900 rounded-full animate-spin"></div>
              ) : (
                <>
                  <span>{t('loginButton')}</span>
                  <FiArrowRight className="text-lg" />
                </>
              )}
            </button>
          </form>

          {/* Google Sign-in Option */}
          <div className="relative my-4">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-amber-200/80" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-white px-2 text-slate-500 font-semibold">
                किंवा / or
              </span>
            </div>
          </div>

          <GoogleSignInButton
            onError={(errMsg) => toast.error(errMsg)}
            onSuccess={() => toast.success(t('loginSuccess') || 'Logged in successfully')}
          />

          {/* Quick Feature Badges with Little Bit of Green */}
          <div className="mt-6 pt-5 border-t border-amber-100 grid grid-cols-2 gap-2 text-xs">
            <div className="flex items-center gap-1.5 text-slate-700 font-medium">
              <FiCheckCircle className="text-emerald-600 flex-shrink-0" />
              <span>{t('featDisease')}</span>
            </div>
            <div className="flex items-center gap-1.5 text-slate-700 font-medium">
              <FiCheckCircle className="text-emerald-600 flex-shrink-0" />
              <span>{t('featWeather')}</span>
            </div>
            <div className="flex items-center gap-1.5 text-slate-700 font-medium">
              <FiCheckCircle className="text-emerald-600 flex-shrink-0" />
              <span>{t('featMarket')}</span>
            </div>
            <div className="flex items-center gap-1.5 text-slate-700 font-medium">
              <FiCheckCircle className="text-emerald-600 flex-shrink-0" />
              <span>{t('featVoice')}</span>
            </div>
          </div>
        </div>

        {/* Footer Link */}
        <p className="text-center text-sm text-slate-600 mt-5">
          {t('noAccount')}{' '}
          <Link to="/register" className="font-bold text-emerald-700 hover:text-emerald-800 hover:underline">
            {t('registerLinkText')}
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
