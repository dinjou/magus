# MAGUS PWA Modernization Plan

## Vision Statement

Transform MAGUS from a corporate time-tracking tool into a **personal life analytics platform** that makes self-tracking painless, insightful, and dare we say... fun. The goal is to empower individuals to understand how they spend their time without the friction of traditional time-tracking tools.

---

## Core Philosophy

### Design Principles

1. **Friction-Free Tracking**
   - Minimum viable interaction: Track in 1-2 taps
   - No scrolling required for primary actions
   - Intelligent state management (start becomes stop/interrupt automatically)
   - Forgiving by default: mistakes are easy to fix

2. **Data Ownership & Privacy**
   - Self-hosted: Your data lives on your infrastructure
   - GDPR-compliant data management
   - Export everything, delete everything
   - No telemetry, no tracking, no third-party services (except user-provided APIs)

3. **Mobile-First, Progressive Enhancement**
   - Designed for iPhone in portrait mode
   - Works offline (PWA capabilities)
   - Responsive up to desktop
   - Touch-optimized interactions (long-press, flick-scroll)

4. **Extensible Architecture**
   - API-first design
   - User-generated API keys for automation
   - Documented endpoints (OpenAPI/Swagger)
   - Webhook support for integrations

5. **Aesthetic Joy**
   - Beautiful by default
   - Fun theming system (retro OS themes as stretch goal)
   - Smooth animations and transitions
   - Personality without being cutesy

---

## Technical Architecture

### Deployment Model: Docker-Centric Self-Hosted PWA

```
┌─────────────────────────────────────────────────────────────┐
│                    User's Device (Browser/PWA)               │
│  - React SPA                                                 │
│  - Service Worker (offline support)                          │
│  - IndexedDB (offline cache)                                 │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS/WSS
                         │
┌────────────────────────▼────────────────────────────────────┐
│              Docker Container: Nginx (Reverse Proxy)         │
│  - Serves static React build                                 │
│  - SSL termination (Let's Encrypt ready)                     │
│  - Proxies /api/* to Django                                  │
│  - Proxies /ws/* to Django Channels (WebSocket)              │
└──────────────┬──────────────────────────────────────────────┘
               │
       ┌───────┴────────┬──────────────────────────────┐
       │                │                              │
       ▼                ▼                              ▼
┌─────────────┐  ┌─────────────┐              ┌──────────────┐
│  Django API │  │ Django      │              │ React Build  │
│  + DRF      │  │ Channels    │              │ (static)     │
│  + Gunicorn │  │ (WebSocket) │              └──────────────┘
└──────┬──────┘  └──────┬──────┘
       │                │
   ┌───┴────┬──────────┴┬──────────────┐
   ▼        ▼           ▼              ▼
┌──────┐ ┌─────┐ ┌──────────┐ ┌────────────┐
│ PG   │ │Redis│ │ Celery   │ │ Celery     │
│ SQL  │ │     │ │ Worker   │ │ Beat       │
└──────┘ └─────┘ └──────────┘ └────────────┘
```

### Tech Stack

#### Backend
- **Django 5.1**: Core framework
- **Django REST Framework 3.14+**: RESTful API
- **Django Channels 4.x**: WebSocket support for live updates
- **PostgreSQL 16**: Primary database
- **Redis 7**: Celery broker, WebSocket layer, caching
- **Celery 5.4+**: Async tasks (scheduled exports, email sending)
- **Gunicorn**: WSGI server
- **Daphne**: ASGI server for WebSockets

**Key Django Packages:**
```python
django-cors-headers          # CORS for API
djangorestframework-simplejwt # JWT authentication
drf-spectacular              # OpenAPI schema generation
djangorestframework-api-key  # User-generated API keys
django-environ               # Environment variable management
django-celery-beat           # Periodic task scheduling
django-filter                # Query filtering
Pillow                       # Image handling (user avatars)
```

#### Frontend
- **React 18**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool (fast HMR, optimized builds)
- **TanStack Query (React Query)**: Server state management
- **Zustand**: Client state management (lightweight, no boilerplate)
- **React Router 6**: Client-side routing
- **TailwindCSS 3**: Utility-first styling
- **Headless UI**: Accessible UI components
- **Recharts**: Data visualization
- **date-fns**: Date manipulation
- **Workbox**: PWA service worker management

