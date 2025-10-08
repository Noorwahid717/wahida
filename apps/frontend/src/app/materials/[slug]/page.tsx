import fs from "node:fs/promises";
import path from "node:path";

import matter from "gray-matter";
import ReactMarkdown from "react-markdown";

export const revalidate = 60;

interface MaterialPageProps {
  params: { slug: string };
}

const CONTENT_DIR = path.join(process.cwd(), "content");

async function getMaterial(slug: string) {
  const gradeDirs = await fs.readdir(CONTENT_DIR);
  for (const grade of gradeDirs) {
    const filePath = path.join(CONTENT_DIR, grade, `${slug}.md`);
    try {
      const raw = await fs.readFile(filePath, "utf-8");
      const { data, content } = matter(raw);
      return { metadata: data as Record<string, unknown>, content };
    } catch (error) {
      if (error instanceof Error && "code" in error && error.code !== "ENOENT") {
        throw error;
      }
      continue;
    }
  }
  return null;
}

export async function generateStaticParams() {
  const params: { slug: string }[] = [];
  const gradeDirs = await fs.readdir(CONTENT_DIR);
  for (const grade of gradeDirs) {
    const files = await fs.readdir(path.join(CONTENT_DIR, grade));
    params.push(...files.filter((file) => file.endsWith(".md")).map((file) => ({ slug: file.replace(/\.md$/, "") })));
  }
  return params;
}

export default async function MaterialPage({ params }: MaterialPageProps) {
  const material = await getMaterial(params.slug);
  if (!material) {
    return <div className="p-12 text-sm text-red-500">Materi tidak ditemukan.</div>;
  }
  return (
    <div className="mx-auto flex w-full max-w-4xl flex-col gap-4 px-6 py-12">
      <header>
        <h1 className="text-3xl font-bold text-slate-900">{String(material.metadata.title ?? params.slug)}</h1>
        <p className="text-sm text-slate-500">
          Kelas {String(material.metadata.kelas)} · Topik {String(material.metadata.topik)} · Level {String(material.metadata.level)}
        </p>
      </header>
      <article className="prose max-w-none">
        <ReactMarkdown>{material.content}</ReactMarkdown>
      </article>
    </div>
  );
}
