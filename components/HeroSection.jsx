'use client'

export function HeroSection() {
  return (
    <div style={{
      position: 'relative',
      overflow: 'hidden',
      borderRadius: '1.25rem',
      marginBottom: '2.5rem',
      padding: '4rem 2.5rem 3.5rem',
      background: 'linear-gradient(145deg, #0d0f1a 0%, #111220 50%, #0a0b0f 100%)',
      border: '1px solid rgba(255,255,255,0.07)',
      boxShadow: '0 4px 40px -8px rgba(0,0,0,0.6)',
    }}>
      {/* Background glow orbs */}
      <div style={{
        position: 'absolute',
        top: '-60px',
        right: '-40px',
        width: '320px',
        height: '320px',
        borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(124,106,245,0.15) 0%, transparent 70%)',
        pointerEvents: 'none',
      }} />
      <div style={{
        position: 'absolute',
        bottom: '-80px',
        left: '-60px',
        width: '400px',
        height: '400px',
        borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(79,142,247,0.1) 0%, transparent 70%)',
        pointerEvents: 'none',
      }} />

      {/* Badge */}
      <div style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '0.4rem',
        padding: '0.3rem 0.85rem',
        borderRadius: '99px',
        border: '1px solid rgba(79,142,247,0.35)',
        background: 'rgba(79,142,247,0.08)',
        marginBottom: '1.5rem',
        fontSize: '0.75rem',
        fontWeight: '600',
        color: '#4f8ef7',
        letterSpacing: '0.04em',
        textTransform: 'uppercase',
        animation: 'fadeInUp 0.6s ease both',
      }}>
        <span style={{
          width: '6px',
          height: '6px',
          borderRadius: '50%',
          background: '#4f8ef7',
          boxShadow: '0 0 6px #4f8ef7',
          animation: 'pulse-glow 2s ease-in-out infinite',
        }} />
        Powered by agents-maker
      </div>

      {/* Headline */}
      <h1 style={{
        fontSize: 'clamp(2rem, 5vw, 3.2rem)',
        fontWeight: '800',
        letterSpacing: '-0.04em',
        lineHeight: '1.1',
        margin: '0 0 1rem 0',
        background: 'linear-gradient(135deg, #f0f2ff 0%, #4f8ef7 45%, #7c6af5 80%, #2dd4bf 100%)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        backgroundClip: 'text',
        animation: 'fadeInUp 0.6s ease 0.1s both',
        maxWidth: '700px',
      }}>
        Your Interview,<br />Engineered.
      </h1>

      {/* Subheadline */}
      <p style={{
        fontSize: '1.1rem',
        color: '#9ca3c4',
        maxWidth: '520px',
        lineHeight: '1.7',
        margin: '0 0 2.5rem 0',
        animation: 'fadeInUp 0.6s ease 0.2s both',
        WebkitTextFillColor: '#9ca3c4',
      }}>
        AI-structured preparation guides for high-stakes interviews.
        Every Q&A, system design, and behavioral answer — built to land the offer.
      </p>

      {/* Stat pills */}
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: '0.75rem',
        animation: 'fadeInUp 0.6s ease 0.3s both',
      }}>
        {[
          { icon: '📚', label: '10+ Active Guides' },
          { icon: '💬', label: '300+ Deep-Dive Q&As' },
          { icon: '🏗️', label: 'System Design Breakdowns' },
          { icon: '🔐', label: 'Private Access Only' },
        ].map((stat, i) => (
          <div key={i} style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.45rem',
            padding: '0.45rem 0.9rem',
            borderRadius: '8px',
            background: 'rgba(255,255,255,0.04)',
            border: '1px solid rgba(255,255,255,0.07)',
            fontSize: '0.82rem',
            color: '#c4c9e2',
            fontWeight: '500',
          }}>
            <span>{stat.icon}</span>
            <span>{stat.label}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
