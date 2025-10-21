import fs from "node:fs/promises";
import path from "node:path";
import Link from "next/link";

import matter from "gray-matter";
import ReactMarkdown from "react-markdown";

export const revalidate = 60;

interface MaterialPageProps {
  params: Promise<{ slug: string }>;
}

const CONTENT_DIR = path.join(process.cwd(), "content");

async function getMaterial(slug: string) {
  const gradeDirs = await fs.readdir(CONTENT_DIR);
  for (const grade of gradeDirs) {
    const filePath = path.join(CONTENT_DIR, grade, `${slug}.md`);
    try {
      const raw = await fs.readFile(filePath, "utf-8");
      const { data, content } = matter(raw);
      return { metadata: data as Record<string, unknown>, content, grade };
    } catch (error) {
      if (error instanceof Error && "code" in error && error.code !== "ENOENT") {
        throw error;
      }
      continue;
    }
  }
  return null;
}

async function getClassNavigation() {
  const grades = await fs.readdir(CONTENT_DIR);
  const navigation: Record<string, { title: string; slug: string }[]> = {};
  for (const grade of grades) {
    const files = await fs.readdir(path.join(CONTENT_DIR, grade));
    navigation[grade] = [];
    for (const file of files) {
      if (file.endsWith(".md")) {
        const filePath = path.join(CONTENT_DIR, grade, file);
        const raw = await fs.readFile(filePath, "utf-8");
        const { data } = matter(raw);
        navigation[grade].push({
          title: String(data.title ?? file.replace(/\.md$/, "")),
          slug: file.replace(/\.md$/, ""),
        });
      }
    }
  }
  return navigation;
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
  const resolvedParams = await params;
  const material = await getMaterial(resolvedParams.slug);
  const navigation = await getClassNavigation();
  if (!material) {
    return <div className="p-12 text-sm text-red-500">Materi tidak ditemukan.</div>;
  }
  return (
    <div className="flex min-h-screen bg-background">
      {/* Sidebar Navigation */}
      <aside className="w-64 bg-card shadow-lg p-6 overflow-y-auto border-r">
        <h2 className="text-lg font-semibold text-card-foreground mb-4">Navigasi Kelas</h2>
        {Object.entries(navigation).map(([grade, materials]) => (
          <div key={grade} className="mb-6">
            <h3 className="text-md font-medium text-muted-foreground mb-2">Kelas {grade}</h3>
            <ul className="space-y-1">
              {materials.map((mat) => (
                <li key={mat.slug}>
                  <Link
                    href={`/materials/${mat.slug}`}
                    className={`block px-3 py-2 rounded-md text-sm ${
                      mat.slug === resolvedParams.slug
                        ? "bg-primary/10 text-primary font-medium"
                        : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                    }`}
                  >
                    {mat.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8">
        <div className="max-w-4xl mx-auto">
          <header className="mb-8">
            <h1 className="text-4xl font-bold text-foreground mb-2">
              {String(material.metadata.title ?? resolvedParams.slug)}
            </h1>
            <p className="text-lg text-muted-foreground">
              Kelas {material.grade} · Topik {String(material.metadata.topik)} · Level {String(material.metadata.level)}
            </p>
            <div className="mt-4 flex gap-2">
              <span className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm font-medium">
                {material.grade}
              </span>
              <span className="px-3 py-1 bg-accent text-accent-foreground rounded-full text-sm font-medium">
                {String(material.metadata.topik)}
              </span>
            </div>
          </header>
          <article className="prose prose-lg dark:prose-invert max-w-none bg-card p-8 rounded-lg shadow-sm border">
            <ReactMarkdown
              components={{
                h1: ({ children }) => <h1 className="text-3xl font-bold text-foreground mb-4">{children}</h1>,
                h2: ({ children }) => <h2 className="text-2xl font-semibold text-foreground mb-3">{children}</h2>,
                p: ({ children }) => <p className="text-card-foreground mb-4 leading-relaxed">{children}</p>,
                ul: ({ children }) => <ul className="list-disc list-inside text-card-foreground mb-4 space-y-1">{children}</ul>,
                ol: ({ children }) => <ol className="list-decimal list-inside text-card-foreground mb-4 space-y-1">{children}</ol>,
                code: ({ children }) => <code className="bg-muted px-2 py-1 rounded text-sm font-mono text-foreground">{children}</code>,
                pre: ({ children }) => <pre className="bg-muted p-4 rounded overflow-x-auto">{children}</pre>,
              }}
            >
              {material.content}
            </ReactMarkdown>
          </article>
        </div>
      </main>
    </div>
  );
}
