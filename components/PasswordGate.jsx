'use client'

import React, { useState, useEffect } from 'react'

export function PasswordGate({ password = 'Suvishal', children }) {
  const [unlocked, setUnlocked] = useState(false)
  const [inputVal, setInputVal] = useState('')
  const [error, setError] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [mounted, setMounted] = useState(false)

  const storageKey = `auth_gate_${password.toLowerCase()}`

  useEffect(() => {
    setMounted(true)
    const storedAuth = typeof window !== 'undefined' ? sessionStorage.getItem(storageKey) : null
    if (storedAuth === 'true') {
      setUnlocked(true)
    }
  }, [storageKey])

  const handleUnlock = (e) => {
    if (e) e.preventDefault()
    if (inputVal.trim() === password) {
      setUnlocked(true)
      setError('')
      if (typeof window !== 'undefined') {
        sessionStorage.setItem(storageKey, 'true')
      }
    } else {
      setError('Incorrect password. Please try again.')
    }
  }

  const handleLock = () => {
    setUnlocked(false)
    setInputVal('')
    setError('')
    if (typeof window !== 'undefined') {
      sessionStorage.removeItem(storageKey)
    }
  }

  if (!mounted) {
    return (
      <div style={{ padding: '3rem', textAlign: 'center', color: '#6b7280' }}>
        Loading preparation guide...
      </div>
    )
  }

  if (!unlocked) {
    return (
      <div style={{
        maxWidth: '540px',
        margin: '4rem auto',
        padding: '2.5rem',
        borderRadius: '1rem',
        background: 'linear-gradient(145deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%)',
        border: '1px solid rgba(255, 255, 255, 0.12)',
        boxShadow: '0 20px 40px -15px rgba(0, 0, 0, 0.3)',
        backdropFilter: 'blur(10px)',
        textAlign: 'center',
        fontFamily: 'inherit'
      }}>
        <div style={{
          fontSize: '3rem',
          marginBottom: '1rem',
          display: 'inline-block',
          filter: 'drop-shadow(0 4px 10px rgba(59, 130, 246, 0.3))'
        }}>
          🔒
        </div>
        
        <h2 style={{
          fontSize: '1.5rem',
          fontWeight: '700',
          marginBottom: '0.5rem',
          letterSpacing: '-0.025em'
        }}>
          Restricted Preparation Material
        </h2>
        
        <p style={{
          fontSize: '0.925rem',
          color: '#9ca3af',
          marginBottom: '2rem',
          lineHeight: '1.5'
        }}>
          This preparation guide for <strong>Suvishal Kalakoti (Operations Analyst)</strong> is protected. Please enter the access password to continue.
        </p>

        <form onSubmit={handleUnlock} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ position: 'relative', width: '100%' }}>
            <input
              type={showPassword ? 'text' : 'password'}
              placeholder="Enter password..."
              value={inputVal}
              onChange={(e) => {
                setInputVal(e.target.value)
                if (error) setError('')
              }}
              style={{
                width: '100%',
                padding: '0.85rem 3rem 0.85rem 1.1rem',
                borderRadius: '0.625rem',
                border: error ? '1.5px solid #ef4444' : '1px solid rgba(255, 255, 255, 0.2)',
                background: 'rgba(0, 0, 0, 0.25)',
                color: '#f3f4f6',
                fontSize: '1rem',
                outline: 'none',
                boxSizing: 'border-box'
              }}
              autoFocus
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              aria-label={showPassword ? "Hide password" : "Show password"}
              style={{
                position: 'absolute',
                right: '0.85rem',
                top: '50%',
                transform: 'translateY(-50%)',
                background: 'none',
                border: 'none',
                color: '#9ca3af',
                cursor: 'pointer',
                fontSize: '0.85rem'
              }}
            >
              {showPassword ? 'Hide' : 'Show'}
            </button>
          </div>

          {error && (
            <div style={{
              color: '#f87171',
              fontSize: '0.875rem',
              textAlign: 'left',
              fontWeight: '500'
            }}>
              ⚠️ {error}
            </div>
          )}

          <button
            type="submit"
            style={{
              padding: '0.85rem 1.5rem',
              borderRadius: '0.625rem',
              border: 'none',
              background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)',
              color: '#ffffff',
              fontSize: '1rem',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
              boxShadow: '0 4px 12px rgba(37, 99, 235, 0.35)'
            }}
          >
            Unlock Preparation Guide
          </button>
        </form>

        <div style={{
          marginTop: '1.75rem',
          paddingTop: '1.25rem',
          borderTop: '1px solid rgba(255, 255, 255, 0.08)',
          fontSize: '0.8rem',
          color: '#6b7280'
        }}>
          Protected candidate preparation suite
        </div>
      </div>
    )
  }

  return (
    <div>
      <div style={{
        display: 'flex',
        justifyContent: 'flex-end',
        marginBottom: '1rem'
      }}>
        <button
          onClick={handleLock}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.4rem',
            padding: '0.4rem 0.85rem',
            borderRadius: '0.5rem',
            border: '1px solid rgba(255, 255, 255, 0.15)',
            background: 'rgba(255, 255, 255, 0.05)',
            color: '#9ca3af',
            fontSize: '0.825rem',
            cursor: 'pointer'
          }}
        >
          🔒 Lock Guide
        </button>
      </div>
      {children}
    </div>
  )
}
