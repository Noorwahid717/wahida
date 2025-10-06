import { ImageResponse } from "next/og";

export const size = {
  width: 64,
  height: 64,
};

export const contentType = "image/png";

export default function Icon() {
  return new ImageResponse(
    (
      <div
        style={{
          height: "100%",
          width: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: "linear-gradient(135deg, #1e3a8a, #9333ea)",
          fontSize: 32,
          color: "white",
          fontWeight: 700,
        }}
      >
        WA
      </div>
    ),
    {
      ...size,
    }
  );
}
