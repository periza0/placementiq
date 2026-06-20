import { FileText, Building2 } from "lucide-react";

function SourceCard({ company, file, path }) {
  return (
    <div
      // Use the backend path without adding new visible UI or changing the card layout.
      title={path}
      className="
        mt-3
        flex
        items-center
        gap-4
        rounded-2xl
        border
        border-white/10
        bg-white/5
        px-5
        py-4
        backdrop-blur-xl
        transition-all
        duration-300
        hover:border-purple-400/40
        hover:bg-white/10
      "
    >
      {/* File Icon */}
      <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-purple-500/15">
        <FileText className="h-5 w-5 text-purple-300" />
      </div>

      {/* Content */}
      <div className="flex flex-col">
        <h3 className="text-sm font-medium text-white">
          {file}
        </h3>

        <p className="mt-1 flex items-center gap-1 text-xs text-white/60">
          <Building2 size={14} />
          {company}
        </p>
      </div>
    </div>
  );
}

export default SourceCard;
