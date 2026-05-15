import { useState, useEffect } from 'react'

const API = '/api/v1'
const REFRESH_MS = 3000

const SENSOR_COLORS = {
  temperature: { accent: '#f59e0b', bg: 'rgba(245,158,11,0.12)' },
  humidity:    { accent: '#3b82f6', bg: 'rgba(59,130,246,0.12)' },
  pressure:    { accent: '#10b981', bg: 'rgba(16,185,129,0.12)' },
}
const SENSOR_UNITS = { temperature: '°C', humidity: '%', pressure: 'hPa' }

function StatCard({ label, value, sub }) {
  return (
    <div className="card">
      <div className="stat-value">{value != null ? value.toLocaleString() : '—'}</div>
      <div className="stat-label">{label}</div>
      {sub && <div className="stat-sub">{sub}</div>}
    </div>
  )
}

function SensorCard({ type, count, total }) {
  const pct = total > 0 ? Math.round((count / total) * 100) : 0
  const { accent, bg } = SENSOR_COLORS[type] ?? { accent: '#6366f1', bg: 'rgba(99,102,241,0.12)' }
  return (
    <div className="card sensor-card">
      <div className="sensor-header">
        <span className="sensor-badge" style={{ background: bg, color: accent }}>
          {type}
        </span>
        <span className="sensor-count">{count?.toLocaleString() ?? 0}</span>
      </div>
      <div className="bar-track">
        <div
          className="bar-fill"
          style={{ width: `${pct}%`, background: accent }}
        />
      </div>
      <div className="bar-footer">
        <span className="dim">{SENSOR_UNITS[type]} readings</span>
        <span style={{ color: accent }}>{pct}%</span>
      </div>
    </div>
  )
}

function RecentTable({ rows }) {
  if (!rows.length) {
    return (
      <div className="card">
        <p className="dim" style={{ textAlign: 'center', padding: '2rem' }}>
          No messages yet — waiting for data…
        </p>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="table-header">
        <h3>Recent Messages</h3>
        <span className="dim" style={{ fontSize: '0.75rem' }}>last {rows.length}</span>
      </div>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Device</th>
              <th>Type</th>
              <th>Value</th>
              <th>Normalized</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => {
              const colors = SENSOR_COLORS[r.sensor_type]
              return (
                <tr key={i}>
                  <td className="mono">{r.device_id}</td>
                  <td>
                    <span
                      className="type-badge"
                      style={{ background: colors?.bg, color: colors?.accent }}
                    >
                      {r.sensor_type}
                    </span>
                  </td>
                  <td className="mono">
                    {r.value} {SENSOR_UNITS[r.sensor_type]}
                  </td>
                  <td className="mono dim">{r.normalized}</td>
                  <td className="dim">{new Date(r.timestamp).toLocaleTimeString()}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default function App() {
  const [stats, setStats] = useState(null)
  const [recent, setRecent] = useState([])
  const [updatedAt, setUpdatedAt] = useState(null)
  const [error, setError] = useState(false)

  const fetchAll = async () => {
    try {
      const [s, r] = await Promise.all([
        fetch(`${API}/stats/`).then(res => res.json()),
        fetch(`${API}/stats/recent?limit=15`).then(res => res.json()),
      ])
      setStats(s)
      setRecent(r)
      setUpdatedAt(new Date())
      setError(false)
    } catch {
      setError(true)
    }
  }

  useEffect(() => {
    fetchAll()
    const id = setInterval(fetchAll, REFRESH_MS)
    return () => clearInterval(id)
  }, [])

  const sensorTotal = stats
    ? Object.values(stats.by_sensor_type).reduce((a, b) => a + b, 0)
    : 0

  return (
    <div className="app">
      <header>
        <div className="header-left">
          <span className={`pulse-dot ${error ? 'error' : ''}`} />
          <span className="header-title">RiTech IoT</span>
          <span className="header-sub">Dashboard</span>
        </div>
        <div className="header-right dim">
          {error
            ? 'Connection error — retrying…'
            : updatedAt
            ? `Updated ${updatedAt.toLocaleTimeString()}`
            : 'Connecting…'}
        </div>
      </header>

      <main>
        <section className="grid grid-4">
          <StatCard label="Total Messages" value={stats?.total_messages} />
          <StatCard label="Active Devices" value={stats?.device_count} />
          <StatCard label="MongoDB" value={stats?.total_messages} sub="raw ingestion" />
          <StatCard label="Postgres" value={stats?.postgres_total} sub="permanent storage" />
        </section>

        <section className="grid grid-3">
          {['temperature', 'humidity', 'pressure'].map(t => (
            <SensorCard
              key={t}
              type={t}
              count={stats?.by_sensor_type?.[t] ?? 0}
              total={sensorTotal}
            />
          ))}
        </section>

        <RecentTable rows={recent} />
      </main>
    </div>
  )
}
