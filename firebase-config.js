// Importando os módulos necessários do Firebase (versão 10.8.0)
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
import { getFirestore, doc, setDoc, getDoc, updateDoc, arrayUnion, arrayRemove } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

// Configuração do seu projeto no Firebase
const firebaseConfig = {
    apiKey: "SUA_API_KEY_REAL",
    authDomain: "larpratico-ee811.firebaseapp.com",
    projectId: "larpratico-ee811",
    storageBucket: "larpratico-ee811.appspot.com",
    messagingSenderId: "SEU_MESSAGING_SENDER_ID",
    appId: "SEU_APP_ID"
};

// Inicializando o Firebase e disponibilizando as funções globalmente para o index.html
const app = initializeApp(firebaseConfig);
window.firebaseAuth = getAuth(app);
window.firebaseDb = getFirestore(app);
window.dbFns = { doc, setDoc, getDoc, updateDoc, arrayUnion, arrayRemove };
window.authFns = { createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged };
