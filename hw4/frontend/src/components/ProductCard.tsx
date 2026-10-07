import { Link } from 'react-router-dom'
import { formatPrice, type Product } from '../types'

export default function ProductCard({ product }: { product: Product }) {
  return (
    <Link to={`/products/${product.product_id}`} className="card">
      <div className="card-image">
        <img src={product.image_url} alt={product.name} loading="lazy" />
      </div>
      <div className="card-body">
        <h3>{product.name}</h3>
        <p className="card-price">{formatPrice(product.price)}</p>
        <p className="card-description">{product.short_description}</p>
      </div>
    </Link>
  )
}
