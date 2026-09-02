'use client'

import React, { useState, useEffect, useRef } from 'react'

export function PasswordGate({ password = 'Suvishal', children }) {
  const [unlocked, setUnlocked] = useState(false)
  const [inputVal, setInputVal] = useState('')
  const [error, setError] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [mounted, setMounted] = useState(false)
  const [shaking, setShaking] = useState(false)
  const [unlocking, setUnlocking] = useState(false)
  const [focused, setFocused] = useState(false)
  const inputRef = useRef(null)

  const storageKey = `auth_gate_${password.toLowerCase()}`

  useEffect(() => {
    setMounted(true)
    const storedAuth = typeof window !== 'undefined' ? sessionStorage.getItem(storageKey) : null
    if (storedAuth === 'true') setUnlocked(true)
  }, [storageKey])

  const handleUnlock = (e) => {
    if (e) e.preventDefault()
    if (inputVal.trim() === password) {
      setUnlocking(true)
      setTimeout(() => {
        setUnlocked(true)
        setError('')
        if (typeof window !== 'undefined') sessionStorage.setItem(storageKey, 'true')
      }, 600)
    } else {
      setError('Incorrect password. Please try again.')
      setShaking(true)
      setTimeout(() => setShaking(false), 600)
    }
  }

  const handleLock = () => {
    setUnlocked(false)
    setInputVal('')
    setError('')
    setUnlocking(false)
    if (typeof window !== 'undefined') sessionStorage.removeItem(storageKey)
  }

  if (!mounted) {
    return (
      <div style={{
        padding: '4rem',
        textAlign: 'center',
        color: '#7a7f99',
        fontFamily: "'Inter', sans-serif",
        fontSize: '0.9rem',
      }}>
        <div style={{
          width: '32px',
          height: '32px',
          border: '2px solid rgba(79,142,247,0.3)',
          borderTopColor: '#4f8ef7',
          borderRadius: '50%',
          margin: '0 auto 1rem',
          animation: 'spin-slow 0.8s linear infinite',
        }} />
        Loading preparation guide...
      </div>
    )
  }

  if (!unlocked) {
    return (
      <>
        <style>{`
          @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to   { opacity: 1; transform: translateY(0); }
          }
          @keyframes pulse-ring {
            0%   { transform: scale(1); opacity: 0.6; }
            50%  { transform: scale(1.15); opacity: 0.2; }
            100% { transform: scale(1); opacity: 0.6; }
          }
          @keyframes shake {
            0%, 100% { transform: translateX(0); }
            20%       { transform: translateX(-8px); }
            40%       { transform: translateX(8px); }
            60%       { transform: translateX(-5px); }
            80%       { transform: translateX(5px); }
          }
          @keyframes shimmer {
            0%   { background-position: -200% center; }
            100% { background-position: 200% center; }
          }
          @keyframes unlockPop {
            0%   { transform: scale(1); }
            40%  { transform: scale(1.08); }
            100% { transform: scale(1); opacity: 0; }
          }
          @keyframes spin-slow {
            from { transform: rotate(0deg); }
            to   { transform: rotate(360deg); }
          }
          @keyframes float {
            0%, 100% { transform: translateY(0); }
            50%       { transform: translateY(-5px); }
          }
          .pg-input:focus {
            outline: none !important;
            border-color: #4f8ef7 !important;
            box-shadow: 0 0 0 3px rgba(79,142,247,0.15) !important;
          }
          .pg-btn:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 24px rgba(79,142,247,0.45) !important;
          }
          .pg-btn:active {
            transform: translateY(0) !important;
          }
        `}</style>

        <div style={{
          minHeight: '60vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '2rem',
          animation: 'fadeInUp 0.5s ease both',
        }}>
          <div style={{
            width: '100%',
            maxWidth: '480px',
            borderRadius: '1.5rem',
            background: 'linear-gradient(145deg, rgba(17,18,32,0.95) 0%, rgba(19,21,31,0.98) 100%)',
            border: '1px solid rgba(255,255,255,0.09)',
            boxShadow: '0 24px 80px -16px rgba(0,0,0,0.6), 0 0 0 1px rgba(79,142,247,0.06)',
            padding: '2.75rem 2.5rem',
            textAlign: 'center',
            fontFamily: "'Inter', sans-serif",
            position: 'relative',
            overflow: 'hidden',
            animation: unlocking ? 'unlockPop 0.6s ease forwards' : 'none',
          }}>

            {/* Top gradient line */}
            <div style={{
              position: 'absolute',
              top: 0,
              left: '15%',
              right: '15%',
              height: '1px',
              background: 'linear-gradient(90deg, transparent, rgba(79,142,247,0.7), rgba(124,106,245,0.7), transparent)',
            }} />

            {/* BG orb */}
            <div style={{
              position: 'absolute',
              top: '-60px',
              right: '-60px',
              width: '200px',
              height: '200px',
              borderRadius: '50%',
              background: 'radial-gradient(circle, rgba(124,106,245,0.08) 0%, transparent 70%)',
              pointerEvents: 'none',
            }} />

            {/* Lock icon with pulse ring */}
            <div style={{
              position: 'relative',
              width: '72px',
              height: '72px',
              margin: '0 auto 1.75rem',
              animation: 'float 3s ease-in-out infinite',
            }}>
              <div style={{
                position: 'absolute',
                inset: '-8px',
                borderRadius: '50%',
                border: '1.5px solid rgba(79,142,247,0.3)',
                animation: 'pulse-ring 2.5s ease-in-out infinite',
              }} />
              <div style={{
                width: '72px',
                height: '72px',
                borderRadius: '20px',
                background: 'linear-gradient(135deg, rgba(79,142,247,0.15) 0%, rgba(124,106,245,0.15) 100%)',
                border: '1px solid rgba(79,142,247,0.3)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 8px 24px rgba(79,142,247,0.2)',
              }}>
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                  <rect x="3" y="11" width="18" height="11" rx="2.5" stroke="#4f8ef7" strokeWidth="1.5"/>
                  <path d="M7 11V7a5 5 0 0110 0v4" stroke="#7c6af5" strokeWidth="1.5" strokeLinecap="round"/>
                  <circle cx="12" cy="16" r="1.5" fill="#4f8ef7"/>
                  <line x1="12" y1="17.5" x2="12" y2="19.5" stroke="#4f8ef7" strokeWidth="1.5" strokeLinecap="round"/>
                </svg>
              </div>
            </div>

            {/* Title */}
            <h2 style={{
              fontSize: '1.4rem',
              fontWeight: '700',
              color: '#f0f2ff',
              margin: '0 0 0.5rem',
              letterSpacing: '-0.03em',
            }}>
              Protected Guide
            </h2>

            <p style={{
              fontSize: '0.875rem',
              color: '#7a7f99',
              margin: '0 0 2rem',
              lineHeight: '1.6',
              WebkitTextFillColor: '#7a7f99',
            }}>
              This material for <strong style={{ color: '#c4c9e2', WebkitTextFillColor: '#c4c9e2' }}>Suvishal Kalakoti</strong> is password-protected.
              Enter your access key to continue.
            </p>

            <form onSubmit={handleUnlock} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {/* Input wrapper */}
              <div style={{
                position: 'relative',
                animation: shaking ? 'shake 0.5s ease' : 'none',
              }}>
                <input
                  ref={inputRef}
                  className="pg-input"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Enter access password..."
                  value={inputVal}
                  onChange={(e) => {
                    setInputVal(e.target.value)
                    if (error) setError('')
                  }}
                  onFocus={() => setFocused(true)}
                  onBlur={() => setFocused(false)}
                  autoFocus
                  style={{
                    width: '100%',
                    padding: '0.9rem 3.5rem 0.9rem 1.2rem',
                    borderRadius: '0.75rem',
                    border: error
                      ? '1.5px solid rgba(239,68,68,0.6)'
                      : '1.5px solid rgba(255,255,255,0.1)',
                    background: 'rgba(0,0,0,0.3)',
                    color: '#f0f2ff',
                    fontSize: '0.975rem',
                    boxSizing: 'border-box',
                    fontFamily: "'Inter', sans-serif",
                    transition: 'all 0.2s ease',
                    letterSpacing: showPassword ? '0' : '0.1em',
                  }}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                  style={{
                    position: 'absolute',
                    right: '0.9rem',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    background: 'none',
                    border: 'none',
                    color: '#7a7f99',
                    cursor: 'pointer',
                    fontSize: '0.8rem',
                    fontWeight: '500',
                    padding: '0.25rem',
                    fontFamily: "'Inter', sans-serif",
                    transition: 'color 0.15s ease',
                  }}
                >
                  {showPassword ? 'Hide' : 'Show'}
                </button>
              </div>

              {/* Error */}
              {error && (
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.4rem',
                  color: '#f87171',
                  fontSize: '0.82rem',
                  fontWeight: '500',
                  textAlign: 'left',
                  padding: '0.6rem 0.85rem',
                  background: 'rgba(239,68,68,0.08)',
                  border: '1px solid rgba(239,68,68,0.2)',
                  borderRadius: '0.5rem',
                }}>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="12" r="10" stroke="#f87171" strokeWidth="1.5"/>
                    <line x1="12" y1="8" x2="12" y2="12" stroke="#f87171" strokeWidth="1.5" strokeLinecap="round"/>
                    <circle cx="12" cy="16" r="1" fill="#f87171"/>
                  </svg>
                  {error}
                </div>
              )}

              {/* Submit button */}
              <button
                className="pg-btn"
                type="submit"
                style={{
                  padding: '0.9rem 1.5rem',
                  borderRadius: '0.75rem',
                  border: 'none',
                  background: 'linear-gradient(135deg, #4f8ef7 0%, #7c6af5 100%)',
                  backgroundSize: '200% auto',
                  color: '#ffffff',
                  fontSize: '0.975rem',
                  fontWeight: '600',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  boxShadow: '0 4px 16px rgba(79,142,247,0.35)',
                  fontFamily: "'Inter', sans-serif",
                  letterSpacing: '-0.01em',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '0.5rem',
                }}
              >
                {unlocking ? (
                  <>
                    <div style={{
                      width: '16px',
                      height: '16px',
                      border: '2px solid rgba(255,255,255,0.3)',
                      borderTopColor: '#fff',
                      borderRadius: '50%',
                      animation: 'spin-slow 0.7s linear infinite',
                    }} />
                    Unlocking...
                  </>
                ) : (
                  <>
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
                      <path d="M12 2L3 7v5c0 5.25 3.75 10.15 9 11.35C17.25 22.15 21 17.25 21 12V7L12 2Z" fill="white" fillOpacity="0.8"/>
                      <path d="M9 12l2 2 4-4" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    Unlock Preparation Guide
                  </>
                )}
              </button>
            </form>

            {/* Bottom note */}
            <div style={{
              marginTop: '1.75rem',
              paddingTop: '1.25rem',
              borderTop: '1px solid rgba(255,255,255,0.06)',
              fontSize: '0.75rem',
              color: '#4a4f6a',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.4rem',
            }}>
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none">
                <rect x="3" y="11" width="18" height="11" rx="2" stroke="#4a4f6a" strokeWidth="1.5"/>
                <path d="M7 11V7a5 5 0 0110 0v4" stroke="#4a4f6a" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
              Protected candidate preparation suite · PrepSuite
            </div>
          </div>
        </div>
      </>
    )
  }

  // Unlocked view
  return (
    <div>
      <div style={{
        display: 'flex',
        justifyContent: 'flex-end',
        marginBottom: '1.25rem',
      }}>
        <button
          onClick={handleLock}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.4rem',
            padding: '0.4rem 0.875rem',
            borderRadius: '0.5rem',
            border: '1px solid rgba(255,255,255,0.1)',
            background: 'rgba(255,255,255,0.04)',
            color: '#7a7f99',
            fontSize: '0.8rem',
            cursor: 'pointer',
            fontFamily: "'Inter', sans-serif",
            fontWeight: '500',
            transition: 'all 0.15s ease',
          }}
        >
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none">
            <rect x="3" y="11" width="18" height="11" rx="2" stroke="#7a7f99" strokeWidth="1.5"/>
            <path d="M7 11V7a5 5 0 0110 0v4" stroke="#7a7f99" strokeWidth="1.5" strokeLinecap="round"/>
          </svg>
          Lock Guide
        </button>
      </div>
      {children}
    </div>
  )
}
