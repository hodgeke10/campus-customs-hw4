import { Route, Routes } from 'react-router-dom'
import NavBar from './components/NavBar'
import ChatWidget from './components/ChatWidget'
import Home from './pages/Home'
import Products from './pages/Products'
import ProductDetail from './pages/ProductDetail'
import Cart from './pages/Cart'
import About from './pages/About'
import LogIn from './pages/LogIn'
import CreateAccount from './pages/CreateAccount'

export default function App() {
  return (
    <div className="app">
      <NavBar />
      <main className="page">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/products" element={<Products />} />
          <Route path="/products/:productId" element={<ProductDetail />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/about" element={<About />} />
          <Route path="/login" element={<LogIn />} />
          <Route path="/create-account" element={<CreateAccount />} />
        </Routes>
      </main>
      <footer className="footer">
        <p>Officially Licensed Merchandise</p>
        <p>Campus Customs &middot; 57 Broadway, New Haven, CT</p>
      </footer>
      <ChatWidget />
    </div>
  )
}
