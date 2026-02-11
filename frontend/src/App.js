import React, { useState, useEffect, createContext, useContext } from 'react';
import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import axios from "axios";
import { Toaster, toast } from 'sonner';
import InteractiveExerciseScreen from './components/InteractiveExerciseScreen';
import RealMarketZone from './components/RealMarketZone';
import AdvancedBacktest from './components/AdvancedBacktest';
import { OnboardingFlow, LessonCycle, ScoreDisplay, SkillMap, LESSON_DATA } from './components/LearningSystem';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Auth Context
const AuthContext = createContext(null);

const useAuth = () => useContext(AuthContext);

// ==================== HELPER FUNCTION FOR ERROR HANDLING ====================

const getErrorMessage = (error, fallbackMessage = 'An error occurred') => {
  if (!error?.response?.data) return fallbackMessage;
  
  const detail = error.response.data.detail;
  
  // If detail is a string, return it
  if (typeof detail === 'string') return detail;
  
  // If detail is an array (Pydantic validation errors), extract messages
  if (Array.isArray(detail)) {
    const messages = detail.map(err => {
      if (typeof err === 'string') return err;
      if (err.msg) return err.msg;
      return fallbackMessage;
    });
    return messages.join('. ');
  }
  
  // If detail is an object with a message
  if (detail?.msg) return detail.msg;
  if (detail?.message) return detail.message;
  
  return fallbackMessage;
};

// ==================== AUTH SCREENS ====================

