export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

// Authenticated fetch utility
export async function authenticatedFetch(url: string, options: RequestInit = {}): Promise<Response> {
  const supabase = (await import('@/lib/supabase')).supabase;
  const { data: { session } } = await supabase.auth.getSession();
  
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers as Record<string, string>,
  };
  
  if (session?.access_token) {
    headers['Authorization'] = `Bearer ${session.access_token}`;
  }
  
  return fetch(url, {
    ...options,
    headers,
  });
}
