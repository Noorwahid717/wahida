"use client";

import { useQuery } from "@tanstack/react-query";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Doughnut } from "react-chartjs-2";
import { useAuth } from "@/app/providers";
import { authenticatedFetch, API_BASE_URL } from "@/lib/api";

ChartJS.register(ArcElement, Tooltip, Legend);

interface ProgressData {
  user_id: string;
  streak_days: number;
  badges: string[];
  last_active: string;
}

export function ProgressChart() {
  const { user } = useAuth();

  const { data, isLoading, error } = useQuery({
    queryKey: ["progress"],
    queryFn: () => fetchProgress(user!.id),
    enabled: !!user, // Only run if user is authenticated
  });

  async function fetchProgress(userId: string): Promise<ProgressData> {
    const response = await authenticatedFetch(
      `${API_BASE_URL}/api/progress/${userId}`
    );
    if (!response.ok) {
      throw new Error("Failed to fetch progress");
    }
    return response.json();
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        Loading progress...
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64 text-red-500">
        Error loading progress
      </div>
    );
  }

  // Use real data if available, otherwise fallback to demo data
  const progressData = data
    ? {
        labels: ["Streak Days", "Badges Earned", "Activities"],
        datasets: [
          {
            label: "Progress",
            data: [
              data.streak_days,
              data.badges.length,
              Math.min(data.streak_days * 2, 100), // Estimate activities
            ],
            backgroundColor: [
              "rgba(79, 70, 229, 0.8)",
              "rgba(236, 72, 153, 0.8)",
              "rgba(34, 197, 94, 0.8)",
            ],
            borderWidth: 0,
          },
        ],
      }
    : {
        labels: ["Materi", "Kuis", "Latihan"],
        datasets: [
          {
            label: "Progres",
            data: [65, 45, 30],
            backgroundColor: [
              "rgba(79, 70, 229, 0.8)",
              "rgba(236, 72, 153, 0.8)",
              "rgba(34, 197, 94, 0.8)",
            ],
            borderWidth: 0,
          },
        ],
      };

  const options = {
    plugins: {
      legend: {
        display: true,
        position: "bottom" as const,
      },
      tooltip: {
        callbacks: {
          label: function (context: { label?: string; parsed: number }) {
            const label = context.label || "";
            const value = context.parsed;
            if (data && label === "Streak Days") {
              return `${label}: ${value} days`;
            }
            if (data && label === "Badges Earned") {
              return `${label}: ${value}`;
            }
            return `${label}: ${value}%`;
          },
        },
      },
    },
  };

  return <Doughnut data={progressData} options={options} />;
}
