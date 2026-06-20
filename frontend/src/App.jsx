import { useEffect, useRef, useState } from "react";
import { sendMessage } from "./services/api";
import Navbar from "./components/Navbar";
import InputBox from "./components/InputBox";
import Message from "./components/Message";

const LOADING_MESSAGE_ID = "polaris-loading";
const SOURCE_REQUEST_WORDS = ["source", "sources", "file", "files", "document", "documents"];

function shouldShowSources(question) {
  return SOURCE_REQUEST_WORDS.some((word) =>
    question.toLowerCase().includes(word)
  );
}

function uniqueCompanyNames(sources) {
  return [...new Set(sources.map((source) => source.company).filter(Boolean))];
}

function App() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // Keep the newest chat item visible after every message or loading-state update.
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const question = input;
    const showSources = shouldShowSources(question);

    // Add the user message and the temporary Polaris loading message in one update.
    setMessages((prev) => [
      ...prev,
      {
        id: `user-${Date.now()}`,
        role: "user",
        text: question,
        sources: [],
        showSources: false,
      },
      {
        id: LOADING_MESSAGE_ID,
        role: "assistant",
        text: "Polaris is searching 600+ job descriptions...",
        sources: [],
        showSources,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const data = await sendMessage(question);
      const sources = Array.isArray(data.sources) ? data.sources : [];

      setMessages((prev) =>
        prev.map((message) =>
          message.id === LOADING_MESSAGE_ID
            ? {
                // Replace the temporary loading item with the real assistant response.
                id: `assistant-${Date.now()}`,
                role: "assistant",
                text: data.answer,
                // Keep sources hidden unless the user explicitly asks for them.
                sources,
                showSources,
              }
            : message
        )
      );
    } catch (error) {
      setMessages((prev) =>
        prev.map((message) =>
          message.id === LOADING_MESSAGE_ID
            ? {
                // Keep failures in the normal chat stream so the user sees what happened.
                id: `error-${Date.now()}`,
                role: "assistant",
                text: "Something went wrong. Please try again.",
                sources: [],
                showSources: false,
              }
            : message
        )
      );

      console.error(error);
    }

    setLoading(false);
  };

  return (
    <main className="relative h-screen overflow-hidden bg-[#080A10]">

      {/* Background */}
      <div
        className="absolute inset-0 "
        style={{
          background: `
            radial-gradient(ellipse 55% 65% at 79% 47%, rgba(186,36,128,.48) 0%, rgba(116,27,103,.27) 34%, transparent 64%),
            radial-gradient(ellipse 48% 58% at 10% 78%, rgba(150,45,125,.34) 0%, rgba(76,28,88,.28) 36%, transparent 72%),
            radial-gradient(ellipse 60% 85% at 22% 30%, rgba(78,28,104,.46) 0%, rgba(45,20,68,.42) 42%, transparent 76%),
            radial-gradient(ellipse 38% 70% at 48% 62%, rgba(5,5,12,.78) 0%, rgba(11,8,22,.5) 45%, transparent 76%),
            linear-gradient(90deg,#1B0D2C 0%,#261032 25%,#191027 51%,#060b0f 100%)
          `,
        }}
      />

      <Navbar />


      {/* This full-width section owns scrolling so the scrollbar stays at the viewport edge. */}
      <section className="relative z-10 h-full w-full overflow-y-auto">
        <div className="mx-auto flex min-h-full w-full max-w-3xl flex-col gap-4 px-5 pt-20 pb-44">

          {messages.map((message) => (
            <div key={message.id}>

              <Message
                role={message.role}
                text={message.text}
                loading={message.id === LOADING_MESSAGE_ID}
              />

              {message.showSources && message.sources?.length > 0 && (
                // Show source names only when the user asks, without file-style cards.
                <p className="mt-2 text-sm leading-6 text-white/60 sm:text-xs">
                  Sources: {uniqueCompanyNames(message.sources).join(", ")}
                </p>
              )}

            </div>
          ))}

          <div ref={messagesEndRef} />
        </div>

      </section>

      <InputBox
        input={input}
        setInput={setInput}
        onSend={handleSend}
        loading={loading}
      />
    </main>
  );
}

export default App;
