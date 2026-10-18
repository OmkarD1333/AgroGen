import React from 'react';
import { useLanguage } from '../hooks/useLanguage';
import { FiGlobe } from 'react-icons/fi';

const LanguageToggle = ({ className = '' }) => {
  const { isMarathi, isEnglish, setLanguage } = useLanguage();

  return (
    <div
      className={`inline-flex items-center gap-1.5 p-1 bg-white/90 backdrop-blur-md border border-amber-200 shadow-md shadow-amber-900/5 rounded-full ${className}`}
      role="group"
      aria-label="Language Selector"
    >
      <div className="pl-2 pr-1 text-amber-700 flex items-center gap-1 text-xs font-semibold">
        <FiGlobe className="text-sm text-green-700" />
        <span className="hidden sm:inline">भाषा / Lang:</span>
      </div>

      {/* Marathi Button */}
      <button
        type="button"
        onClick={() => setLanguage('mr')}
        className={`px-3 py-1 text-xs font-bold rounded-full transition-all duration-200 ${
          isMarathi
            ? 'bg-amber-400 text-slate-900 shadow-sm shadow-amber-500/30 ring-1 ring-amber-500/50'
            : 'text-slate-600 hover:text-slate-900 hover:bg-amber-50'
        }`}
      >
        मराठी
      </button>

      {/* English Button */}
      <button
        type="button"
        onClick={() => setLanguage('en')}
        className={`px-3 py-1 text-xs font-bold rounded-full transition-all duration-200 ${
          isEnglish
            ? 'bg-amber-400 text-slate-900 shadow-sm shadow-amber-500/30 ring-1 ring-amber-500/50'
            : 'text-slate-600 hover:text-slate-900 hover:bg-amber-50'
        }`}
      >
        English
      </button>
    </div>
  );
};

export default LanguageToggle;
