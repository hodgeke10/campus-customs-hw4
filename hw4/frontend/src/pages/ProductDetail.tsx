import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { fetchProduct } from '../api'
import { useCart } from '../cart'
import { formatPrice, type Product } from '../types'

export default function ProductDetail() {
  const { productId } = useParams<{ productId: string }>()
  const { addItem } = useCart()
  const [product, setProduct] = useState<Product | null>(null)
  const [status, setStatus] = useState<'loading' | 'ready' | 'missing' | 'error'>('loading')
  const [selectedSize, setSelectedSize] = useState<string | null>(null)
  const [added, setAdded] = useState(false)

  useEffect(() => {
    if (!productId) return
    setStatus('loading')
    setSelectedSize(null)
    setAdded(false)
    fetchProduct(productId)
      .then((item) => {
        setProduct(item)
        setStatus('ready')
      })
      .catch((error: Error) =>
        setStatus(error.message.includes('404') ? 'missing' : 'error'),
      )
  }, [productId])

  if (status === 'loading') return <p className="placeholder">Loading…</p>

  if (status === 'missing')
    return (
      <section>
        <h1>We don&rsquo;t carry that one</h1>
        <p className="lede">
          That product isn&rsquo;t in our catalogue. <Link to="/products">Browse the
          collection</Link> instead.
        </p>
      </section>
    )

  if (status === 'error' || !product)
    return (
      <p className="placeholder">
        We could not reach the catalogue. Make sure the backend is running on port 8000.
      </p>
    )

  const inStock = product.inventory.filter((item) => item.quantity > 0)
  const soldOut = inStock.length === 0

  function handleAdd() {
    if (!product || !selectedSize) return
    addItem(product, selectedSize)
    setAdded(true)
    window.setTimeout(() => setAdded(false), 2000)
  }

  return (
    <article className="detail">
      <nav className="breadcrumb">
        <Link to="/products">Products</Link> <span>/</span> {product.name}
      </nav>

      <div className="detail-layout">
        <div className="detail-image">
          <img src={product.image_url} alt={product.name} />
        </div>

        <div className="detail-info">
          <p className="eyebrow">{product.category}</p>
          <h1>{product.name}</h1>
          <p className="detail-price">{formatPrice(product.price)}</p>

          <p className="detail-description">{product.description}</p>

          {product.colors.length > 0 && (
            <div className="detail-block">
              <h2>Colors</h2>
              <p className="detail-colors">{product.colors.join(', ')}</p>
            </div>
          )}

          <div className="detail-block">
            <h2>Select a size</h2>
            {soldOut ? (
              <p className="out-of-stock-note">Every size is sold out right now.</p>
            ) : (
              <ul className="sizes">
                {product.inventory.map(({ size, quantity }) => {
                  const available = quantity > 0
                  const isSelected = selectedSize === size
                  return (
                    <li key={size}>
                      <button
                        type="button"
                        className={`size${isSelected ? ' selected' : ''}${
                          available ? '' : ' sold-out'
                        }`}
                        disabled={!available}
                        aria-pressed={isSelected}
                        onClick={() => setSelectedSize(size)}
                        title={available ? `${quantity} in stock` : 'Out of stock'}
                      >
                        <span className="size-label">{size}</span>
                        <span className="size-stock">
                          {available ? `${quantity} left` : 'Sold out'}
                        </span>
                      </button>
                    </li>
                  )
                })}
              </ul>
            )}
          </div>

          <div className="add-row">
            <button
              type="button"
              className="btn btn-primary add-to-bag"
              disabled={soldOut || !selectedSize}
              onClick={handleAdd}
            >
              {soldOut
                ? 'Sold out'
                : selectedSize
                  ? `Add ${selectedSize} to Bag`
                  : 'Select a size'}
            </button>
            {added && <span className="added-note">Added to your bag ✓</span>}
          </div>

          <p className="licensed-note">Officially licensed Yale merchandise</p>
        </div>
      </div>
    </article>
  )
}
