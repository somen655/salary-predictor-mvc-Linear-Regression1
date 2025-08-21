import React, { useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000'

export default function App() {
  const [form, setForm] = useState({
    years_experience: 3.0,
    education_level: 'Bachelor',
    job_title: 'Data Scientist',
    city: 'Bengaluru',
    company_size: 'Medium',
    skills_python: 1,
    skills_java: 0,
    skills_aws: 1,
    skills_sql: 1
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const onChange = (e) => {
    const { name, value } = e.target
    setForm((f) => ({ ...f, [name]: ['skills_python','skills_java','skills_aws','skills_sql'].includes(name) ? Number(value) : value }))
  }

  const predict = async () => {
    setLoading(true); setError(null)
    try {
      const res = await fetch(`${API_BASE}/api/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      })
      const j = await res.json()
      if (!res.ok) throw new Error(j.errors ? j.errors.join('; ') : 'Prediction failed')
      setResult(j.predicted_salary_inr)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', padding: 24 }}>
      <h1>Salary Predictor (React)</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, minmax(0, 320px))', gap: 12 }}>
        <label>Years Experience
          <input name="years_experience" type="number" step="0.1" value={form.years_experience} onChange={onChange}/>
        </label>
        <label>Education
          <select name="education_level" value={form.education_level} onChange={onChange}>
            {['High School','Bachelor','Master','PhD'].map(x => <option key={x} value={x}>{x}</option>)}
          </select>
        </label>
        <label>Job Title
          <select name="job_title" value={form.job_title} onChange={onChange}>
            {['Backend Engineer','Data Analyst','Data Scientist','ML Engineer','Full Stack Engineer'].map(x => <option key={x} value={x}>{x}</option>)}
          </select>
        </label>
        <label>City
          <select name="city" value={form.city} onChange={onChange}>
            {['Bengaluru','Hyderabad','Pune','Mumbai','Chennai','Delhi NCR'].map(x => <option key={x} value={x}>{x}</option>)}
          </select>
        </label>
        <label>Company Size
          <select name="company_size" value={form.company_size} onChange={onChange}>
            {['Small','Medium','Large'].map(x => <option key={x} value={x}>{x}</option>)}
          </select>
        </label>
        {['skills_python','skills_java','skills_aws','skills_sql'].map(k => (
          <label key={k}>{k.replace('skills_','').toUpperCase()} (0/1)
            <input name={k} type="number" min="0" max="1" value={form[k]} onChange={onChange}/>
          </label>
        ))}
      </div>
      <div style={{ marginTop: 16 }}>
        <button onClick={predict} disabled={loading}>{loading ? 'Predicting...' : 'Predict'}</button>
      </div>
      {error && <p style={{ color: 'crimson' }}>{error}</p>}
      {result && <h2>Predicted: ₹ {result.toLocaleString('en-IN')}</h2>}
    </div>
  )
}
