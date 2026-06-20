import logo from "../assets/polarislogo.png";

function Message({
  role,
  text,
  loading = false,
}) {
  const isUser = role === "user";

  return (
    <div
      className={`mb-8 flex w-full ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`max-w-3xl rounded-3xl px-6 py-5 ${
          isUser
            ? "bg-white text-black"
            : "border border-white/10 bg-white/5 text-white backdrop-blur-xl"
        }`}
      >
        {!isUser && (
          <div className="mb-4 flex items-center gap-2">
            <img
              src={logo}
              alt="Polaris"
              className="h-6 w-6"
            />

            <span className="font-medium">
              Polaris
            </span>
          </div>
        )}

        {loading ? (
          <p className="text-white/80">
            {/* Loading copy is passed from App so chat state owns what appears. */}
            {text}
          </p>
        ) : (
          <p className="whitespace-pre-wrap leading-7">
            {text}
          </p>
        )}
      </div>
    </div>
  );
}

export default Message;
