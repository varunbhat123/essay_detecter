import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Essay Detector",
  description: "AI-powered essay analysis dashboard for admissions essays",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="bg-slate-950 text-white antialiased">{children}</body>
    </html>
  );
}
