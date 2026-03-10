export default function StatsBar() {

  return (

    <div style={{
      marginTop: "20px",
      padding: "12px",
      border: "1px solid #00ffff",
      background: "#050505"
    }}>

      <h3 style={{color:"#00ffff"}}>System Status</h3>

      <div style={{marginTop:"6px"}}>LLM Engine: Online</div>
      <div>Adversarial Engine: Ready</div>
      <div>API Connection: Active</div>

    </div>

  )

}
