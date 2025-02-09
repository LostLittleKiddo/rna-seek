"use client"
import React, { useState, useEffect } from "react";
import Link from "next/link";
import { UserAuth } from "../context/AuthContext";

const Navbar = () => {
  const { user, googleSignIn, logOut } = UserAuth();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const handleSignIn = async () => {
    try {
      await googleSignIn();
    } catch (error) {
      console.log(error);
      setError("Failed to sign in. Please try again.");
    }
  };

  const handleSignOut = async () => {
    try {
      await logOut();
    } catch (error) {
      console.log(error);
      setError("Failed to sign out. Please try again.");
    }
  };

  useEffect(() => {
    const checkAuthentication = async () => {
      await new Promise((resolve) => setTimeout(resolve, 50));
      setLoading(false);
    };
    checkAuthentication();
  }, [user]);

  return (
    <div className="h-20 w-full border-b-2 flex items-center justify-between bg-blue-500 p-4">
      <ul className="flex">
        <li className="p-2">
          <Link href="/" className="hover:text-white text-xl font-bold" aria-label="Home">Home</Link>
        </li>
        <li className="p-2">
          <Link href="/about" className="hover:text-white text-xl font-bold" aria-label="About">About</Link>
        </li>
        <li className="p-2">
          <Link href="/contact" className="hover:text-white text-xl font-bold" aria-label="Contact">Contact</Link>
        </li>
        {!user ? null : (
          <li className="p-2">
            <Link href="/tools" className="hover:text-white text-xl font-bold" aria-label="Tools">Tools</Link>
          </li>
        )}
      </ul>

      {loading ? (
        <div className="text-xl font-bold">Loading...</div>
      ) : !user ? (
        <ul className="flex">
          <li onClick={handleSignIn} className="p-2 hover:text-white cursor-pointer text-xl font-bold" aria-label="Login">
            Login
          </li>
        </ul>
      ) : (
        <div className="flex items-center space-x-4">
          <p className="cursor-default text-xl font-bold">Welcome, {user.displayName}</p>
          <p className="hover:text-red-800 cursor-pointer text-xl font-bold" onClick={handleSignOut} aria-label="Sign out">
            Sign out
          </p>
        </div>
      )}
      {error && <p className="text-red-500 text-xl font-bold">{error}</p>}
    </div>
  );
};

export default Navbar;