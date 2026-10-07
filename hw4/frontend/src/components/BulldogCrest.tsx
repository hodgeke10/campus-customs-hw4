/**
 * Original Yale-style bulldog crest illustration (not a copyrighted mark).
 * A navy shield with a friendly bulldog face and a gold collar.
 */
export default function BulldogCrest({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      viewBox="0 0 200 220"
      role="img"
      aria-label="Campus Customs bulldog crest"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Shield */}
      <path
        d="M100 8 L188 34 V120 C188 168 150 198 100 212 C50 198 12 168 12 120 V34 Z"
        fill="#00356b"
        stroke="#c6a15b"
        strokeWidth="5"
      />
      {/* Inner hairline */}
      <path
        d="M100 22 L176 44 V118 C176 160 143 186 100 198 C57 186 24 160 24 118 V44 Z"
        fill="none"
        stroke="#e7d7b4"
        strokeWidth="1.5"
        opacity="0.6"
      />

      {/* Bulldog */}
      <g transform="translate(100 108)">
        {/* Ears */}
        <path d="M-46 -34 q-14 -6 -18 12 q-2 16 16 18 Z" fill="#f3efe5" />
        <path d="M46 -34 q14 -6 18 12 q2 16 -16 18 Z" fill="#f3efe5" />
        {/* Head */}
        <ellipse cx="0" cy="-6" rx="46" ry="42" fill="#faf7ef" />
        {/* Brow */}
        <path d="M-40 -20 q18 -16 40 -10 M40 -20 q-18 -16 -40 -10" fill="none" stroke="#c9c2b0" strokeWidth="2" />
        {/* Eyes */}
        <circle cx="-20" cy="-14" r="6.5" fill="#1c2330" />
        <circle cx="20" cy="-14" r="6.5" fill="#1c2330" />
        <circle cx="-18" cy="-16" r="2" fill="#fff" />
        <circle cx="22" cy="-16" r="2" fill="#fff" />
        {/* Snout */}
        <ellipse cx="0" cy="18" rx="30" ry="24" fill="#fff" />
        <path d="M-16 6 q16 -10 32 0" fill="none" stroke="#c9c2b0" strokeWidth="2" />
        {/* Nose */}
        <path d="M-11 8 q11 -7 22 0 q0 10 -11 13 q-11 -3 -11 -13 Z" fill="#1c2330" />
        {/* Mouth */}
        <path d="M0 21 V30 M0 30 q-12 6 -20 0 M0 30 q12 6 20 0" fill="none" stroke="#1c2330" strokeWidth="2.5" strokeLinecap="round" />
        {/* Jowls */}
        <path d="M-30 20 q-6 18 10 24 M30 20 q6 18 -10 24" fill="none" stroke="#c9c2b0" strokeWidth="2" />
      </g>

      {/* Gold collar */}
      <rect x="62" y="150" width="76" height="12" rx="6" fill="#c6a15b" />
      <circle cx="100" cy="156" r="5" fill="#00356b" />
    </svg>
  )
}
