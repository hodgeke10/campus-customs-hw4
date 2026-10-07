import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth'
import { useCart } from '../cart'

const links = [
  { to: '/', label: 'Home', end: true },
  { to: '/products', label: 'Products' },
  { to: '/about', label: 'About Us' },
]

export default function NavBar() {
  const { user, signOut } = useAuth()
  const { count } = useCart()
  const navigate = useNavigate()

  return (
    <header className="navbar">
      <NavLink to="/" className="brand">
        <span className="brand-mark">Y</span>
        <span className="brand-text">
          <strong>Campus Customs</strong>
          <small>Yale Bulldog Blue</small>
        </span>
      </NavLink>

      <nav className="nav-links">
        {links.map(({ to, label, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
          >
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="nav-auth">
        <NavLink to="/cart" className="cart-link" aria-label={`Bag, ${count} items`}>
          <span className="cart-icon" aria-hidden="true">🛍</span>
          {count > 0 && <span className="cart-count">{count}</span>}
        </NavLink>
        {user ? (
          <>
            <span className="nav-greeting">Hi, {user.first_name ?? user.name}</span>
            <button
              type="button"
              className="btn btn-ghost"
              onClick={() => {
                signOut()
                navigate('/')
              }}
            >
              Log Out
            </button>
          </>
        ) : (
          <>
            <NavLink to="/login" className="btn btn-ghost">
              Log In
            </NavLink>
            <NavLink to="/create-account" className="btn btn-primary">
              Create Account
            </NavLink>
          </>
        )}
      </div>
    </header>
  )
}
