# Wahida Production Deployment Guide

## Overview

Wahida is a full-stack educational AI platform with the following components:
- **Frontend**: Next.js 15 with TypeScript, Tailwind CSS
- **Backend**: FastAPI with Python, PostgreSQL, Redis
- **AI Services**: OpenAI GPT, Google Gemini, FAISS vector search
- **Infrastructure**: Docker, Railway, Vercel

## Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Vercel        │    │   Railway       │
│   Frontend      │◄──►│   Backend API   │
│   (Next.js)     │    │   (FastAPI)     │
└─────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   Supabase      │    │   Railway       │
│   Auth & DB     │    │   PostgreSQL    │
│                 │    │   Redis         │
└─────────────────┘    └─────────────────┘
```

## Prerequisites

- GitHub account
- Railway account (for backend/database)
- Vercel account (for frontend)
- Supabase account (for auth)
- API keys for services

## Step 1: Environment Setup

### 1.1 Clone and configure

```bash
git clone https://github.com/noah-isme/wahida.git
cd wahida
cp .env.production.example .env.production
```

### 1.2 Set up external services

#### Supabase (Authentication & Database)
1. Create project at https://supabase.com
2. Get `SUPABASE_URL` and `SUPABASE_ANON_KEY`
3. Configure authentication providers (Email)

#### Railway (Backend Infrastructure)
1. Create account at https://railway.app
2. Create PostgreSQL database
3. Create Redis database
4. Get connection strings

#### API Keys
- OpenAI API Key
- Google Gemini API Key
- PostHog API Key (for analytics)

### 1.3 Configure environment variables

Edit `.env.production` with your actual values:

```bash
# Database
POSTGRES_DSN=postgresql+psycopg://user:pass@host:5432/db

# Redis
REDIS_URL=rediss://default:pass@host:port

# Auth
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key

# AI Services
OPENAI_API_KEY=sk-...
GOOGLE_GEMINI_API_KEY=AIza...

# Analytics
POSTHOG_API_KEY=phc_...
```

## Step 2: Backend Deployment (Railway)

### 2.1 Create Railway project

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
railway init wahida-backend
```

### 2.2 Deploy services

#### PostgreSQL Database
```bash
railway add postgresql
railway variables set POSTGRES_DSN=your-connection-string
```

#### Redis Database
```bash
railway add redis
railway variables set REDIS_URL=your-redis-url
```

#### API Service
```bash
railway add --name api
railway variables set APP_NAME="Wahida API Production"
railway variables set BACKEND_CORS_ORIGINS="https://wahida.vercel.app"
# Set all other environment variables...
```

### 2.3 Deploy

```bash
railway up
```

## Step 3: Frontend Deployment (Vercel)

### 3.1 Install Vercel CLI

```bash
npm install -g vercel
vercel login
```

### 3.2 Deploy frontend

```bash
cd apps/frontend
vercel --prod

# Set environment variables
vercel env add NEXT_PUBLIC_API_BASE_URL
vercel env add NEXT_PUBLIC_SUPABASE_URL
vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY
vercel env add NEXT_PUBLIC_POSTHOG_KEY
```

### 3.3 Configure domain

```bash
vercel domains add wahida.vercel.app
```

## Step 4: Database Setup

### 4.1 Run migrations

```bash
# Connect to Railway PostgreSQL
railway connect

# Run migrations (if using Alembic)
alembic upgrade head
```

### 4.2 Seed initial data

```bash
# Run seed script
python scripts/seed_quiz_standalone.py
```

## Step 5: Testing & Monitoring

### 5.1 Health checks

```bash
# API health
curl https://your-api.railway.app/healthz

# Frontend
curl https://wahida.vercel.app
```

### 5.2 Monitoring

- **PostHog**: Analytics and user tracking
- **Railway**: Application logs and metrics
- **Supabase**: Auth logs and database monitoring

## Step 6: DNS & SSL

Railway and Vercel provide automatic SSL certificates. Configure your domain:

1. Add CNAME record pointing to Vercel
2. Update CORS origins in Railway environment
3. Test HTTPS everywhere

## Troubleshooting

### Common Issues

1. **CORS errors**: Check `BACKEND_CORS_ORIGINS` in Railway
2. **Database connection**: Verify PostgreSQL connection string
3. **Auth issues**: Check Supabase configuration
4. **Build failures**: Check Docker logs in Railway

### Logs

```bash
# Railway logs
railway logs

# Vercel logs
vercel logs
```

## Performance Optimization

1. **Database indexing**: Add indexes on frequently queried columns
2. **Caching**: Implement Redis caching for API responses
3. **CDN**: Use Vercel's edge network for global distribution
4. **Monitoring**: Set up alerts for performance metrics

## Security Checklist

- [ ] Environment variables not committed to git
- [ ] Database credentials rotated regularly
- [ ] HTTPS enabled everywhere
- [ ] CORS properly configured
- [ ] API rate limiting active
- [ ] Authentication required for sensitive endpoints
- [ ] Input validation and sanitization
- [ ] Dependencies updated regularly

## Cost Estimation

- **Railway**: ~$10-20/month (database + app hosting)
- **Vercel**: ~$0-20/month (depending on usage)
- **Supabase**: ~$0-25/month (depending on usage)
- **External APIs**: Pay per usage

## Support

For issues or questions:
- GitHub Issues: https://github.com/noah-isme/wahida/issues
- Documentation: https://github.com/noah-isme/wahida/docs

---

🎉 **Congratulations! Wahida is now live in production!**

Your educational AI platform is ready to help students learn with personalized AI tutoring, interactive quizzes, and comprehensive progress tracking.