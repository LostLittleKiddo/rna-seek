// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries
import { getAuth } from "firebase/auth";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDg_Bypfceqcy7MkhapzP5EOtrq7-h8z8k",
  authDomain: "rna-seek.firebaseapp.com",
  projectId: "rna-seek",
  storageBucket: "rna-seek.firebasestorage.app",
  messagingSenderId: "631626305414",
  appId: "1:631626305414:web:7dd271fe030750242ee607"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
