interface StreakBadgeProps {
  current: number;
  longest: number;
  name: string;
  icon: string;
}

export function StreakBadge({ current, longest, name, icon }: StreakBadgeProps) {
  return (
    <div className="flex items-center gap-3 rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-amber-900">
      <span className="text-2xl" role="img" aria-label={name}>
        {icon}
      </span>
      <div>
        <p className="text-sm font-semibold">{name}</p>
        <p className="text-xs">Streak saat ini {current} hari · Terpanjang {longest} hari</p>
      </div>
    </div>
  );
}
