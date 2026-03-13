import type { Metadata } from "next"
import { JetBrains_Mono } from "next/font/google"
import "./globals.css"

const mono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap",
})

export const metadata: Metadata = {
  title: "CodeXRay — Codebase Intelligence",
  description: "AI-powered architecture analysis for GitHub repositories",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={mono.variable}>
      <body style={{ backgroundColor: "#080c10", color: "#ffffff", minHeight: "100vh" }}>
        {children}
      </body>
    </html>
  )
}