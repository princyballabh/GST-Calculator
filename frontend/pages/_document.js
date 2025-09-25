import { Html, Head, Main, NextScript } from "next/document";

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <meta charSet="utf-8" />
        <meta
          name="description"
          content="Professional GST Calculator with PDF upload functionality for accurate tax calculations"
        />
        <meta
          name="keywords"
          content="GST, calculator, tax, HSN, PDF, upload, India"
        />
        <meta name="author" content="GST Calculator Pro" />
        <meta name="theme-color" content="#6F1D1B" />

        {/* Favicon */}
        <link
          rel="icon"
          href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🧮</text></svg>"
        />

        {/* Preload fonts */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="true"
        />

        {/* Open Graph tags */}
        <meta property="og:title" content="GST Calculator Pro" />
        <meta
          property="og:description"
          content="Professional GST Calculator with PDF upload functionality"
        />
        <meta property="og:type" content="website" />
        <meta property="og:image" content="/og-image.png" />

        {/* Twitter Card tags */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="GST Calculator Pro" />
        <meta
          name="twitter:description"
          content="Professional GST Calculator with PDF upload functionality"
        />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
