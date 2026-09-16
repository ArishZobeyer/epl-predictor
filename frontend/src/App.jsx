import { useState } from 'react'

function App() {
  const [homeForm, setHomeForm] = useState(0)
  const [awayForm, setAwayForm] = useState(0)
  const [prediction, setPrediction] = useState(null)

  async function handlePredict() {
    const response = await fetch('https://epl-predictor-uwm7.onrender.com/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        home_form: Number(homeForm),
        away_form: Number(awayForm),
        h2h_home_wins: 0,
        h2h_away_wins: 0,
        h2h_draws: 0
      })
    })
    const data = await response.json()
    setPrediction(data)
  }

  return (
    <div>
      <h1>EPL Match Predictor</h1>

      <label>
        Home team form (points, last 5 games):
        <input
          type="number"
          value={homeForm}
          onChange={(e) => setHomeForm(e.target.value)}
        />
      </label>

      <br />

      <label>
        Away team form (points, last 5 games):
        <input
          type="number"
          value={awayForm}
          onChange={(e) => setAwayForm(e.target.value)}
        />
      </label>

      <br />

      <button onClick={handlePredict}>Predict</button>

      {prediction && (
        <div>
          <p>Home win: {(prediction.home_win_prob * 100).toFixed(1)}%</p>
          <p>Draw: {(prediction.draw_prob * 100).toFixed(1)}%</p>
          <p>Away win: {(prediction.away_win_prob * 100).toFixed(1)}%</p>
        </div>
      )}
    </div>
  )
}

export default App