const stages = [
  "Recon",
  "Vulnerability",
  "Exploit",
  "PrivEsc",
  "Persistence",
  "Exfiltration"
]

export default function KillChainGraph({ rounds }: any) {

  const currentStage = Math.min(rounds.length, stages.length)

  return (

    <div style={{ marginTop: 50 }}>

      <h2>Cyber Attack Kill Chain</h2>

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginTop: 20
        }}
      >

        {stages.map((stage, index) => {

          const active = index < currentStage

          return (

            <div
              key={stage}
              style={{
                textAlign: "center",
                flex: 1
              }}
            >

              <div
                style={{
                  height: "30px",
                  background: active ? "#00ffff" : "#222",
                  borderRadius: "5px",
                  margin: "5px"
                }}
              />

              <p
                style={{
                  fontSize: "12px",
                  color: active ? "#00ffff" : "#555"
                }}
              >
                {stage}
              </p>

            </div>

          )

        })}

      </div>

    </div>

  )

}
