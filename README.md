# ![magus icon](https://github.com/Hyliana/gaebolg/blob/c370d729505a8ee35047fe2385bf7cf7794cda2f/krono/magus/static/magus/favicon.ico) MAGUS 



[![Version](https://img.shields.io/badge/version-2.0.0--beta-blue.svg)](https://github.com/dinjou/magus)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.0.7-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/react-18.3-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/typescript-5.6-blue.svg)](https://www.typescriptlang.org/)

---

## The Story

I built the first version of MAGUS over a weekend a few months back because my team needed to track how we were spending our time in a high-pressure, real-time response environment. I had SQL knowledge, some Python chops, and enough web dev experience to cobble together a Django app with PostgreSQL and Redis backing it. My friend @Malathair and ChatGPT helped me fill in the gaps, and I went from concept to deployment in about three days.

That first version worked. It solved the problem. But it was never meant to last.

Fast forward to October 2025: I realized something. I struggle with feeling like I never have time for anything. Every task feels overwhelming before I even start. Everything seems to take forever, and I can never tell if I'm actually making progress or just spinning my wheels.

I needed a way to quantify my experience. To see how I actually spend my time, not how I *feel* like I spend it. To match my perception with reality. Numbers don't lie, and I figured if I could see patterns in my own time usage, maybe I could stop feeling so overwhelmed.

Funny thing is, I'd already built the bones of exactly what I needed. It was just dressed up as a corporate tool.

So I sat down with Cursor AI and rebuilt MAGUS from the ground up. What you're looking at now is the result of a single 4-hour session where we transformed my (admittedly prety weak) corporate time-tracker into a personal life analytics platform. One that I actually *want* to use every day.

This isn't about productivity theater. **This is about me understanding myself.**

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

## Quick Start (Production-Ready)

**One command to rule them all:**

```bash
./scripts/start.sh
```

This will:
- Auto-generate secure passwords for internal services
- Create a `.env` file if it doesn't exist
- Start all services with Docker Compose

### Manual Setup

If you prefer manual control:

```bash
# 1. Generate secrets (or create .env manually)
./scripts/generate-secrets.sh

# 2. Edit .env and update ALLOWED_HOSTS for your domain
nano .env

# 3. Start services
docker compose up -d
```

### Access Points

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000/api/
- **Django Admin:** http://localhost:8000/admin/
- **API Docs:** http://localhost:8000/api/docs/

## Quick Start (Development)

### Prerequisites

- Docker Engine 24.0+
- Docker Compose 2.20+
- Python 3 (for setup script)
- 4GB RAM minimum
- 10GB disk space

### Setup (2 Minutes)

```bash
# 1. Clone the repository
git clone https://github.com/dinjou/magus.git
cd magus

# 2. Run the interactive setup script
bash scripts/setup.sh

# The script will:
# - Generate secure random passwords automatically
# - Ask for your domain(s) or IP(s) for access
# - Configure email (optional)
# - Create a production-ready .env file

# 3. Start MAGUS
docker compose -f docker-compose.prod.yml up -d

# 4. Wait for services to be ready (~30 seconds)
docker compose -f docker-compose.prod.yml ps

# 5. Open your browser
# Frontend: http://your-domain/
# API Docs: http://your-domain/api/docs/
```

### First User

```bash
# Create your account via the UI at http://your-domain/register
# Or create a superuser for admin access:
docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

That's it. You're tracking time.

### Adding More Domains Later

Just update the `ALLOWED_HOSTS` line in `.env`:

```bash
# Edit .env
ALLOWED_HOSTS=localhost,127.0.0.1,your-ip,your-domain.com

# Restart services to apply changes
docker compose -f docker-compose.prod.yml restart web celery celery-beat nginx
```

**Note:** CORS and CSRF origins are automatically built from `ALLOWED_HOSTS`, so you only need to maintain one line!

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

The setup script (`bash scripts/setup.sh`) creates a `.env` file with secure defaults. You can manually edit if needed:

```bash
# Security (auto-generated by setup script)
SECRET_KEY=auto-generated-50-char-random-string
DEBUG=False  # True for development

# Domain Configuration (YOU configure this)
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
# Note: CORS and CSRF origins are automatically built from ALLOWED_HOSTS

# Database (auto-generated - internal use only)
POSTGRES_DB=magus_prod
POSTGRES_USER=magus_user
POSTGRES_PASSWORD=auto-generated-secure-password

# Redis (auto-generated - internal use only)
REDIS_PASSWORD=auto-generated-secure-password

# Email (optional - for CSV exports)
EMAIL_HOST=smtp.sendgrid.net
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-api-key
```

**Important:** The database and Redis passwords are for internal Docker communication only. You don't need to remember them or change them unless you're exposing those services externally (not recommended).

---

## Production Deployment

### Initial Setup

```bash
# 1. Clone on your production server
git clone https://github.com/dinjou/magus.git
cd magus

# 2. Run setup script with your production domain
bash scripts/setup.sh
# When prompted, enter your domain (e.g., magus.yourdomain.com)

# 3. Start MAGUS
docker compose -f docker-compose.prod.yml up -d
```

### SSL/TLS Setup

MAGUS is designed to run behind a reverse proxy (like nginx, Caddy, or Traefik) that handles HTTPS termination. 

**Recommended Setup:**
- Use a reverse proxy on your server to handle HTTPS
- Point it to port 80 (nginx service) or port 8000 (direct to Django)
- Let your reverse proxy manage SSL certificates (Let's Encrypt, etc.)

**Example with existing reverse proxy:**
Just point your proxy to `http://your-server-ip:80` and it works!

### Backups

Automated daily PostgreSQL backups are included. Backups are stored in `./backups/` with 30-day retention.

**Manual backup:**
```bash
docker compose -f docker-compose.prod.yml exec db \
  pg_dump -U magus_user magus_prod | gzip > backup_$(date +%Y%m%d).sql.gz
```

**Restore from backup:**
```bash
gunzip < backup.sql.gz | \
  docker compose -f docker-compose.prod.yml exec -T db \
  psql -U magus_user magus_prod
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

## Why "MAGUS"?

The project name is a Chrono Trigger reference - because time is the theme here, and the name felt right.

Originally called "gaebolg" after the cursed spear from Irish mythology. It was meant to be a "tip of the spear" application - something to pry the door open, to get basic insight into how time was being used so we could take meaningful action.

Renamed to MAGUS because it's easier to pronounce and the Chrono Trigger connection was too good to pass up.

The icon stays, though. Nostalgia.

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

## Known Issues

- Email exports print to console in dev mode (configure SMTP for production). Or maybe it doesn't. I didn't really test it because I didn't want to spend any more time getting an SNMP server up and running tonight.
- Health checks show "unhealthy" due to missing requests module in container (doesn't affect functionality)
- Analytics Week/Month views require completed (stopped) tasks to show data

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

No license is provided for this code.

This is meant to be for personal betterment, but I woluld like to show it off as a portfolio piece while still retaining some ownership of my code and not have it get commercialized by another party that doesn't care about such a goal. 

If you get benefit from my tool though, please let me know. I uh... I didn't realize how quickly I would rack up API fees from Cursor. (^w^) Your thanks would mean a lot.

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
