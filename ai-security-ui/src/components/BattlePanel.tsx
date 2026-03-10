import { useEffect, useState } from "react"
import "./BattlePanel.css"

type Round = {
  attack_strategy: string
  defense_response: string
}

type BattlePanelProps = {
  rounds: Round[]
  setPressure: React.Dispatch<React.SetStateAction<number[]>>
}

export default function BattlePanel({ rounds, setPressure }: BattlePanelProps) {
  const [expandedRound, setExpandedRound] = useState<number | null>(null)
  const [pressureData, setPressureData] = useState<number[]>([])

  useEffect(() => {
    if (!rounds || rounds.length === 0) {
      setPressure([])
      setPressureData([])
      return
    }

    // Enhanced pressure calculation
    const pressureValues = rounds.map((r, i) => {
      // Base factors
      const attackLength = r.attack_strategy.length
      const defenseLength = r.defense_response.length
      
      // Complexity scoring
      const attackComplexity = (attackLength / 100) * 3
      const defenseEffectiveness = Math.max(0, (defenseLength / 120) * 2.5)
      
      // Escalation factor (pressure tends to increase over rounds)
      const escalation = i * 0.5
      
      // Calculate net pressure
      const rawPressure = attackComplexity - defenseEffectiveness + escalation + 2
      
      // Clamp between 1-10
      const pressure = Math.max(1, Math.min(10, Math.round(rawPressure)))
      
      return pressure
    })

    setPressure(pressureValues)
    setPressureData(pressureValues)
  }, [rounds, setPressure])

  const getAttackIntensity = (strategy: string) => {
    const length = strategy.length
    if (length > 150) return { label: "EXTREME", color: "#ff0000" }
    if (length > 100) return { label: "HIGH", color: "#ff6600" }
    if (length > 50) return { label: "MODERATE", color: "#ffae00" }
    return { label: "LOW", color: "#00ff9c" }
  }

  const getDefenseStrength = (response: string) => {
    const length = response.length
    if (length > 180) return { label: "STRONG", color: "#00ff9c" }
    if (length > 120) return { label: "MODERATE", color: "#00ffff" }
    if (length > 60) return { label: "WEAK", color: "#ffae00" }
    return { label: "MINIMAL", color: "#ff6600" }
  }

  const getPressureLevel = (pressure: number) => {
    if (pressure >= 8) return { label: "CRITICAL", color: "#ff0000", icon: "🚨" }
    if (pressure >= 6) return { label: "HIGH", color: "#ff6600", icon: "⚠️" }
    if (pressure >= 4) return { label: "MODERATE", color: "#ffae00", icon: "⚡" }
    return { label: "LOW", color: "#00ff9c", icon: "✓" }
  }

  if (!rounds || rounds.length === 0) {
    return (
      <div className="battle-panel-container">
        <div className="battle-empty">
          <div className="empty-icon">⚔️</div>
          <h3 className="empty-title">NO BATTLE DATA</h3>
          <p className="empty-message">
            Execute a test to view adversarial engagement analysis
          </p>
        </div>
      </div>
    )
  }

  // Calculate statistics
  const avgPressure = (pressureData.reduce((a, b) => a + b, 0) / pressureData.length).toFixed(1)
  const maxPressure = Math.max(...pressureData)
  const criticalRounds = pressureData.filter(p => p >= 8).length
  const totalEngagements = rounds.length

  return (
    <div className="battle-panel-container">
      {/* Header */}
      <div className="battle-header">
        <div className="header-icon-wrapper">
          <div className="icon-rings">
            <div className="ring ring-1"></div>
            <div className="ring ring-2"></div>
          </div>
          <span className="header-icon">⚔️</span>
        </div>
        <div className="header-content">
          <h2 className="battle-title">ENGAGEMENT ANALYSIS</h2>
          <div className="battle-subtitle">Attack vs Defense Dynamics</div>
        </div>
        <div className="header-badge">
          <span className="badge-value">{rounds.length}</span>
          <span className="badge-label">ROUNDS</span>
        </div>
      </div>

      <div className="battle-divider"></div>

      {/* Statistics Overview */}
      <div className="stats-overview">
        <div className="overview-card">
          <div className="overview-icon">📊</div>
          <div className="overview-content">
            <div className="overview-label">Avg Pressure</div>
            <div className="overview-value">{avgPressure}</div>
          </div>
        </div>

        <div className="overview-card">
          <div className="overview-icon">⚡</div>
          <div className="overview-content">
            <div className="overview-label">Peak Pressure</div>
            <div className="overview-value">{maxPressure}</div>
          </div>
        </div>

        <div className="overview-card">
          <div className="overview-icon">🚨</div>
          <div className="overview-content">
            <div className="overview-label">Critical Rounds</div>
            <div className="overview-value">{criticalRounds}</div>
          </div>
        </div>

        <div className="overview-card">
          <div className="overview-icon">🎯</div>
          <div className="overview-content">
            <div className="overview-label">Total Engagements</div>
            <div className="overview-value">{totalEngagements}</div>
          </div>
        </div>
      </div>

      {/* Rounds List */}
      <div className="rounds-list">
        {rounds.map((round, index) => {
          const isExpanded = expandedRound === index
          const pressure = pressureData[index] || 0
          const pressureInfo = getPressureLevel(pressure)
          const attackInfo = getAttackIntensity(round.attack_strategy)
          const defenseInfo = getDefenseStrength(round.defense_response)

          return (
            <div
              key={index}
              className={`battle-round ${isExpanded ? "expanded" : ""}`}
              style={{ animationDelay: `${index * 0.08}s` }}
            >
              {/* Round Header */}
              <div
                className="round-header"
                onClick={() => setExpandedRound(isExpanded ? null : index)}
              >
                <div className="round-number-badge">
                  <span className="round-prefix">R</span>
                  <span className="round-number">{String(index + 1).padStart(2, '0')}</span>
                </div>

                <div className="round-summary">
                  <div className="summary-row">
                    <div className="summary-item attack">
                      <span className="item-icon">⚔️</span>
                      <span className="item-label">Attack:</span>
                      <span 
                        className="item-badge"
                        style={{ 
                          color: attackInfo.color,
                          borderColor: attackInfo.color 
                        }}
                      >
                        {attackInfo.label}
                      </span>
                    </div>

                    <div className="summary-item defense">
                      <span className="item-icon">🛡️</span>
                      <span className="item-label">Defense:</span>
                      <span 
                        className="item-badge"
                        style={{ 
                          color: defenseInfo.color,
                          borderColor: defenseInfo.color 
                        }}
                      >
                        {defenseInfo.label}
                      </span>
                    </div>
                  </div>

                  <div className="pressure-indicator">
                    <div className="pressure-bar-container">
                      <div className="pressure-bar-bg"></div>
                      <div 
                        className="pressure-bar-fill"
                        style={{ 
                          width: `${pressure * 10}%`,
                          background: pressureInfo.color,
                          boxShadow: `0 0 15px ${pressureInfo.color}80`
                        }}
                      ></div>
                      <div className="pressure-value">{pressure}</div>
                    </div>
                    <div 
                      className="pressure-label"
                      style={{ color: pressureInfo.color }}
                    >
                      <span className="pressure-icon">{pressureInfo.icon}</span>
                      {pressureInfo.label}
                    </div>
                  </div>
                </div>

                <div className="expand-button">
                  <span className={`expand-arrow ${isExpanded ? "rotated" : ""}`}>
                    ▼
                  </span>
                </div>
              </div>

              {/* Round Details (Expandable) */}
              <div className={`round-details ${isExpanded ? "visible" : ""}`}>
                <div className="details-divider"></div>

                {/* Attack Section */}
                <div className="engagement-block attack-block">
                  <div className="block-header">
                    <div className="block-icon attack-icon">⚔️</div>
                    <div className="block-title">ATTACK VECTOR</div>
                    <div className="block-line attack-line"></div>
                    <div 
                      className="block-intensity"
                      style={{ 
                        color: attackInfo.color,
                        borderColor: attackInfo.color 
                      }}
                    >
                      {attackInfo.label}
                    </div>
                  </div>
                  <div className="block-content attack-content">
                    <div className="content-text">{round.attack_strategy}</div>
                    <div className="content-meta">
                      <span className="meta-item">
                        📏 {round.attack_strategy.length} chars
                      </span>
                      <span className="meta-item">
                        📝 {round.attack_strategy.split(' ').length} words
                      </span>
                    </div>
                  </div>
                </div>

                {/* VS Divider */}
                <div className="vs-divider">
                  <div className="vs-line"></div>
                  <div className="vs-badge">VS</div>
                  <div className="vs-line"></div>
                </div>

                {/* Defense Section */}
                <div className="engagement-block defense-block">
                  <div className="block-header">
                    <div className="block-icon defense-icon">🛡️</div>
                    <div className="block-title">DEFENSE RESPONSE</div>
                    <div className="block-line defense-line"></div>
                    <div 
                      className="block-intensity"
                      style={{ 
                        color: defenseInfo.color,
                        borderColor: defenseInfo.color 
                      }}
                    >
                      {defenseInfo.label}
                    </div>
                  </div>
                  <div className="block-content defense-content">
                    <div className="content-text">{round.defense_response}</div>
                    <div className="content-meta">
                      <span className="meta-item">
                        📏 {round.defense_response.length} chars
                      </span>
                      <span className="meta-item">
                        📝 {round.defense_response.split(' ').length} words
                      </span>
                    </div>
                  </div>
                </div>

                {/* Round Analytics */}
                <div className="round-analytics">
                  <div className="analytics-title">ROUND ANALYSIS</div>
                  <div className="analytics-grid">
                    <div className="analytics-metric">
                      <div className="metric-icon">🎯</div>
                      <div className="metric-info">
                        <div className="metric-label">Outcome</div>
                        <div className="metric-value">
                          {pressure > 6 ? "Attack Dominant" : pressure > 3 ? "Balanced" : "Defense Strong"}
                        </div>
                      </div>
                    </div>
                    <div className="analytics-metric">
                      <div className="metric-icon">⚖️</div>
                      <div className="metric-info">
                        <div className="metric-label">Balance</div>
                        <div className="metric-value">
                          {Math.abs(attackInfo.label.length - defenseInfo.label.length) < 2 ? "Even" : "Uneven"}
                        </div>
                      </div>
                    </div>
                    <div className="analytics-metric">
                      <div className="metric-icon">📊</div>
                      <div className="metric-info">
                        <div className="metric-label">Pressure Index</div>
                        <div className="metric-value">{pressure}/10</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