**Key Frontend Libraries:**
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "typescript": "^5.2.0",
  "@tanstack/react-query": "^5.0.0",
  "zustand": "^4.4.0",
  "react-router-dom": "^6.20.0",
  "tailwindcss": "^3.3.0",
  "@headlessui/react": "^1.7.0",
  "recharts": "^2.10.0",
  "date-fns": "^2.30.0",
  "axios": "^1.6.0",
  "workbox-core": "^7.0.0",
  "workbox-precaching": "^7.0.0",
  "workbox-routing": "^7.0.0"
}
```

#### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Reverse proxy & static file serving
- **Let's Encrypt/Certbot**: SSL certificates (optional)

---

## Data Model Design

### Updated Schema

#### User & Profile
```python
# Extends Django's built-in User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_for_exports = models.EmailField(blank=True)
    timezone = models.CharField(max_length=50, default='America/Denver')
    theme = models.CharField(max_length=20, default='dark')
    long_press_duration = models.FloatField(default=1.5)  # seconds
    pinned_tasks_visible = models.IntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Settings
    enable_live_activities = models.BooleanField(default=True)
    openai_api_key = models.CharField(max_length=255, blank=True)  # encrypted
```

#### TaskType (Per-User Customizable)
```python
class TaskType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10, default='📊')
    color = models.CharField(max_length=7, default='#3A8E61')  # hex color
    
    # Organization
    is_pinned = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', 'name']
        unique_together = ['user', 'name']
        indexes = [
            models.Index(fields=['user', 'is_archived']),
            models.Index(fields=['user', 'is_pinned']),
        ]
```

#### Task (Time Entries)
```python
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_type = models.ForeignKey(TaskType, on_delete=models.PROTECT)
    
    # Timestamps (stored in UTC)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    
    # Status
    interrupted = models.BooleanField(default=False)
    is_manual_entry = models.BooleanField(default=False)
    
    # Optional metadata
    notes = models.TextField(blank=True)
    
    # Audit trail
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited_by_user = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['user', '-start_time']),
            models.Index(fields=['user', 'end_time']),
            models.Index(fields=['user', 'task_type', '-start_time']),
        ]
    
    @property
    def duration(self):
        """Calculate duration in seconds"""
        if not self.end_time:
            return (timezone.now() - self.start_time).total_seconds()
        return (self.end_time - self.start_time).total_seconds()
```

#### APIKey (User-Generated Tokens)
```python
class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # e.g., "Home Automation", "iOS Shortcuts"
    key_prefix = models.CharField(max_length=8)  # First 8 chars for display
    key_hash = models.CharField(max_length=128)  # Hashed key for security
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Permissions (for future granular access control)
    can_read = models.BooleanField(default=True)
    can_write = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
