import { useEffect, useMemo, useState } from 'react'
import { fetchProducts } from '../api'
import { useChatResults } from '../chatResults'
import ProductCard from '../components/ProductCard'
import type { Product } from '../types'

export default function Products() {
  const { active, query, matches, clear } = useChatResults()
  const [products, setProducts] = useState<Product[]>([])
  const [category, setCategory] = useState('All')
  const [status, setStatus] = useState<'loading' | 'ready' | 'error'>('loading')

  useEffect(() => {
    fetchProducts()
      .then((items) => {
        setProducts(items)
        setStatus('ready')
      })
      .catch(() => setStatus('error'))
  }, [])

  const categories = useMemo(
    () => ['All', ...Array.from(new Set(products.map((p) => p.category))).sort()],
    [products],
  )

  // When the chat has pushed matches, the grid shows those instead of the full catalogue.
  if (active) {
    return (
      <section>
        <p className="eyebrow">From your chat</p>
        <h1>Matches for “{query}”</h1>
        <div className="chat-results-bar">
          <span>
            Showing {matches.length} {matches.length === 1 ? 'item' : 'items'} the shop
            assistant found.
          </span>
          <button type="button" className="chip" onClick={clear}>
            Show all products
          </button>
        </div>
        <div className="grid">
          {matches.map((product) => (
            <ProductCard key={product.product_id} product={product} />
          ))}
        </div>
      </section>
    )
  }

  const visible =
    category === 'All' ? products : products.filter((p) => p.category === category)

  return (
    <section>
      <p className="eyebrow">The Collection</p>
      <h1>Products</h1>
      <p className="lede">
        Yale crewnecks, hoodies, tees, quarter-zips, and fleece &mdash; every piece
        licensed by the University.
      </p>

      {status === 'loading' && (
        <div className="grid" aria-busy="true" aria-label="Loading the collection">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="card skeleton-card">
              <div className="card-image skeleton" />
              <div className="card-body">
                <div className="skeleton skeleton-line" />
                <div className="skeleton skeleton-line short" />
              </div>
            </div>
          ))}
        </div>
      )}

      {status === 'error' && (
        <p className="placeholder">
          We could not reach the catalogue. Make sure the backend is running on port 8000.
        </p>
      )}

      {status === 'ready' && (
        <>
          <div className="filters">
            {categories.map((label) => (
              <button
                key={label}
                type="button"
                className={label === category ? 'chip active' : 'chip'}
                onClick={() => setCategory(label)}
              >
                {label}
              </button>
            ))}
            <span className="filter-count">
              {visible.length} {visible.length === 1 ? 'item' : 'items'}
            </span>
          </div>

          <div className="grid">
            {visible.map((product) => (
              <ProductCard key={product.product_id} product={product} />
            ))}
          </div>
        </>
      )}
    </section>
  )
}
