import { Playfair_Display, Space_Grotesk } from 'next/font/google';
import Link from 'next/link';
import Providers from './providers';
import './globals.css';

const serif = Playfair_Display({
  variable: '--font-serif',
  subsets: ['latin'],
  weight: ['500', '700']
});

const sans = Space_Grotesk({
  variable: '--font-sans',
  subsets: ['latin'],
  weight: ['400', '500', '700']
});

export const metadata = {
  title: 'MusePicker | Compare Museum and Activity Ticket Prices',
  description: 'MusePicker compares museum, gallery, theater, and attraction ticket offers across booking platforms.'
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${serif.variable} ${sans.variable}`}>
      <body>
        <Providers>
          <div className="bg-orb bg-orb-a" />
          <div className="bg-orb bg-orb-b" />
          <header className="site-header">
            <Link href="/" className="brand-link" aria-label="MusePicker home">
              MusePicker
            </Link>
            <nav className="site-nav" aria-label="Primary">
              <Link href="/search">Search</Link>
              <Link href="/admin">Admin</Link>
            </nav>
          </header>
          <main className="page-shell">{children}</main>
        </Providers>
      </body>
    </html>
  );
}
