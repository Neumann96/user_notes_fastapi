import React, { useEffect, useMemo, useRef, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "";

export default function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [status, setStatus] = useState("");
  const [busy, setBusy] = useState(false);
  const rafRef = useRef(0);

  const isAuthed = useMemo(() => Boolean(token), [token]);

  useEffect(() => {
    if (token) {
      localStorage.setItem("token", token);
    } else {
      localStorage.removeItem("token");
    }
  }, [token]);

  useEffect(() => {
    const handleMove = (event) => {
      const { clientX, clientY } = event;
      if (rafRef.current) return;
      rafRef.current = requestAnimationFrame(() => {
        document.documentElement.style.setProperty("--mx", `${clientX}px`);
        document.documentElement.style.setProperty("--my", `${clientY}px`);
        document.documentElement.style.setProperty("--cx", `${clientX}px`);
        document.documentElement.style.setProperty("--cy", `${clientY}px`);
        rafRef.current = 0;
      });
    };

    window.addEventListener("mousemove", handleMove);
    return () => window.removeEventListener("mousemove", handleMove);
  }, []);

  useEffect(() => {
    if (isAuthed) {
      loadNotes();
    } else {
      setNotes([]);
    }
  }, [isAuthed]);

  const showError = async (response) => {
    try {
      const data = await response.json();
      setStatus(data.detail || "Request failed");
    } catch {
      setStatus("Request failed");
    }
  };

  const register = async (event) => {
    event.preventDefault();
    setStatus("");
    setBusy(true);
    try {
      const res = await fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });

      if (!res.ok) {
        await showError(res);
        return;
      }

      setStatus("Registered. You can sign in now.");
    } finally {
      setBusy(false);
    }
  };

  const login = async (event) => {
    event.preventDefault();
    setStatus("");
    setBusy(true);
    try {
      const body = new URLSearchParams();
      body.append("username", email);
      body.append("password", password);

      const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body
      });

      if (!res.ok) {
        await showError(res);
        return;
      }

      const data = await res.json();
      setToken(data.access_token);
      setStatus("Signed in.");
    } finally {
      setBusy(false);
    }
  };

  const loadNotes = async () => {
    setStatus("");
    const res = await fetch(`${API_BASE}/notes/`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!res.ok) {
      await showError(res);
      return;
    }

    const data = await res.json();
    setNotes(data);
  };

  const createNote = async (event) => {
    event.preventDefault();
    if (!title.trim()) {
      setStatus("Title is required.");
      return;
    }

    setBusy(true);
    setStatus("");
    try {
      const res = await fetch(`${API_BASE}/notes/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ title, content })
      });

      if (!res.ok) {
        await showError(res);
        return;
      }

      setTitle("");
      setContent("");
      await loadNotes();
      setStatus("Note saved.");
    } finally {
      setBusy(false);
    }
  };

  const logout = () => {
    setToken("");
    setNotes([]);
    setStatus("Signed out.");
  };

  return (
    <div className="app">
      <div className="cursor-dot" aria-hidden />
      <header className="topbar">
        <div>
          <span className="title">user_notes</span>
          <span className="subtitle">minimal notes for focused minds</span>
        </div>
        <div className="top-actions">
          <span className="api">
            API: {API_BASE ? API_BASE.replace("http://", "").replace("https://", "") : "proxy (localhost:8000)"}
          </span>
          {isAuthed && (
            <button className="ghost" onClick={logout} type="button">
              Logout
            </button>
          )}
        </div>
      </header>

      <main className="grid">
        <section className="card">
          <h2>Access</h2>
          <form className="stack" onSubmit={login}>
            <label className="field">
              <span>Email</span>
              <input
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="you@domain.com"
                required
              />
            </label>
            <label className="field">
              <span>Password</span>
              <input
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="••••••"
                required
                minLength={6}
              />
            </label>
            <div className="row">
              <button type="submit" disabled={busy}>
                Sign in
              </button>
              <button type="button" className="ghost" onClick={register} disabled={busy}>
                Register
              </button>
            </div>
          </form>
          <p className="status" role="status">
            {status || " "}
          </p>
        </section>

        <section className="card wide">
          <h2>Notes</h2>
          <form className="stack" onSubmit={createNote}>
            <label className="field">
              <span>Title</span>
              <input
                type="text"
                value={title}
                onChange={(event) => setTitle(event.target.value)}
                placeholder="New idea"
                disabled={!isAuthed || busy}
              />
            </label>
            <label className="field">
              <span>Content</span>
              <textarea
                rows={4}
                value={content}
                onChange={(event) => setContent(event.target.value)}
                placeholder="Write your thought"
                disabled={!isAuthed || busy}
              />
            </label>
            <div className="row">
              <button type="submit" disabled={!isAuthed || busy}>
                Save note
              </button>
              <button type="button" className="ghost" onClick={loadNotes} disabled={!isAuthed || busy}>
                Refresh
              </button>
            </div>
          </form>

          <div className="notes">
            {isAuthed ? (
              notes.length ? (
                notes.map((note) => (
                  <article className="note" key={note.id}>
                    <h3>{note.title}</h3>
                    <p>{note.content || "(empty)"}</p>
                  </article>
                ))
              ) : (
                <div className="empty">No notes yet.</div>
              )
            ) : (
              <div className="empty">Sign in to see your notes.</div>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

