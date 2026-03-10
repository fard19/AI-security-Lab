import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

export default function AttackDefenseChart({ rounds }: any) {

  const data = rounds.map((r: any) => ({
    round: `R${r.round}`,
    attack: r.attack_strategy.length,
    defense: r.defense_response.length
  }));

  return (

    <div style={{ marginTop: 40 }}>

      <h2>Attack vs Defense</h2>

      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data}>
          <CartesianGrid stroke="#00ffff33" />
          <XAxis dataKey="round" stroke="#00ffff" />
          <YAxis stroke="#00ffff" />
          <Tooltip />
          <Bar dataKey="attack" fill="#ff4444" />
          <Bar dataKey="defense" fill="#00ffff" />
        </BarChart>
      </ResponsiveContainer>

    </div>

  );
}
