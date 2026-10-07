export default function About() {
  return (
    <section>
      <p className="eyebrow">About Us</p>
      <h1>Fifty years on the same corner.</h1>
      <p className="lede about-lede">
        Campus Customs opened at 57 Broadway in 1975 and never moved. We are the oldest
        licensed Yale merchandise shop in New Haven, which mostly means we have had a long
        time to figure out what people actually want to wear.
      </p>

      <div className="about-row">
        <div className="about-text">
          <h2>What we make our name on</h2>
          <p>
            The replica Y sweater is the piece we are known for. We developed it more than
            forty years ago &mdash; cotton, made in the United States, with the felt Y
            stitched on rather than printed &mdash; and it has stayed in the shop ever
            since, largely unchanged, because there was never a good argument for changing
            it.
          </p>
          <p>
            Around it we have built a collection that follows the University: crewnecks for
            all fourteen residential colleges, hoodies and tees for the varsity teams, gear
            for the graduate and professional schools, and the family shirts that get bought
            by the armful on move-in weekend.
          </p>
        </div>
        <img
          className="about-photo"
          src="/photos/about-sweater.jpg"
          alt="A stack of folded knit sweaters"
          loading="lazy"
        />
      </div>

      <div className="about-row reverse">
        <div className="about-text">
          <h2>Licensed, and particular about it</h2>
          <p>
            Everything on this site is officially licensed by Yale. We also do our own
            screen printing, embroidery, and digital printing in-house, which is how the
            shop started and why we are fussy about how a graphic sits on a garment.
          </p>
        </div>
        <img
          className="about-photo"
          src="/photos/about-printing.jpg"
          alt="A t-shirt being screen printed on a press"
          loading="lazy"
        />
      </div>

      <div className="about-row">
        <div className="about-text">
          <h2>Come find us</h2>
          <p>
            57 Broadway, New Haven, open seven days a week. If you would rather shop from
            your desk, the collection here is the same one on our shelves, and our shop
            assistant can answer questions about sizes, colors, and what is in stock before
            you order.
          </p>
        </div>
        <img
          className="about-photo"
          src="/photos/about-shop.jpg"
          alt="A clothing shop window display"
          loading="lazy"
        />
      </div>
    </section>
  )
}
