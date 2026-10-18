import React, { useEffect, useRef, useState } from 'react';
import { authService } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export const GoogleSignInButton = ({ onError, onSuccess }) => {
  const buttonContainerRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const { loginWithTokenAndUser } = useAuth();
  const navigate = useNavigate();

  const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
  const hasGisConfig = googleClientId && !googleClientId.includes('your_google_client_id');

  // Handle message from OAuth popup window
  useEffect(() => {
    const handleAuthMessage = (event) => {
      if (event.origin !== window.location.origin) return;
      if (event.data?.type === 'GOOGLE_AUTH_SUCCESS') {
        const { token, user } = event.data;
        loginWithTokenAndUser(token, user);
        if (onSuccess) onSuccess(event.data);
        setLoading(false);
        navigate('/dashboard');
      } else if (event.data?.type === 'GOOGLE_AUTH_ERROR') {
        setLoading(false);
        if (onError) onError(event.data.error || 'Google authentication failed');
      }
    };

    window.addEventListener('message', handleAuthMessage);
    return () => window.removeEventListener('message', handleAuthMessage);
  }, [loginWithTokenAndUser, onSuccess, onError, navigate]);

  // Open Google OAuth consent / account selection screen in a popup window
  const handleGoogleSignIn = () => {
    setLoading(true);
    try {
      const apiBase = import.meta.env.VITE_API_BASE_URL || '/api';
      const loginUrl = `${apiBase}/auth/google/login`;

      const width = 500;
      const height = 650;
      const left = window.screenX + Math.max(0, (window.outerWidth - width) / 2);
      const top = window.screenY + Math.max(0, (window.outerHeight - height) / 2);

      const popup = window.open(
        loginUrl,
        'GoogleSignInPopup',
        `width=${width},height=${height},left=${left},top=${top},status=no,menubar=no,toolbar=no`
      );

      if (!popup || popup.closed || typeof popup.closed === 'undefined') {
        // Fallback to direct redirect if popups are blocked by browser
        window.location.href = loginUrl;
      }
    } catch (err) {
      setLoading(false);
      if (onError) onError(err.message || 'Failed to initiate Google sign in');
    }
  };

  // Google Identity Services (GIS) One-Tap / ID Token callback
  const handleCredentialResponse = async (response) => {
    setLoading(true);
    try {
      const data = await authService.verifyGoogleCredential(response.credential);
      loginWithTokenAndUser(data.access_token, data.user);
      if (onSuccess) onSuccess(data);
      navigate('/dashboard');
    } catch (err) {
      const message = err.response?.data?.detail || 'Google authentication failed';
      if (onError) onError(message);
    } finally {
      setLoading(false);
    }
  };

  // Initialize Google Identity Services if valid Client ID is present
  useEffect(() => {
    if (!hasGisConfig || typeof window === 'undefined' || !window.google?.accounts?.id) {
      return;
    }

    try {
      window.google.accounts.id.initialize({
        client_id: googleClientId,
        callback: handleCredentialResponse,
        auto_select: false,
        cancel_on_tap_outside: true,
      });

      if (buttonContainerRef.current) {
        window.google.accounts.id.renderButton(buttonContainerRef.current, {
          theme: 'outline',
          size: 'large',
          type: 'standard',
          shape: 'pill',
          text: 'signin_with',
          logo_alignment: 'left',
          width: '100%',
        });
      }

      window.google.accounts.id.prompt();
    } catch (e) {
      console.warn('GIS initialization notice:', e);
    }
  }, [googleClientId, hasGisConfig]);

  return (
    <div className="w-full flex flex-col items-center">
      {hasGisConfig && <div ref={buttonContainerRef} className="w-full min-h-[44px]" />}

      {(!hasGisConfig || !buttonContainerRef.current?.hasChildNodes()) && (
        <button
          type="button"
          onClick={handleGoogleSignIn}
          disabled={loading}
          className="w-full flex items-center justify-center gap-3 px-4 py-3 bg-white text-slate-800 font-semibold rounded-xl border border-slate-200 hover:bg-slate-50 hover:shadow-md active:scale-[0.99] transition-all duration-200 disabled:opacity-70 disabled:cursor-not-allowed group shadow-sm"
          id="google-signin-btn"
        >
          {loading ? (
            <div className="w-5 h-5 border-2 border-emerald-600 border-t-transparent rounded-full animate-spin" />
          ) : (
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path
                fill="#4285F4"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="#34A853"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="#FBBC05"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
              />
              <path
                fill="#EA4335"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
              />
            </svg>
          )}
          <span className="text-sm font-medium tracking-wide">
            {loading ? 'Connecting to Google...' : 'Continue with Google'}
          </span>
        </button>
      )}
    </div>
  );
};

export default GoogleSignInButton;
