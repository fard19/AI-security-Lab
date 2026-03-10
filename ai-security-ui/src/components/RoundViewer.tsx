import { useState } from "react"
import "./RoundViewer.css"

type Round = {
  attack_strategy: string
  defense_response: string
  net_pressure: number
  risk_level: string
}

type RoundViewerProps = {
  rounds: Round[]
}

export default function RoundViewer({ rounds }: RoundViewerProps) {
  const [expandedRound, setExpandedRound] = useState<number | null>(null)

  const getRiskColor = (risk: string) => {
    const r = risk.toLowerCase()
    if (r.includes("critical")) return "#ff0000"
    if (r.includes("high")) return "#ff3c3c"
    if (r.includes("moderate")) return "#ffae00"
    if (r.includes("low")) return "#00ff9c"
    return "#00ffff"
  }

  const getRiskIcon = (risk: string) => {
    const r = risk.toLowerCase()
    if (r.includes("critical")) return "🚨"
    if (r.includes("high")) return "⚠️"
    if (r.includes("moderate")) return "⚡"
    if (r.includes("low")) return "✓"
    return "🛡️"
  }

  const getPressureLevel = (pressure: number) => {
    if (pressure >= 8) return "extreme"
    if (pressure >= 6) return "high"
    if (pressure >= 4) return "moderate"
    return "low"
  }

  if (rounds.length === 0) {
    return (
      <div className="round-viewer-empty">
        <div className="empty-state">
          <div className="empty-icon">⚔️</div>
          <h3 className="empty-title">NO BATTLE DATA</h3>
          <p className="empty-message">
            Execute a test to view adversarial engagement rounds
          </p>
          <div className="empty-decoration">
            <div className="decoration-line"></div>
            <div className="decoration-dot"></div>
            <div className="decoration-line"></div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="round-viewer">
      {/* Header */}
      <div className="viewer-header">
        <div className="header-icon-wrapper">
          <div className="header-icon-ring"></div>
          <span className="header-icon">⚔️</span>
        </div>
        <div className="header-content">
          <h2 className="viewer-title">BATTLE ANALYSIS</h2>
          <div className="viewer-subtitle">
            {rounds.length} Adversarial Engagement{rounds.length !== 1 ? "s" : ""}
          </div>
        </div>
        <div className="header-stats">
          <div className="stat-badge">
            <span className="stat-value">{rounds.length}</span>
            <span className="stat-label">ROUNDS</span>
          </div>
        </div>
      </div>

      <div className="neon-divider"></div>

      {/* Rounds Grid */}
      <div className="rounds-container">
        {rounds.map((round, index) => {
          const isExpanded = expandedRound === index
          const riskColor = getRiskColor(round.risk_level)
          const pressureLevel = getPressureLevel(round.net_pressure)

          return (
            <div
              key={index}
              className={`round-card ${isExpanded ? "expanded" : ""}`}
              style={{ 
                animationDelay: `${index * 0.1}s`,
                borderColor: `${riskColor}40`
              }}
            >
              {/* Round Header */}
              <div 
                className="round-header"
                onClick={() => setExpandedRound(isExpanded ? null : index)}
              >
                <div className="round-number">
                  <span className="round-label">ROUND</span>
                  <span className="round-digit">{String(index + 1).padStart(2, '0')}</span>
                </div>

                <div className="round-metrics">
                  {/* Pressure Gauge */}
                  <div className="metric-item pressure">
                    <div className="metric-label">PRESSURE</div>
                    <div className="pressure-gauge">
                      <div className="gauge-bg"></div>
                      <div 
                        className={`gauge-fill ${pressureLevel}`}
                        style={{ width: `${Math.min(round.net_pressure * 10, 100)}%` }}
                      ></div>
                      <div className="gauge-value">{round.net_pressure}</div>
                    </div>
                  </div>

                  {/* Risk Badge */}
                  <div className="metric-item risk">
                    <div className="metric-label">THREAT LEVEL</div>
                    <div 
                      className="risk-badge"
                      style={{ 
                        borderColor: riskColor,
                        color: riskColor,
                        boxShadow: `0 0 15px ${riskColor}40`
                      }}
                    >
                      <span className="risk-icon">{getRiskIcon(round.risk_level)}</span>
                      <span className="risk-text">{round.risk_level.toUpperCase()}</span>
                    </div>
                  </div>
                </div>

                <div className="expand-indicator">
                  <span className={`expand-icon ${isExpanded ? "rotated" : ""}`}>
                    ▼
                  </span>
                </div>
              </div>

              {/* Round Content */}
              <div className={`round-content ${isExpanded ? "visible" : ""}`}>
                <div className="content-divider"></div>

                {/* Attack Section */}
                <div className="engagement-section attack">
                  <div className="section-header">
                    <div className="section-icon attack-icon">🔴</div>
                    <div className="section-title">ATTACK VECTOR</div>
                    <div className="section-line attack-line"></div>
                  </div>
                  <div className="section-content">
                    <div className="content-box attack-box">
                      <div className="content-text">{round.attack_strategy}</div>
                      <div className="content-glow attack-glow"></div>
                    </div>
                  </div>
                </div>

                {/* VS Separator */}
                <div className="vs-separator">
                  <div className="vs-line"></div>
                  <div className="vs-badge">VS</div>
                  <div className="vs-line"></div>
                </div>

                {/* Defense Section */}
                <div className="engagement-section defense">
                  <div className="section-header">
                    <div className="section-icon defense-icon">🔵</div>
                    <div className="section-title">DEFENSE RESPONSE</div>
                    <div className="section-line defense-line"></div>
                  </div>
                  <div className="section-content">
                    <div className="content-box defense-box">
                      <div className="content-text">{round.defense_response}</div>
                      <div className="content-glow defense-glow"></div>
                    </div>
                  </div>
                </div>

                {/* Analytics Footer */}
                <div className="round-analytics">
                  <div className="analytics-grid">
                    <div className="analytics-item">
                      <div className="analytics-icon">📊</div>
                      <div className="analytics-content">
                        <div className="analytics-label">Pressure Index</div>
                        <div className="analytics-value">{round.net_pressure}/10</div>
                      </div>
                    </div>
                    <div className="analytics-item">
                      <div className="analytics-icon">🎯</div>
                      <div className="analytics-content">
                        <div className="analytics-label">Attack Intensity</div>
                        <div className="analytics-value">
                          {round.net_pressure >= 7 ? "High" : round.net_pressure >= 4 ? "Medium" : "Low"}
                        </div>
                      </div>
                    </div>
                    <div className="analytics-item">
                      <div className="analytics-icon">🛡️</div>
                      <div className="analytics-content">
                        <div className="analytics-label">Defense Status</div>
                        <div className="analytics-value">
                          {round.net_pressure <= 3 ? "Strong" : round.net_pressure <= 6 ? "Moderate" : "Weak"}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Card Glow Effect */}
              <div 
                className="card-glow"
                style={{ background: `radial-gradient(circle at center, ${riskColor}15, transparent)` }}
              ></div>
            </div>
          )
        })}
      </div>

      {/* Summary Footer */}
      <div className="viewer-footer">
        <div className="footer-stats">
          <div className="footer-stat">
            <span className="footer-label">Avg Pressure:</span>
            <span className="footer-value">
              {(rounds.reduce((sum, r) => sum + r.net_pressure, 0) / rounds.length).toFixed(1)}
            </span>
          </div>
          <div className="footer-stat">
            <span className="footer-label">Peak Pressure:</span>
            <span className="footer-value">
              {Math.max(...rounds.map(r => r.net_pressure))}
            </span>
          </div>
          <div className="footer-stat">
            <span className="footer-label">High Risk Rounds:</span>
            <span className="footer-value">
              {rounds.filter(r => r.risk_level.toLowerCase().includes("high")).length}
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}