```

#### ScheduledExport (Automated CSV Exports)
```python
class ScheduledExport(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    email_to = models.EmailField()
    is_active = models.BooleanField(default=True)
    
    last_sent = models.DateTimeField(null=True, blank=True)
    next_scheduled = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## API Design

### RESTful API Endpoints

#### Authentication
```
POST   /api/auth/register/          # User registration
POST   /api/auth/login/             # JWT token generation
POST   /api/auth/refresh/           # Refresh JWT token
POST   /api/auth/logout/            # Invalidate token
```

#### User Profile
```
GET    /api/profile/                # Get current user profile
PATCH  /api/profile/                # Update profile settings
DELETE /api/profile/                # Delete account (GDPR)
GET    /api/profile/export/         # Export all user data (JSON)
```

#### Task Types
```
GET    /api/task-types/             # List user's task types
POST   /api/task-types/             # Create new task type
GET    /api/task-types/{id}/        # Get specific task type
PATCH  /api/task-types/{id}/        # Update task type
DELETE /api/task-types/{id}/        # Archive task type (soft delete)
POST   /api/task-types/reorder/     # Bulk reorder
POST   /api/task-types/{id}/pin/    # Toggle pin status
```

#### Tasks (Time Entries)
```
GET    /api/tasks/                  # List tasks (filterable, paginated)
POST   /api/tasks/                  # Create manual task entry
GET    /api/tasks/{id}/             # Get specific task
PATCH  /api/tasks/{id}/             # Edit task entry
DELETE /api/tasks/{id}/             # Delete task entry

POST   /api/tasks/start/            # Start tracking a task
POST   /api/tasks/stop/             # Stop current task
POST   /api/tasks/interrupt/        # Stop current, start new (atomic)
GET    /api/tasks/current/          # Get currently active task

# Query parameters for filtering:
# ?start_date=2023-10-01&end_date=2023-10-31
# ?task_type=5
# ?interrupted=true
# ?page=1&page_size=50
```

#### Analytics
```
GET    /api/analytics/summary/      # Today's summary
GET    /api/analytics/daily/        # Daily breakdown (date range)
GET    /api/analytics/weekly/       # Weekly aggregates
GET    /api/analytics/monthly/      # Monthly aggregates
GET    /api/analytics/heatmap/      # Activity heatmap data
GET    /api/analytics/trends/       # Time-series trend data
GET    /api/analytics/insights/     # AI-generated insights (if enabled)
```

#### Export & API Keys
```
POST   /api/export/csv/             # Generate & email CSV export
GET    /api/export/scheduled/       # List scheduled exports
POST   /api/export/scheduled/       # Create scheduled export
PATCH  /api/export/scheduled/{id}/  # Update scheduled export
DELETE /api/export/scheduled/{id}/  # Delete scheduled export

GET    /api/api-keys/               # List user's API keys
POST   /api/api-keys/               # Generate new API key
DELETE /api/api-keys/{id}/          # Revoke API key
```

#### WebSocket
```
WS     /ws/tasks/                   # Real-time task updates
```

---

## User Experience Flow

### Primary User Journey: Tracking Time

```
┌─────────────────────────────────────────┐
│ 1. IDLE STATE                           │
│                                         │
│ Currently Tracking: [Empty]             │
│                                         │
│ Quick Start: [Grid of Pinned Tasks]    │
│ ← scroll → [More pinned if needed]     │
│                                         │
│ [+ More Tasks ▼] (collapsed)            │
│                                         │
│ Today's Summary: [Brief stats]          │
└─────────────────────────────────────────┘
         │
         │ Tap "Deep Work"
         ▼
┌─────────────────────────────────────────┐
│ 2. TRACKING STATE                       │
│                                         │
│ Currently Tracking:                     │
│ ┌─────────────────────────────────────┐ │
│ │ 📊 Deep Work                        │ │
│ │ ⏱️  00:01:23 (live updating)        │ │
│ │ Started: 2:34 PM                    │ │
│ │                                     │ │
│ │     [⏹️  Stop]                      │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Quick Start: [Grid - slightly grayed]   │
│ (tapping another task triggers          │
│  interrupt confirmation)                │
└─────────────────────────────────────────┘
         │
         │ Tap "Stop"
         ▼
┌─────────────────────────────────────────┐
│ 3. COMPLETED STATE                      │
│                                         │
│ ✅ Deep Work tracked: 1h 23m            │
│                                         │
│ Quick Start: [Active again]             │
│                                         │
│ Today's Summary: [Updated stats]        │
│ ├─ Deep Work:  1h 23m  ████████░░      │
│ ...                                     │
└─────────────────────────────────────────┘
```

### Secondary Journey: Reviewing & Editing

```
Bottom of Main Screen:
[📊 Review My Time] button

         ▼

┌─────────────────────────────────────────┐
│ Review & Edit                           │
│                                         │
│ Filter: [Today ▼] [All Tasks ▼]        │
│                                         │
│ ┌──────────────────────────────────┐   │
│ │ 📊 Deep Work                     │   │
│ │ 2:34 PM - 3:57 PM (1h 23m)       │   │
│ │ [✏️  Edit]                       │   │
│ └──────────────────────────────────┘   │
│                                         │
│ ┌──────────────────────────────────┐   │
│ │ 📧 Email                         │   │
│ │ 1:15 PM - 2:20 PM (1h 5m)        │   │
│ │ ⚠️  Interrupted                   │   │
│ │ [✏️  Edit]                       │   │
│ └──────────────────────────────────┘   │
│                                         │
│ [Load More...]                          │
└─────────────────────────────────────────┘
```

### Editing Modal

```
┌─────────────────────────────────────────┐
│ Edit Task Entry                    [×]  │
├─────────────────────────────────────────┤
│                                         │
│ Task Type:  [Deep Work      ▼]         │
│                                         │
│ Start Time: [Oct 15] [2:34 PM]         │
│                                         │
│ End Time:   [Oct 15] [3:57 PM]         │
│                                         │
│ Status:     □ Interrupted               │
│                                         │
│ Notes:      [________________]          │
│             [________________]          │
│                                         │
│ Duration: 1h 23m                        │
│                                         │
│     [Cancel]         [Save Changes]     │
└─────────────────────────────────────────┘
```

---

## UI/UX Specifications

### Main Dashboard Layout

**Mobile (375px - 428px width):**
- Header: 56px fixed height
  - Logo/Title (left)
  - Settings icon (right)
  - Hamburger menu (right-most)
  
- Currently Tracking Card: 120-180px (dynamic height)
  - Only visible when tracking active
  - Prominent timer display
  - Stop button (large, obvious)
  
- Quick Start Grid: Variable height
  - 2 columns on narrow screens (<375px)
  - 3 columns on standard phones (375px-428px)
  - 4 columns on larger phones (>428px)
  - Horizontal scroll if pinned > grid width
  - Each card: 100-120px wide × 80px tall
  - Touch targets: minimum 44×44px
  
- More Tasks Accordion: Collapsed by default
  - All tasks, scrollable list
  - Search bar at top when expanded
  
- Today's Summary: 200-300px
  - Compact stats
  - Bar graphs
  - Total time
  
- Review Button: 56px fixed at bottom

**Tablet/Desktop (>768px):**
- Sidebar navigation (left, 240px)
- Main content area (fluid)
- Quick Start grid: 4-6 columns
- Summary alongside main content

### Interaction Patterns

**Touch Gestures:**
- **Tap:** Start/Stop task
- **Long-press (1.5s):** Pin/Unpin task (with haptic feedback)
- **Horizontal scroll:** Navigate pinned tasks (with momentum)
- **Pull-to-refresh:** Refresh data
- **Swipe left on entry:** Quick edit/delete

**Visual Feedback:**
- Loading states: Skeleton screens (no spinners)
- Success: Green toast notification (3s auto-dismiss)
- Error: Red toast notification (manual dismiss)
- State changes: Smooth 200-300ms transitions
- Active task: Pulsing indicator

**Accessibility:**
- ARIA labels on all interactive elements
- Keyboard navigation support
- Focus visible indicators
- Color contrast: WCAG AA minimum
- Screen reader announcements for state changes
- Reduced motion respect

---

## Theming System

### Core Themes (MVP)

**Dark Theme (Default):**
```css
--bg-primary: #2C2F33
--bg-secondary: #23272A
--bg-tertiary: #1E2124
--text-primary: #FFFFFF
--text-secondary: #B9BBBE
--accent: #7289DA
--success: #3A8E61
--error: #B35A5A
--warning: #8B7D5A
```

**Light Theme:**
```css
--bg-primary: #FFFFFF
--bg-secondary: #F6F6F7
--bg-tertiary: #E3E5E8
--text-primary: #2C2F33
--text-secondary: #72767D
--accent: #5865F2
--success: #3BA55D
--error: #ED4245
--warning: #FEE75C
```

### Stretch Goal: Retro OS Themes

**Aqua (Mac OS X Leopard):**
- Brushed metal textures
- Blue lozenge buttons
- Unified toolbar
- Glassy translucency effects

**Aero (Windows 7):**
- Glass effects with blur
- Blue/white color scheme
- Subtle gradients
- Window chrome styling

**Metro (Windows 8):**
- Flat design
- Vibrant solid colors
- Typography-focused
- Edge-to-edge layouts

**Luna (Windows XP):**
- Blue/green gradients
- Rounded window corners
- 3D-effect buttons
- Start button aesthetic

**Implementation:**
- CSS custom properties for colors
- Theme-specific component variants
- Asset swapping for textures/icons
- JS class toggling on root element

---

## Data Visualization Specifications

### Chart Types & Use Cases

#### 1. Horizontal Bar Chart (Primary)
**Use:** Daily time breakdown
```
Deep Work    ████████████████░░ 4h 23m
Email        ██████████░░░░░░░░ 2h 15m
Meetings     ██████░░░░░░░░░░░░ 1h 30m
Break        ████░░░░░░░░░░░░░░ 0h 45m
```
- Shows proportion of day
- Easy to compare categories
- Clear labels with durations

#### 2. Heatmap Calendar
**Use:** Activity patterns over time
```
        Mon Tue Wed Thu Fri Sat Sun
Week 1  🟩  🟨  🟩  🟦  🟩  ⬜  ⬜
Week 2  🟩  🟩  🟨  🟩  🟦  🟨  ⬜
Week 3  🟨  🟩  🟩  🟦  🟩  ⬜  🟨
```
- Color intensity = hours tracked
- Quickly see productive days
- Identify patterns (e.g., low Mondays)

#### 3. Stacked Area Chart
**Use:** Time allocation trends over weeks/months
```
     Hours
     10│        ▓▓▓▓▓▓▓▓
      8│      ▓▓▒▒▒▒▒▒▒▒▓▓
      6│    ▓▓▒▒░░░░░░▒▒▒▒▓▓
      4│  ▓▓▒▒░░░░░░░░░░▒▒▒▒▓▓
      2│▓▓▒▒░░░░░░░░░░░░░░▒▒▒▒▓▓
      0└────────────────────────────
       W1  W2  W3  W4  W1  W2  W3
       
Legend: ░░ Deep Work  ▒▒ Email  ▓▓ Meetings
```
- Shows trends over time
- Cumulative view of how time is spent
- Spot shifts in allocation

#### 4. Donut Chart
**Use:** Weekly/monthly total breakdown
```
       Total: 40h 15m
     
          ┌─────────┐
        ╱             ╲
       │    ███████    │
       │  ██       ██  │
       │ █           █ │
       │█     40h     █│
       │█     15m     █│
       │ █           █ │
       │  ██       ██  │
       │    ███████    │
        ╲             ╱
          └─────────┘
          
    Deep Work: 45%
    Email: 25%
    Meetings: 20%
    Other: 10%
```
- Center shows total time tracked
- Outer ring shows breakdown
- Percentages for context

#### 5. Time-of-Day Cluster Chart
**Use:** When you do different activities
```
     Hour
     23│                    
     21│    □ □             
     19│  □ ■ ■ □           
     17│  ■ ■ ■ ■ □         
     15│  ■ ■ ■ ■ ■         
     13│  □ □ ■ ■ □         
     11│    ■ ■ ■           
      9│    ■ ■ ■ ■         
      7│      □ □           
      5│                    
       └────────────────────
        M  T  W  T  F  S  S
        
■ Deep Work    □ Meetings
```
- Visualize when tasks typically happen
- Identify optimal work times
- Spot schedule patterns

### View Modes

**Hourly View:**
- Timeline with 24 hours
- Blocks showing task durations
- Today only

**Daily View:**
- Bar charts and donut charts
- Select specific day
- Detailed breakdown

**Weekly View:**
- Stacked area chart
- Heatmap for the week
- Mon-Sun comparison

**Monthly View:**
- Calendar heatmap
- Total hours by week
- Category distribution

**All-Time View:**
- Long-term trends
- Cumulative statistics
- Personal records (longest task, most productive day, etc.)

---

## Email & Notification System

### Email Configuration
- **Provider:** Configurable SMTP (SendGrid, AWS SES, Gmail, etc.)
- **Templates:** HTML + Plain text fallback
- **Queue:** Celery for async sending

### Email Types

#### 1. CSV Export Email
```
Subject: Your MAGUS Time Tracking Export - [Date Range]

Hi [Username],

Your requested time tracking data is attached.

Export Details:
- Date Range: Oct 1, 2025 - Oct 15, 2025
- Total Entries: 156
- Total Time Tracked: 87h 23m

[Download CSV]

---
This export was generated automatically from your MAGUS instance.
```

#### 2. Scheduled Export Email
```
Subject: Weekly Time Tracking Report - Week of [Date]

Hi [Username],

Your weekly time tracking report is ready.

This Week's Summary:
- Total Tracked: 42h 15m
- Most Time Spent: Deep Work (18h 32m)
- Longest Session: 3h 45m (Deep Work on Oct 12)

[Download Full Report CSV]

---
You're receiving this because you have weekly exports enabled.
Manage your export settings: [Link]
```

### Push Notifications (Web Push API)

**Live Activity Updates:**
- "You've been tracking Deep Work for 2 hours" (every hour)
- "Currently tracking: Deep Work • 00:45:23" (persistent notification)

**Implementation:**
- Service worker with push event listener
- User permission request on first enable
- Badge icons with timer display
- Action buttons: "Stop Task", "Interrupt", "Dismiss"

**Note:** iOS Safari has limited Web Push support. For true Live Activities:
- Document API endpoints for third-party apps
- User could build iOS Shortcuts or use IFTTT
- Consider future native app for Live Activities

---

## AI Insights Feature (Stretch Goal)

### User-Provided OpenAI Integration

**Settings Configuration:**
```
┌─────────────────────────────────────────┐
│ AI Insights (Optional)                  │
├─────────────────────────────────────────┤
│                                         │
│ Enable AI-powered productivity         │
│ suggestions and time analysis.          │
│                                         │
│ OpenAI API Key:                         │
│ [sk-...************************]        │
│                                         │
│ Model: [gpt-4-turbo ▼]                 │
│                                         │
│ □ Weekly insights email                 │
│ □ On-demand analysis only               │
│                                         │
│ Privacy Note: Your time tracking data   │
│ will be sent to OpenAI. API key is      │
│ encrypted and never shared.             │
│                                         │
│ [Test Connection]  [Save]               │
└─────────────────────────────────────────┘
```

### Insight Types

**1. Pattern Recognition:**
- "You tend to do your best deep work between 9 AM and 12 PM"
- "Your longest uninterrupted sessions happen on Tuesdays"
- "You're most productive after a morning break"

**2. Time Optimization:**
- "You spent 15 hours on email this week. Consider batching email time into 2-3 focused sessions."
- "Your meetings are scattered throughout the day. Blocking them together might give you longer focus periods."

**3. Balance Analysis:**
- "Your deep work time decreased 30% this week compared to last week"
- "You're tracking 45% more than your 6-week average. Great momentum!"

**4. Suggestions:**
- "Based on your patterns, consider blocking 10 AM - 12 PM for deep work"
- "Your Friday afternoons are consistently low-productivity. Maybe time for a 4-day week experiment?"

### Implementation
- Celery task: `generate_ai_insights(user_id, time_period)`
- API endpoint: `GET /api/analytics/insights/?period=week`
- Prompt engineering with structured output
- Cache insights (regenerate daily/weekly)
- Token usage tracking per user

---

## Security Considerations

### Authentication & Authorization
- **JWT tokens:** Short-lived access tokens (15min), longer refresh tokens (7 days)
- **API keys:** SHA-256 hashed, only show full key once at creation
- **Password requirements:** Min 8 chars, complexity enforced
- **Rate limiting:** 
  - Auth endpoints: 5 attempts per 15 min
  - API endpoints: 1000 requests/hour per user
  - API key endpoints: 100 requests/minute per key

### Data Privacy
- **Encryption at rest:** PostgreSQL encryption (optional)
- **Encryption in transit:** HTTPS/TLS 1.2+
- **Sensitive data:** OpenAI keys encrypted with Fernet (symmetric)
- **No tracking:** Zero telemetry, no analytics, no third-party scripts

### GDPR Compliance
- **Right to access:** `/api/profile/export/` (full JSON export)
- **Right to erasure:** `/api/profile/` DELETE (cascade deletes all data)
- **Data portability:** CSV and JSON export formats
- **Minimal data collection:** Only what's needed for functionality
- **Consent:** Clear opt-in for AI features, email notifications

### API Security
- **CORS:** Configured for same-origin + user-defined domains
- **CSRF protection:** Django middleware (session auth)
- **SQL injection:** ORM prevents (no raw queries)
- **XSS protection:** React escapes by default, CSP headers
- **Input validation:** DRF serializers, pydantic schemas

---

## Performance Targets

### Frontend
- **Initial load:** < 2 seconds (3G connection)
- **Time to Interactive:** < 3 seconds
- **Lighthouse score:** 90+ across all metrics
- **Bundle size:** < 300 KB gzipped (main bundle)
- **First Contentful Paint:** < 1 second

### Backend
- **API response time:** < 100ms (p95)
- **Database queries:** < 50ms (p95)
- **WebSocket latency:** < 50ms
- **CSV generation:** < 2 seconds for 10,000 entries

### Scalability
- **Concurrent users:** 100+ on single Docker host (16GB RAM)
- **Database size:** Handles 1M+ task entries efficiently
- **Storage:** ~1 MB per user per year (time entries only)

### Offline Support
- **PWA caching:** App shell (HTML/CSS/JS)
- **Data caching:** Last 7 days of tasks
- **Offline actions:** Queue start/stop operations, sync when online
- **Conflict resolution:** Last-write-wins with user notification

---

## Testing Strategy

### Backend Testing
- **Unit tests:** 80%+ coverage
- **Integration tests:** API endpoints, database operations
- **Celery task tests:** Mock email sending, scheduled jobs
- **Authentication tests:** JWT, API key validation
- **Performance tests:** Load testing with Locust

### Frontend Testing
- **Unit tests:** Utilities, hooks, stores (Vitest)
- **Component tests:** React Testing Library
- **Integration tests:** User flows (Playwright)
- **Visual regression:** Percy or Chromatic
- **Accessibility tests:** jest-axe, manual testing

### End-to-End Testing
- **Critical paths:** Login → Start task → Stop task → View stats → Export CSV
- **Error scenarios:** Network failures, invalid inputs
- **Cross-browser:** Chrome, Firefox, Safari (iOS)
- **Performance monitoring:** Lighthouse CI

---

## Deployment & Infrastructure

### Docker Compose Setup

**Services:**
1. **web:** Django + Gunicorn + Daphne
2. **db:** PostgreSQL 16
3. **redis:** Redis 7
4. **celery:** Celery worker
5. **celery-beat:** Celery scheduler
6. **nginx:** Reverse proxy

**Volumes:**
- `postgres_data`: Database persistence
- `static_files`: Collected Django static files
- `media_files`: User uploads (avatars, etc.)

**Environment Variables:**
```bash
# Django
SECRET_KEY=<random-50-char-string>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,localhost
DATABASE_URL=postgresql://user:pass@db:5432/magus

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=<sendgrid-api-key>

# Redis
REDIS_URL=redis://redis:6379/0

# Security
CORS_ALLOWED_ORIGINS=https://yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com

# Optional
SENTRY_DSN=<sentry-url>  # Error tracking
```

### Deployment Checklist
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Static files collected
- [ ] Superuser created
- [ ] SSL certificate configured
- [ ] Backups scheduled
- [ ] Monitoring configured
- [ ] Domain DNS configured

### Backup Strategy
- **Database:** Automated daily backups (pg_dump)
- **Retention:** 30 days rolling
- **Storage:** Local volume + optional S3
- **Restore:** Documented procedure in README

---

## Migration from Current System

### Data Migration Plan

**Phase 1: Prepare New System**
1. Deploy new infrastructure alongside old
2. Run both systems in parallel
3. Export existing data from PostgreSQL

**Phase 2: Data Transformation**
1. Map old `TASK_TYPES` array to new `TaskType` model
2. Create default TaskType entries for each user
3. Migrate Task entries with foreign key relationships
4. Preserve all timestamps, interrupted flags

**Phase 3: User Migration**
1. Reset passwords (notify users via email)
2. Import user accounts
3. Link migrated tasks to users
4. Verify data integrity

**Phase 4: Cutover**
1. Final data sync
2. DNS switch / update URLs
3. Shutdown old system
4. Monitor for issues

**Migration Script:**
```python
# management/commands/migrate_legacy_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from magus.models import TaskType, Task as NewTask
from django.db import connection

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Connect to old database
        # Export legacy tasks
        # Create TaskTypes for each user
        # Migrate Task entries
        # Verify counts match
```

### Breaking Changes
- URLs changed from `/magus/tasks/` to `/` (PWA)
- API endpoints now under `/api/`
- Authentication switches from session to JWT (for API)
- No more Electron wrapper

### User Communication
- Send email 2 weeks before migration
- Document new features
- Provide screenshots/tutorial
- Offer office hours for questions

---

## Future Enhancements (Post-MVP)

### Roadmap Ideas

**Phase 2 (Post-Launch):**
- Native iOS app with WatchOS complication
- Webhook support for automation
- Task templates/sequences
- Goal setting with progress tracking
- Pomodoro timer integration

**Phase 3 (Long-term):**
- Team/family accounts (shared tasks)
- Public API for third-party integrations
- Siri Shortcuts support
- Location-based auto-tracking (geofencing)
- Integration with calendar apps
- Zapier/Make.com connectors

**Community Features:**
- Docker Hub image for easy deployment
- Homebrew formula for macOS
- One-click installers (Portainer templates)
- Plugin system for extensions
- Community theme marketplace

---

## Success Metrics

### MVP Launch Criteria
- [ ] Can create account and log in
- [ ] Can create custom task types
- [ ] Can start/stop tasks with 1-2 taps
- [ ] Currently tracking task is prominently displayed
- [ ] Can view daily summary with charts
- [ ] Can edit past task entries
- [ ] Can export to CSV via email
- [ ] Mobile-responsive (works on iPhone)
- [ ] PWA installable (Add to Home Screen)
- [ ] Docker deployment works out-of-box
- [ ] API authentication functional
- [ ] Documentation complete

### User Satisfaction Goals
- Time to first track: < 2 minutes (from account creation)
- Daily active use: < 30 seconds average session
- Error rate: < 1% of interactions
- User retention: Self-sustained (personal use)

### Technical Health
- Uptime: 99%+ (monitoring with uptime checks)
- API response time: p95 < 200ms
- Zero data loss incidents
- Regular backups completing successfully

---

## Development Principles

### Code Quality
- Type safety: TypeScript strict mode, Python type hints
- Linting: ESLint, Prettier, Ruff, Black
- Documentation: Inline comments, docstrings, README
- Git workflow: Feature branches, PR reviews (self or pair)
- Commit messages: Conventional commits format

### Iteration Philosophy
- Ship small, ship often
- Perfect is the enemy of done (especially for MVP)
- User feedback over speculation
- Measure before optimizing
- Build for one user (you) first, scale later

### Technical Debt Management
- Document shortcuts taken
- Tag TODOs with context
- Refactor before it hurts
- Balance speed with sustainability

---

## Conclusion

This plan transforms MAGUS from a corporate time-tracker into a personal life analytics platform that respects your time, your privacy, and your data. By focusing on frictionless interaction, beautiful design, and extensible architecture, we're building a tool that actually gets used.

The Docker-first PWA approach gives you the flexibility to self-host, the convenience of mobile access, and the openness to extend however you want. Whether you're tracking deep work sessions, analyzing your productivity patterns, or building custom automations via the API, MAGUS is designed to adapt to your needs.

Most importantly: this is achievable in 2-3 focused days for the MVP, with a clear roadmap for enhancements. Let's build something useful and delightful. 🚀

---

**Next Steps:**
1. Review and approve this plan
2. Create development environment
3. Begin Sprint 1: Foundation & Core Models
4. Iterate based on real-world usage

**Questions? Feedback? Let's discuss before diving into code.**

