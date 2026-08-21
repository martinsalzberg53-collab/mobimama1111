import { useState } from "react";
import API from "../api/axios";
import { useLanguage } from "../context/LanguageContext";

interface Message {
  sender: "user" | "bot";
  text: string;
}

export default function Chat() {
  const { t, language } = useLanguage();
  const [messages, setMessages] = useState<Message[]>([
    {
      sender: "bot",
      text: t("chat.welcome"),
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] =
    useState<MediaRecorder | null>(null);

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
        { message: userMessage, language },
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
            t("chat.error"),
        },
      ]);
    }

    setLoading(false);
  };

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
        formData.append("language", language);

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

  return (
    <div style={{ maxWidth: 800, margin: "30px auto", padding: "0 16px" }}>
      <h2>{t("chat.title")}</h2>
      <p style={{ color: "#64748b", marginBottom: 16 }}>
        {t("chat.subtitle")}
      </p>

      <div
        style={{
          height: 500,
          overflowY: "auto",
          border: "1px solid #ddd",
          padding: 10,
          background: "#f9f9f9",
          borderRadius: 12,
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
                  m.sender === "user" ? "#4f46e5" : "#eee",
                color: m.sender === "user" ? "#fff" : "#000",
                maxWidth: "70%",
              }}
            >
              {m.text}
            </span>
          </div>
        ))}

        {loading && <p>{t("chat.processing")}</p>}
      </div>

      <div style={{ display: "flex", gap: 10, marginTop: 10 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={t("chat.placeholder")}
          style={{ flex: 1, padding: 10 }}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />

        <button onClick={sendMessage} disabled={loading}>
          {t("chat.send")}
        </button>

        <button
          onClick={recording ? stopRecording : startRecording}
          style={{
            background: recording ? "#dc2626" : "#059669",
            color: "#fff",
            padding: "10px 14px",
            borderRadius: 8,
            border: "none",
            cursor: "pointer",
          }}
        >
          {recording ? t("chat.listening") : t("chat.voice")}
        </button>
      </div>
    </div>
  );
}
