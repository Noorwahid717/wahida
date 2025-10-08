FROM node:20-bullseye

WORKDIR /app
COPY package.json pnpm-lock.yaml* package-lock.json* ./
RUN corepack enable && pnpm install --frozen-lockfile || pnpm install

COPY . .

EXPOSE 3000
CMD ["pnpm", "dev", "--hostname", "0.0.0.0", "--port", "3000"]
