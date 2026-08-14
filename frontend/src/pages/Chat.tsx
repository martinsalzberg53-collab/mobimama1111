import { useState } from "react";
import API from "../api/axios";

interface Message {
  sender: "user" | "bot";
  text: string;
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      sender: "bot",
      text: "👋 Hi! I'm Mobi AI. Ask me anything or speak in Twi 🎤",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] =
    useState<MediaRecorder | null>(null);

  // ---------------- TEXT CHAT ----------------
  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input;

    setMessages((prev) => [
      ...prev,
      { sender: "user", text: userMessage },
    ]);

    setInput("");
    setLoading(true);

    try {
      const res = await API.post(
        "/chat/",
        { message: userMessage },
        { timeout: 15000 }
      );

      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: res.data.reply },
      ]);
    } catch (err: any) {
      console.log("CHAT ERROR:", err);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text:
            err?.response?.data?.error ||
            "❌ Error connecting to Mobi AI (backend failed)",
        },
      ]);
    }

    setLoading(false);
  };

  // ---------------- VOICE CHAT ----------------
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      const recorder = new MediaRecorder(stream);
      setMediaRecorder(recorder);

      const chunks: Blob[] = [];

      recorder.ondataavailable = (e) => chunks.push(e.data);

      recorder.onstop = async () => {
        const audioBlob = new Blob(chunks, { type: "audio/webm" });

        const formData = new FormData();
        formData.append("audio", audioBlob);

        try {
          const res = await API.post(
            "/chat/voice/",
            formData,
            { headers: { "Content-Type": "multipart/form-data" } }
          );

          setMessages((prev) => [
            ...prev,
            {
              sender: "user",
              text: res.data.english_text || "🎤 Voice input",
            },
            { sender: "bot", text: res.data.reply },
          ]);
        } catch (err: any) {
          console.log("VOICE ERROR:", err);

          setMessages((prev) => [
            ...prev,
            {
              sender: "bot",
              text:
                err?.response?.data?.error ||
                "❌ Voice processing failed",
            },
          ]);
        }
      };

      recorder.start();
      setRecording(true);
    } catch (err) {
      console.log("MIC ERROR:", err);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "❌ Microphone access denied",
        },
      ]);
    }
  };

  const stopRecording = () => {
    mediaRecorder?.stop();
    setRecording(false);
  };

  // ---------------- UI ----------------
  return (
    <div style={{ maxWidth: 800, margin: "30px auto" }}>
      <h2>🤖 Mobi AI Chat</h2>

      <div
        style={{
          height: 500,
          overflowY: "auto",
          border: "1px solid #ddd",
          padding: 10,
          background: "#f9f9f9",
        }}
      >
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              textAlign: m.sender === "user" ? "right" : "left",
              margin: 10,
            }}
          >
            <span
              style={{
                display: "inline-block",
                padding: 10,
                borderRadius: 10,
                background:
                  m.sender === "user" ? "#007bff" : "#eee",
                color: m.sender === "user" ? "#fff" : "#000",
                maxWidth: "70%",
              }}
            >
              {m.text}
            </span>
          </div>
        ))}

        {loading && <p>🤖 Mobi is thinking...</p>}
      </div>

      <div style={{ display: "flex", gap: 10, marginTop: 10 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask Mobi..."
          style={{ flex: 1, padding: 10 }}
        />

        <button onClick={sendMessage} disabled={loading}>
          Send
        </button>

        <button
          onClick={recording ? stopRecording : startRecording}
          style={{
            background: recording ? "red" : "green",
            color: "#fff",
            padding: "10px",
          }}
        >
          {recording ? "Stop 🎙️" : "Speak 🎤"}
        </button>
      </div>
    </div>
  );
}