export const queryKeys = {
  progress: (userId: string) => ["progress", userId] as const,
  materials: () => ["materials"] as const,
  quiz: (id: string) => ["quiz", id] as const,
};
