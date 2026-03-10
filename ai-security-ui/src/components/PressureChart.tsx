import { Line } from "react-chartjs-2"
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from "chart.js"
import "./PressureChart.css"

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

type Round = {
  attack_strategy: string
  defense_response: string
  net_pressure?: number
}

type PressureChartProps = {
  pressure?: number[]
  rounds?: Round[]
}

export default function PressureChart({ pressure, rounds }: PressureChartProps) {

  // ---------- FIX ----------
  // If pressure array is missing, generate it from rounds
  let pressureHistory: number[] = pressure || []

  if ((!pressureHistory || pressureHistory.length === 0) && rounds && rounds.length > 0) {
    pressureHistory = rounds.map((r, i) => {
      if (r.net_pressure !== undefined) return r.net_pressure

      // fallback pressure estimation
      const attackScore = r.attack_strategy.length / 25
      const defenseScore = r.defense_response.length / 30

      return Math.max(1, Math.round(attackScore - defenseScore + i + 3))
    })
  }

  if (!pressureHistory || pressureHistory.length === 0) {
    return (
      <div className="pressure-chart-wrapper">
        <div className="chart-empty-state">
          <div className="empty-icon-pulse">📊</div>
          <h3 className="empty-title">NO PRESSURE DATA</h3>
          <p className="empty-subtitle">Awaiting adversarial engagement metrics</p>
        </div>
      </div>
    )
  }

  const labels = pressureHistory.map((_, i) => `R${i + 1}`)

  const data = {
    labels,
    datasets: [
      {
        label: "Pressure Index",
        data: pressureHistory,
        borderColor: "#00ffff",
        backgroundColor: "rgba(0,255,255,0.15)",
        borderWidth: 3,
        tension: 0.4,
        pointRadius: 6,
        pointBackgroundColor: "#00ffff",
        fill: true
      }
    ]
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false }
    },
    scales: {
      x: {
        ticks: { color: "#00ffff" },
        grid: { color: "rgba(0,255,255,0.15)" }
      },
      y: {
        min: 0,
        max: 10,
        ticks: { color: "#00ffff" },
        grid: { color: "rgba(0,255,255,0.15)" }
      }
    }
  }

  return (
    <div className="pressure-chart-wrapper">

      <div className="chart-header-section">
        <h3 className="chart-main-title">PRESSURE TRAJECTORY</h3>
      </div>

      <div className="chart-canvas-container" style={{ height: "300px" }}>
        <Line data={data} options={options} />
      </div>

    </div>
  )
}