const AuthScreen = ({ onLogin }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);
  const [showVerification, setShowVerification] = useState(false);
  const [pendingEmail, setPendingEmail] = useState('');
  const [resendLoading, setResendLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (isLogin) {
        const response = await axios.post(`${API}/auth/login`, { email, password });
        localStorage.setItem('tradelingo_user', JSON.stringify(response.data));
        onLogin(response.data);
        toast.success('Welcome back!');
      } else {
        const response = await axios.post(`${API}/auth/register`, { email, password, username });
        // Check if response contains user data (auto-verified) or message (needs verification)
        if (response.data.id) {
          // User was auto-verified, log them in
          localStorage.setItem('tradelingo_user', JSON.stringify(response.data));
          onLogin(response.data);
          toast.success('Account created successfully!');
        } else {
          // Show verification screen
          setPendingEmail(email);
          setShowVerification(true);
          toast.success('Please check your email to verify your account!');
        }
      }
    } catch (error) {
      const errorMsg = getErrorMessage(error, 'An error occurred');
      // Check if it's a verification error
      if (errorMsg.toLowerCase().includes('verify your email')) {
        setPendingEmail(email);
        setShowVerification(true);
      }
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleResendVerification = async () => {
    setResendLoading(true);
    try {
      await axios.post(`${API}/auth/resend-verification`, { email: pendingEmail });
      toast.success('Verification email sent! Check your inbox.');
    } catch (error) {
      toast.error(getErrorMessage(error, 'Failed to resend verification email'));
    } finally {
      setResendLoading(false);
    }
  };

  // Verification waiting screen
  if (showVerification) {
    return (
      <div className="min-h-screen bg-[#0d1117] flex items-center justify-center p-4" data-testid="verification-screen">
        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-blue-600 mb-4">
              <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-white">Check Your Email</h1>
            <p className="text-gray-400 mt-2">We've sent a verification link to</p>
            <p className="text-blue-400 font-semibold mt-1">{pendingEmail}</p>
          </div>

          <div className="bg-[#161b22] border border-gray-800 rounded-2xl p-6">
            <div className="bg-[#0d1117] rounded-lg p-4 mb-6">
              <p className="text-gray-300 text-sm">
                Click the verification link in the email to confirm your account. 
                The link expires in 24 hours.
              </p>
            </div>

            <div className="space-y-4">
              <p className="text-gray-400 text-sm text-center">Didn't receive the email?</p>
              <button
                onClick={handleResendVerification}
                disabled={resendLoading}
                className="w-full border border-blue-500 text-blue-400 hover:bg-blue-600 hover:text-white font-bold py-3 rounded-lg transition-colors disabled:opacity-50"
                data-testid="resend-verification-btn"
              >
                {resendLoading ? 'Sending...' : 'Resend Verification Email'}
              </button>
              <button
                onClick={() => {
                  setShowVerification(false);
                  setIsLogin(true);
                }}
                className="w-full text-gray-400 hover:text-white py-2 transition-colors"
                data-testid="back-to-login-btn"
              >
                Back to Login
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0d1117] flex items-center justify-center p-4" data-testid="auth-screen">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-teal-500 to-blue-600 mb-4">
            <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-white">TradeLingo</h1>
          <p className="text-gray-400 mt-2">Master Smart Money Concepts</p>
        </div>

        {/* Auth Form */}
        <div className="bg-[#161b22] border border-gray-800 rounded-2xl p-6">
          <div className="flex mb-6 bg-[#0d1117] rounded-lg p-1">
            <button
              onClick={() => setIsLogin(true)}
              className={`flex-1 py-2 text-center font-semibold rounded-lg transition-colors ${
                isLogin ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'
              }`}
              data-testid="login-tab"
            >
              Login
            </button>
            <button
              onClick={() => setIsLogin(false)}
              className={`flex-1 py-2 text-center font-semibold rounded-lg transition-colors ${
                !isLogin ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'
              }`}
              data-testid="register-tab"
            >
              Sign Up
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <div>
                <label className="block text-sm text-gray-400 mb-2">Username</label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full bg-[#0d1117] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-blue-500"
                  placeholder="Your username"
                  required={!isLogin}
                  data-testid="username-input"
                />
              </div>
            )}
            <div>
              <label className="block text-sm text-gray-400 mb-2">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-[#0d1117] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-blue-500"
                placeholder="your@email.com"
                required
                data-testid="email-input"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Password</label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-[#0d1117] border border-gray-700 rounded-lg px-4 py-3 pr-12 text-white focus:outline-none focus:border-blue-500"
                  placeholder="••••••••"
                  required
                  data-testid="password-input"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
                  data-testid="password-toggle-btn"
                >
                  {showPassword ? (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                    </svg>
                  ) : (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  )}
                </button>
              </div>
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition-colors disabled:opacity-50"
              data-testid="auth-submit-btn"
            >
              {loading ? 'Loading...' : isLogin ? 'Login' : 'Create Account'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

// ==================== HOME / LEARNING PATH (NEW CURRICULUM) ====================

const HomeScreen = ({ user, onCategorySelect, onLegacyLessonSelect, onRealMarketClick, onStartLesson }) => {
  const [tiers, setTiers] = useState([]);
  const [progress, setProgress] = useState({});
  const [ads, setAds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [userStats, setUserStats] = useState({ 
    accuracy: 60, 
    patience: 2, 
    decisions: 10, 
    streak: 0 
  });
  const [skillMastery, setSkillMastery] = useState([
    { id: 'identify-trends', name: 'Identify Trends', progress: 0 },
    { id: 'spot-consolidation', name: 'Spot Consolidation', progress: 0 },
    { id: 'trend-vs-range', name: 'Trend vs Range Decision', progress: 0 },
  ]);
  const [recommendedSkill, setRecommendedSkill] = useState({
    id: 'identify-trends',
    name: 'Identify Trends',
    description: 'Master this skill to unlock new decision-making abilities.'
  });

  useEffect(() => {
    fetchData();
  }, [user]);

  const fetchData = async () => {
    try {
      const [tiersRes, progressRes, adsRes] = await Promise.all([
        axios.get(`${API}/curriculum/tiers`),
        axios.get(`${API}/curriculum/progress/${user.id}`),
        axios.get(`${API}/ads/propfirms`)
      ]);
      setTiers(tiersRes.data);
      setProgress(progressRes.data);
      setAds(adsRes.data);
      
      // Calculate stats from user data
      const totalProgress = Object.values(progressRes.data).reduce((acc, p) => acc + (p.total_completed || 0), 0);
      setUserStats({
        accuracy: Math.min(100, Math.max(0, 60 + Math.floor(user.xp / 50))),
        patience: Math.floor(user.xp / 100) + 2,
        decisions: totalProgress + 10,
        streak: Math.floor(user.level / 2)
      });
      
      // Update skill mastery based on progress
      const updatedSkills = skillMastery.map(skill => ({
        ...skill,
        progress: Math.min(100, Math.floor(totalProgress / 3))
      }));
      setSkillMastery(updatedSkills);
      
    } catch (error) {
      toast.error('Failed to load curriculum');
    } finally {
      setLoading(false);
    }
  };

  const getCategoryProgress = (categoryId) => {
    const catProgress = progress[categoryId];
    if (!catProgress) return { completed: 0, total: 100, percentage: 0 };
    return {
      completed: catProgress.total_completed || 0,
      total: 100,
      percentage: catProgress.completion_percentage || 0
    };
  };

  const handleSkillSelect = (skill) => {
    if (onStartLesson) {
      onStartLesson(skill);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-[#0d1117]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="pb-24 bg-[#0d1117] min-h-screen" data-testid="home-screen">
      {/* Header */}
      <div className="px-5 pt-6 pb-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-400 text-sm">Welcome back,</p>
            <h1 className="text-2xl font-bold text-white">{user.username}</h1>
          </div>
          <div className="flex items-center gap-2 bg-gray-700/50 px-3 py-1.5 rounded-full">
            <svg className="w-4 h-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
              <path d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" />
            </svg>
            <span className="text-white font-semibold text-sm" data-testid="xp-badge">{user.level}</span>
          </div>
        </div>
      </div>

      {/* Stats Cards Grid */}
      <div className="px-5 grid grid-cols-2 gap-3 mb-6">
        {/* Accuracy Card - Teal/Green */}
        <div className="bg-gradient-to-br from-[#0d3d3d] to-[#0a2929] border border-teal-700/50 rounded-xl p-4" data-testid="accuracy-card">
          <div className="flex items-center gap-2 mb-1">
            <svg className="w-5 h-5 text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" strokeWidth="2"/>
              <circle cx="12" cy="12" r="6" strokeWidth="2"/>
              <circle cx="12" cy="12" r="2" fill="currentColor"/>
            </svg>
            <span className="text-teal-400 text-xs font-medium uppercase tracking-wide">Accuracy</span>
          </div>
          <p className="text-white text-3xl font-bold">{userStats.accuracy}%</p>
        </div>

        {/* Patience Card - Gold/Amber */}
        <div className="bg-gradient-to-br from-[#3d3519] to-[#292510] border border-amber-700/50 rounded-xl p-4" data-testid="patience-card">
          <div className="flex items-center gap-2 mb-1">
            <svg className="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" strokeWidth="2"/>
              <path d="M12 6v6l4 2" strokeWidth="2" strokeLinecap="round"/>
            </svg>
            <span className="text-amber-400 text-xs font-medium uppercase tracking-wide">Patience</span>
          </div>
          <p className="text-white text-3xl font-bold">{userStats.patience}</p>
        </div>

        {/* Decisions Card - Blue */}
        <div className="bg-gradient-to-br from-[#1a2744] to-[#111827] border border-blue-700/50 rounded-xl p-4" data-testid="decisions-card">
          <div className="flex items-center gap-2 mb-1">
            <svg className="w-5 h-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
              <path d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" />
            </svg>
            <span className="text-blue-400 text-xs font-medium uppercase tracking-wide">Decisions</span>
          </div>
          <p className="text-white text-3xl font-bold">{userStats.decisions}</p>
        </div>

        {/* Streak Card - Purple */}
        <div className="bg-gradient-to-br from-[#2d1f4d] to-[#1a1333] border border-purple-700/50 rounded-xl p-4" data-testid="streak-card">
          <div className="flex items-center gap-2 mb-1">
            <svg className="w-5 h-5 text-purple-400" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z" clipRule="evenodd" />
            </svg>
            <span className="text-purple-400 text-xs font-medium uppercase tracking-wide">Streak</span>
          </div>
          <p className="text-white text-3xl font-bold">{userStats.streak}</p>
        </div>
      </div>

      {/* Recommended For You Section */}
      <div className="px-5 mb-6">
        <h2 className="text-gray-400 text-xs font-semibold uppercase tracking-wider mb-3">Recommended For You</h2>
        <button 
          onClick={() => handleSkillSelect(recommendedSkill)}
          className="w-full bg-gradient-to-r from-blue-600/30 to-blue-800/20 border border-blue-500/30 rounded-xl p-4 text-left hover:border-blue-500/50 transition-all"
          data-testid="recommended-card"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-500/20 rounded-full flex items-center justify-center">
                <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" strokeWidth="2"/>
                  <circle cx="12" cy="12" r="3" fill="currentColor"/>
                </svg>
              </div>
              <div>
                <h3 className="text-white font-semibold">Continue Your Journey</h3>
                <p className="text-gray-400 text-sm">{recommendedSkill.description}</p>
                <p className="text-blue-400 text-sm mt-1">{recommendedSkill.name}</p>
              </div>
            </div>
            <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </button>
      </div>

      {/* Skill Mastery Section */}
      <div className="px-5">
        <h2 className="text-gray-400 text-xs font-semibold uppercase tracking-wider mb-3">Skill Mastery</h2>
        <div className="space-y-3">
          {skillMastery.map((skill) => (
            <button
              key={skill.id}
              onClick={() => handleSkillSelect(skill)}
              className="w-full bg-[#161b22] border border-gray-800 rounded-xl p-4 text-left hover:border-gray-700 transition-all"
              data-testid={`skill-${skill.id}`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-white font-medium">{skill.name}</span>
                <span className="text-gray-500 text-sm">{skill.progress}%</span>
              </div>
              <div className="h-1.5 bg-gray-800 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-blue-500 to-blue-400 rounded-full transition-all duration-500"
                  style={{ width: `${skill.progress}%` }}
                />
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Categories Section */}
      <div className="px-5 mt-8">
        <h2 className="text-gray-400 text-xs font-semibold uppercase tracking-wider mb-3">All Categories</h2>
        <div className="space-y-3">
          {tiers.map((tier) => (
            <div key={tier.id}>
              {tier.categories.map((category) => {
                const catProgress = getCategoryProgress(category.id);
                return (
                  <button
                    key={category.id}
                    onClick={() => onCategorySelect(category)}
                    className="w-full bg-[#161b22] border border-gray-800 rounded-xl p-4 text-left hover:border-gray-700 transition-all mb-3"
                    data-testid={`category-${category.id}`}
                  >
                    <div className="flex items-center gap-4">
                      <div 
                        className="w-12 h-12 rounded-xl flex items-center justify-center text-xl"
                        style={{ backgroundColor: (category.color || '#3b82f6') + '20' }}
                      >
                        {category.icon}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between">
                          <h3 className="text-white font-medium">{category.name}</h3>
                          <span className="text-gray-500 text-sm">{Math.round(catProgress.percentage)}%</span>
                        </div>
                        <div className="mt-2 h-1.5 bg-gray-800 rounded-full overflow-hidden">
                          <div 
                            className="h-full rounded-full transition-all duration-500"
                            style={{ 
                              width: `${catProgress.percentage}%`,
                              backgroundColor: category.color || '#3b82f6'
                            }}
                          />
                        </div>
                      </div>
                      <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </button>
                );
              })}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// ==================== COMBINED CATEGORY SCREEN (Book + Levels) ====================

const CategoryScreen = ({ category, user, onBack, onLevelSelect, onReadBook }) => {
  const [lesson, setLesson] = useState(null);
  const [levels, setLevels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [bookRead, setBookRead] = useState(false);

  useEffect(() => {
    fetchData();
  }, [category, user]);

  const fetchData = async () => {
    try {
      // Fetch lesson and levels in parallel
      const [lessonRes, levelsRes] = await Promise.all([
        axios.get(`${API}/curriculum/categories/${category.id}/lesson`).catch(() => ({ data: { has_lesson: false } })),
        axios.get(`${API}/curriculum/categories/${category.id}/levels?user_id=${user.id}`)
      ]);
      
      if (lessonRes.data.has_lesson) {
        setLesson(lessonRes.data);
      }
      setLevels(levelsRes.data);
      
      // Check if user already has progress (meaning they've read the book before)
      const hasProgress = levelsRes.data.some(l => l.completed_exercises > 0);
      setBookRead(hasProgress);
    } catch (error) {
      toast.error('Failed to load category');
    } finally {
      setLoading(false);
    }
  };

  const handleReadBook = () => {
    onReadBook(lesson);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-[#0A0A0A]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#58CC02]"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0A0A0A]" data-testid="category-screen">
      {/* Header */}
      <div className="bg-[#1A1A1A] p-4 sticky top-0 z-10">
        <div className="flex items-center gap-4">
          <button onClick={onBack} className="text-white" data-testid="category-back-btn">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <div className="flex items-center gap-3">
            <span className="text-2xl">{category.icon}</span>
            <div>
              <h1 className="text-lg font-bold text-white">{category.name}</h1>
              <p className="text-xs text-gray-400">10 Níveis • 100 Exercícios</p>
            </div>
          </div>
        </div>
      </div>

      <div className="p-4 pb-24">
        {/* Book Section - Always at top */}
        {lesson && (
          <div className="mb-6">
            <h2 className="text-white font-bold text-lg mb-3 flex items-center gap-2">
              📚 Lição Teórica
            </h2>
            <button
              onClick={handleReadBook}
              className={`w-full rounded-xl p-4 text-left transition-all border-2 ${
                bookRead 
                  ? 'bg-[#2D5016] border-[#58CC02]' 
                  : 'bg-gradient-to-r from-[#1A1A1A] to-[#252525] border-[#58CC02] animate-pulse'
              }`}
              data-testid="read-book-btn"
            >
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 bg-[#58CC02]/20 rounded-xl flex items-center justify-center">
                  <svg className="w-8 h-8 text-[#58CC02]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <div className="flex-1">
                  <h3 className="text-white font-bold text-base">{lesson.title}</h3>
                  <p className="text-gray-400 text-sm mt-1">{lesson.description}</p>
                  <div className="flex items-center gap-3 mt-2">
                    <span className="text-xs text-gray-500">📖 {lesson.total_pages} páginas</span>
                    <span className="text-xs text-gray-500">⏱️ {lesson.estimated_time}</span>
                  </div>
                </div>
                <div className="flex items-center">
                  {bookRead ? (
                    <div className="w-8 h-8 bg-[#58CC02] rounded-full flex items-center justify-center">
                      <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  ) : (
                    <div className="bg-[#58CC02] px-3 py-1 rounded-full">
                      <span className="text-white text-xs font-bold">LER</span>
                    </div>
                  )}
                </div>
              </div>
              {!bookRead && (
                <div className="mt-3 bg-[#FF9600]/10 border border-[#FF9600]/30 rounded-lg p-2">
                  <p className="text-[#FF9600] text-xs text-center">
                    ⚠️ Leia a lição para desbloquear os exercícios
                  </p>
                </div>
              )}
            </button>
          </div>
        )}

        {/* Levels Section */}
        <div>
          <h2 className="text-white font-bold text-lg mb-3 flex items-center gap-2">
            🎯 Níveis de Exercícios
          </h2>
          <div className="grid grid-cols-2 gap-3">
            {levels.map((level) => {
              const progressPercent = (level.completed_exercises / level.total_exercises) * 100;
              // Level 1 requires reading the book first (if there's a lesson)
              const isLevelLocked = lesson && !bookRead && level.level === 1 ? true : !level.is_unlocked;
              
              return (
                <button
                  key={level.level}
                  onClick={() => !isLevelLocked && onLevelSelect(level)}
                  disabled={isLevelLocked}
                  className={`relative p-4 rounded-xl text-left transition-all ${
                    !isLevelLocked
                      ? level.is_completed
                        ? 'bg-[#2D5016] border-2 border-[#58CC02]'
                        : 'bg-[#1A1A1A] hover:bg-[#252525] border-2 border-transparent hover:border-[#58CC02]/50'
                      : 'bg-[#1A1A1A] opacity-50 cursor-not-allowed'
                  }`}
                  data-testid={`level-${level.level}`}
                >
                  {/* Completed Badge */}
                  {level.is_completed && (
                    <div className="absolute -top-2 -right-2 w-6 h-6 bg-[#58CC02] rounded-full flex items-center justify-center">
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  )}
                  
                  {/* Lock Icon */}
                  {isLevelLocked && (
                    <div className="absolute top-2 right-2">
                      <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                      </svg>
                    </div>
                  )}

                  <div className="text-3xl font-bold text-white mb-1">
                    {level.level}
                  </div>
                  <div className="text-xs text-gray-400 mb-2">
                    Nível {level.level}
                  </div>
                  
                  {/* Progress */}
                  <div className="h-1 bg-[#2A2A2A] rounded-full overflow-hidden mb-1">
                    <div 
                      className="h-full bg-[#58CC02] transition-all"
                      style={{ width: `${progressPercent}%` }}
                    />
                  </div>
                  <div className="text-xs text-gray-500">
                    {level.completed_exercises}/{level.total_exercises}
                  </div>
                  
                  <div className="mt-2 text-xs text-[#FF9600]">
                    +{level.xp_per_exercise} XP cada
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

// ==================== BOOK READER SCREEN ====================

const BookReaderScreen = ({ category, lesson, onBack, onFinish }) => {
  const [currentPage, setCurrentPage] = useState(1);

  const handleNextPage = () => {
    if (currentPage < lesson.total_pages) {
      setCurrentPage(prev => prev + 1);
    } else {
      onFinish();
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(prev => prev - 1);
    }
  };

  const page = lesson.pages.find(p => p.page === currentPage);
  const progressPercent = (currentPage / lesson.total_pages) * 100;

  return (
    <div className="h-screen bg-[#0A0A0A] flex flex-col overflow-hidden" data-testid="book-reader-screen">
      {/* Header */}
      <div className="bg-[#1A1A1A] px-4 py-3 shrink-0">
        <div className="flex items-center justify-between mb-2">
          <button onClick={onBack} className="text-white hover:text-gray-300" data-testid="book-back-btn">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <div className="flex-1 mx-4">
            <div className="flex items-center justify-between text-xs text-gray-400 mb-1">
              <span>{category.name}</span>
              <span>{currentPage}/{lesson.total_pages}</span>
            </div>
            <div className="h-1.5 bg-[#2A2A2A] rounded-full overflow-hidden">
              <div 
                className="h-full bg-[#58CC02] transition-all duration-300"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>
          <button 
            onClick={onFinish} 
            className="text-gray-400 hover:text-white text-sm"
            data-testid="skip-book-btn"
          >
            Pular
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto p-4">
        {page && (
          <>
            {/* Title */}
            <div className="mb-4 text-center">
              <h1 className="text-2xl font-bold text-white mb-1">{page.title}</h1>
              {page.subtitle && (
                <p className="text-[#58CC02] text-sm">{page.subtitle}</p>
              )}
            </div>

            {/* Image */}
            {page.image && (
              <div className="mb-4 rounded-xl overflow-hidden">
                <img 
                  src={page.image} 
                  alt={page.title}
                  className="w-full h-48 object-cover"
                  onError={(e) => { e.target.style.display = 'none'; }}
                />
              </div>
            )}

            {/* Content - Markdown style */}
            <div className="bg-[#1A1A1A] rounded-xl p-4 mb-4">
              <div className="prose prose-invert prose-sm max-w-none">
                {page.content.split('\n').map((line, index) => {
                  // Headers
                  if (line.startsWith('## ')) {
                    return <h3 key={index} className="text-[#58CC02] font-bold text-lg mt-4 mb-2">{line.replace('## ', '')}</h3>;
                  }
                  if (line.startsWith('### ')) {
                    return <h4 key={index} className="text-[#FF9600] font-bold text-base mt-3 mb-1">{line.replace('### ', '')}</h4>;
                  }
                  // Bold text with **
                  if (line.includes('**')) {
                    const parts = line.split(/\*\*(.*?)\*\*/g);
                    return (
                      <p key={index} className="text-gray-300 text-sm mb-2">
                        {parts.map((part, i) => 
                          i % 2 === 1 ? <strong key={i} className="text-white">{part}</strong> : part
                        )}
                      </p>
                    );
                  }
                  // List items
                  if (line.startsWith('• ') || line.startsWith('- ') || line.startsWith('* ')) {
                    return (
                      <div key={index} className="flex items-start gap-2 mb-1">
                        <span className="text-[#58CC02] mt-1">•</span>
                        <p className="text-gray-300 text-sm">{line.replace(/^[•\-*]\s*/, '')}</p>
                      </div>
                    );
                  }
                  // Numbered lists
                  if (/^\d+\.\s/.test(line)) {
                    const num = line.match(/^(\d+)\./)[1];
                    return (
                      <div key={index} className="flex items-start gap-2 mb-1">
                        <span className="text-[#58CC02] font-bold min-w-[20px]">{num}.</span>
                        <p className="text-gray-300 text-sm">{line.replace(/^\d+\.\s*/, '')}</p>
                      </div>
                    );
                  }
                  // Code blocks (basic support)
                  if (line.startsWith('```')) {
                    return null;
                  }
                  // Checkmarks ✅
                  if (line.includes('✅') || line.includes('✓')) {
                    return (
                      <p key={index} className="text-gray-300 text-sm mb-2 flex items-center gap-2">
                        <span className="text-[#58CC02]">✓</span>
                        {line.replace(/[✅✓]\s*/, '')}
                      </p>
                    );
                  }
                  // Normal text
                  if (line.trim()) {
                    return <p key={index} className="text-gray-300 text-sm mb-2">{line}</p>;
                  }
                  return null;
                })}
              </div>
            </div>

            {/* Tip Box */}
            {page.tip && (
              <div className="bg-[#FF9600]/10 border border-[#FF9600]/30 rounded-xl p-4 mb-4">
                <div className="flex items-start gap-3">
                  <span className="text-xl">💡</span>
                  <div>
                    <p className="text-[#FF9600] font-bold text-sm mb-1">Dica</p>
                    <p className="text-gray-300 text-sm">{page.tip}</p>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Navigation Footer */}
      <div className="p-4 bg-[#1A1A1A] shrink-0">
        <div className="flex gap-3">
          {currentPage > 1 && (
            <button
              onClick={handlePrevPage}
              className="flex-1 py-3 bg-[#2A2A2A] text-white font-bold rounded-xl hover:bg-[#3A3A3A] transition-colors"
              data-testid="prev-page-btn"
            >
              ← Anterior
            </button>
          )}
          <button
            onClick={handleNextPage}
            className="flex-1 py-3 bg-[#58CC02] hover:bg-[#4CAD02] text-white font-bold rounded-xl transition-colors"
            data-testid="next-page-btn"
          >
            {currentPage < lesson.total_pages ? 'Próxima →' : 'Começar Exercícios →'}
          </button>
        </div>
        
        {/* Page Dots */}
        <div className="flex justify-center gap-1.5 mt-3">
          {Array.from({ length: lesson.total_pages }, (_, i) => (
            <button
              key={i}
              onClick={() => setCurrentPage(i + 1)}
              className={`w-2 h-2 rounded-full transition-all ${
                i + 1 === currentPage 
                  ? 'bg-[#58CC02] w-6' 
                  : i + 1 < currentPage 
                  ? 'bg-[#58CC02]/50' 
                  : 'bg-[#3A3A3A]'
              }`}
              data-testid={`page-dot-${i + 1}`}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

// ==================== CATEGORY LEVELS SCREEN ====================

const CategoryLevelsScreen = ({ category, user, onBack, onLevelSelect }) => {
  const [levels, setLevels] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLevels();
  }, [category, user]);

  const fetchLevels = async () => {
    try {
      const response = await axios.get(
        `${API}/curriculum/categories/${category.id}/levels?user_id=${user.id}`
      );
      setLevels(response.data);
    } catch (error) {
      toast.error('Failed to load levels');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-[#0A0A0A]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#58CC02]"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0A0A0A]" data-testid="category-levels-screen">
      {/* Header */}
      <div className="bg-[#1A1A1A] p-4 sticky top-0 z-10">
        <div className="flex items-center gap-4">
          <button onClick={onBack} className="text-white" data-testid="levels-back-btn">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <div className="flex items-center gap-3">
            <span className="text-2xl">{category.icon}</span>
            <div>
              <h1 className="text-lg font-bold text-white">{category.name}</h1>
              <p className="text-xs text-gray-400">10 Levels • 100 Exercises</p>
            </div>
          </div>
        </div>
      </div>

      {/* Levels Grid */}
      <div className="p-4 pb-24">
        <div className="grid grid-cols-2 gap-3">
          {levels.map((level) => {
            const progressPercent = (level.completed_exercises / level.total_exercises) * 100;
            
            return (
              <button
                key={level.level}
                onClick={() => level.is_unlocked && onLevelSelect(level)}
                disabled={!level.is_unlocked}
                className={`relative p-4 rounded-xl text-left transition-all ${
                  level.is_unlocked
                    ? level.is_completed
                      ? 'bg-[#2D5016] border-2 border-[#58CC02]'
                      : 'bg-[#1A1A1A] hover:bg-[#252525] border-2 border-transparent hover:border-[#58CC02]/50'
                    : 'bg-[#1A1A1A] opacity-50 cursor-not-allowed'
                }`}
                data-testid={`level-${level.level}`}
              >
                {/* Completed Badge */}
                {level.is_completed && (
                  <div className="absolute -top-2 -right-2 w-6 h-6 bg-[#58CC02] rounded-full flex items-center justify-center">
                    <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                )}
                
                {/* Lock Icon */}
                {!level.is_unlocked && (
                  <div className="absolute top-2 right-2">
                    <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                  </div>
                )}

                <div className="text-3xl font-bold text-white mb-1">
                  {level.level}
                </div>
                <div className="text-xs text-gray-400 mb-2">
                  Level {level.level}
                </div>
                
                {/* Progress */}
                <div className="h-1 bg-[#2A2A2A] rounded-full overflow-hidden mb-1">
                  <div 
                    className="h-full bg-[#58CC02] transition-all"
                    style={{ width: `${progressPercent}%` }}
                  />
                </div>
                <div className="text-xs text-gray-500">
                  {level.completed_exercises}/{level.total_exercises}
                </div>
                
                <div className="mt-2 text-xs text-[#FF9600]">
                  +{level.xp_per_exercise} XP each
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};

// ==================== EXERCISE SCREEN ====================

const ExerciseScreen = ({ category, level, user, onBack, onComplete }) => {
  const [exercises, setExercises] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [sessionXP, setSessionXP] = useState(0);
  
  // Lesson intro state
  const [lessonIntro, setLessonIntro] = useState(null);
  const [showIntro, setShowIntro] = useState(true);

  useEffect(() => {
    fetchLessonIntro();
    fetchExercises();
  }, [category, level, user]);

  const fetchLessonIntro = async () => {
    try {
      const response = await axios.get(
        `${API}/curriculum/categories/${category.id}/levels/${level.level}/intro`
      );
      if (response.data.has_intro) {
        setLessonIntro(response.data);
      } else {
        setShowIntro(false);
      }
    } catch (error) {
      setShowIntro(false);
    }
  };

  const fetchExercises = async () => {
    try {
      const response = await axios.get(
        `${API}/curriculum/categories/${category.id}/levels/${level.level}/exercises?user_id=${user.id}`
      );
      const exerciseList = response.data;
      const firstIncomplete = exerciseList.findIndex(ex => !ex.is_completed);
      setExercises(exerciseList);
      setCurrentIndex(firstIncomplete >= 0 ? firstIncomplete : 0);
    } catch (error) {
      toast.error('Failed to load exercises');
    } finally {
      setLoading(false);
    }
  };

  const currentExercise = exercises[currentIndex];
  const progress = ((currentIndex + 1) / exercises.length) * 100;

  const handleAnswerSelect = (index) => {
    if (showResult || submitting) return;
    setSelectedAnswer(index);
  };

  const handleSubmit = async () => {
    if (selectedAnswer === null || submitting) return;
    
    setSubmitting(true);
    const isCorrect = selectedAnswer === currentExercise.correct_answer;
    
    try {
      const response = await axios.post(`${API}/curriculum/exercises/complete`, {
        user_id: user.id,
        exercise_id: currentExercise.id,
        is_correct: isCorrect
      });
      
      setSessionXP(prev => prev + response.data.xp_gained);
      setShowResult(true);
    } catch (error) {
      toast.error('Failed to submit answer');
    } finally {
      setSubmitting(false);
    }
  };

  const handleNext = () => {
    if (currentIndex < exercises.length - 1) {
      setCurrentIndex(prev => prev + 1);
      setSelectedAnswer(null);
      setShowResult(false);
    } else {
      onComplete(sessionXP);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-[#0A0A0A]">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-[#58CC02]"></div>
      </div>
    );
  }

  if (!currentExercise) {
    return (
      <div className="h-screen bg-[#0A0A0A] flex items-center justify-center">
        <div className="text-center">
          <p className="text-white mb-4">No exercises available</p>
          <button onClick={onBack} className="text-[#58CC02]">Go Back</button>
        </div>
      </div>
    );
  }

  const isCorrect = selectedAnswer === currentExercise.correct_answer;

  // Show lesson intro first
  if (showIntro && lessonIntro) {
    return (
      <div className="h-screen bg-[#0A0A0A] flex flex-col overflow-hidden" data-testid="lesson-intro-screen">
        {/* Header */}
        <div className="bg-[#1A1A1A] px-4 py-3 flex items-center gap-3 shrink-0">
          <button onClick={onBack} className="text-white hover:text-gray-300">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <div className="flex-1">
            <h1 className="text-white font-bold text-lg">{category.name}</h1>
            <p className="text-gray-400 text-xs">Level {level.level}</p>
          </div>
          <span className="text-gray-400 text-xs flex items-center gap-1">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {lessonIntro.duration}
          </span>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-4">
          {/* Title Section */}
          <div className="mb-6 text-center">
            <h2 className="text-2xl font-bold text-white mb-2">{lessonIntro.title}</h2>
            <p className="text-[#58CC02] text-sm">{lessonIntro.subtitle}</p>
          </div>

          {/* Image */}
          {lessonIntro.image && (
            <div className="mb-6 rounded-xl overflow-hidden">
              <img 
                src={lessonIntro.image} 
                alt={lessonIntro.title}
                className="w-full h-48 object-cover"
              />
            </div>
          )}

          {/* Content - Markdown style */}
          <div className="bg-[#1A1A1A] rounded-xl p-4 mb-6">
            <div className="prose prose-invert prose-sm max-w-none">
              {lessonIntro.content.split('\n').map((line, index) => {
                // Headers
                if (line.startsWith('## ')) {
                  return <h3 key={index} className="text-[#58CC02] font-bold text-lg mt-4 mb-2">{line.replace('## ', '')}</h3>;
                }
                if (line.startsWith('### ')) {
                  return <h4 key={index} className="text-[#FF9600] font-bold text-base mt-3 mb-1">{line.replace('### ', '')}</h4>;
                }
                // Bold text
                if (line.includes('**')) {
                  const parts = line.split(/\*\*(.*?)\*\*/g);
                  return (
                    <p key={index} className="text-gray-300 text-sm mb-2">
                      {parts.map((part, i) => 
                        i % 2 === 1 ? <strong key={i} className="text-white">{part}</strong> : part
                      )}
                    </p>
                  );
                }
                // List items
                if (line.startsWith('• ') || line.startsWith('- ')) {
                  return (
                    <div key={index} className="flex items-start gap-2 mb-1">
                      <span className="text-[#58CC02] mt-1">•</span>
                      <p className="text-gray-300 text-sm">{line.replace(/^[•-]\s*/, '')}</p>
                    </div>
                  );
                }
                // Code blocks
                if (line.startsWith('```')) {
                  return null;
                }
                // Normal text
                if (line.trim()) {
                  return <p key={index} className="text-gray-300 text-sm mb-2">{line}</p>;
                }
                return null;
              })}
            </div>
          </div>

          {/* Key Points */}
          {lessonIntro.key_points && lessonIntro.key_points.length > 0 && (
            <div className="bg-[#1A1A1A] rounded-xl p-4 mb-6 border border-[#58CC02]/30">
              <h4 className="text-[#58CC02] font-bold mb-3 flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Pontos Chave
              </h4>
              <ul className="space-y-2">
                {lessonIntro.key_points.map((point, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <span className="text-[#58CC02] font-bold">{index + 1}.</span>
                    <span className="text-gray-300 text-sm">{point}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Start Button */}
        <div className="p-4 bg-[#1A1A1A] shrink-0">
          <button
            onClick={() => setShowIntro(false)}
            className="w-full py-4 bg-[#58CC02] hover:bg-[#4CAD02] text-white font-bold rounded-xl text-lg transition-all"
            data-testid="start-exercises-btn"
          >
            Começar Exercícios
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen bg-[#0A0A0A] flex flex-col overflow-hidden" data-testid="exercise-screen">
      {/* Compact Header */}
      <div className="bg-[#1A1A1A] px-4 py-2 flex items-center gap-3 shrink-0">
        <button onClick={onBack} className="text-white hover:text-gray-300" data-testid="exercise-back-btn">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <div className="flex-1">
          <div className="h-1.5 bg-[#2A2A2A] rounded-full overflow-hidden">
            <div className="h-full bg-[#58CC02] transition-all" style={{ width: `${progress}%` }} />
          </div>
        </div>
        <span className="text-white text-xs font-medium">{currentIndex + 1}/{exercises.length}</span>
        <span className="text-[#FF9600] text-xs font-medium">+{sessionXP} XP</span>
      </div>

      {/* Main Content - Vertical Stack Layout */}
      <div className="flex-1 flex flex-col p-3 gap-2 min-h-0 overflow-auto">
        {/* Image on TOP - Full width */}
        {currentExercise.image_url && (
          <div className="w-full rounded-lg overflow-hidden bg-[#1A1A1A] shrink-0">
            <img 
              src={currentExercise.image_url} 
              alt={currentExercise.title}
              className="w-full h-auto max-h-[180px] object-contain mx-auto"
            />
          </div>
        )}
        
        {/* Question */}
        <div className="bg-[#1A1A1A] rounded-lg p-3 shrink-0">
          <p className="text-white text-sm font-medium text-center">{currentExercise.question}</p>
        </div>
        
        {/* Options - Handle both text and image options */}
        {currentExercise.answer_type === 'image_choice' ? (
          /* IMAGE OPTIONS - 2x2 Grid of images */
          <div className="grid grid-cols-2 gap-2">
            {currentExercise.options?.map((imageUrl, index) => (
              <button
                key={index}
                onClick={() => handleAnswerSelect(index)}
                disabled={showResult}
                className={`relative rounded-lg overflow-hidden transition-all border-2 ${
                  showResult
                    ? index === currentExercise.correct_answer
                      ? 'border-[#58CC02] ring-2 ring-[#58CC02]'
                      : selectedAnswer === index
                      ? 'border-[#FF4B4B] ring-2 ring-[#FF4B4B]'
                      : 'border-[#2A2A2A]'
                    : selectedAnswer === index
                    ? 'border-[#58CC02] ring-2 ring-[#58CC02]'
                    : 'border-[#2A2A2A] hover:border-[#4A4A4A]'
                }`}
                data-testid={`image-option-${index}`}
              >
                <img 
                  src={imageUrl} 
                  alt={`Option ${String.fromCharCode(65 + index)}`}
                  className="w-full h-24 object-cover"
                />
                <span className={`absolute top-1 left-1 w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold ${
                  showResult && index === currentExercise.correct_answer
                    ? 'bg-[#58CC02] text-white'
                    : showResult && selectedAnswer === index
                    ? 'bg-[#FF4B4B] text-white'
                    : selectedAnswer === index
                    ? 'bg-[#58CC02] text-white'
                    : 'bg-black/60 text-white'
                }`}>
                  {String.fromCharCode(65 + index)}
                </span>
                {showResult && index === currentExercise.correct_answer && (
                  <span className="absolute top-1 right-1 text-lg">✓</span>
                )}
                {showResult && selectedAnswer === index && index !== currentExercise.correct_answer && (
                  <span className="absolute top-1 right-1 text-lg">✗</span>
                )}
              </button>
            ))}
          </div>
        ) : (
          /* TEXT OPTIONS - Original 2x2 Grid */
          <div className="grid grid-cols-2 gap-2">
            {currentExercise.options?.map((option, index) => (
              <button
                key={index}
                onClick={() => handleAnswerSelect(index)}
                disabled={showResult}
                className={`p-2 rounded-lg text-left transition-all text-xs flex items-start gap-1.5 min-h-[50px] ${
                  showResult
                    ? index === currentExercise.correct_answer
                      ? 'bg-[#58CC02] text-white'
                      : selectedAnswer === index
                      ? 'bg-[#FF4B4B] text-white'
                      : 'bg-[#2A2A2A] text-gray-400'
                    : selectedAnswer === index
                    ? 'bg-[#58CC02] text-white'
                    : 'bg-[#2A2A2A] text-white hover:bg-[#3A3A3A]'
                }`}
                data-testid={`option-${index}`}
              >
                <span className="w-5 h-5 rounded-full bg-black/20 flex items-center justify-center text-[10px] font-bold shrink-0">
                  {String.fromCharCode(65 + index)}
                </span>
                <span className="line-clamp-3 leading-tight">{option}</span>
              </button>
            ))}
          </div>
        )}

        {/* Feedback - Compact */}
        {showResult && (
          <div className={`p-2 rounded-lg shrink-0 ${isCorrect ? 'bg-[#2D5016]' : 'bg-[#4B1A1A]'}`}>
            <div className="flex items-center gap-2">
              {isCorrect ? (
                <>
                  <span className="text-lg">🎯</span>
                  <span className="text-white font-bold text-xs">Correct!</span>
                </>
              ) : (
                <>
                  <span className="text-lg">😅</span>
                  <span className="text-white font-bold text-xs">Not quite!</span>
                </>
              )}
              <span className="text-gray-300 text-xs flex-1 truncate">
                {isCorrect ? currentExercise.feedback_correct : currentExercise.feedback_wrong}
              </span>
            </div>
          </div>
        )}

        {/* Action Button */}
        <div className="shrink-0">
          {!showResult ? (
            <button
              onClick={handleSubmit}
              disabled={selectedAnswer === null || submitting}
              className="w-full bg-[#58CC02] text-white font-bold py-3 rounded-xl disabled:opacity-50"
              data-testid="submit-answer-btn"
            >
              {submitting ? 'Checking...' : 'Check Answer'}
            </button>
          ) : (
            <button
              onClick={handleNext}
              className="w-full bg-[#58CC02] text-white font-bold py-3 rounded-xl"
              data-testid="next-exercise-btn"
            >
              {currentIndex < exercises.length - 1 ? 'Continue' : 'Complete Level'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

// ==================== LEVEL COMPLETE MODAL ====================

const LevelCompleteModal = ({ xpGained, onContinue }) => {
  return (
    <div className="fixed inset-0 bg-black/90 flex items-center justify-center z-50 p-4">
      <div className="bg-[#1A1A1A] rounded-2xl p-6 text-center max-w-sm w-full">
        <div className="text-6xl mb-4">🏆</div>
        <h2 className="text-2xl font-bold text-white mb-2">Level Complete!</h2>
        <p className="text-gray-400 mb-4">You've mastered this level</p>
        <div className="text-3xl font-bold text-[#FF9600] mb-6">+{xpGained} XP</div>
        <button
          onClick={onContinue}
          className="w-full bg-[#58CC02] text-white font-bold py-4 rounded-xl"
          data-testid="level-complete-continue"
        >
          Continue Learning
        </button>
      </div>
    </div>
  );
};

// ==================== LESSON DETAIL SCREEN (LEGACY) ====================

const LessonScreen = ({ lesson, user, onBack, onComplete }) => {
  const [showQuiz, setShowQuiz] = useState(false);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [xpGained, setXpGained] = useState(0);

  const handleAnswerSelect = (index) => {
    if (showResult) return;
    setSelectedAnswer(index);
    setIsCorrect(index === lesson.quiz.correct);
    setShowResult(true);
  };

  const handleComplete = async () => {
    try {
      const response = await axios.post(`${API}/lessons/${lesson.id}/complete`, {
        user_id: user.id
      });
      setXpGained(response.data.xp_gained);
      setShowSuccess(true);
    } catch (error) {
      toast.error('Failed to complete lesson');
    }
  };

  const handleContinue = () => {
    if (showSuccess) {
      onComplete();
    } else if (showResult && isCorrect) {
      handleComplete();
    } else if (showResult && !isCorrect) {
      setSelectedAnswer(null);
      setShowResult(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0A0A0A]" data-testid="lesson-screen">
      {/* Header */}
      <div className="bg-[#1A1A1A] p-4 flex items-center gap-4 sticky top-0 z-10">
        <button onClick={onBack} className="text-white" data-testid="lesson-back-btn">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <div className="flex-1">
          <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-[#58CC02] transition-all"
              style={{ width: showQuiz ? '100%' : '50%' }}
            />
          </div>
        </div>
        <span className="text-white font-medium">+{lesson.xp_reward} XP</span>
      </div>

      {/* Success Modal */}
      {showSuccess && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
          <div className="bg-[#1A1A1A] rounded-2xl p-6 text-center max-w-sm w-full">
            <div className="w-20 h-20 bg-[#58CC02] rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">Lesson Complete!</h2>
            <div className="text-3xl font-bold text-[#FF9600] mb-4">+{xpGained} XP</div>
            <button
              onClick={handleContinue}
              className="w-full bg-[#58CC02] text-white font-bold py-3 rounded-lg"
              data-testid="continue-btn"
            >
              Continue
            </button>
          </div>
        </div>
      )}

      {/* Content */}
      <div className="p-4">
        {!showQuiz ? (
          /* Lesson Content */
          <div>
            <h1 className="text-2xl font-bold text-white mb-2">{lesson.title}</h1>
            <p className="text-gray-400 mb-6">{lesson.description}</p>
            <div className="bg-[#1A1A1A] rounded-xl p-4 mb-6">
              <div className="text-gray-300 whitespace-pre-line leading-relaxed">
                {lesson.content}
              </div>
            </div>
            <button
              onClick={() => setShowQuiz(true)}
              className="w-full bg-[#58CC02] text-white font-bold py-4 rounded-xl"
              data-testid="start-quiz-btn"
            >
              Take Quiz
            </button>
          </div>
        ) : (
          /* Quiz */
          <div>
            <h2 className="text-xl font-bold text-white mb-6">Quiz Time!</h2>
            <div className="bg-[#1A1A1A] rounded-xl p-4 mb-6">
              <p className="text-white text-lg mb-4">{lesson.quiz.question}</p>
              <div className="space-y-3">
                {lesson.quiz.options.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => handleAnswerSelect(index)}
                    disabled={showResult}
                    className={`w-full p-4 rounded-xl text-left transition-all ${
                      selectedAnswer === index
                        ? showResult
                          ? isCorrect
                            ? 'bg-[#58CC02] text-white'
                            : 'bg-[#FF4B4B] text-white'
                          : 'bg-[#58CC02] text-white'
                        : showResult && index === lesson.quiz.correct
                        ? 'bg-[#58CC02] text-white'
                        : 'bg-[#2A2A2A] text-white hover:bg-[#3A3A3A]'
                    }`}
                    data-testid={`quiz-option-${index}`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="w-8 h-8 rounded-full bg-black/20 flex items-center justify-center font-bold">
                        {String.fromCharCode(65 + index)}
                      </span>
                      <span>{option}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {showResult && (
              <div className={`p-4 rounded-xl mb-4 ${isCorrect ? 'bg-[#2D5016]' : 'bg-[#4B1A1A]'}`}>
                <div className="flex items-center gap-2 mb-2">
                  {isCorrect ? (
                    <svg className="w-6 h-6 text-[#58CC02]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    <svg className="w-6 h-6 text-[#FF4B4B]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  )}
                  <span className="text-white font-bold">{isCorrect ? 'Correct!' : 'Incorrect'}</span>
                </div>
                <p className="text-gray-300 text-sm">{lesson.quiz.explanation}</p>
              </div>
            )}

            {showResult && (
              <button
                onClick={handleContinue}
                className={`w-full font-bold py-4 rounded-xl ${
                  isCorrect ? 'bg-[#58CC02] text-white' : 'bg-gray-700 text-white'
                }`}
                data-testid="quiz-continue-btn"
              >
                {isCorrect ? 'Complete Lesson' : 'Try Again'}
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

// ==================== JOURNAL SCREEN ====================

const JournalScreen = ({ user }) => {
  const [entries, setEntries] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [showReflection, setShowReflection] = useState(false);
  const [newEntry, setNewEntry] = useState({
    win: true,
    confluences: [],
    description: '',
    photo: null,
    reflection_change: '',
    reflection_mistakes: '',
    reflection_proud: ''
  });
  const [newConfluence, setNewConfluence] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEntries();
  }, [user]);

  const fetchEntries = async () => {
    try {
      const response = await axios.get(`${API}/journal/${user.id}`);
      setEntries(response.data);
    } catch (error) {
      toast.error('Failed to load journal');
    } finally {
      setLoading(false);
    }
  };

  const handlePhotoUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setNewEntry({ ...newEntry, photo: reader.result });
      };
      reader.readAsDataURL(file);
    }
  };

  const addConfluence = () => {
    if (newConfluence.trim()) {
      setNewEntry({
        ...newEntry,
        confluences: [...newEntry.confluences, newConfluence.trim()]
      });
      setNewConfluence('');
    }
  };

  const removeConfluence = (index) => {
    setNewEntry({
      ...newEntry,
      confluences: newEntry.confluences.filter((_, i) => i !== index)
    });
  };

  const handleSaveTrade = () => {
    if (!newEntry.description.trim()) {
      toast.error('Please add a trade description');
      return;
    }
    setShowForm(false);
    setShowReflection(true);
  };

  const handleSaveEntry = async () => {
    try {
      await axios.post(`${API}/journal`, {
        user_id: user.id,
        ...newEntry
      });
      toast.success('Trade logged successfully!');
      setShowReflection(false);
      setNewEntry({
        win: true,
        confluences: [],
        description: '',
        photo: null,
        reflection_change: '',
        reflection_mistakes: '',
        reflection_proud: ''
      });
      fetchEntries();
    } catch (error) {
      toast.error('Failed to save entry');
    }
  };

  const handleDelete = async (entryId) => {
    try {
      await axios.delete(`${API}/journal/${entryId}`);
      toast.success('Entry deleted');
      fetchEntries();
    } catch (error) {
      toast.error('Failed to delete entry');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#58CC02]"></div>
      </div>
    );
  }

  return (
    <div className="pb-24" data-testid="journal-screen">
      {/* Header */}
      <div className="bg-[#1A1A1A] p-4 sticky top-0 z-10">
        <h1 className="text-xl font-bold text-white">Trading Journal</h1>
        <p className="text-sm text-gray-400">Track your trades and reflections</p>
      </div>

      {/* Add Entry Button */}
      <div className="p-4">
        <button
          onClick={() => setShowForm(true)}
          className="w-full bg-[#58CC02] text-white font-bold py-4 rounded-xl flex items-center justify-center gap-2"
          data-testid="add-trade-btn"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Log New Trade
        </button>
      </div>

      {/* Trade Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black/90 z-50 overflow-y-auto">
          <div className="min-h-screen p-4">
            <div className="bg-[#1A1A1A] rounded-2xl p-4">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-white">New Trade Entry</h2>
                <button onClick={() => setShowForm(false)} className="text-gray-400">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              {/* Win/Loss Selection */}
              <div className="mb-6">
                <label className="block text-sm text-gray-400 mb-2">Result</label>
                <div className="flex gap-3">
                  <button
                    onClick={() => setNewEntry({ ...newEntry, win: true })}
                    className={`flex-1 py-3 rounded-xl font-bold transition-colors ${
                      newEntry.win ? 'bg-[#58CC02] text-white' : 'bg-[#2A2A2A] text-gray-400'
                    }`}
                    data-testid="win-btn"
                  >
                    ✅ WIN
                  </button>
                  <button
                    onClick={() => setNewEntry({ ...newEntry, win: false })}
                    className={`flex-1 py-3 rounded-xl font-bold transition-colors ${
                      !newEntry.win ? 'bg-[#FF4B4B] text-white' : 'bg-[#2A2A2A] text-gray-400'
                    }`}
                    data-testid="loss-btn"
                  >
                    ❌ LOSS
                  </button>
                </div>
              </div>

              {/* Confluences */}
              <div className="mb-6">
                <label className="block text-sm text-gray-400 mb-2">Confluences</label>
                <div className="flex gap-2 mb-2">
                  <input
                    type="text"
                    value={newConfluence}
                    onChange={(e) => setNewConfluence(e.target.value)}
                    placeholder="Add confluence..."
                    className="flex-1 bg-[#0A0A0A] border border-gray-700 rounded-lg px-4 py-2 text-white"
                    data-testid="confluence-input"
                  />
                  <button
                    onClick={addConfluence}
                    className="bg-[#58CC02] px-4 py-2 rounded-lg text-white font-bold"
                    data-testid="add-confluence-btn"
                  >
                    Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {newEntry.confluences.map((conf, index) => (
                    <span key={index} className="bg-[#2A2A2A] px-3 py-1 rounded-full text-white text-sm flex items-center gap-2">
                      {conf}
                      <button onClick={() => removeConfluence(index)} className="text-gray-400 hover:text-white">
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              </div>

              {/* Description */}
              <div className="mb-6">
                <label className="block text-sm text-gray-400 mb-2">Trade Description</label>
                <textarea
                  value={newEntry.description}
                  onChange={(e) => setNewEntry({ ...newEntry, description: e.target.value })}
                  placeholder="Describe your trade setup, entry, and exit..."
                  className="w-full bg-[#0A0A0A] border border-gray-700 rounded-lg px-4 py-3 text-white h-32 resize-none"
                  data-testid="description-input"
                />
              </div>

              {/* Photo Upload */}
              <div className="mb-6">
                <label className="block text-sm text-gray-400 mb-2">Trade Screenshot</label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handlePhotoUpload}
                  className="hidden"
                  id="photo-upload"
                />
                <label
                  htmlFor="photo-upload"
                  className="block w-full bg-[#0A0A0A] border border-dashed border-gray-700 rounded-lg p-4 text-center cursor-pointer hover:border-[#58CC02] transition-colors"
                >
                  {newEntry.photo ? (
                    <img src={newEntry.photo} alt="Trade" className="max-h-40 mx-auto rounded-lg" />
                  ) : (
                    <div className="text-gray-400">
                      <svg className="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <span>Upload Screenshot</span>
                    </div>
                  )}
                </label>
              </div>

              <button
                onClick={handleSaveTrade}
                className="w-full bg-[#58CC02] text-white font-bold py-4 rounded-xl"
                data-testid="save-trade-btn"
              >
                Continue to Reflection
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Reflection Modal */}
      {showReflection && (
        <div className="fixed inset-0 bg-black/90 z-50 overflow-y-auto">
          <div className="min-h-screen p-4">
            <div className="bg-[#1A1A1A] rounded-2xl p-4">
              <h2 className="text-xl font-bold text-white mb-6">Daily Reflection</h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-2">What would you change today?</label>
                  <textarea
                    value={newEntry.reflection_change}
                    onChange={(e) => setNewEntry({ ...newEntry, reflection_change: e.target.value })}
                    className="w-full bg-[#0A0A0A] border border-gray-700 rounded-lg px-4 py-3 text-white h-24 resize-none"
                    data-testid="reflection-change-input"
                  />
                </div>

                <div>
                  <label className="block text-sm text-gray-400 mb-2">What mistakes did you make?</label>
                  <textarea
                    value={newEntry.reflection_mistakes}
                    onChange={(e) => setNewEntry({ ...newEntry, reflection_mistakes: e.target.value })}
                    className="w-full bg-[#0A0A0A] border border-gray-700 rounded-lg px-4 py-3 text-white h-24 resize-none"
                    data-testid="reflection-mistakes-input"
                  />
                </div>

                <div>
                  <label className="block text-sm text-gray-400 mb-2">What are you proud of?</label>
                  <textarea
                    value={newEntry.reflection_proud}
                    onChange={(e) => setNewEntry({ ...newEntry, reflection_proud: e.target.value })}
                    className="w-full bg-[#0A0A0A] border border-gray-700 rounded-lg px-4 py-3 text-white h-24 resize-none"
                    data-testid="reflection-proud-input"
                  />
                </div>
              </div>

              <button
                onClick={handleSaveEntry}
                className="w-full bg-[#58CC02] text-white font-bold py-4 rounded-xl mt-6"
                data-testid="save-reflection-btn"
              >
                Save Journal Entry
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Journal Entries */}
      <div className="px-4 space-y-4">
        {entries.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-[#1A1A1A] rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <p className="text-gray-400">No trades logged yet</p>
            <p className="text-gray-500 text-sm">Start journaling to track your progress</p>
          </div>
        ) : (
          entries.map(entry => (
            <div key={entry.id} className="bg-[#1A1A1A] rounded-xl p-4" data-testid={`journal-entry-${entry.id}`}>
              {/* Header */}
              <div className="flex items-center justify-between mb-3">
                <span className={`px-3 py-1 rounded-full text-sm font-bold ${
                  entry.win ? 'bg-[#58CC02] text-white' : 'bg-[#FF4B4B] text-white'
                }`}>
                  {entry.win ? '✅ WIN' : '❌ LOSS'}
                </span>
                <span className="text-gray-400 text-sm">
                  {new Date(entry.created_at).toLocaleDateString()}
                </span>
              </div>

              {/* Photo */}
              {entry.photo && (
                <img src={entry.photo} alt="Trade" className="w-full h-40 object-cover rounded-lg mb-3" />
              )}

              {/* Description */}
              <p className="text-gray-300 mb-3">{entry.description}</p>

              {/* Confluences */}
              {entry.confluences && entry.confluences.length > 0 && (
                <div className="mb-3">
                  <p className="text-sm text-gray-400 mb-1">Confluences:</p>
                  <div className="flex flex-wrap gap-2">
                    {entry.confluences.map((conf, index) => (
                      <span key={index} className="bg-[#2A2A2A] px-2 py-1 rounded text-sm text-white flex items-center gap-1">
                        <svg className="w-3 h-3 text-[#58CC02]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        {conf}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Reflections */}
              {(entry.reflection_change || entry.reflection_mistakes || entry.reflection_proud) && (
                <div className="border-t border-gray-700 pt-3 mt-3 space-y-2">
                  {entry.reflection_change && (
                    <div>
                      <p className="text-xs text-gray-500">What I'd change:</p>
                      <p className="text-sm text-gray-300">{entry.reflection_change}</p>
                    </div>
                  )}
                  {entry.reflection_mistakes && (
                    <div>
                      <p className="text-xs text-gray-500">Mistakes:</p>
                      <p className="text-sm text-gray-300">{entry.reflection_mistakes}</p>
                    </div>
                  )}
                  {entry.reflection_proud && (
                    <div>
                      <p className="text-xs text-gray-500">Proud of:</p>
                      <p className="text-sm text-gray-300">{entry.reflection_proud}</p>
                    </div>
                  )}
                </div>
              )}

              {/* Delete Button */}
              <button
                onClick={() => handleDelete(entry.id)}
                className="mt-3 text-[#FF4B4B] text-sm hover:underline"
                data-testid={`delete-entry-${entry.id}`}
              >
                Delete Entry
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

// ==================== SECURITY TAB ====================

const SecurityTab = ({ user }) => {
  const [activeSection, setActiveSection] = useState('password');
  const [loading, setLoading] = useState(false);
  const [twoFAStatus, setTwoFAStatus] = useState({ is_enabled: false, has_backup_codes: false });
  const [sessions, setSessions] = useState([]);
  const [activityLog, setActivityLog] = useState([]);
  const [backupCodes, setBackupCodes] = useState([]);
  const [showBackupCodes, setShowBackupCodes] = useState(false);
  
  // Password change form
  const [passwordForm, setPasswordForm] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  
  // 2FA form
  const [otpCode, setOtpCode] = useState('');
  const [pendingOtp, setPendingOtp] = useState(null);
  const [disablePassword, setDisablePassword] = useState('');

  useEffect(() => {
    fetchSecurityData();
  }, [user]);

  const fetchSecurityData = async () => {
    try {
      const [twoFARes, sessionsRes, activityRes] = await Promise.all([
        axios.get(`${API}/security/2fa/status/${user.id}`),
        axios.get(`${API}/security/sessions/${user.id}`),
        axios.get(`${API}/security/activity/${user.id}?limit=20`)
      ]);
      setTwoFAStatus(twoFARes.data);
      setSessions(sessionsRes.data);
      setActivityLog(activityRes.data);
    } catch (error) {
      console.error('Failed to fetch security data');
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    if (passwordForm.new_password !== passwordForm.confirm_password) {
      toast.error('New passwords do not match');
      return;
    }
    if (passwordForm.new_password.length < 8) {
      toast.error('Password must be at least 8 characters');
      return;
    }
    
    setLoading(true);
    try {
      await axios.post(`${API}/security/change-password`, {
        user_id: user.id,
        current_password: passwordForm.current_password,
        new_password: passwordForm.new_password,
        confirm_password: passwordForm.confirm_password
      });
      toast.success('Password changed successfully');
      setPasswordForm({ current_password: '', new_password: '', confirm_password: '' });
      fetchSecurityData();
    } catch (error) {
      toast.error(getErrorMessage(error, 'Failed to change password'));
    } finally {
      setLoading(false);
    }
  };

  const handleEnable2FA = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API}/security/2fa/enable`, {
        user_id: user.id,
        email: user.email
      });
      setPendingOtp(response.data.otp_demo); // Demo only - remove in production
      toast.success('OTP sent to your email');
    } catch (error) {
      toast.error(getErrorMessage(error, 'Failed to initiate 2FA'));
    } finally {
      setLoading(false);
    }
  };

  const handleVerify2FA = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API}/security/2fa/verify`, {
        user_id: user.id,
        otp_code: otpCode
      });
      setBackupCodes(response.data.backup_codes);
      setShowBackupCodes(true);
      setOtpCode('');
      setPendingOtp(null);
      fetchSecurityData();
      toast.success('2FA enabled successfully!');
    } catch (error) {
      toast.error(getErrorMessage(error, 'Invalid OTP'));
    } finally {
      setLoading(false);
    }
  };

  const handleDisable2FA = async () => {
    if (!disablePassword) {
      toast.error('Please enter your password');
      return;
    }
    setLoading(true);
    try {
      await axios.post(`${API}/security/2fa/disable`, {
        user_id: user.id,
        password: disablePassword
      });
      setDisablePassword('');
      fetchSecurityData();
      toast.success('2FA disabled');
    } catch (error) {
      toast.error(getErrorMessage(error, 'Failed to disable 2FA'));
    } finally {
      setLoading(false);
    }
  };

  const handleRegenerateBackupCodes = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API}/security/2fa/regenerate-codes/${user.id}`);
      setBackupCodes(response.data.backup_codes);
      setShowBackupCodes(true);
      toast.success('Backup codes regenerated');
    } catch (error) {
      toast.error('Failed to regenerate codes');
    } finally {
      setLoading(false);
    }
  };

  const handleLogoutSession = async (sessionId) => {
    try {
      await axios.delete(`${API}/security/sessions/${sessionId}`);
      toast.success('Session terminated');
      fetchSecurityData();
    } catch (error) {
      toast.error('Failed to terminate session');
    }
  };

  const handleLogoutAll = async () => {
    setLoading(true);
    try {
      await axios.post(`${API}/security/sessions/logout-all/${user.id}`);
      toast.success('Logged out from all devices');
      fetchSecurityData();
    } catch (error) {
      toast.error('Failed to logout from all devices');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const getEventIcon = (eventType) => {
    switch (eventType) {
      case 'password_change':
        return '🔐';
      case 'login':
        return '🔑';
      case '2fa_enabled':
        return '✅';
      case '2fa_disabled':
        return '❌';
      case 'logout_all':
      case 'session_logout':
        return '🚪';
      default:
        return '📋';
    }
  };

  return (
    <div className="p-4 space-y-6" data-testid="security-tab">
      {/* Section Navigation */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {[
          { id: 'password', label: 'Password' },
          { id: '2fa', label: '2FA' },
          { id: 'sessions', label: 'Sessions' },
          { id: 'activity', label: 'Activity' }
        ].map(section => (
          <button
            key={section.id}
            onClick={() => setActiveSection(section.id)}
            className={`px-4 py-2 rounded-lg font-medium whitespace-nowrap transition-colors ${
              activeSection === section.id
                ? 'bg-[#58CC02] text-white'
                : 'bg-[#2A2A2A] text-gray-400 hover:text-white'
            }`}
            data-testid={`security-section-${section.id}`}
          >
            {section.label}
          </button>
        ))}
      </div>

      {/* Password Change Section */}
      {activeSection === 'password' && (
        <div className="bg-[#1A1A1A] rounded-xl p-4" data-testid="password-section">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <svg className="w-5 h-5 text-[#58CC02]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            Change Password
          </h3>
          <form onSubmit={handlePasswordChange} className="space-y-4">
            <div>
              <label className="block text-sm text-gray-400 mb-2">Current Password</label>
              <input
                type="password"
                value={passwordForm.current_password}
                onChange={(e) => setPasswordForm({ ...passwordForm, current_password: e.target.value })}
                className="w-full bg-[#0A0A0A] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-[#58CC02]"
                required
                data-testid="current-password-input"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">New Password</label>
              <input
                type="password"
                value={passwordForm.new_password}
                onChange={(e) => setPasswordForm({ ...passwordForm, new_password: e.target.value })}
                className="w-full bg-[#0A0A0A] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-[#58CC02]"
                required
                minLength={8}
                data-testid="new-password-input"
              />
              <p className="text-xs text-gray-500 mt-1">Minimum 8 characters</p>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Confirm New Password</label>
              <input
                type="password"
                value={passwordForm.confirm_password}
                onChange={(e) => setPasswordForm({ ...passwordForm, confirm_password: e.target.value })}
                className="w-full bg-[#0A0A0A] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-[#58CC02]"
                required
                data-testid="confirm-password-input"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-[#58CC02] hover:bg-[#4CAF00] text-white font-bold py-3 rounded-lg transition-colors disabled:opacity-50"
              data-testid="change-password-btn"
            >
              {loading ? 'Changing...' : 'Change Password'}
            </button>
          </form>
        </div>
      )}

      {/* 2FA Section */}
      {activeSection === '2fa' && (
        <div className="bg-[#1A1A1A] rounded-xl p-4" data-testid="2fa-section">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <svg className="w-5 h-5 text-[#58CC02]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
            Two-Factor Authentication
          </h3>
          
          <div className="flex items-center justify-between mb-4 p-3 bg-[#0A0A0A] rounded-lg">
            <div>
              <p className="text-white font-medium">2FA Status</p>
              <p className="text-sm text-gray-400">Email-based one-time password</p>
            </div>
            <span className={`px-3 py-1 rounded-full text-sm font-bold ${
              twoFAStatus.is_enabled ? 'bg-[#58CC02] text-white' : 'bg-gray-700 text-gray-400'
            }`}>
              {twoFAStatus.is_enabled ? 'Enabled' : 'Disabled'}
            </span>
          </div>

          {!twoFAStatus.is_enabled ? (
            <div className="space-y-4">
              {!pendingOtp ? (
                <button
                  onClick={handleEnable2FA}
                  disabled={loading}
                  className="w-full bg-[#58CC02] hover:bg-[#4CAF00] text-white font-bold py-3 rounded-lg transition-colors disabled:opacity-50"
                  data-testid="enable-2fa-btn"
                >
                  {loading ? 'Sending OTP...' : 'Enable 2FA'}
                </button>
              ) : (
                <div className="space-y-4">
                  <div className="p-3 bg-[#2D5016] rounded-lg">
                    <p className="text-white text-sm">OTP sent to your email. Demo code: <span className="font-mono font-bold">{pendingOtp}</span></p>
                  </div>
                  <div>
                    <label className="block text-sm text-gray-400 mb-2">Enter OTP Code</label>
                    <input
                      type="text"
                      value={otpCode}
                      onChange={(e) => setOtpCode(e.target.value)}
                      placeholder="000000"
                      maxLength={6}
                      className="w-full bg-[#0A0A0A] border border-gray-700 rounded-lg px-4 py-3 text-white text-center text-xl tracking-widest font-mono focus:outline-none focus:border-[#58CC02]"
                      data-testid="otp-input"
                    />
                  </div>
                  <button
                    onClick={handleVerify2FA}
                    disabled={loading || otpCode.length !== 6}
                    className="w-full bg-[#58CC02] hover:bg-[#4CAF00] text-white font-bold py-3 rounded-lg transition-colors disabled:opacity-50"
                    data-testid="verify-otp-btn"
                  >
                    {loading ? 'Verifying...' : 'Verify & Enable'}
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              <button
                onClick={handleRegenerateBackupCodes}
                disabled={loading}
                className="w-full bg-[#2A2A2A] hover:bg-[#3A3A3A] text-white font-bold py-3 rounded-lg transition-colors disabled:opacity-50"
                data-testid="regenerate-codes-btn"
              >
                Regenerate Backup Codes
              </button>
              
              <div className="border-t border-gray-700 pt-4">
                <label className="block text-sm text-gray-400 mb-2">Disable 2FA (requires password)</label>
                <div className="flex gap-2">
                  <input
                    type="password"
                    value={disablePassword}
                    onChange={(e) => setDisablePassword(e.target.value)}
                    placeholder="Enter password"
                    className="flex-1 bg-[#0A0A0A] border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-[#FF4B4B]"
                    data-testid="disable-2fa-password"
                  />
                  <button
                    onClick={handleDisable2FA}
                    disabled={loading}
                    className="bg-[#FF4B4B] hover:bg-[#E04343] text-white font-bold px-4 py-2 rounded-lg transition-colors disabled:opacity-50"
                    data-testid="disable-2fa-btn"
                  >
                    Disable
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Backup Codes Modal */}
          {showBackupCodes && (
            <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
              <div className="bg-[#1A1A1A] rounded-2xl p-6 max-w-sm w-full">
                <h3 className="text-xl font-bold text-white mb-4">🔐 Backup Codes</h3>
                <p className="text-gray-400 text-sm mb-4">
                  Save these codes in a safe place. Each code can only be used once to recover your account.
                </p>
                <div className="grid grid-cols-2 gap-2 mb-4">
                  {backupCodes.map((code, index) => (
                    <div key={index} className="bg-[#0A0A0A] p-2 rounded text-center font-mono text-white">
                      {code}
                    </div>
                  ))}
                </div>
                <button
                  onClick={() => setShowBackupCodes(false)}
                  className="w-full bg-[#58CC02] text-white font-bold py-3 rounded-lg"
                  data-testid="close-backup-codes-btn"
                >
                  I've Saved My Codes
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Sessions Section */}
      {activeSection === 'sessions' && (
        <div className="bg-[#1A1A1A] rounded-xl p-4" data-testid="sessions-section">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <svg className="w-5 h-5 text-[#58CC02]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              Active Sessions
            </h3>
            {sessions.length > 0 && (
              <button
                onClick={handleLogoutAll}
                disabled={loading}
                className="text-[#FF4B4B] text-sm font-medium hover:underline disabled:opacity-50"
                data-testid="logout-all-btn"
              >
                Logout All
              </button>
            )}
          </div>

          {sessions.length === 0 ? (
            <p className="text-gray-400 text-center py-4">No active sessions</p>
          ) : (
            <div className="space-y-3">
              {sessions.map(session => (
                <div key={session.id} className="flex items-center justify-between p-3 bg-[#0A0A0A] rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-[#2A2A2A] rounded-lg flex items-center justify-center">
                      <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                    </div>
                    <div>
                      <p className="text-white font-medium flex items-center gap-2">
                        {session.device_info}
                        {session.is_current && (
                          <span className="text-xs bg-[#58CC02] text-white px-2 py-0.5 rounded">Current</span>
                        )}
                      </p>
                      <p className="text-sm text-gray-400">{formatDate(session.last_active)}</p>
                    </div>
                  </div>
                  {!session.is_current && (
                    <button
                      onClick={() => handleLogoutSession(session.id)}
                      className="text-[#FF4B4B] text-sm font-medium hover:underline"
                      data-testid={`logout-session-${session.id}`}
                    >
                      Logout
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Activity Log Section */}
      {activeSection === 'activity' && (
        <div className="bg-[#1A1A1A] rounded-xl p-4" data-testid="activity-section">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <svg className="w-5 h-5 text-[#58CC02]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Security Activity
          </h3>

          {activityLog.length === 0 ? (
            <p className="text-gray-400 text-center py-4">No security activity yet</p>
          ) : (
            <div className="space-y-3">
              {activityLog.map(log => (
                <div key={log.id} className="flex items-start gap-3 p-3 bg-[#0A0A0A] rounded-lg">
                  <span className="text-xl">{getEventIcon(log.event_type)}</span>
                  <div className="flex-1">
                    <p className="text-white font-medium">{log.description}</p>
                    <p className="text-sm text-gray-400">{formatDate(log.created_at)}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// ==================== PROFILE SCREEN ====================

const ProfileScreen = ({ user, onLogout, onUserUpdate }) => {
  const [loading, setLoading] = useState(false);
  const [activeProfileTab, setActiveProfileTab] = useState('account');

  const handleUpgrade = async (plan) => {
    setLoading(true);
    try {
      await axios.post(`${API}/subscription/upgrade`, {
        user_id: user.id,
        plan
      });
      // Refresh user data
      const response = await axios.get(`${API}/users/${user.id}`);
      localStorage.setItem('tradelingo_user', JSON.stringify(response.data));
      onUserUpdate(response.data);
      toast.success(`Upgraded to ${plan}!`);
    } catch (error) {
      toast.error('Failed to upgrade');
    } finally {
      setLoading(false);
    }
  };

  const stats = [
    { label: 'Total XP', value: user.xp, color: '#FF9600' },
    { label: 'Level', value: user.level, color: '#58CC02' },
    { label: 'Lessons', value: user.completed_lessons?.length || 0, color: '#3B82F6' },
  ];

  const plans = [
    {
      id: 'free',
      name: 'Free',
      price: '$0',
      features: ['20 SMC Lessons', 'Basic Journal', 'Prop Firm Ads'],
      current: user.subscription === 'free'
    },
    {
      id: 'standard',
      name: 'Standard',
      price: '$9.99/mo',
      features: ['No Ads', 'Advanced Journal', 'Priority Support'],
      current: user.subscription === 'standard'
    },
    {
      id: 'pro',
      name: 'Pro',
      price: '$19.99/mo',
      features: ['Everything in Standard', 'AI Trading Tutor', 'Trade Simulator'],
      current: user.subscription === 'pro'
    }
  ];

  return (
    <div className="pb-24" data-testid="profile-screen">
      {/* Header */}
      <div className="bg-[#1A1A1A] p-6 text-center">
        <div className="w-20 h-20 bg-[#58CC02] rounded-full flex items-center justify-center mx-auto mb-3">
          <span className="text-3xl font-bold text-white">
            {user.username?.charAt(0).toUpperCase()}
          </span>
        </div>
        <h1 className="text-xl font-bold text-white">{user.username}</h1>
        <p className="text-gray-400">{user.email}</p>
        <div className="mt-2 inline-block bg-[#FF9600] px-3 py-1 rounded-full">
          <span className="text-white font-semibold text-sm">{user.rank}</span>
        </div>
      </div>

      {/* Profile Tabs */}
      <div className="flex border-b border-gray-800">
        <button
          onClick={() => setActiveProfileTab('account')}
          className={`flex-1 py-3 text-center font-medium transition-colors ${
            activeProfileTab === 'account'
              ? 'text-[#58CC02] border-b-2 border-[#58CC02]'
              : 'text-gray-400 hover:text-white'
          }`}
          data-testid="profile-tab-account"
        >
          Account
        </button>
        <button
          onClick={() => setActiveProfileTab('security')}
          className={`flex-1 py-3 text-center font-medium transition-colors ${
            activeProfileTab === 'security'
              ? 'text-[#58CC02] border-b-2 border-[#58CC02]'
              : 'text-gray-400 hover:text-white'
          }`}
          data-testid="profile-tab-security"
        >
          Security
        </button>
      </div>

      {/* Account Tab Content */}
      {activeProfileTab === 'account' && (
        <>
          {/* Stats */}
          <div className="p-4">
            <div className="grid grid-cols-3 gap-3">
              {stats.map(stat => (
                <div key={stat.label} className="bg-[#1A1A1A] p-4 rounded-xl text-center">
                  <div className="text-2xl font-bold" style={{ color: stat.color }}>
                    {stat.value}
                  </div>
                  <div className="text-sm text-gray-400">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Subscription Plans */}
          <div className="p-4">
            <h2 className="text-lg font-bold text-white mb-4">Subscription Plans</h2>
            <div className="space-y-3">
              {plans.map(plan => (
                <div
                  key={plan.id}
                  className={`bg-[#1A1A1A] p-4 rounded-xl border-2 ${
                    plan.current ? 'border-[#58CC02]' : 'border-transparent'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <div>
                      <h3 className="text-white font-bold">{plan.name}</h3>
                      <p className="text-[#58CC02] font-semibold">{plan.price}</p>
                    </div>
                    {plan.current ? (
                      <span className="bg-[#58CC02] text-white px-3 py-1 rounded-full text-sm font-bold">
                        Current
                      </span>
                    ) : plan.id !== 'free' ? (
                      <button
                        onClick={() => handleUpgrade(plan.id)}
                        disabled={loading}
                        className="bg-[#58CC02] text-white px-4 py-2 rounded-lg font-bold hover:bg-[#4CAF00] disabled:opacity-50"
                        data-testid={`upgrade-${plan.id}-btn`}
                      >
                        Upgrade
                      </button>
                    ) : null}
                  </div>
                  <ul className="space-y-1">
                    {plan.features.map((feature, index) => (
                      <li key={index} className="text-gray-400 text-sm flex items-center gap-2">
                        <svg className="w-4 h-4 text-[#58CC02]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>

          {/* Logout */}
          <div className="p-4">
            <button
              onClick={onLogout}
              className="w-full bg-[#FF4B4B] text-white font-bold py-3 rounded-xl"
              data-testid="logout-btn"
            >
              Logout
            </button>
          </div>
        </>
      )}

      {/* Security Tab Content */}
      {activeProfileTab === 'security' && (
        <SecurityTab user={user} />
      )}
    </div>
  );
};

// ==================== BOTTOM NAVIGATION ====================

const BottomNav = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'home', label: 'Learn', icon: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
      </svg>
    )},
    { id: 'backtest', label: 'Backtest', icon: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
      </svg>
    )},
    { id: 'journal', label: 'Journal', icon: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
      </svg>
    )},
    { id: 'profile', label: 'Profile', icon: (
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
      </svg>
    )}
  ];

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-[#161b22] border-t border-gray-800 px-2 py-2 z-40">
      <div className="flex justify-around">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex flex-col items-center py-2 px-3 rounded-lg transition-colors ${
              activeTab === tab.id 
                ? tab.id === 'backtest' ? 'text-purple-400' : 'text-blue-400' 
                : 'text-gray-500 hover:text-gray-300'
            }`}
            data-testid={`nav-${tab.id}`}
          >
            {tab.icon}
            <span className="text-[10px] mt-1 font-medium">{tab.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

// ==================== PRO UPGRADE SCREEN ====================

const ProUpgradeScreen = ({ user, onUpgrade, onBack }) => {
  const [loading, setLoading] = useState(false);

  const handleUpgrade = async () => {
    setLoading(true);
    try {
      await axios.post(`${API}/subscription/upgrade`, {
        user_id: user.id,
        plan: 'pro'
      });
      toast.success('Upgraded to Pro! Welcome to the elite.');
      onUpgrade();
    } catch (error) {
      toast.error('Failed to upgrade. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const features = [
    { icon: '📊', title: 'Real Market Replay', desc: 'Practice with actual historical market data' },
    { icon: '🎯', title: 'Advanced Analysis', desc: 'Get AI-powered insights on your trading decisions' },
    { icon: '📈', title: 'Multiple Assets', desc: 'Trade ES, NQ, Gold, Bitcoin and more' },
    { icon: '⚡', title: 'Unlimited Sessions', desc: 'No limits on practice sessions' },
    { icon: '🏆', title: 'Leaderboards', desc: 'Compete with traders worldwide' },
    { icon: '📱', title: 'Priority Support', desc: '24/7 dedicated support team' },
  ];

  return (
    <div className="min-h-screen bg-[#0d1117] pb-24" data-testid="pro-upgrade-screen">
      {/* Header */}
      <div className="bg-gradient-to-b from-purple-900/30 to-transparent px-5 pt-6 pb-8">
        <button 
          onClick={onBack} 
          className="text-gray-400 hover:text-white mb-4"
          data-testid="upgrade-back-btn"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-purple-500 to-purple-700 mb-4">
            <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">Upgrade to Pro</h1>
          <p className="text-gray-400">Unlock the full power of TradeLingo</p>
        </div>
      </div>

      {/* Backtest Preview - Locked */}
      <div className="px-5 mb-6">
        <div className="relative bg-[#161b22] border border-gray-800 rounded-xl p-4 overflow-hidden">
          {/* Blurred background */}
          <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 to-blue-900/20 backdrop-blur-sm"></div>
          
          {/* Content preview */}
          <div className="relative opacity-50">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-12 h-12 bg-purple-600/30 rounded-xl flex items-center justify-center">
                <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <div>
                <h3 className="text-white font-semibold">Real Market Backtest</h3>
                <p className="text-gray-500 text-sm">ES Futures - 5min</p>
              </div>
            </div>
            <div className="h-32 bg-[#0d1117] rounded-lg flex items-center justify-center">
              <div className="flex gap-1">
                {[40, 60, 45, 70, 55, 80, 65, 90, 75, 85].map((h, i) => (
                  <div key={i} className="w-4 bg-green-500/30 rounded-t" style={{ height: `${h}%` }}></div>
                ))}
              </div>
            </div>
          </div>
          
          {/* Lock overlay */}
          <div className="absolute inset-0 flex items-center justify-center bg-black/60 rounded-xl">
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-600/20 rounded-full flex items-center justify-center mx-auto mb-3">
                <svg className="w-8 h-8 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <p className="text-white font-semibold">Pro Feature</p>
              <p className="text-gray-400 text-sm">Upgrade to access</p>
            </div>
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="px-5 mb-6">
        <h2 className="text-gray-400 text-xs font-semibold uppercase tracking-wider mb-3">What You Get</h2>
        <div className="grid grid-cols-2 gap-3">
          {features.map((feature, i) => (
            <div key={i} className="bg-[#161b22] border border-gray-800 rounded-xl p-4">
              <span className="text-2xl mb-2 block">{feature.icon}</span>
              <h3 className="text-white font-semibold text-sm mb-1">{feature.title}</h3>
              <p className="text-gray-500 text-xs">{feature.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Pricing */}
      <div className="px-5 mb-6">
        <div className="bg-gradient-to-r from-purple-600/20 to-blue-600/20 border border-purple-500/30 rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <div>
              <p className="text-gray-400 text-sm">Pro Plan</p>
              <div className="flex items-baseline gap-1">
                <span className="text-4xl font-bold text-white">$19</span>
                <span className="text-gray-400">/month</span>
              </div>
            </div>
            <div className="bg-purple-500/20 px-3 py-1 rounded-full">
              <span className="text-purple-400 text-sm font-medium">Most Popular</span>
            </div>
          </div>
          
          <ul className="space-y-2 mb-4">
            {['All Backtest features', 'Unlimited practice sessions', 'Advanced analytics', 'Priority support'].map((item, i) => (
              <li key={i} className="flex items-center gap-2 text-gray-300 text-sm">
                <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                {item}
              </li>
            ))}
          </ul>

          <button
            onClick={handleUpgrade}
            disabled={loading}
            className="w-full bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white font-bold py-4 rounded-xl transition-all disabled:opacity-50"
            data-testid="upgrade-pro-btn"
          >
            {loading ? 'Processing...' : 'Upgrade to Pro'}
          </button>
        </div>
      </div>

      {/* Guarantee */}
      <div className="px-5 text-center">
        <div className="flex items-center justify-center gap-2 text-gray-500 text-sm">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
          <span>7-day money-back guarantee</span>
        </div>
      </div>
    </div>
  );
};

// ==================== MAIN APP ====================

const MainApp = ({ user: initialUser, onLogout }) => {
  const [user, setUser] = useState(initialUser);
  const [activeTab, setActiveTab] = useState('home');
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [selectedLevel, setSelectedLevel] = useState(null);
  const [showLevelComplete, setShowLevelComplete] = useState(false);
  const [levelXP, setLevelXP] = useState(0);
  const [readingBook, setReadingBook] = useState(null);
  const [showRealMarket, setShowRealMarket] = useState(false);
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [activeLesson, setActiveLesson] = useState(null);

  // Check if user needs onboarding
  useEffect(() => {
    const hasCompletedOnboarding = localStorage.getItem('tradelingo_onboarding_complete');
    if (!hasCompletedOnboarding && user.xp < 10) {
      setShowOnboarding(true);
    }
  }, [user]);

  const handleOnboardingComplete = () => {
    localStorage.setItem('tradelingo_onboarding_complete', 'true');
    setShowOnboarding(false);
    toast.success('Bem-vindo ao TradeLingo! 🚀');
  };

  const handleStartLesson = (skill) => {
    // Get lessons for this skill
    const skillLessons = LESSON_DATA[skill.id];
    if (skillLessons && skillLessons.level1 && skillLessons.level1[0]) {
      setActiveLesson(skillLessons.level1[0]);
    } else {
      // Fallback: go to category
      toast.info('Em breve: mais lições para esta competência!');
    }
  };

  const handleLessonComplete = (result) => {
    // Update scores based on result
    if (result.correct) {
      toast.success(`+10 Precisão! ${result.answer === 'wait' ? '+5 Paciência!' : ''}`);
    }
    setActiveLesson(null);
    refreshUser();
  };

  const refreshUser = async () => {
    try {
      const response = await axios.get(`${API}/users/${user.id}`);
      localStorage.setItem('tradelingo_user', JSON.stringify(response.data));
      setUser(response.data);
    } catch (error) {
      console.error('Failed to refresh user');
    }
  };

  const handleCategorySelect = (category) => {
    setSelectedCategory(category);
    setSelectedLevel(null);
    setReadingBook(null);
  };

  const handleReadBook = (lesson) => {
    setReadingBook(lesson);
  };

  const handleFinishBook = () => {
    setReadingBook(null);
    // Force refresh to update bookRead state
  };

  const handleLevelSelect = (level) => {
    setSelectedLevel(level);
  };

  const handleExerciseComplete = (xpGained) => {
    setLevelXP(xpGained);
    setShowLevelComplete(true);
    refreshUser();
  };

  const handleLevelCompleteClose = () => {
    setShowLevelComplete(false);
    setSelectedLevel(null);
    setLevelXP(0);
  };

  const handleBackToHome = () => {
    setSelectedCategory(null);
    setSelectedLevel(null);
    setReadingBook(null);
    setShowRealMarket(false);
  };

  const handleBackToCategory = () => {
    setSelectedLevel(null);
    setReadingBook(null);
  };

  // Level Complete Modal
  if (showLevelComplete) {
    return (
      <LevelCompleteModal 
        xpGained={levelXP} 
        onContinue={handleLevelCompleteClose}
      />
    );
  }

  // Onboarding Flow for new users
  if (showOnboarding) {
    return (
      <OnboardingFlow 
        user={user}
        onComplete={handleOnboardingComplete}
      />
    );
  }

  // Active Lesson (5-step cycle)
  if (activeLesson) {
    return (
      <LessonCycle
        lesson={activeLesson}
        user={user}
        onComplete={handleLessonComplete}
      />
    );
  }

  // Real Market Zone
  if (showRealMarket) {
    return (
      <RealMarketZone
        user={user}
        onBack={handleBackToHome}
      />
    );
  }

  // Exercise Screen - Use Interactive for all chart_ categories
  if (selectedCategory && selectedLevel) {
    if (selectedCategory.id.startsWith('chart_')) {
      return (
        <InteractiveExerciseScreen
          category={selectedCategory}
          level={selectedLevel}
          user={user}
          onBack={handleBackToCategory}
          onComplete={handleExerciseComplete}
        />
      );
    }
    return (
      <ExerciseScreen
        category={selectedCategory}
        level={selectedLevel}
        user={user}
        onBack={handleBackToCategory}
        onComplete={handleExerciseComplete}
      />
    );
  }

  // Book Reader Screen - Full screen book reading
  if (selectedCategory && readingBook) {
    return (
      <BookReaderScreen
        category={selectedCategory}
        lesson={readingBook}
        onBack={handleBackToCategory}
        onFinish={handleFinishBook}
      />
    );
  }

  // Combined Category Screen (Book + Levels)
  if (selectedCategory) {
    return (
      <CategoryScreen
        category={selectedCategory}
        user={user}
        onBack={handleBackToHome}
        onLevelSelect={handleLevelSelect}
        onReadBook={handleReadBook}
      />
    );
  }

  return (
    <div className="min-h-screen bg-[#0d1117]" data-testid="main-app">
      <div className="max-w-lg mx-auto">
        {activeTab === 'home' && (
          <HomeScreen 
            user={user} 
            onCategorySelect={handleCategorySelect}
            onRealMarketClick={() => setShowRealMarket(true)}
            onStartLesson={handleStartLesson}
          />
        )}
        {activeTab === 'backtest' && (
          user.subscription === 'pro' ? (
            <AdvancedBacktest
              user={user}
              onBack={() => setActiveTab('home')}
            />
          ) : (
            <ProUpgradeScreen
              user={user}
              onUpgrade={() => {
                refreshUser();
                setActiveTab('backtest');
              }}
              onBack={() => setActiveTab('home')}
            />
          )
        )}
        {activeTab === 'journal' && <JournalScreen user={user} />}
        {activeTab === 'profile' && (
          <ProfileScreen
            user={user}
            onLogout={onLogout}
            onUserUpdate={setUser}
          />
        )}
        <BottomNav activeTab={activeTab} setActiveTab={setActiveTab} />
      </div>
    </div>
  );
};

// ==================== APP WRAPPER ====================

// ==================== EMAIL VERIFICATION PAGE ====================

const VerifyEmailPage = ({ onVerified }) => {
  const [status, setStatus] = useState('verifying'); // verifying, success, error
  const [message, setMessage] = useState('');

  useEffect(() => {
    const verifyEmail = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const token = urlParams.get('token');

      if (!token) {
        setStatus('error');
        setMessage('No verification token found');
        return;
      }

      try {
        const response = await axios.post(`${API}/auth/verify-email`, { token });
        setStatus('success');
        setMessage(response.data.message);
        
        // Auto-login after verification
        if (response.data.user) {
          localStorage.setItem('tradelingo_user', JSON.stringify(response.data.user));
          setTimeout(() => {
            onVerified(response.data.user);
          }, 2000);
        }
      } catch (error) {
        setStatus('error');
        setMessage(getErrorMessage(error, 'Verification failed'));
      }
    };

    verifyEmail();
  }, [onVerified]);

  return (
    <div className="min-h-screen bg-[#0A0A0A] flex items-center justify-center p-4" data-testid="verify-email-page">
      <div className="w-full max-w-md text-center">
        {status === 'verifying' && (
          <>
            <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-[#58CC02] mx-auto mb-4"></div>
            <h2 className="text-2xl font-bold text-white">Verifying your email...</h2>
            <p className="text-gray-400 mt-2">Please wait a moment</p>
          </>
        )}

        {status === 'success' && (
          <>
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-[#58CC02] mb-4">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-white">Email Verified!</h2>
            <p className="text-gray-400 mt-2">{message}</p>
            <p className="text-[#58CC02] mt-4">Redirecting to dashboard...</p>
          </>
        )}

        {status === 'error' && (
          <>
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-red-500 mb-4">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-white">Verification Failed</h2>
            <p className="text-gray-400 mt-2">{message}</p>
            <button
              onClick={() => window.location.href = '/'}
              className="mt-6 bg-[#58CC02] hover:bg-[#4CAF00] text-white font-bold py-3 px-6 rounded-lg transition-colors"
            >
              Go to Login
            </button>
          </>
        )}
      </div>
    </div>
  );
};

// ==================== ADMIN PANEL ====================

const AdminPanel = ({ onLogout }) => {
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [pagination, setPagination] = useState({});
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchData();
  }, [page, search]);

  const fetchData = async () => {
    try {
      const [statsRes, usersRes] = await Promise.all([
        axios.get(`${API}/admin/stats`),
        axios.get(`${API}/admin/users`, { params: { page, limit: 20, search: search || undefined } })
      ]);
      setStats(statsRes.data);
      setUsers(usersRes.data.users);
      setPagination(usersRes.data.pagination);
    } catch (error) {
      toast.error('Failed to load admin data');
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyUser = async (userId) => {
    try {
      await axios.post(`${API}/admin/users/${userId}/verify`);
      toast.success('User verified!');
      fetchData();
    } catch (error) {
      toast.error('Failed to verify user');
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user?')) return;
    try {
      await axios.delete(`${API}/admin/users/${userId}`);
      toast.success('User deleted');
      fetchData();
    } catch (error) {
      toast.error('Failed to delete user');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0A0A0A] flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#58CC02]"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0A0A0A] p-6" data-testid="admin-panel">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white">Admin Dashboard</h1>
          <p className="text-gray-400">Manage users and view statistics</p>
        </div>
        <button
          onClick={onLogout}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors"
        >
          Logout
        </button>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-[#1A1A1A] rounded-xl p-6">
            <p className="text-gray-400 text-sm">Total Users</p>
            <p className="text-3xl font-bold text-white">{stats.users.total}</p>
          </div>
          <div className="bg-[#1A1A1A] rounded-xl p-6">
            <p className="text-gray-400 text-sm">Verified Users</p>
            <p className="text-3xl font-bold text-[#58CC02]">{stats.users.verified}</p>
          </div>
          <div className="bg-[#1A1A1A] rounded-xl p-6">
            <p className="text-gray-400 text-sm">Pending Verification</p>
            <p className="text-3xl font-bold text-yellow-500">{stats.users.unverified}</p>
          </div>
          <div className="bg-[#1A1A1A] rounded-xl p-6">
            <p className="text-gray-400 text-sm">Signups (7 days)</p>
            <p className="text-3xl font-bold text-blue-500">{stats.users.recent_signups_7d}</p>
          </div>
        </div>
      )}

      {/* Subscription Stats */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-[#1A1A1A] rounded-xl p-4 flex items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-gray-600 flex items-center justify-center">
              <span className="text-lg">🆓</span>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Free Users</p>
              <p className="text-xl font-bold text-white">{stats.subscriptions.free}</p>
            </div>
          </div>
          <div className="bg-[#1A1A1A] rounded-xl p-4 flex items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-blue-600 flex items-center justify-center">
              <span className="text-lg">⭐</span>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Standard Users</p>
              <p className="text-xl font-bold text-white">{stats.subscriptions.standard}</p>
            </div>
          </div>
          <div className="bg-[#1A1A1A] rounded-xl p-4 flex items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-purple-600 flex items-center justify-center">
              <span className="text-lg">👑</span>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Pro Users</p>
              <p className="text-xl font-bold text-white">{stats.subscriptions.pro}</p>
            </div>
          </div>
        </div>
      )}

      {/* Users Table */}
      <div className="bg-[#1A1A1A] rounded-xl p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-white">Users</h2>
          <input
            type="text"
            placeholder="Search by email or username..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="bg-[#0A0A0A] border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-[#58CC02] w-64"
          />
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="text-left text-gray-400 border-b border-gray-700">
                <th className="pb-3 px-2">Username</th>
                <th className="pb-3 px-2">Email</th>
                <th className="pb-3 px-2">Status</th>
                <th className="pb-3 px-2">XP</th>
                <th className="pb-3 px-2">Rank</th>
                <th className="pb-3 px-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id} className="border-b border-gray-800 text-white">
                  <td className="py-3 px-2">{user.username}</td>
                  <td className="py-3 px-2 text-gray-400">{user.email}</td>
                  <td className="py-3 px-2">
                    {user.is_verified ? (
                      <span className="bg-green-500/20 text-green-500 px-2 py-1 rounded text-sm">Verified</span>
                    ) : (
                      <span className="bg-yellow-500/20 text-yellow-500 px-2 py-1 rounded text-sm">Pending</span>
                    )}
                  </td>
                  <td className="py-3 px-2">{user.xp}</td>
                  <td className="py-3 px-2 text-[#58CC02]">{user.rank}</td>
                  <td className="py-3 px-2">
                    <div className="flex gap-2">
                      {!user.is_verified && (
                        <button
                          onClick={() => handleVerifyUser(user.id)}
                          className="text-green-500 hover:text-green-400 text-sm"
                        >
                          Verify
                        </button>
                      )}
                      <button
                        onClick={() => handleDeleteUser(user.id)}
                        className="text-red-500 hover:text-red-400 text-sm"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="flex justify-between items-center mt-4 text-gray-400">
          <span>Page {pagination.page} of {pagination.pages}</span>
          <div className="flex gap-2">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="px-3 py-1 bg-[#0A0A0A] rounded disabled:opacity-50"
            >
              Previous
            </button>
            <button
              onClick={() => setPage(p => Math.min(pagination.pages, p + 1))}
              disabled={page === pagination.pages}
              className="px-3 py-1 bg-[#0A0A0A] rounded disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// ==================== ADMIN LOGIN ====================

const AdminLogin = ({ onAdminLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post(`${API}/admin/login`, { email, password });
      if (response.data.success) {
        onAdminLogin(response.data);
        toast.success('Welcome, Admin!');
      }
    } catch (error) {
      toast.error(getErrorMessage(error, 'Invalid admin credentials'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0A0A0A] flex items-center justify-center p-4" data-testid="admin-login">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white">Admin Login</h1>
          <p className="text-gray-400 mt-2">TradeLingo Admin Panel</p>
        </div>

        <div className="bg-[#1A1A1A] rounded-2xl p-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm text-gray-400 mb-2">Admin Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-[#0A0A0A] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-[#58CC02]"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-[#0A0A0A] border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-[#58CC02]"
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-[#58CC02] hover:bg-[#4CAF00] text-white font-bold py-3 rounded-lg transition-colors disabled:opacity-50"
            >
              {loading ? 'Logging in...' : 'Login as Admin'}
            </button>
          </form>
          <div className="mt-4 text-center">
            <a href="/" className="text-gray-400 hover:text-white text-sm">
              Back to User Login
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    // Check for saved user session
    const savedUser = localStorage.getItem('tradelingo_user');
    const savedAdmin = localStorage.getItem('tradelingo_admin');
    
    if (savedAdmin) {
      setIsAdmin(true);
      setLoading(false);
      return;
    }
    
    if (savedUser) {
      try {
        const userData = JSON.parse(savedUser);
        // Verify user still exists
        axios.get(`${API}/users/${userData.id}`)
          .then(response => {
            setUser(response.data);
            localStorage.setItem('tradelingo_user', JSON.stringify(response.data));
          })
          .catch(() => {
            localStorage.removeItem('tradelingo_user');
          })
          .finally(() => setLoading(false));
      } catch (e) {
        localStorage.removeItem('tradelingo_user');
        setLoading(false);
      }
    } else {
      setLoading(false);
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('tradelingo_user');
    localStorage.removeItem('tradelingo_admin');
    setUser(null);
    setIsAdmin(false);
    toast.success('Logged out successfully');
  };

  const handleAdminLogin = (adminData) => {
    localStorage.setItem('tradelingo_admin', JSON.stringify(adminData));
    setIsAdmin(true);
  };

  const handleVerified = (userData) => {
    setUser(userData);
    // Clear URL params
    window.history.replaceState({}, document.title, '/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0A0A0A] flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#58CC02]"></div>
      </div>
    );
  }

  // Check for verification token in URL
  const urlParams = new URLSearchParams(window.location.search);
  const verifyToken = urlParams.get('token');
  const isVerifyPage = window.location.pathname === '/verify' || verifyToken;
  
  // Check for admin page
  const isAdminPage = window.location.pathname === '/admin';

  // Handle verification page
  if (isVerifyPage && !user) {
    return (
      <div className="App">
        <Toaster position="top-center" richColors />
        <VerifyEmailPage onVerified={handleVerified} />
      </div>
    );
  }

  // Handle admin pages
  if (isAdminPage) {
    return (
      <div className="App">
        <Toaster position="top-center" richColors />
        {isAdmin ? (
          <AdminPanel onLogout={handleLogout} />
        ) : (
          <AdminLogin onAdminLogin={handleAdminLogin} />
        )}
      </div>
    );
  }

  return (
    <div className="App">
      <Toaster position="top-center" richColors />
      {user ? (
        <MainApp user={user} onLogout={handleLogout} />
      ) : (
        <AuthScreen onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;
