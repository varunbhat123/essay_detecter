import * as React from "react";

type TextareaProps = React.TextareaHTMLAttributes<HTMLTextAreaElement> & {
  label?: string;
  helper?: string;
};

export function Textarea({ label, helper, className = "", ...props }: TextareaProps) {
  return (
    <div className="w-full">
      {label ? (
        <label className="mb-2 block text-sm font-medium text-slate-200">{label}</label>
      ) : null}
      <textarea
        className={`min-h-[260px] w-full rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-base text-slate-100 shadow-inner shadow-slate-950/30 outline-none transition focus:border-cyan-400/60 focus:ring-2 focus:ring-cyan-400/20 ${className}`}
        {...props}
      />
      {helper ? <p className="mt-2 text-xs text-slate-400">{helper}</p> : null}
    </div>
  );
}
