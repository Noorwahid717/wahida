interface StreakBadgeProps {
  current: number;
  longest: number;
  name: string;
  icon: string;
}

export function StreakBadge({ current, longest, name, icon }: StreakBadgeProps) {
  return (
    <div className="flex items-center gap-3 rounded-lg border bg-accent px-4 py-3 text-accent-foreground">
      <span className="text-2xl" role="img" aria-label={name}>
        {icon}
      </span>
      <div>
        <p className="text-sm font-semibold">{name}</p>
        <p className="text-xs opacity-90">Streak saat ini {current} hari · Terpanjang {longest} hari</p>
      </div>
    </div>
  );
}
