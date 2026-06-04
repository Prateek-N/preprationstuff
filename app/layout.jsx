import { Footer, Layout, Navbar } from 'nextra-theme-docs'
import { Head } from 'nextra/components'
import { getPageMap } from 'nextra/page-map'
import 'nextra-theme-docs/style.css'

export const metadata = {
  title: 'Preparation Stuff',
  description: 'Markdown notes and interview prep'
}

const navbar = <Navbar logo={<b>Preparation Stuff</b>} />
const footer = <Footer>© {new Date().getFullYear()} Preparation Stuff</Footer>

export default async function RootLayout({ children }) {
  return (
    <html lang="en" dir="ltr" suppressHydrationWarning>
      <Head />
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

