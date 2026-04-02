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
          <div className="bg-layer" />
          <header className="site-header">
            <div className="header-inner">
              <Link href="/" className="brand-link" aria-label="MusePicker home">
                <span className="brand-dot" />
                MusePicker
              </Link>
              <nav className="site-nav" aria-label="Primary">
                <Link href="/">Home</Link>
                <Link href="/search">Search</Link>
              </nav>
            </div>
          </header>
          <main className="page-shell">{children}</main>
          <footer className="site-footer">
            <div className="footer-inner">
              <div>
                <p className="footer-brand">MusePicker</p>
                <p className="footer-muted">Compare cultural ticket prices across booking platforms.</p>
              </div>
              <div className="footer-links">
                <Link href="/">Home</Link>
                <Link href="/search">Search</Link>
                <Link href="mailto:yunboshim@gmail.com?subject=MusePicker%20City%20Request">Request a city</Link>
              </div>
            </div>
          </footer>
        </Providers>
      </body>
    </html>
  );
}
