import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState<any>(null);

  const sendQuery = async () => {
    try {
      const res = await fetch(
        "http://127.0.0.1:8000/chat?query=" + encodeURIComponent(query),
        { method: "POST" }
      );

      if (!res.ok) {
        throw new Error("HTTP error " + res.status);
      }

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      console.error("Fetch error:", err);
      alert("Backend not reachable");
    }
  };


  return (
    <main style={{ padding: 40 }}>
      <h1>InstantAI</h1>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a question..."
      />

      <button onClick={sendQuery}>Ask</button>

      {response && (
        <>
          <h3>Summary</h3>
          <p>{response.summary}</p>

          <h3>Evidence</h3>
          <pre>{JSON.stringify(response.evidence, null, 2)}</pre>
        </>
      )}
    </main>
  );
}
