import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { signup } from '../api'
import { useAuth } from '../auth'

export default function CreateAccount() {
  const { signIn } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirm: '',
  })
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const update = (field: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((prev) => ({ ...prev, [field]: e.target.value }))

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault()
    setError('')

    if (form.password.length < 8) {
      setError('Password must be at least 8 characters.')
      return
    }
    if (form.password !== form.confirm) {
      setError('Passwords do not match.')
      return
    }

    setSubmitting(true)
    try {
      const user = await signup({
        first_name: form.first_name,
        last_name: form.last_name,
        email: form.email,
        password: form.password,
      })
      signIn(user)
      navigate('/products')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not create the account.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section className="form-page">
      <h1>Create Account</h1>
      {error && <p className="form-error">{error}</p>}
      <form className="form" onSubmit={handleSubmit}>
        <div className="form-row">
          <label>
            First Name
            <input
              type="text"
              autoComplete="given-name"
              required
              value={form.first_name}
              onChange={update('first_name')}
            />
          </label>
          <label>
            Last Name
            <input
              type="text"
              autoComplete="family-name"
              required
              value={form.last_name}
              onChange={update('last_name')}
            />
          </label>
        </div>
        <label>
          Email
          <input
            type="email"
            autoComplete="email"
            required
            value={form.email}
            onChange={update('email')}
          />
        </label>
        <label>
          Password
          <input
            type="password"
            autoComplete="new-password"
            required
            minLength={8}
            value={form.password}
            onChange={update('password')}
          />
        </label>
        <label>
          Confirm Password
          <input
            type="password"
            autoComplete="new-password"
            required
            value={form.confirm}
            onChange={update('confirm')}
          />
        </label>
        <button type="submit" className="btn btn-primary" disabled={submitting}>
          {submitting ? 'Creating…' : 'Create Account'}
        </button>
      </form>
      <p className="form-footnote">
        Already have an account? <Link to="/login">Log in</Link>.
      </p>
    </section>
  )
}
