import React, { useState } from "react";

export default function AuthPage({
  onLoginSuccess,
}: {
  onLoginSuccess: () => void;
}) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = () => {
    if (username === "admin" && password === "admin123") {
      onLoginSuccess();
    } else {
      setError("Invalid username or password");
    }
  };

  return (
    <div className="w-full max-w-md bg-white rounded-3xl border border-slate-200 shadow-sm p-8">
      <h2 className="text-2xl font-bold mb-2">Welcome back</h2>
      <p className="text-slate-500 text-sm mb-6">
        Sign in to access InstantAI
      </p>

      <div className="space-y-4">
        <input
          className="w-full px-4 py-2 border rounded-xl text-sm"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          className="w-full px-4 py-2 border rounded-xl text-sm"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && (
          <div className="text-sm text-rose-600 bg-rose-50 px-3 py-2 rounded-lg">
            {error}
          </div>
        )}

        <button
          onClick={handleLogin}
          className="w-full bg-blue-600 text-white py-2.5 rounded-xl font-bold hover:bg-blue-700 transition-all"
        >
          Sign In
        </button>
      </div>

      <p className="text-[11px] text-slate-400 mt-6 text-center">
        Demo credentials: <strong>admin / admin123</strong>
      </p>
    </div>
  );
}
