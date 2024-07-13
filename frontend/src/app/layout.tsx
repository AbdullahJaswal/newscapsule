import type { Metadata } from "next";
import { Inter as Font } from "next/font/google";
import "./globals.css";
import React from "react";
import { ThemeProvider } from "@/components/utils/theme-provider";
import Navbar from "@/components/navbar";
import Footer from "@/components/footer";

const font = Font({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "NewsCapsule",
  description:
    "NewsCapsule provides wikinews in a simple and easy to read format.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={font.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          <section className="flex flex-col mx-auto justify-between min-h-screen">
            <Navbar />

            <main className="py-4 mb-auto max-w-7xl mx-auto flex justify-center overflow-y-auto">
              {children}
            </main>

            <Footer />
          </section>
        </ThemeProvider>
      </body>
    </html>
  );
}
