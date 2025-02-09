import Navbar from "../components/Navbar";
import "./globals.css";
import { Inter } from "next/font/google";
import { AuthContextProvider } from "../context/AuthContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "RNAseek",
  description: "RNAseek: Comprehensive RNA sequencing analysis with bioinformatics tools",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={`${inter.className} p-4 h-screen bg-cover bg-center`} style={{ backgroundImage: 'url(/bgp.jpg)' }}>
        <AuthContextProvider>
          <Navbar />
          <div className="container mx-auto p-6 bg-white bg-opacity-75 rounded-lg">
            {children}
          </div>
        </AuthContextProvider>
      </body>
    </html>
  );
}