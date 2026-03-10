import { useState } from "react";

import ControlPanel from "./components/ControlPanel";
import RoundViewer from "./components/RoundViewer";
import StatsBar from "./components/StatsBar";

import PressureChart from "./components/PressureChart";
import AttackDefenseChart from "./components/AttackDefenseChart";
import RiskMeter from "./components/RiskMeter";
import KillChainGraph from "./components/KillChainGraph";

import "./App.css";
import "./Header.css";

function App() {

  const [rounds, setRounds] = useState<any[]>([]);
  const [, setRisk] = useState<string | null>(null);
  const [pressure, setPressure] = useState<number[]>([]);

  const latestPressure =
    pressure.length > 0
      ? pressure[pressure.length - 1]
      : 0;

  return (

    <div
      style={{
        background: "#050505",
        color: "#00ffff",
        minHeight: "100vh",
        padding: "20px",
        fontFamily: "Rajdhani, monospace",
      }}
    >

      {/* ========================= */}
      {/* MODERN HEADER */}
      {/* ========================= */}

      <div className="ai-lab-header">

        <div className="header-glow-ring"></div>

        <h1 className="ai-title">
          <span className="ai">AI</span>
          <span className="security">SECURITY</span>
          <span className="lab">LAB</span>
        </h1>

        <div className="header-subtitle">
          ADVERSARIAL DEFENSE SIMULATION ENVIRONMENT
        </div>

        <div className="scan-line"></div>

      </div>

      {/* ========================= */}
      {/* SYSTEM STATUS */}
      {/* ========================= */}

      <StatsBar />

      {/* ========================= */}
      {/* CONTROL PANEL */}
      {/* ========================= */}

      <ControlPanel
        setRounds={setRounds}
        setRisk={setRisk}
        setPressure={setPressure}
      />

      {/* ========================= */}
      {/* BATTLE ROUNDS */}
      {/* ========================= */}

      <RoundViewer rounds={rounds} />

      {/* ========================= */}
      {/* ANALYTICS DASHBOARD */}
      {/* ========================= */}

      {rounds.length > 0 && (

        <div style={{ marginTop: "60px" }}>

          <h2 style={{ textAlign: "center" }}>
            AI Security Analytics
          </h2>

          {/* Pressure Trend */}
          <PressureChart rounds={rounds} />

          {/* Attack vs Defense */}
          <AttackDefenseChart rounds={rounds} />

          {/* Risk Meter */}
          <RiskMeter pressure={latestPressure} />

          {/* Cyber Attack Kill Chain */}
          <KillChainGraph rounds={rounds} />

        </div>

      )}

    </div>

  );
}

export default App;
