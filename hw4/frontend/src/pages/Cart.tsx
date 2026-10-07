import { Link } from 'react-router-dom'
import { useCart } from '../cart'
import { formatPrice } from '../types'

export default function Cart() {
  const { items, subtotal, removeItem, clear } = useCart()

  if (items.length === 0) {
    return (
      <section>
        <p className="eyebrow">Your Bag</p>
        <h1>Your bag is empty</h1>
        <p className="lede">
          Nothing here yet. <Link to="/products">Browse the collection</Link> and add a
          piece or two.
        </p>
      </section>
    )
  }

  return (
    <section>
      <p className="eyebrow">Your Bag</p>
      <h1>Your bag</h1>

      <ul className="cart-list">
        {items.map((item) => (
          <li key={`${item.product_id}-${item.size}`} className="cart-item">
            <Link to={`/products/${item.product_id}`} className="cart-thumb">
              <img src={item.image_url} alt={item.name} loading="lazy" />
            </Link>
            <div className="cart-item-info">
              <Link to={`/products/${item.product_id}`} className="cart-item-name">
                {item.name}
              </Link>
              <p className="cart-item-meta">
                Size {item.size} &middot; Qty {item.quantity}
              </p>
            </div>
            <div className="cart-item-right">
              <span className="cart-item-price">
                {formatPrice(item.price * item.quantity)}
              </span>
              <button
                type="button"
                className="cart-remove"
                onClick={() => removeItem(item.product_id, item.size)}
              >
                Remove
              </button>
            </div>
          </li>
        ))}
      </ul>

      <div className="cart-summary">
        <div className="cart-subtotal">
          <span>Subtotal</span>
          <strong>{formatPrice(subtotal)}</strong>
        </div>
        <p className="cart-note">
          This is a demo bag — checkout isn&rsquo;t connected. Come see us at 57 Broadway to
          complete your order.
        </p>
        <div className="cart-actions">
          <button type="button" className="btn btn-primary" disabled>
            Checkout
          </button>
          <button type="button" className="btn btn-ghost" onClick={clear}>
            Clear bag
          </button>
        </div>
      </div>
    </section>
  )
}
