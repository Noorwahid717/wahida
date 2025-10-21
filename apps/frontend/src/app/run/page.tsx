import { AuthGuard } from "@/components/auth-guard";

export default function RunPage() {
  return (
    <AuthGuard>
      <div className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-6 py-12">
        <header>
          <h1 className="text-3xl font-bold text-foreground">Sandbox Kode</h1>
          <p className="text-sm text-muted-foreground">Jalankan kode Python dengan aman.</p>
        </header>
        <div className="rounded-lg border bg-card p-6 shadow-sm">
          <p className="text-muted-foreground">Fitur ini sedang dalam pengembangan. Gunakan MSW mock untuk testing.</p>
        </div>
      </div>
    </AuthGuard>
  );
}