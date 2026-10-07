import { Link } from 'react-router-dom'
import BulldogCrest from '../components/BulldogCrest'

export default function Home() {
  return (
    <>
      <section className="hero hero-split">
        <div className="hero-copy">
          <p className="eyebrow">On Broadway since 1975</p>
          <h1>The sweatshirt you&rsquo;ll still be wearing in twenty years.</h1>
          <p className="lede">
            We stock Yale crewnecks, hoodies, tees, quarter-zips, and fleece &mdash; the
            everyday kind you pull on for a walk across Old Campus, not the kind that stays
            folded in a drawer. Every piece is licensed by the University.
          </p>
          <div className="hero-actions">
            <Link to="/products" className="btn btn-primary">
              Browse the Collection
            </Link>
            <Link to="/about" className="btn btn-ghost">
              Who We Are
            </Link>
          </div>
        </div>
        <div className="hero-crest">
          <BulldogCrest className="bulldog-crest" />
        </div>
      </section>

      <section className="campus-band">
        <div className="campus-caption">
          <p className="eyebrow">Made for the quad</p>
          <h2>Gear that lives where you do.</h2>
          <p>
            From Old Campus to the Bowl, our Bulldogs wear it to class, to The Game, and all
            the way to reunions.
          </p>
        </div>
      </section>

      <section className="pillars">
        <article className="pillar">
          <img
            className="pillar-photo"
            src="/photos/section-ask.jpg"
            alt="Shoppers browsing apparel in a clothing store"
            loading="lazy"
          />
          <h2>Ask before you buy</h2>
          <p>
            Not sure whether a crewneck comes in your size, or what a graphic actually looks
            like up close? Ask our shop assistant. It reads from the same stock list we do,
            so if something is sold out in a medium, it will tell you so.
          </p>
        </article>
        <article className="pillar">
          <img
            className="pillar-photo"
            src="/photos/section-sport.jpg"
            alt="A college crew team rowing on the water"
            loading="lazy"
          />
          <h2>Residential colleges to varsity teams</h2>
          <p>
            Davenport, Grace Hopper, Morse. Crew, fencing, sailing, ice hockey. Graduate
            schools, family gear, and the Harvard&ndash;Yale shirt that only makes sense in
            November.
          </p>
        </article>
        <article className="pillar">
          <img
            className="pillar-photo"
            src="/photos/section-store.jpg"
            alt="Interior of a clothing boutique with racks of apparel"
            loading="lazy"
          />
          <h2>A real store, not just a website</h2>
          <p>
            We have been at 57 Broadway for five decades, open seven days a week. Come in
            and try things on, or let us ship them to you.
          </p>
        </article>
      </section>
    </>
  )
}
