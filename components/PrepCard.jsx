'use client'

import { useState } from 'react'

export function PrepCard({ name, role, company, tags = [], href, locked = false }) {
  const [hovered, setHovered] = useState(false)

  return (
    <a
      href={href}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        display: 'block',
        textDecoration: 'none',
        borderRadius: '1rem',
        border: `1px solid ${hovered ? 'rgba(79,142,247,0.35)' : 'rgba(255,255,255,0.07)'}`,
        background: hovered
          ? 'linear-gradient(145deg, #151723 0%, #1a1c2a 100%)'
          : 'linear-gradient(145deg, #111218 0%, #13151f 100%)',
        padding: '1.5rem',
        transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
        transform: hovered ? 'translateY(-4px)' : 'translateY(0)',
        boxShadow: hovered
          ? '0 12px 40px -8px rgba(79,142,247,0.2), 0 4px 16px -4px rgba(0,0,0,0.4)'
          : '0 4px 16px -4px rgba(0,0,0,0.3)',
        position: 'relative',
        overflow: 'hidden',
        cursor: 'pointer',
      }}
    >
      {/* Top glow line */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: '10%',
        right: '10%',
        height: '1px',
        background: 'linear-gradient(90deg, transparent, rgba(79,142,247,0.6), transparent)',
        opacity: hovered ? 1 : 0,
        transition: 'opacity 0.25s ease',
      }} />

      {/* Header row */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        marginBottom: '1rem',
      }}>
        {/* Avatar */}
        <div style={{
          width: '44px',
          height: '44px',
          borderRadius: '12px',
          background: 'linear-gradient(135deg, #4f8ef7 0%, #7c6af5 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '1.1rem',
          fontWeight: '700',
          color: 'white',
          flexShrink: 0,
          boxShadow: '0 4px 12px rgba(79,142,247,0.3)',
          fontFamily: "'Inter', sans-serif",
        }}>
          {name.charAt(0).toUpperCase()}
        </div>

        {/* Lock badge */}
        {locked && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.3rem',
            padding: '0.25rem 0.6rem',
            borderRadius: '6px',
            background: 'rgba(124,106,245,0.1)',
            border: '1px solid rgba(124,106,245,0.25)',
            fontSize: '0.7rem',
            fontWeight: '600',
            color: '#7c6af5',
            letterSpacing: '0.04em',
            textTransform: 'uppercase',
          }}>
            🔐 Protected
          </div>
        )}
      </div>

      {/* Name */}
      <div style={{
        fontSize: '1.05rem',
        fontWeight: '700',
        color: '#f0f2ff',
        marginBottom: '0.25rem',
        letterSpacing: '-0.02em',
        fontFamily: "'Inter', sans-serif",
      }}>
        {name}
      </div>

      {/* Role */}
      <div style={{
        fontSize: '0.875rem',
        color: '#4f8ef7',
        fontWeight: '500',
        marginBottom: '0.15rem',
        fontFamily: "'Inter', sans-serif",
      }}>
        {role}
      </div>

      {/* Company */}
      <div style={{
        fontSize: '0.8rem',
        color: '#7a7f99',
        marginBottom: '1.1rem',
        fontFamily: "'Inter', sans-serif",
      }}>
        {company}
      </div>

      {/* Divider */}
      <div style={{
        height: '1px',
        background: 'rgba(255,255,255,0.06)',
        marginBottom: '1rem',
      }} />

      {/* Tags */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
        {tags.map((tag) => (
          <span key={tag} style={{
            fontSize: '0.72rem',
            fontWeight: '600',
            color: '#2dd4bf',
            background: 'rgba(45,212,191,0.08)',
            border: '1px solid rgba(45,212,191,0.2)',
            padding: '0.2rem 0.55rem',
            borderRadius: '5px',
            letterSpacing: '0.02em',
            fontFamily: "'Inter', sans-serif",
          }}>
            {tag}
          </span>
        ))}
      </div>

      {/* Arrow */}
      <div style={{
        position: 'absolute',
        bottom: '1.25rem',
        right: '1.25rem',
        width: '28px',
        height: '28px',
        borderRadius: '8px',
        background: hovered ? 'rgba(79,142,247,0.2)' : 'rgba(255,255,255,0.04)',
        border: '1px solid rgba(79,142,247,0.25)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        transition: 'all 0.25s ease',
        transform: hovered ? 'translate(2px, -2px)' : 'translate(0,0)',
      }}>
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
          <path d="M7 17L17 7M17 7H7M17 7v10" stroke={hovered ? '#4f8ef7' : '#7a7f99'} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </div>
    </a>
  )
}
