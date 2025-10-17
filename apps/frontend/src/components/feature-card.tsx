import Link from "next/link";
import { ReactNode } from "react";

import { cn } from "@/lib/utils";

interface FeatureCardProps {
  title: string;
  description: string;
  icon: ReactNode;
  href?: string;
  className?: string;
}

export function FeatureCard({ title, description, icon, href, className }: FeatureCardProps) {
  const content = (
    <div
      className={cn(
        "rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur shadow-lg cursor-pointer transition-all hover:shadow-xl hover:scale-105",
        "dark:bg-slate-900/40 dark:border-slate-700/60",
        className,
      )}
    >
      <div className="flex items-start gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-purple-500 to-indigo-500 text-white">
          {icon}
        </div>
        <div>
          <h3 className="text-xl font-semibold text-slate-900 dark:text-slate-50">{title}</h3>
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-200/80">{description}</p>
        </div>
      </div>
    </div>
  );

  if (href) {
    return <Link href={href}>{content}</Link>;
  }

  return content;
}
