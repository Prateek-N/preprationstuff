import { Footer, Layout, Navbar } from 'nextra-theme-docs'
import { Head } from 'nextra/components'
import { getPageMap } from 'nextra/page-map'
import 'nextra-theme-docs/style.css'
import './globals.css'
import { SiteNavbar } from '../components/SiteNavbar'
import { SiteFooter } from '../components/SiteFooter'

export const metadata = {
  title: 'PrepSuite — Interview Preparation Portal',
  description: 'Premium candidate interview preparation guides, powered by agents-maker.'
}

const navbar = <Navbar logo={<SiteNavbar />} />
const footer = <Footer><SiteFooter /></Footer>

export default async function RootLayout({ children }) {
  return (
    <html lang="en" dir="ltr" suppressHydrationWarning>
      <Head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap"
          rel="stylesheet"
        />
      </Head>
      <body>
        <Layout
          navbar={navbar}
          pageMap={await getPageMap()}
          docsRepositoryBase="https://github.com/Prateek-N/preprationstuff/tree/main"
          footer={footer}
          sidebar={{ autoCollapse: true, toggleButton: true }}
          toc={{ backToTop: true }}
        >
          {children}
        </Layout>
      </body>
    </html>
  )
}
