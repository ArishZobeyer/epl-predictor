import { useState, useEffect } from 'react'

const API_URL = 'http://localhost:5000'  // we'll swap this to your live Render URL before redeploying

function App() {
  const [teams, setTeams] = useState([])
  const [homeTeam, setHomeTeam] = useState('')
  const [awayTeam, setAwayTeam] = useState('')
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetch(`${API_URL}/teams`)
      .then(res => res.json())
      .then(data => {
        setTeams(data)
        setHomeTeam(data[0])
        setAwayTeam(data[1])
      })
  }, [])

  async function handlePredict() {
    setLoading(true)
    const response = await fetch(`${API_URL}/predict-by-teams`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ home_team: homeTeam, away_team: awayTeam })
    })
    const data = await response.json()
    setPrediction(data)
    setLoading(false)
  }

  return (
    <div>
      <h1>EPL Match Predictor</h1>

      <label>
        Home team:
        <select value={homeTeam} onChange={(e) => setHomeTeam(e.target.value)}>
          {teams.map(team => (
            <option key={team} value={team}>{team}</option>
          ))}
        </select>
      </label>

      <br />

      <label>
        Away team:
        <select value={awayTeam} onChange={(e) => setAwayTeam(e.target.value)}>
          {teams.map(team => (
            <option key={team} value={team}>{team}</option>
          ))}
        </select>
      </label>

      <br />

      <button onClick={handlePredict} disabled={loading}>
        {loading ? 'Predicting...' : 'Predict'}
      </button>

      {prediction && (
        <div>
          <p>{prediction.home_team} form: {prediction.home_form} pts</p>
          <p>{prediction.away_team} form: {prediction.away_form} pts</p>
          <p>Home win: {(prediction.home_win_prob * 100).toFixed(1)}%</p>
          <p>Draw: {(prediction.draw_prob * 100).toFixed(1)}%</p>
          <p>Away win: {(prediction.away_win_prob * 100).toFixed(1)}%</p>
        </div>
      )}
    </div>
  )
}

export default App