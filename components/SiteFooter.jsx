export function SiteFooter() {
  return (
    <div style={{
      width: '100%',
      padding: '2.5rem 2rem 1.5rem',
      borderTop: '1px solid rgba(255,255,255,0.07)',
      background: 'rgba(10,11,15,0.6)',
      display: 'flex',
      flexDirection: 'column',
      gap: '1.5rem',
      fontFamily: "'Inter', sans-serif",
    }}>
      {/* Top row */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        flexWrap: 'wrap',
        gap: '1.5rem',
      }}>
        {/* Brand */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <div style={{
              width: '24px',
              height: '24px',
              borderRadius: '6px',
              background: 'linear-gradient(135deg, #4f8ef7 0%, #7c6af5 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}>
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
                <path d="M12 2L3 7v5c0 5.25 3.75 10.15 9 11.35C17.25 22.15 21 17.25 21 12V7L12 2Z" fill="white" fillOpacity="0.9"/>
                <path d="M9 12l2 2 4-4" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <span style={{
              fontSize: '0.95rem',
              fontWeight: '700',
              background: 'linear-gradient(135deg, #f0f2ff 0%, #4f8ef7 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
            }}>PrepSuite</span>
          </div>
          <p style={{
            fontSize: '0.8rem',
            color: '#7a7f99',
            margin: 0,
            maxWidth: '240px',
            lineHeight: '1.5',
          }}>
            Interview preparation — engineered for outcomes.
          </p>
        </div>

        {/* Powered by badge */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          padding: '0.5rem 0.875rem',
          borderRadius: '8px',
          border: '1px solid rgba(255,255,255,0.08)',
          background: 'rgba(255,255,255,0.03)',
        }}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="10" stroke="#7c6af5" strokeWidth="1.5"/>
            <path d="M12 6v6l4 2" stroke="#7c6af5" strokeWidth="1.5" strokeLinecap="round"/>
          </svg>
          <span style={{ fontSize: '0.75rem', color: '#7a7f99' }}>
            Structured by{' '}
            <span style={{ color: '#7c6af5', fontWeight: '600' }}>agents-maker</span>
          </span>
        </div>
      </div>

      {/* Bottom bar */}
      <div style={{
        paddingTop: '1rem',
        borderTop: '1px solid rgba(255,255,255,0.05)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '0.5rem',
      }}>
        <span style={{ fontSize: '0.75rem', color: '#4a4f6a' }}>
          © {new Date().getFullYear()} PrepSuite. Protected material.
        </span>
        <span style={{ fontSize: '0.75rem', color: '#4a4f6a' }}>
          Dark mode · Private access only
        </span>
      </div>
    </div>
  )
}
