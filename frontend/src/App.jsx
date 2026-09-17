import { useState, useEffect } from 'react'

const API_URL = 'https://epl-predictor-uwm7.onrender.com'

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
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-blue-950 to-slate-900 text-white flex items-center justify-center p-6">
      <div className="w-full max-w-xl">

        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold tracking-tight">
            EPL Match <span className="text-emerald-400">Predictor</span>
          </h1>
          <p className="text-slate-400 mt-2">ML-powered outcome predictions from real match data</p>
        </div>

        <div className="bg-slate-900/60 backdrop-blur border border-slate-700/50 rounded-2xl p-8 shadow-2xl shadow-emerald-500/5">

          <div className="space-y-5">
            <div>
              <label className="text-sm text-slate-400 mb-1 block">Home Team</label>
              <select
                value={homeTeam}
                onChange={(e) => setHomeTeam(e.target.value)}
                className="w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-3 outline-none focus:border-emerald-400 transition-colors"
              >
                {teams.map(team => (
                  <option key={team} value={team}>{team}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-sm text-slate-400 mb-1 block">Away Team</label>
              <select
                value={awayTeam}
                onChange={(e) => setAwayTeam(e.target.value)}
                className="w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-3 outline-none focus:border-emerald-400 transition-colors"
              >
                {teams.map(team => (
                  <option key={team} value={team}>{team}</option>
                ))}
              </select>
            </div>

            <button
              onClick={handlePredict}
              disabled={loading}
              className="w-full bg-emerald-500 hover:bg-emerald-400 hover:scale-[1.02] active:scale-[0.98] transition-all duration-150 font-semibold py-3 rounded-lg disabled:opacity-50 disabled:hover:scale-100 shadow-lg shadow-emerald-500/20"
            >
              {loading ? 'Predicting...' : 'Predict Outcome'}
            </button>
          </div>

          {prediction && (
            <div className="mt-8 pt-6 border-t border-slate-700/50 space-y-4">
              <div className="flex justify-between text-sm text-slate-400">
                <span>{prediction.home_team} — form: {prediction.home_form} pts</span>
                <span>{prediction.away_team} — form: {prediction.away_form} pts</span>
              </div>

              <ProbBar label={`${prediction.home_team} Win`} value={prediction.home_win_prob} color="bg-emerald-500" />
              <ProbBar label="Draw" value={prediction.draw_prob} color="bg-amber-500" />
              <ProbBar label={`${prediction.away_team} Win`} value={prediction.away_win_prob} color="bg-rose-500" />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function ProbBar({ label, value, color }) {
  const pct = (value * 100).toFixed(1)
  return (
    <div>
      <div className="flex justify-between text-sm mb-1">
        <span className="text-slate-300">{label}</span>
        <span className="font-semibold">{pct}%</span>
      </div>
      <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden">
        <div
          className={`${color} h-full rounded-full transition-all duration-700 ease-out`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}

export default App