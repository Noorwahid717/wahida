"use client";

import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Doughnut } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

const data = {
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
  },
};

export function ProgressChart() {
  return <Doughnut data={data} options={options} />;
}
