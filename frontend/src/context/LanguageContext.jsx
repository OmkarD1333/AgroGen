import React, { createContext, useContext, useState, useEffect } from 'react';

const LanguageContext = createContext(null);

export const translations = {
  mr: {
    // Brand
    brandName: 'AgroGen AI',
    tagline: 'शेतकऱ्यांचे विश्वासू डिजिटल साथीदार',
    subTagline: 'आधुनिक शेती सल्लागार आणि स्मार्ट सहाय्यक',

    // Language Toggle
    langSwitchLabel: 'भाषा बदला',
    currentLang: 'मराठी',
    switchPrompt: 'Switch to English',

    // Auth Common
    emailLabel: 'ईमेल पत्ता',
    emailPlaceholder: 'तुमचा ईमेल टाका (उदा. farmer@example.com)',
    passwordLabel: 'पासवर्ड',
    passwordPlaceholder: 'किमान ६ अक्षरे',
    forgotPassword: 'पासवर्ड विसरलात?',
    adminContactTip: 'कृपया पासवर्ड रीसेट करण्यासाठी ॲडमिनशी संपर्क साधा.',

    // Login
    loginTitle: 'खात्यात प्रवेश करा',
    loginSubtitle: 'आपल्या शेती सहाय्यकाचा वापर करण्यासाठी लॉगिन करा.',
    loginButton: 'लॉगिन करा',
    noAccount: 'नवीन शेतकरी आहात?',
    registerLinkText: 'येथे नोंदणी करा',
    loginSuccess: 'लॉगिन यशस्वी झाले! AgroGen AI मध्ये स्वागत आहे.',
    fillRequired: 'कृपया सर्व माहिती अचूक भरा.',

    // Features Highlights
    featDisease: 'पिक रोग निदान AI',
    featWeather: 'हवामान अंदाज',
    featMarket: 'ताजे बाजार भाव',
    featVoice: 'बोलून प्रश्न विचारा',

    // Register
    registerTitle: 'नवीन खाते तयार करा',
    registerSubtitle: 'AgroGen AI सोबत स्मार्ट शेतीची सुरुवात करा.',
    fullNameLabel: 'पूर्ण नाव',
    fullNamePlaceholder: 'उदा. रमेश ज्ञानोबा पाटील',
    phoneLabel: 'मोबाईल क्रमांक',
    phonePlaceholder: '+91 9876543210',
    confirmPasswordLabel: 'पासवर्ड पुष्टी',
    confirmPasswordPlaceholder: 'पासवर्ड पुन्हा टाका',
    preferredLangLabel: 'प्राधान्याची भाषा',
    registerButton: 'नोंदणी पूर्ण करा',
    hasAccount: 'आधीपासून खाते आहे का?',
    loginLinkText: 'येथे लॉगिन करा',
    passwordMinLength: 'पासवर्ड किमान ६ अक्षरांचा असावा.',
    passwordMismatch: 'दोन्ही पासवर्ड जुळत नाहीत.',
    registerSuccess: 'नोंदणी यशस्वी! आपले स्वागत आहे.',
    phoneInvalid: 'कृपया १० अंकांचा वैध मोबाईल क्रमांक टाका (६ ते ९ ने सुरू होणारा).',
    emailAlreadyExists: 'हा ईमेल आधीपासूनच नोंदणीकृत आहे.',
    phoneAlreadyExists: 'हा मोबाईल क्रमांक आधीपासूनच दुसऱ्या खात्याशी जोडलेला आहे.',

    // Dashboard / Navbar
    greeting: 'नमस्कार',
    farmerFriend: 'शेतकरी मित्र',
    welcomeDesc: 'आपल्या पिकांचे रक्षण आणि बाजारातील सर्वोत्तम दरांची माहिती एकाच ठिकाणी मिळवा.',
    verifiedBadge: 'प्रमाणीकृत शेतकरी',
    logout: 'बाहेर पडा',
    dashboard: 'डॅशबोर्ड',
    comingSoon: 'हा विभाग लवकरच सुरू होत आहे.',
    comingSoonDesc: 'कृपया डॅशबोर्डवर उपलब्ध सेवांचा लाभ घ्या.',

    // Services
    svcDiseaseTitle: 'पिक रोग निदान',
    svcDiseaseDesc: 'पानांचा फोटो अपलोड करा व त्वरित AI उपचार मिळवा.',
    svcWeatherTitle: 'हवामान अंदाज',
    svcWeatherDesc: 'आपल्या भागातील अचूक तापमान व पावसाचा अंदाज.',
    svcMarketTitle: 'बाजार भाव (मंडी)',
    svcMarketDesc: 'महाराष्ट्रातील प्रमुख बाजार समित्यांचे ताजे भाव.',
    svcSchemesTitle: 'सरकारी योजना',
    svcSchemesDesc: 'शेतकऱ्यांसाठी शासकीय अनुदान व योजनांची माहिती.',
    svcChatTitle: 'Agro AI सल्लागार',
    svcChatDesc: 'शेतीविषयक कोणत्याही प्रश्नावर त्वरित उत्तर मिळवा.',
    svcVoiceTitle: 'व्हॉईस सहाय्यक',
    svcVoiceDesc: 'मराठीत प्रश्न विचारा आणि आवाजात उत्तरे ऐका.',
  },
  en: {
    // Brand
    brandName: 'AgroGen AI',
    tagline: 'Farmers’ Trusted Digital Companion',
    subTagline: 'Modern Agricultural Intelligence & Smart Assistant',

    // Language Toggle
    langSwitchLabel: 'Change Language',
    currentLang: 'English',
    switchPrompt: 'मराठीत बदला',

    // Auth Common
    emailLabel: 'Email Address',
    emailPlaceholder: 'Enter your email (e.g. farmer@example.com)',
    passwordLabel: 'Password',
    passwordPlaceholder: 'At least 6 characters',
    forgotPassword: 'Forgot Password?',
    adminContactTip: 'Please contact support to reset your password.',

    // Login
    loginTitle: 'Welcome Back',
    loginSubtitle: 'Sign in to access your smart farming assistant.',
    loginButton: 'Sign In',
    noAccount: 'New to AgroGen?',
    registerLinkText: 'Create an account',
    loginSuccess: 'Login successful! Welcome to AgroGen AI.',
    fillRequired: 'Please fill in all required fields.',

    // Features Highlights
    featDisease: 'AI Crop Disease Detection',
    featWeather: 'Weather Forecast',
    featMarket: 'Live Mandi Prices',
    featVoice: 'Voice Guided Assistant',

    // Register
    registerTitle: 'Create Farmer Account',
    registerSubtitle: 'Start your precision agriculture journey with AgroGen AI.',
    fullNameLabel: 'Full Name',
    fullNamePlaceholder: 'e.g. Ramesh Patil',
    phoneLabel: 'Mobile Number',
    phonePlaceholder: '+91 9876543210',
    confirmPasswordLabel: 'Confirm Password',
    confirmPasswordPlaceholder: 'Re-enter your password',
    preferredLangLabel: 'Preferred Language',
    registerButton: 'Create Account',
    hasAccount: 'Already have an account?',
    loginLinkText: 'Sign in here',
    passwordMinLength: 'Password must be at least 6 characters long.',
    passwordMismatch: 'Passwords do not match.',
    registerSuccess: 'Registration successful! Welcome.',
    phoneInvalid: 'Please enter a valid 10-digit mobile number (starting with 6-9).',
    emailAlreadyExists: 'This email is already registered.',
    phoneAlreadyExists: 'This mobile number is already registered with another account.',

    // Dashboard / Navbar
    greeting: 'Welcome',
    farmerFriend: 'Farmer',
    welcomeDesc: 'Empowering your farmland with AI diagnostics, live mandi rates, and precision insights.',
    verifiedBadge: 'Verified Farmer',
    logout: 'Sign Out',
    dashboard: 'Dashboard',
    comingSoon: 'Coming Soon',
    comingSoonDesc: 'This module is under preparation. Please explore other features on your dashboard.',

    // Services
    svcDiseaseTitle: 'Crop Disease AI',
    svcDiseaseDesc: 'Upload a leaf photo for instant AI diagnosis and remedy recommendations.',
    svcWeatherTitle: 'Weather Forecast',
    svcWeatherDesc: 'Hyper-local weather metrics, rain alerts, and humidity trends.',
    svcMarketTitle: 'Live Mandi Prices',
    svcMarketDesc: 'Real-time crop rates from APMCs across Maharashtra.',
    svcSchemesTitle: 'Government Schemes',
    svcSchemesDesc: 'Verified central and state agricultural subsidies and benefits.',
    svcChatTitle: 'Agro AI Advisory',
    svcChatDesc: '24/7 intelligent conversational advisor for all farming queries.',
    svcVoiceTitle: 'Voice Assistant',
    svcVoiceDesc: 'Ask questions using your voice and listen to spoken answers.',
  },
  hi: {
    brandName: 'AgroGen AI',
    tagline: 'किसानों का विश्वसनीय डिजिटल साथी',
    subTagline: 'आधुनिक कृषि बुद्धिमत्ता और स्मार्ट सहायक',
    langSwitchLabel: 'भाषा बदलें',
    currentLang: 'हिंदी',
    switchPrompt: 'Switch to English',
    emailLabel: 'ईमेल पता',
    emailPlaceholder: 'अपना ईमेल दर्ज करें (उदा. farmer@example.com)',
    passwordLabel: 'पासवर्ड',
    passwordPlaceholder: 'कम से कम ६ अक्षर',
    forgotPassword: 'पासवर्ड भूल गए?',
    adminContactTip: 'कृपया पासवर्ड रीसेट के लिए व्यवस्थापक से संपर्क करें।',
    loginTitle: 'खाते में प्रवेश करें',
    loginSubtitle: 'अपने स्मार्ट कृषि सहायक का उपयोग करने के लिए लॉगिन करें।',
    loginButton: 'लॉगिन करें',
    noAccount: 'नए किसान हैं?',
    registerLinkText: 'यहाँ खाता बनाएं',
    loginSuccess: 'लॉगिन सफल! AgroGen AI में आपका स्वागत है।',
    fillRequired: 'कृपया सभी आवश्यक फ़ील्ड भरें।',
    featDisease: 'फसल रोग निदान AI',
    featWeather: 'मौसम पूर्वानुमान',
    featMarket: 'मंडी भाव',
    featVoice: 'बोलकर प्रश्न पूछें',
    registerTitle: 'नया किसान खाता बनाएं',
    registerSubtitle: 'AgroGen AI के साथ स्मार्ट खेती की शुरुआत करें।',
    fullNameLabel: 'पूरा नाम',
    fullNamePlaceholder: 'उदा. रमेश पाटील',
    phoneLabel: 'मोबाइल नंबर',
    phonePlaceholder: '+91 9876543210',
    confirmPasswordLabel: 'पासवर्ड की पुष्टि करें',
    confirmPasswordPlaceholder: 'पासवर्ड पुनः दर्ज करें',
    preferredLangLabel: 'मुख्य भाषा',
    registerButton: 'खाता बनाएं',
    hasAccount: 'क्या आपके पास पहले से खाता है?',
    loginLinkText: 'यहाँ लॉगिन करें',
    passwordMinLength: 'पासवर्ड कम से कम ६ अक्षरों का होना चाहिए।',
    passwordMismatch: 'पासवर्ड मेल नहीं खा रहे हैं।',
    registerSuccess: 'पंजीकरण सफल! आपका स्वागत है।',
    phoneInvalid: 'कृपया १० अंकों का वैध मोबाइल नंबर दर्ज करें (६-९ से शुरू होने वाला)।',
    emailAlreadyExists: 'यह ईमेल पहले से पंजीकृत है।',
    phoneAlreadyExists: 'यह मोबाइल नंबर पहले से किसी अन्य खाते से जुड़ा हुआ है।',
    greeting: 'नमस्ते',
    farmerFriend: 'किसान मित्र',
    welcomeDesc: 'अपने खेतों की सुरक्षा और मंडी के सर्वोत्तम भावों की जानकारी एक ही स्थान पर प्राप्त करें।',
    verifiedBadge: 'प्रमाणित किसान',
    logout: 'लॉग आउट',
    dashboard: 'डैशबोर्ड',
    comingSoon: 'शीघ्र आ रहा है',
    comingSoonDesc: 'यह सुविधा जल्द ही उपलब्ध होगी।',
    svcDiseaseTitle: 'फसल रोग निदान',
    svcDiseaseDesc: 'पत्ती का फोटो अपलोड करें और तुरंत AI उपचार पाएं।',
    svcWeatherTitle: 'मौसम पूर्वानुमान',
    svcWeatherDesc: 'सटीक तापमान, बारिश का अनुमान और मौसम अपडेट।',
    svcMarketTitle: 'मंडी भाव',
    svcMarketDesc: 'प्रमुख मंडियों के दैनिक ताजा भाव।',
    svcSchemesTitle: 'सरकारी योजनाएं',
    svcSchemesDesc: 'किसानों के लिए सरकारी अनुदान और सब्सिडी।',
    svcChatTitle: 'Agro AI सलाहकार',
    svcChatDesc: 'खेती से जुड़े किसी भी सवाल का तुरंत जवाब पाएं।',
    svcVoiceTitle: 'वॉयस सहायक',
    svcVoiceDesc: 'बोलकर सवाल पूछें और आवाज में जवाब सुनें।',
  },
};

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState(() => {
    return localStorage.getItem('agrogen_lang') || 'en';
  });

  useEffect(() => {
    localStorage.setItem('agrogen_lang', language);
  }, [language]);

  const toggleLanguage = () => {
    setLanguage((prev) => (prev === 'mr' ? 'en' : 'mr'));
  };

  const t = (key) => {
    return translations[language]?.[key] || translations['en']?.[key] || key;
  };

  const value = {
    language,
    isMarathi: language === 'mr',
    isEnglish: language === 'en',
    isHindi: language === 'hi',
    setLanguage,
    toggleLanguage,
    t,
  };

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

export default LanguageContext;
