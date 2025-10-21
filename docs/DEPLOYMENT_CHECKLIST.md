# Wahida Production Deployment Checklist

## 🔍 Pre-Deployment Verification

### Environment Setup
- [ ] `.env.production` file created and populated with production values
- [ ] All required API keys configured:
  - [ ] `OPENAI_API_KEY`
  - [ ] `GOOGLE_GEMINI_API_KEY`
  - [ ] `SUPABASE_URL` and `SUPABASE_ANON_KEY`
  - [ ] `POSTHOG_API_KEY`
  - [ ] `JUDGE0_RAPIDAPI_KEY`
  - [ ] `SUPABASE_JWT_SECRET`

### Code Quality
- [ ] All tests passing (`npm test` in frontend, pytest in API)
- [ ] Linting clean (`npm run lint` in frontend)
- [ ] Type checking successful (`npm run type-check` in frontend)
- [ ] Database migrations up to date

## 🐳 Local Testing

### Docker Build Testing
- [ ] API Dockerfile.prod builds successfully
- [ ] Frontend Dockerfile.prod builds successfully
- [ ] Production docker-compose.prod.yml starts without errors
- [ ] All services healthy (PostgreSQL, Redis, API, Web)
- [ ] API health check passes (`curl http://localhost:8000/healthz`)
- [ ] Frontend accessible (`curl http://localhost:3000`)

### Data Seeding
- [ ] Quiz data seeded successfully
- [ ] Content data ingested
- [ ] Vector embeddings generated

## ☁️ Cloud Infrastructure Setup

### Railway (Backend)
- [ ] Railway account created
- [ ] GitHub repository connected to Railway
- [ ] PostgreSQL database provisioned
- [ ] Redis database provisioned
- [ ] Environment variables configured in Railway dashboard
- [ ] API service deployed successfully
- [ ] Database migrations run automatically

### Vercel (Frontend)
- [ ] Vercel account created
- [ ] GitHub repository connected to Vercel
- [ ] Build settings configured:
  - [ ] Build Command: `cd apps/frontend && pnpm build`
  - [ ] Output Directory: `apps/frontend/.next`
  - [ ] Install Command: `pnpm install`
- [ ] Environment variables set in Vercel dashboard
- [ ] Frontend deployed successfully

## 🔗 Domain & Networking

### Domain Configuration
- [ ] Custom domain purchased/available
- [ ] DNS records configured:
  - [ ] Frontend: CNAME to Vercel
  - [ ] Backend: CNAME to Railway
- [ ] SSL certificates auto-provisioned

### CORS & Security
- [ ] CORS origins configured for production domain
- [ ] Environment-specific security headers set
- [ ] Rate limiting configured appropriately

## 📊 Monitoring & Analytics

### PostHog Setup
- [ ] PostHog project created
- [ ] API key configured in both frontend and backend
- [ ] Analytics events tracking user interactions
- [ ] Error tracking enabled

### Health Monitoring
- [ ] Railway health checks configured
- [ ] Vercel deployment monitoring active
- [ ] Database connection monitoring
- [ ] API response time monitoring

## 🧪 Production Testing

### Functional Testing
- [ ] User authentication flow works
- [ ] Chat functionality operational
- [ ] Quiz system functional
- [ ] Code execution working
- [ ] Progress tracking saving data
- [ ] Material browsing working

### Performance Testing
- [ ] Page load times acceptable (< 3 seconds)
- [ ] API response times < 500ms
- [ ] Database queries optimized
- [ ] Static assets properly cached

### Security Testing
- [ ] Authentication required for protected routes
- [ ] API keys not exposed in frontend
- [ ] HTTPS enforced everywhere
- [ ] No sensitive data in logs

## 🚀 Go-Live Preparation

### Backup & Recovery
- [ ] Database backup strategy in place
- [ ] Rollback plan documented
- [ ] Emergency contact list ready

### Documentation
- [ ] User documentation updated
- [ ] API documentation accessible
- [ ] Deployment runbook complete
- [ ] Troubleshooting guide ready

### Team Communication
- [ ] Stakeholders notified of launch date
- [ ] Support team briefed
- [ ] Monitoring alerts configured
- [ ] Incident response plan ready

## 🎯 Post-Launch Activities

### Monitoring (First 24 hours)
- [ ] Error rates monitored
- [ ] User sign-up rates tracked
- [ ] Performance metrics collected
- [ ] Database load monitored

### Optimization
- [ ] CDN configuration optimized
- [ ] Database indexes reviewed
- [ ] Caching strategies implemented
- [ ] Bundle sizes optimized

### User Feedback
- [ ] User feedback collection active
- [ ] Support tickets monitored
- [ ] Feature usage analytics reviewed
- [ ] A/B testing setup for improvements

---

## 📋 Quick Reference Commands

### Local Testing
```bash
# Test production build locally
docker-compose -f docker-compose.prod.yml up --build -d

# Check service health
curl http://localhost:8000/healthz
curl http://localhost:3000

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Deployment
```bash
# Run deployment script
./scripts/deploy.sh

# Manual Railway deployment
railway deploy

# Manual Vercel deployment
vercel --prod
```

### Monitoring
```bash
# Check Railway logs
railway logs

# Check Vercel deployment
vercel logs

# Database health
railway psql
```

---

**Status:** ⏳ Ready for deployment
**Last Updated:** Oktober 19, 2025</content>
<parameter name="filePath">/home/noah/project/wahida/docs/DEPLOYMENT_CHECKLIST.md