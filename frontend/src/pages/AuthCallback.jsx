import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { exchangeGoogleCode } from '../services/api';
import { CheckCircle2, AlertCircle } from 'lucide-react';

export const AuthCallback = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { loginWithTokenAndUser } = useAuth();
  const [status, setStatus] = useState('processing');
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const token = searchParams.get('token');
    const code = searchParams.get('code');
    const error = searchParams.get('error');

    const handleError = (msg) => {
      setStatus('error');
      setErrorMessage(msg);
      if (window.opener && !window.opener.closed) {
        window.opener.postMessage(
          { type: 'GOOGLE_AUTH_ERROR', error: msg },
          window.location.origin
        );
        setTimeout(() => window.close(), 1500);
      } else {
        setTimeout(() => navigate('/login?error=' + encodeURIComponent(msg)), 2500);
      }
    };

    const completeLogin = (authToken, authUser) => {
      loginWithTokenAndUser(authToken, authUser);
      setStatus('success');

      if (window.opener && !window.opener.closed) {
        window.opener.postMessage(
          { type: 'GOOGLE_AUTH_SUCCESS', token: authToken, user: authUser },
          window.location.origin
        );
        setTimeout(() => window.close(), 600);
      } else {
        setTimeout(() => {
          navigate('/dashboard');
        }, 1000);
      }
    };

    if (error) {
      handleError(decodeURIComponent(error));
      return;
    }

    if (token) {
      const user = {
        id: searchParams.get('user_id'),
        full_name: searchParams.get('name') || 'Farmer',
        email: searchParams.get('email') || '',
        avatar_url: searchParams.get('avatar') || null,
        role: searchParams.get('role') || 'farmer',
        auth_provider: searchParams.get('auth_provider') || 'google',
        is_active: true,
      };
      completeLogin(token, user);
    } else if (code) {
      // Exchange Google authorization code with backend
      exchangeGoogleCode(code)
        .then((data) => {
          completeLogin(data.access_token, data.user);
        })
        .catch((err) => {
          const detail = err.response?.data?.detail || err.message || 'Google code exchange failed';
          handleError(detail);
        });
    } else {
      handleError('No authentication token received from Google callback.');
    }
  }, [searchParams, loginWithTokenAndUser, navigate]);

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-slate-900/90 backdrop-blur-xl border border-slate-800 rounded-2xl p-8 text-center shadow-2xl">
        {status === 'processing' && (
          <div className="flex flex-col items-center">
            <div className="w-14 h-14 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin mb-4" />
            <h2 className="text-xl font-bold text-white mb-2">Authenticating with Google</h2>
            <p className="text-sm text-slate-400">Verifying your Google account and syncing your farmer profile...</p>
          </div>
        )}

        {status === 'success' && (
          <div className="flex flex-col items-center">
            <CheckCircle2 className="w-16 h-16 text-emerald-400 mb-4 animate-bounce" />
            <h2 className="text-2xl font-bold text-white mb-2">Welcome to AgroGen AI!</h2>
            <p className="text-sm text-slate-400">Successfully signed in. Redirecting to your dashboard...</p>
          </div>
        )}

        {status === 'error' && (
          <div className="flex flex-col items-center">
            <AlertCircle className="w-16 h-16 text-rose-400 mb-4" />
            <h2 className="text-xl font-bold text-white mb-2">Authentication Failed</h2>
            <p className="text-sm text-rose-300 mb-4">{errorMessage}</p>
            <p className="text-xs text-slate-500">Redirecting to login page...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AuthCallback;
