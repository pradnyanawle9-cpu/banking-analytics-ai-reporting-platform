import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Banking AI Reporting Platform",
  description: "AI-powered banking analytics and reporting platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}