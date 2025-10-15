# MAGUS 

![magus icon](https://github.com/Hyliana/gaebolg/blob/c370d729505a8ee35047fe2385bf7cf7794cda2f/krono/magus/static/magus/favicon.ico)

[![Version](https://img.shields.io/badge/version-2.0.0--beta-blue.svg)](https://github.com/yourusername/magus)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.0.7-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/react-18.3-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/typescript-5.6-blue.svg)](https://www.typescriptlang.org/)

*formerly known as gaebolg*

---

## The Story

I built the first version of MAGUS over a weekend a few months back because my team needed to track how we were spending our time in a high-pressure, real-time response environment. I had SQL knowledge, some Python chops, and enough web dev experience to cobble together a Django app with PostgreSQL and Redis backing it. My friend @Malathair and ChatGPT helped me fill in the gaps, and I went from concept to deployment in about three days.

That first version worked. It solved the problem. But it was never meant to last.

Fast forward to October 2025: I realized I didn't need a corporate time-tracking tool. **I needed to understand how I spend my life.** Not for a boss, not for a report, but for *me*. I needed self-analysis without the pain. I needed data-gathering that didn't feel like work.

So I sat down with Cursor AI and rebuilt MAGUS from the ground up. What you're looking at now is the result of a single 15-hour session where we:

- Ripped out the Electron wrapper and went full PWA
- Added a modern React + TypeScript frontend
- Built a proper REST API with DRF
- Containerized everything with Docker
- Made it beautiful, fast, and actually enjoyable to use
- Added analytics so I could see patterns in my time
- Built in automation via API keys
- Made it extensible without being bloated

This isn't a quick-and-dirty fix anymore. **This is a tool I actually want to use every day.**

---

## What Is MAGUS?

MAGUS is a self-hosted personal time tracking and life analytics platform. It's designed around a simple philosophy: **tracking your time shouldn't feel like a chore.**

One tap to start. One tap to stop. Live updates. Beautiful charts. Export your data whenever you want. Automate it if you're into that. But most importantly: **it stays out of your way.**

---

## Core Philosophy

### For Humans, Not Corporations

Traditional time tracking is built for managers, not for you. MAGUS flips that. This is about understanding yourself:

- How much deep work did I actually do today?
- When am I most productive?
- Am I spending time where I want to spend it?

No timesheets. No approvals. No justifications. Just data, insights, and understanding.

### Friction-Free Tracking

The best time tracker is the one you'll actually use. MAGUS is designed for minimum viable interaction:

- **1-2 taps to track anything**
- No scrolling required for primary actions
- Smart state management (start becomes stop automatically)
- Mistakes are easy to fix
- Works offline (coming soon)

### Your Data, Your Server

Self-hosted means you own everything. No tracking, no telemetry, no third-party services. Your time data lives on your infrastructure, period.

GDPR-compliant data export and deletion built in, because even if it's just for you, it should be done right.

---

## Features

### Time Tracking
- **One-Tap Tracking:** Quick start grid for your favorite tasks
- **Live Timer:** See elapsed time update in real-time
- **Smart Interruption:** Switch tasks with automatic interruption handling
- **Task History:** View and edit all your time entries
- **Manual Editing:** Fix mistakes without needing admin access

### Customization
- **Custom Task Types:** Create your own categories with emoji and colors
- **Pin Favorites:** Keep frequent tasks at your fingertips
- **Archive Old Tasks:** Hide without deleting (data integrity preserved)
- **Per-User Lists:** Multi-user support with isolated task lists

### Analytics
- **Today's Summary:** At-a-glance breakdown with progress bars
- **Time Views:** Switch between today, week, and month
- **Beautiful Charts:** Bar charts and pie charts using your task colors
- **Detailed Stats:** Session counts, durations, percentages

### Data & Automation
- **CSV Export:** Download or email your time data
- **API Keys:** Generate tokens for automation and integrations
- **Full REST API:** Documented with OpenAPI/Swagger
- **iOS Shortcuts Ready:** Automate tracking from your phone
- **Celery Tasks:** Background jobs for exports and scheduled tasks

---

## Tech Stack

### Backend
- **Django 5.0.7** - Web framework
- **Django REST Framework** - API
- **PostgreSQL 16** - Database
- **Redis 7** - Cache & Celery broker
- **Celery** - Async tasks
- **Gunicorn** - WSGI server

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TanStack Query** - Server state
- **Zustand** - Client state
- **TailwindCSS** - Styling
- **Recharts** - Data visualization

### DevOps
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy
- **GitHub Actions** - CI/CD
- **Let's Encrypt Ready** - SSL/TLS

---

## Quick Start

### Prerequisites

- Docker Engine 24.0+
- Docker Compose 2.20+
- 4GB RAM minimum
- 10GB disk space

### Setup (5 Minutes)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/magus.git
cd magus

# 2. Create environment file
cp env.template .env

# 3. Start everything
docker-compose up -d

# 4. Wait for services to be healthy (~30 seconds)
docker-compose ps

# 5. Open your browser
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/api/docs/
```

### First User

```bash
# Create your account via the UI at http://localhost:5173/register
# Or create a superuser for admin access:
docker-compose exec web python manage.py createsuperuser
```

That's it. You're tracking time.

---

## How It Works

### The User Experience

1. **Register** - Create your account (default task types auto-created)
2. **Customize** - Add your own task types in Settings
3. **Track** - Tap a task to start tracking
4. **Analyze** - View your time breakdown and charts
5. **Export** - Download CSV whenever you want
6. **Automate** - Generate API keys for integrations

### The Architecture

```
Browser/PWA
    ↓
Nginx (Reverse Proxy)
    ↓
Django API + React SPA
    ↓
PostgreSQL + Redis + Celery
```

Everything runs in Docker. One command to start, one command to stop.

---

## API Usage

### Generate an API Key

1. Go to Settings → API Keys
2. Enter a name, click "Generate Key"
3. **Copy the key immediately** - it's only shown once!

### Example: Start Tracking via API

```bash
curl -X POST http://localhost:8000/api/tasks/start/ \
  -H "Authorization: Api-Key your_generated_key" \
  -H "Content-Type: application/json" \
  -d '{"task_type_id": 1, "notes": "Deep work session"}'
```

### iOS Shortcuts Integration

1. Create new Shortcut
2. Add "Get Contents of URL"
3. Method: POST
4. URL: `http://your-server:8000/api/tasks/start/`
5. Headers: 
   - `Authorization: Api-Key YOUR_KEY`
   - `Content-Type: application/json`
6. Body: `{"task_type_id": 1}`

Done. Now you can track time from Siri or widgets.

Full API documentation: http://localhost:8000/api/docs/

---

## Development Journey

### Version History

**v1.0** (2024) - Original MAGUS
- Corporate time-tracking tool
- Electron wrapper
- Manual admin console management
- Quick-and-dirty weekend project

**v2.0.0-beta** (October 2025) - Complete Rewrite
- Personal life analytics platform
- Docker-first self-hosted PWA
- Modern React + TypeScript frontend
- Full REST API with automation
- Beautiful analytics and charts
- Mobile-first responsive design
- Built in one 15-hour session with Cursor AI

### What Changed

Everything. Well, almost everything. The core concept stayed the same - track time without pain. But the execution? Total overhaul.

Went from "this works for my team" to "I want to use this every day." From Electron desktop app to mobile-responsive PWA. From hardcoded task lists to per-user customization. From manual DB exports to one-click CSV downloads.

The bones were there. The vision was there. We just rebuilt it **right**.

---

## Project Structure

```
magus/
├── krono/                  # Django backend
│   ├── krono/             # Project settings
│   └── magus/             # Main app
│       ├── api/           # REST API endpoints
│       ├── models.py      # Database models
│       ├── authentication.py  # API key auth
│       └── tasks.py       # Celery tasks
├── frontend/              # React frontend
│   ├── src/
│   │   ├── api/          # API client
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── hooks/        # Custom hooks
│   │   └── store/        # Zustand stores
│   └── public/           # Static assets
├── nginx/                # Nginx config
├── docker-compose.yml    # Development compose
├── docker-compose.prod.yml  # Production compose
├── Dockerfile           # Application container
└── requirements.txt     # Python dependencies
```

---

## Configuration

### Environment Variables

Key variables in `.env`:

```bash
# Security
SECRET_KEY=your-50-char-random-string
DEBUG=False  # True for development

# Database
DATABASE_URL=postgresql://user:pass@db:5432/magus

# Email (for CSV exports)
EMAIL_HOST=smtp.sendgrid.net
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-api-key
```

See `env.template` for full list with examples.

---

## Production Deployment

### SSL/TLS Setup

```bash
# 1. Update domain in env.template
ALLOWED_HOSTS=yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# 2. Use production compose
docker-compose -f docker-compose.prod.yml up -d

# 3. Get SSL certificate
docker-compose run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  -d yourdomain.com
```

### Backups

Automated daily PostgreSQL backups included in production compose. Stored in `./backups/` with 30-day retention.

Manual backup:
```bash
docker-compose exec db pg_dump -U magus_user magus | gzip > backup.sql.gz
```

---

## Troubleshooting

### Containers Won't Start

```bash
# Check logs
docker-compose logs -f

# Common issues:
# - Port 80/443/5432/6379 already in use
# - .env file missing or incorrect
# - Not enough disk space
```

### Frontend Not Loading

```bash
# Restart Vite dev server
cd frontend
npm run dev

# Or rebuild frontend for production
npm run build
```

### Database Issues

```bash
# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d
```

### API Returns 401

- Check your JWT token hasn't expired (15 min lifetime)
- For API keys, verify header format: `Authorization: Api-Key your_key`
- Check key is active in Settings → API Keys

---

## Contributing

This is primarily a personal project, but I'm open to:

- Bug reports and fixes
- Feature suggestions (that don't break the core philosophy)
- UI/UX improvements
- Documentation improvements

**No corporate features.** No surveillance. No bullshit. This is for individuals who want to understand themselves better.

---

## Roadmap

### v2.1 (In Progress)
- [ ] PWA features (offline support, install to home screen)
- [ ] Smooth animations and transitions
- [ ] Mobile gesture support (long-press, swipe)
- [ ] iOS Live Activities integration

### v2.x (Future)
- [ ] Retro OS themes (Aqua, Aero, Metro, Luna)
- [ ] AI insights with user-provided OpenAI keys
- [ ] Advanced analytics (heatmaps, trends)
- [ ] Native iOS app for true WatchOS integration
- [ ] Webhook support for automation

### Won't Build
- Team features (use v1.0 if you need that)
- Manager dashboards
- Approval workflows
- Surveillance features

---

## Why "MAGUS"?

Originally called "gaebolg" (after the cursed spear from Irish mythology - seemed fitting for a tool that tracks every minute of your workday). 

Renamed to MAGUS because:
1. It's easier to pronounce
2. Mages are wise and understand things
3. Understanding how you spend your time is kind of magical
4. I like the acronym potential (Multi-user Analytics & Granular Usage System)

The icon stays, though. Nostalgia.

---

## Technical Notes

### Why Docker?

Because I don't want to spend hours setting up environments. `docker-compose up` and you're done. Deploy anywhere. Scale however. Delete and rebuild in seconds.

Plus it makes this genuinely portable. Run it on your home server, a VPS, a Raspberry Pi, whatever. If it runs Docker, it runs MAGUS.

### Why React + TypeScript?

The original was server-side rendered Django templates. They worked, but let's be real - a time tracking app benefits from real-time updates, smooth interactions, and offline capability. React with TypeScript gives us type safety, a massive ecosystem, and the foundation for PWA features.

Plus Vite is stupid fast for development.

### Why PostgreSQL over SQLite?

Multi-user support from day one. Even though I built this for personal use, I wanted the architecture to support my original team use case if needed. PostgreSQL is production-ready, has excellent Django support, and scales forever.

### Why Self-Hosted?

Your time data is *your* data. I don't want it on someone else's server. I don't want it analyzed for ad targeting. I don't want it subject to ToS changes or company pivots.

Self-hosted means you control everything. The code is open. The data is yours. The infrastructure is yours.

---

## Performance

- **Initial Load:** < 2 seconds
- **API Response:** < 100ms (p95)
- **Live Timer Updates:** Every second, smooth
- **Offline Support:** Coming in v2.1
- **Bundle Size:** < 300KB gzipped

Tested on:
- Desktop Chrome, Firefox, Safari
- iPhone 14 Pro (Safari)
- Android (Chrome)

---

## Security

- JWT authentication with auto-refresh
- API keys hashed with SHA-256
- HTTPS/TLS ready
- CORS protection
- CSRF protection
- Input validation
- SQL injection prevention (ORM)
- XSS protection

### Data Privacy

- No telemetry
- No tracking
- No third-party analytics
- Optional OpenAI integration (you provide your own key)
- GDPR-compliant data export and deletion

---

## Architecture Decisions

### Why Not Native Mobile?

I considered it. iOS app with WatchOS complications would be sick. But:

1. **PWA gets you 90% there** - Install to home screen, works offline, fast
2. **One codebase** - Desktop + mobile from the same code
3. **No App Store bullshit** - Update whenever, no approval process
4. **API-first means native later** - Can always build native apps that talk to this API

PWA now, native if WatchOS becomes critical.

### Why Celery?

Background tasks for exports, email sending, and future scheduled jobs. Could've used Django-Q or Dramatiq, but Celery is battle-tested and has great docs.

Also, it was already there from v1.0 and it wasn't causing problems.

### Why TanStack Query?

Server state management that actually makes sense. Automatic caching, refetching, and synchronization. The live timer updates and analytics refresh are trivial with Query's built-in intervals.

---

## Known Issues

- Email exports print to console in dev mode (configure SMTP for production)
- Health checks show "unhealthy" due to missing requests module in container (doesn't affect functionality)
- Analytics Week/Month views require completed (stopped) tasks to show data
- PWA features not yet implemented (Sprint 8-9)

---

## Credits

### v1.0 (2024)
- **Me:** Concept, development, deployment
- **@Malathair:** Friend who filled knowledge gaps
- **ChatGPT:** Pair programming partner

### v2.0 (2025)
- **Me:** Product vision, requirements, testing
- **Claude (Cursor AI):** Architecture, implementation, pair programming

Built in one session. No breaks. Pure flow state.

---

## License

MIT License - See LICENSE file

Use it, modify it, deploy it, whatever. Just don't turn it into corporate surveillance software. That's literally the opposite of the point.

---

## Questions?

Open an issue. Or don't. This is mostly for me anyway.

But if you find it useful, let me know. Always cool to hear about tools actually being used.

---

## Changelog

### v2.0.0-beta (October 15, 2025)

**Complete Rewrite - PWA Modernization**

- Migrated from Electron to Docker-based PWA
- Added React + TypeScript frontend with Vite
- Implemented full REST API with DRF
- Added user-customizable task types (per-user)
- Built modern responsive UI with TailwindCSS
- Added real-time analytics with charts
- Implemented CSV export (download & email)
- Added API key generation for automation
- Created Docker deployment environment
- Added GitHub Actions CI/CD
- Implemented manual entry editing
- Added JWT authentication with auto-refresh
- Built task interruption with smart confirmation
- Designed mobile-first interface

**Breaking Changes:**
- URLs changed from `/magus/` to `/`
- Authentication now JWT-based (was session)
- Task types now per-user (was hardcoded global)
- API-first architecture (no Electron)

**Migration:** v1.0 to v2.0 migration scripts coming in v2.0.0 final release

### v1.0.0 (June 2024)

Original MAGUS - Corporate time tracking tool
- Django + PostgreSQL + Redis
- Electron desktop wrapper
- Hardcoded task types
- Admin console for data management
- Heartbeat-based session tracking
- Weekend project that shipped

---

**Last Updated:** October 15, 2025  
**Status:** Active Development (v2.0.0-beta)  
**Stability:** Tested and working, ready for daily use
