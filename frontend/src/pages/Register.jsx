import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useLanguage } from '../hooks/useLanguage';
import { getErrorMessage } from '../services/api';
import toast from 'react-hot-toast';
import { FiUser, FiMail, FiPhone, FiLock, FiEye, FiEyeOff, FiArrowRight, FiGlobe } from 'react-icons/fi';
import { GiWheat } from 'react-icons/gi';
import LanguageToggle from '../components/LanguageToggle';
import GoogleSignInButton from '../components/auth/GoogleSignInButton';

const LANGUAGE_OPTIONS = [
  { code: 'en', label: 'English', subLabel: 'English', icon: '🌐' },
  { code: 'mr', label: 'मराठी', subLabel: 'Marathi', icon: '🌾' },
  { code: 'hi', label: 'हिंदी', subLabel: 'Hindi', icon: '🇮🇳' },
];

const Register = () => {
  const { language, setLanguage, t } = useLanguage();
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone: '',
    password: '',
    confirm_password: '',
    preferred_lang: 'en', // English as default
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'phone') {
      // Only permit numbers and maximum 10 digits
      const digitsOnly = value.replace(/\D/g, '').slice(0, 10);
      setFormData((prev) => ({ ...prev, [name]: digitsOnly }));
      return;
    }
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleLanguageSelect = (langCode) => {
    setFormData((prev) => ({ ...prev, preferred_lang: langCode }));
    setLanguage(langCode);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.full_name || !formData.email || !formData.password) {
      toast.error(t('fillRequired'));
      return;
    }

    if (formData.password.length < 6) {
      toast.error(t('passwordMinLength'));
      return;
    }

    if (formData.password !== formData.confirm_password) {
      toast.error(t('passwordMismatch'));
      return;
    }

    const cleanPhone = formData.phone.trim();
    if (cleanPhone && (cleanPhone.length !== 10 || !/^[6-9]\d{9}$/.test(cleanPhone))) {
      toast.error(t('phoneInvalid'), { duration: 6000 });
      return;
    }

    try {
      setLoading(true);
      await register({
        full_name: formData.full_name.trim(),
        email: formData.email.trim(),
        phone: cleanPhone || undefined,
        password: formData.password,
        preferred_lang: formData.preferred_lang || 'en',
      });

      toast.success(t('registerSuccess'), { duration: 5000 });
      navigate('/dashboard', { replace: true });
    } catch (error) {
      console.error('Registration error:', error);
      const serverMsg = getErrorMessage(error) || '';
      
      // Translate known server messages to active language (en/mr/hi)
      if (serverMsg.toLowerCase().includes('email already')) {
        toast.error(t('emailAlreadyExists'), { duration: 6000 });
      } else if (serverMsg.toLowerCase().includes('mobile number is already') || serverMsg.toLowerCase().includes('phone already')) {
        toast.error(t('phoneAlreadyExists'), { duration: 6000 });
      } else if (serverMsg.toLowerCase().includes('valid 10-digit mobile')) {
        toast.error(t('phoneInvalid'), { duration: 6000 });
      } else {
        toast.error(serverMsg, { duration: 6000 });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center px-4 py-8 relative overflow-hidden bg-gradient-to-b from-white via-amber-50/40 to-emerald-50/30">
      {/* Top Floating Language Switcher Bar */}
      <div className="w-full max-w-lg flex justify-between items-center mb-4 px-1">
        <div className="flex items-center gap-1.5 text-xs font-semibold text-emerald-800 bg-emerald-100/70 border border-emerald-300/60 px-3 py-1 rounded-full">
          <span className="w-2 h-2 rounded-full bg-emerald-600 animate-pulse"></span>
          AgroGen Smart AI
        </div>
        <LanguageToggle />
      </div>

      <div className="w-full max-w-lg relative z-10">
        {/* Brand Header */}
        <div className="text-center mb-5">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-amber-400 p-1 shadow-md shadow-amber-400/30 mb-2 border-2 border-white">
            <div className="w-full h-full bg-amber-50 rounded-[12px] flex items-center justify-center">
              <GiWheat className="text-amber-600 text-2xl" />
            </div>
          </div>
          <h1 className="text-2xl font-extrabold tracking-tight text-slate-900">
            Agro<span className="text-amber-500">Gen</span> <span className="text-emerald-600 font-bold">AI</span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            {t('registerSubtitle')}
          </p>
        </div>

        {/* Card */}
        <div className="white-card p-7 border border-amber-200/80 shadow-warm-lg">
          <div className="mb-5">
            <h2 className="text-xl font-bold text-slate-900">{t('registerTitle')}</h2>
          </div>

          <form onSubmit={handleSubmit} className="space-y-3.5">
            {/* Full Name */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                {t('fullNameLabel')} <span className="text-amber-600">*</span>
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-amber-500">
                  <FiUser className="text-base" />
                </div>
                <input
                  type="text"
                  name="full_name"
                  required
                  placeholder={t('fullNamePlaceholder')}
                  value={formData.full_name}
                  onChange={handleChange}
                  className="auth-input-light pl-10"
                />
              </div>
            </div>

            {/* Email Address */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                {t('emailLabel')} <span className="text-amber-600">*</span>
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-amber-500">
                  <FiMail className="text-base" />
                </div>
                <input
                  type="email"
                  name="email"
                  required
                  placeholder={t('emailPlaceholder')}
                  value={formData.email}
                  onChange={handleChange}
                  className="auth-input-light pl-10"
                />
              </div>
            </div>

            {/* Phone Number */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                {t('phoneLabel')}
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-amber-500">
                  <FiPhone className="text-base" />
                </div>
                <input
                  type="tel"
                  name="phone"
                  maxLength={10}
                  inputMode="numeric"
                  pattern="[0-9]{10}"
                  placeholder="9876543210"
                  value={formData.phone}
                  onChange={handleChange}
                  className="auth-input-light pl-10"
                />
              </div>
            </div>

            {/* Main Preferred Language Selection */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
                  <FiGlobe className="text-emerald-600" />
                  <span>{t('preferredLangLabel')}</span>
                  <span className="text-amber-600">*</span>
                </label>
                <span className="text-[10px] font-semibold text-emerald-800 bg-emerald-50 border border-emerald-200/90 px-2 py-0.5 rounded-full">
                  Default: English
                </span>
              </div>
              <div className="grid grid-cols-3 gap-2">
                {LANGUAGE_OPTIONS.map((lang) => {
                  const isSelected = formData.preferred_lang === lang.code;
                  return (
                    <button
                      key={lang.code}
                      type="button"
                      onClick={() => handleLanguageSelect(lang.code)}
                      className={`relative flex flex-col items-center justify-center py-2 px-1 rounded-xl border text-center transition-all duration-200 ${
                        isSelected
                          ? 'bg-amber-100/90 border-amber-500 text-slate-950 shadow-sm ring-2 ring-amber-400 font-bold'
                          : 'bg-white border-amber-200/80 text-slate-600 hover:bg-amber-50/70 hover:border-amber-300'
                      }`}
                    >
                      <span className="text-base mb-0.5">{lang.icon}</span>
                      <span className="text-xs font-bold leading-tight">{lang.label}</span>
                      <span className="text-[10px] text-slate-500 font-normal">{lang.subLabel}</span>
                      {isSelected && (
                        <span className="w-2 h-2 rounded-full bg-emerald-600 absolute top-1.5 right-1.5 shadow-sm"></span>
                      )}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Password & Confirm Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                  {t('passwordLabel')} <span className="text-amber-600">*</span>
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-amber-500">
                    <FiLock className="text-base" />
                  </div>
                  <input
                    type={showPassword ? 'text' : 'password'}
                    name="password"
                    required
                    placeholder={t('passwordPlaceholder')}
                    value={formData.password}
                    onChange={handleChange}
                    className="auth-input-light pl-10 pr-9"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 pr-2.5 flex items-center text-slate-400 hover:text-slate-700"
                    tabIndex="-1"
                  >
                    {showPassword ? <FiEyeOff className="text-sm" /> : <FiEye className="text-sm" />}
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                  {t('confirmPasswordLabel')} <span className="text-amber-600">*</span>
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-amber-500">
                    <FiLock className="text-base" />
                  </div>
                  <input
                    type={showPassword ? 'text' : 'password'}
                    name="confirm_password"
                    required
                    placeholder={t('confirmPasswordPlaceholder')}
                    value={formData.confirm_password}
                    onChange={handleChange}
                    className="auth-input-light pl-10"
                  />
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="btn-yellow flex items-center justify-center gap-2 mt-3"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-slate-900/30 border-t-slate-900 rounded-full animate-spin"></div>
              ) : (
                <>
                  <span>{t('registerButton')}</span>
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
            onSuccess={() => toast.success(t('registerSuccess') || 'Account created successfully')}
          />
        </div>

        {/* Footer Link */}
        <p className="text-center text-sm text-slate-600 mt-5">
          {t('hasAccount')}{' '}
          <Link to="/login" className="font-bold text-emerald-700 hover:text-emerald-800 hover:underline">
            {t('loginLinkText')}
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
