interface Props {
  pressure: number
}

export default function RiskMeter({ pressure }: Props) {

  const percent = Math.min(Math.max((pressure + 5) / 10, 0), 1)

  const color =
    percent < 0.3
      ? "#00ff00"
      : percent < 0.6
      ? "#ffff00"
      : "#ff0000"

  return (
    <div style={{ marginTop: 30 }}>

      <h2>⚠ Risk Meter</h2>

      <div
        style={{
          width: "100%",
          height: "30px",
          background: "#222",
          borderRadius: "10px",
          overflow: "hidden"
        }}
      >
        <div
          style={{
            width: `${percent * 100}%`,
            height: "100%",
            background: color,
            transition: "width 0.5s"
          }}
        />
      </div>

      <p style={{ marginTop: 10 }}>
        Pressure Score: {pressure}
      </p>

    </div>
  )
}
