import { useState } from "react";
import { SendHorizontal } from "lucide-react";
import logo from "../assets/polarislogo.png";
function InputBox({ input, setInput, onSend, loading }) {
  const [focused, setFocused] = useState(false);

  const handleKeyDown = (e) => {
    // Enter sends the current prompt; Shift+Enter keeps the textarea multiline.
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  return (
    <div className="fixed bottom-6 left-1/2 z-50 w-[95%] max-w-4xl -translate-x-1/2">

      <div className="relative flex items-end rounded-3xl border border-white/10 bg-white/10 backdrop-blur-xl">

        {input.length === 0 && !focused && (

          <div className="pointer-events-none absolute left-6 top-4 flex max-w-[calc(100%-6rem)] items-start gap-2 text-white/40">
            <img
              src={logo}
              alt="Polaris"
              className="mt-1 h-4 w-4 shrink-0 object-contain"
            />
            <span className="leading-6">
              Hi! I'm Polaris. Ask me anything about your placement job descriptions.
            </span>
          </div>
        )}

        <textarea
          rows={1}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          onKeyDown={handleKeyDown}
          placeholder=""
          className="
            h-20
            flex-1
            resize-none
            bg-transparent
            px-6
            py-5
            text-white
            placeholder:text-white/40
            outline-none
            relative
            z-10
          "
        />

        <button
          onClick={onSend}
          disabled={loading}
          className="
            m-3
            flex
            h-12
            w-12
            items-center
            justify-center
            rounded-full
            bg-white
            text-black
            transition
            hover:scale-105
            disabled:opacity-40
          "
        >
          <SendHorizontal size={20} />
        </button>

      </div>
{/* Footer */}
<div className="mt-4 flex items-center justify-center gap-2 text-xs text-white/60">
  <img
    src={logo}
    alt="Polaris"
    className="h-4 w-4 object-contain"
  />

  <p>
    <span className="font-medium text-white/80">Polaris</span> — Your Guiding Star for understanding job descriptions.
  </p>
</div>
    </div>

  );
}


export default InputBox;
