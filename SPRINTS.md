# MAGUS Development Sprints

This document breaks down the MAGUS modernization into actionable sprints with specific user stories, tasks, and acceptance criteria.

---

## Sprint Organization

- **Sprint Duration:** Flexible (aim for 1-2 days per sprint for MVP)
- **Story Points:** Rough time estimates (1 point ≈ 1 hour)
- **Priority:** P0 (Must have for MVP) → P3 (Nice to have)

---

## Sprint 0: Project Setup & Infrastructure (8-10 hours) [P0]

**Goal:** Set up the development environment, Docker infrastructure, and baseline project structure.

### Stories

#### Story 0.1: Docker Environment Setup (3 points)
**As a** developer  
**I want** a fully containerized development environment  
**So that** deployment is consistent and reproducible

**Tasks:**
- [ ] Create `docker-compose.yml` with all services (web, db, redis, celery, celery-beat, nginx)
- [ ] Write `Dockerfile` for Django application
- [ ] Configure PostgreSQL 16 container with persistent volume
- [ ] Configure Redis 7 container
- [ ] Set up Nginx reverse proxy configuration
- [ ] Create `.env.example` with all required environment variables
- [ ] Document startup procedure in `DOCKER.md`

**Acceptance Criteria:**
- `docker-compose up` starts all services successfully
- Django connects to PostgreSQL
- Redis is accessible from Django and Celery
- Nginx serves static files and proxies to Django
- Environment variables load correctly

---

#### Story 0.2: Django Project Restructuring (2 points)
**As a** developer  
**I want** the Django project organized for API-first architecture  
**So that** the codebase is maintainable and scalable

**Tasks:**
- [ ] Install Django REST Framework and dependencies
- [ ] Install django-cors-headers, djangorestframework-simplejwt
- [ ] Install drf-spectacular for API docs
- [ ] Install djangorestframework-api-key
- [ ] Install django-environ for environment management
- [ ] Configure CORS settings
- [ ] Configure JWT authentication
- [ ] Set up DRF in settings.py
- [ ] Create `api` app for REST endpoints
- [ ] Configure spectacular for OpenAPI schema

**Acceptance Criteria:**
- DRF installed and configured
- `/api/schema/` returns OpenAPI schema
- `/api/docs/` shows Swagger UI
- JWT token generation works
- CORS allows frontend development server

---

#### Story 0.3: React + TypeScript + Vite Setup (3 points)
**As a** developer  
**I want** a modern React frontend with TypeScript and Vite  
**So that** development is fast and code is type-safe

**Tasks:**
- [ ] Create `frontend/` directory
- [ ] Initialize Vite project with React + TypeScript template
- [ ] Install core dependencies: react-router, tanstack-query, zustand, axios
- [ ] Install TailwindCSS and configure
- [ ] Install Headless UI for accessible components
- [ ] Configure Vite proxy to Django backend
- [ ] Set up basic routing structure
- [ ] Create `.env.example` for frontend
- [ ] Configure build output to Django static directory
- [ ] Create npm scripts for dev/build/preview

**Acceptance Criteria:**
- `npm run dev` starts Vite dev server
- Hot module replacement works
- TailwindCSS utilities available
- Can make API calls to Django backend
- TypeScript strict mode enabled with no errors
- Build outputs to `krono/staticfiles/`

---

#### Story 0.4: Database Schema Migration (2 points)
**As a** developer  
**I want** the new database schema in place  
**So that** I can build features on the updated models

**Tasks:**
- [ ] Update `Profile` model with new fields (timezone, theme, long_press_duration, etc.)
- [ ] Create `TaskType` model
- [ ] Update `Task` model to reference TaskType (foreign key)
- [ ] Create `APIKey` model
- [ ] Create `ScheduledExport` model
- [ ] Write data migration script to convert existing data
- [ ] Add indexes for query optimization
- [ ] Create Django admin interfaces for new models

**Acceptance Criteria:**
- All models created with correct fields
- Migrations apply without errors
- Existing task data migrated successfully
- Admin interfaces functional
- Database queries use indexes

---

## Sprint 1: Authentication & User Management (6-8 hours) [P0]

**Goal:** Implement JWT authentication, user registration, profile management, and basic API structure.

### Stories

#### Story 1.1: User Authentication API (3 points)
**As a** user  
**I want** to register and log in securely  
**So that** my time tracking data is private

**Tasks:**
- [ ] Create `/api/auth/register/` endpoint (POST)
- [ ] Create `/api/auth/login/` endpoint (POST, returns JWT)
- [ ] Create `/api/auth/refresh/` endpoint (POST, refresh token)
- [ ] Create `/api/auth/logout/` endpoint (POST, blacklist token)
- [ ] Write serializers for registration and login
- [ ] Add password validation
- [ ] Create Profile automatically on user creation (signal)
- [ ] Write unit tests for auth endpoints
- [ ] Document authentication flow

**Acceptance Criteria:**
- User can register with username, email, password
- User receives JWT access & refresh tokens on login
- Tokens can be refreshed before expiry
- Invalid credentials return appropriate errors
- Profile created automatically on registration

---

#### Story 1.2: User Profile API (2 points)
**As a** user  
**I want** to view and update my profile settings  
**So that** I can customize my experience

**Tasks:**
- [ ] Create `/api/profile/` endpoint (GET, PATCH)
- [ ] Create `ProfileSerializer` with all fields
- [ ] Allow updating: email_for_exports, timezone, theme, long_press_duration, pinned_tasks_visible
- [ ] Validate timezone choices
- [ ] Encrypt OpenAI API key before saving
- [ ] Write unit tests
- [ ] Document profile fields

**Acceptance Criteria:**
- Authenticated user can GET their profile
- User can PATCH update profile fields
- Timezone validated against standard list
- OpenAI key encrypted in database
- Returns 401 for unauthenticated requests

---

#### Story 1.3: React Authentication Flow (3 points)
**As a** user  
**I want** a clean login and registration interface  
**So that** I can access the app easily

**Tasks:**
- [ ] Create `LoginPage` component
- [ ] Create `RegisterPage` component
- [ ] Create auth store (Zustand) for user state
- [ ] Implement JWT token storage (localStorage with expiry)
- [ ] Create `ProtectedRoute` component
- [ ] Create `AuthProvider` context
- [ ] Handle token refresh automatically
- [ ] Create logout functionality
- [ ] Style with TailwindCSS (mobile-first)
- [ ] Add form validation and error display

**Acceptance Criteria:**
- User can register with validation
- User can login and receive tokens
- Tokens stored securely in localStorage
- Protected routes redirect to login if not authenticated
- Auto-refresh tokens before expiry
- Logout clears tokens and redirects
- Forms are responsive and accessible

---

## Sprint 2: Task Types Management (6-8 hours) [P0]

**Goal:** Allow users to create, edit, archive, and organize their custom task types.

### Stories

#### Story 2.1: Task Types CRUD API (3 points)
**As a** user  
**I want** to manage my custom task types via API  
**So that** I can track what matters to me

**Tasks:**
- [ ] Create `TaskTypeViewSet` with all CRUD operations
- [ ] Create `TaskTypeSerializer`
- [ ] Filter task types by user (queryset)
- [ ] Implement soft delete (is_archived)
- [ ] Add `reorder` custom action for bulk sort_order updates
- [ ] Add `pin` custom action to toggle is_pinned
- [ ] Validate unique task names per user
- [ ] Write comprehensive tests (CRUD, permissions, edge cases)
- [ ] Document endpoints in OpenAPI

**Acceptance Criteria:**
- User can list their task types (archived excluded by default)
- User can create task types with name, emoji, color
- User can update task types
- User can archive (not delete) task types
- User can reorder task types
- User can pin/unpin task types
- Cannot access other users' task types
- Archived task types can be filtered with `?show_archived=true`

---

#### Story 2.2: Task Type Management UI (4 points)
**As a** user  
**I want** a settings page to manage my task types  
**So that** I can customize my tracking list

**Tasks:**
- [ ] Create `SettingsPage` component with tabs
- [ ] Create `TaskTypesTab` component
- [ ] Create `TaskTypeCard` component
- [ ] Implement drag-and-drop reordering (react-beautiful-dnd or dnd-kit)
- [ ] Create `TaskTypeModal` for create/edit
- [ ] Add emoji picker component
- [ ] Add color picker component
- [ ] Implement pin toggle (long-press on task card)
- [ ] Implement archive functionality (with confirmation)
- [ ] Show archived tasks in separate section
- [ ] Sync reorder changes to API
- [ ] Add loading and error states
- [ ] Make responsive for mobile

**Acceptance Criteria:**
- User can view all task types in settings
- User can create new task type with emoji and color
- User can edit existing task type
- User can drag-and-drop to reorder
- User can long-press (1.5s) to pin/unpin
- User can archive task types (with confirmation)
- Archived tasks shown separately, can be un-archived
- Changes sync to backend immediately
- Mobile-friendly with touch interactions
- Visual feedback for all actions

---

#### Story 2.3: Default Task Types Seeding (1 point)
**As a** new user  
**I want** some default task types to get started  
**So that** I don't face an empty list

**Tasks:**
- [ ] Create management command to seed default task types
- [ ] Define sensible defaults: Deep Work 💻, Email 📧, Meeting 🤝, Break 🍔, Call 📞
- [ ] Run seeding on user registration (signal)
- [ ] Allow users to archive defaults if not needed

**Acceptance Criteria:**
- New users get 5 default task types
- Defaults have emoji, colors, and logical sort order
- Can be customized/archived like any other task type

---

## Sprint 3: Task Tracking Core (8-10 hours) [P0]

**Goal:** Implement the core task tracking functionality - start, stop, interrupt, and view current task.

### Stories

#### Story 3.1: Task Tracking API (4 points)
**As a** user  
**I want** API endpoints to start, stop, and interrupt tasks  
**So that** I can track my time programmatically

**Tasks:**
- [ ] Create `TaskViewSet` with standard CRUD
- [ ] Create `TaskSerializer` with nested TaskType
- [ ] Implement `/api/tasks/start/` action (POST with task_type_id)
- [ ] Implement `/api/tasks/stop/` action (POST, stops current task)
- [ ] Implement `/api/tasks/interrupt/` action (POST, stops current, starts new)
- [ ] Implement `/api/tasks/current/` action (GET, returns active task)
- [ ] Add validation: can't start if already tracking (unless interrupt)
- [ ] Add validation: can't stop if nothing tracking
- [ ] Store all times in UTC
- [ ] Filter tasks by user automatically
- [ ] Add query filters: date range, task_type, interrupted status
- [ ] Write comprehensive tests
- [ ] Document endpoints

**Acceptance Criteria:**
- POST `/api/tasks/start/` with task_type_id starts tracking
- POST `/api/tasks/stop/` ends current task
- POST `/api/tasks/interrupt/` atomically stops current and starts new
- GET `/api/tasks/current/` returns active task or null
- GET `/api/tasks/` returns user's tasks (paginated, filtered)
- All timestamps stored in UTC
- Returns 400 if trying to start when already tracking (without interrupt)
- Returns 400 if trying to stop when not tracking

---

#### Story 3.2: Main Dashboard UI - Tracking Card (3 points)
**As a** user  
**I want** a prominent "currently tracking" display  
**So that** I always know what I'm tracking

**Tasks:**
- [ ] Create `DashboardPage` component
- [ ] Create `CurrentTaskCard` component
- [ ] Display task name, emoji, start time
- [ ] Display live-updating timer (using interval)
- [ ] Show prominent "Stop" button
- [ ] Handle stop action (API call)
- [ ] Show empty state when not tracking
- [ ] Add smooth transitions when starting/stopping
- [ ] Style with glass-morphism effect (slightly elevated card)
- [ ] Make mobile-friendly (large touch targets)

**Acceptance Criteria:**
- Card only visible when task is active
- Timer updates every second
- Stop button ends task successfully
- Smooth fade-in/out transitions
- Card is visually prominent (top of dashboard)
- Responsive on mobile

---

#### Story 3.3: Quick Start Grid (3 points)
**As a** user  
**I want** a grid of my pinned tasks for quick starting  
**So that** I can start tracking with one tap

**Tasks:**
- [ ] Create `QuickStartGrid` component
- [ ] Fetch pinned task types from API
- [ ] Create `TaskTypeButton` component (emoji, name, color border)
- [ ] Implement horizontal scroll for overflow
- [ ] Show appropriate number based on user settings
- [ ] Handle task start (calls API)
- [ ] Show interrupt confirmation if already tracking
- [ ] Disable grid (gray out) when task is active
- [ ] Add momentum scrolling on mobile
- [ ] Show scroll indicators (fade edges)

**Acceptance Criteria:**
- Shows only pinned task types
- Grid scrolls horizontally on overflow
- Tapping a task starts tracking it
- If already tracking, shows interrupt confirmation
- Confirmation: "End [current task] and start [new task]?"
- Grid visually de-emphasized when tracking
- Smooth scrolling on mobile
- Responsive grid (2-4 columns based on screen width)

---

#### Story 3.4: More Tasks Dropdown (2 points)
**As a** user  
**I want** access to all my task types, not just pinned ones  
**So that** I can start any task

**Tasks:**
- [ ] Create `AllTasksDropdown` component
- [ ] Button: "+ More Tasks ▼"
- [ ] Fetch all task types (excluding archived)
- [ ] Expand/collapse accordion
- [ ] Search/filter functionality
- [ ] Scrollable list of all tasks
- [ ] Same start behavior as quick grid
- [ ] Sort by: pinned first, then sort_order, then name

**Acceptance Criteria:**
- Button toggles dropdown open/closed
- Shows all task types when open
- Can search/filter tasks by name
- Tapping task starts it (with interrupt logic)
- Scrollable if many tasks
- Closes after starting a task

---

## Sprint 4: Analytics & Visualizations (8-10 hours) [P0]

**Goal:** Build the analytics dashboard with charts, stats, and multiple time views.

### Stories

#### Story 4.1: Analytics API Endpoints (4 points)
**As a** user  
**I want** API endpoints that aggregate my time tracking data  
**So that** I can view statistics

**Tasks:**
- [ ] Create `/api/analytics/summary/` endpoint (today's totals by task type)
- [ ] Create `/api/analytics/daily/` endpoint (specific day breakdown)
- [ ] Create `/api/analytics/weekly/` endpoint (weekly aggregates)
- [ ] Create `/api/analytics/monthly/` endpoint (monthly aggregates)
- [ ] Create `/api/analytics/heatmap/` endpoint (activity heatmap data)
- [ ] Create `/api/analytics/trends/` endpoint (time-series data)
- [ ] Add date range filtering (?start_date=, ?end_date=)
- [ ] Optimize queries (aggregation, select_related, prefetch_related)
- [ ] Convert UTC to user's timezone for display
- [ ] Return durations in seconds and human-readable format
- [ ] Write tests for calculations
- [ ] Document endpoints

**Acceptance Criteria:**
- Summary returns today's totals grouped by task type
- Daily returns specified day's breakdown
- Weekly returns 7-day aggregates
- Monthly returns full month aggregates
- Heatmap returns activity by day/hour
- Trends returns time-series for charts
- All times converted to user's timezone
- Efficient queries (minimal N+1 problems)

---

#### Story 4.2: Today's Summary Display (2 points)
**As a** user  
**I want** to see today's summary on the main dashboard  
**So that** I know how I've spent my time

**Tasks:**
- [ ] Create `TodaysSummary` component
- [ ] Fetch summary data from API
- [ ] Create `SummaryBar` component (task type, duration, progress bar)
- [ ] Display total tracked time at bottom
- [ ] Calculate percentages for progress bars
- [ ] Show emoji and color per task type
- [ ] Format durations (e.g., "3h 24m")
- [ ] Handle empty state (no tracking today)
- [ ] Auto-refresh every minute
- [ ] Make responsive

**Acceptance Criteria:**
- Shows list of task types tracked today
- Each task shows duration and percentage bar
- Total tracked time at bottom
- Updates automatically when task stops
- Responsive on mobile
- Empty state: "No time tracked today yet"

---

#### Story 4.3: Analytics Page with Charts (4 points)
**As a** user  
**I want** detailed charts and visualizations  
**So that** I can analyze my time patterns

**Tasks:**
- [ ] Create `AnalyticsPage` component
- [ ] Add tab/view switcher: Hourly, Daily, Weekly, Monthly, All-Time
- [ ] Implement Horizontal Bar Chart (using Recharts)
- [ ] Implement Donut Chart for percentages
- [ ] Implement Heatmap Calendar
- [ ] Implement Stacked Area Chart for trends
- [ ] Implement Time-of-Day Cluster visualization
- [ ] Add date range picker for filtering
- [ ] Add task type filter
- [ ] Display key metrics (total, average, longest session)
- [ ] Make charts responsive
- [ ] Add loading skeletons
- [ ] Handle empty states

**Acceptance Criteria:**
- User can switch between time views
- Charts render correctly with real data
- Date range filtering works
- Can filter by specific task types
- Charts responsive on mobile
- Tooltips show detailed information
- Loading states while fetching data
- Empty state: "No data for this period"

---

## Sprint 5: Manual Entry Editing (6-8 hours) [P0]

**Goal:** Allow users to view task history and manually edit entries to fix mistakes.

### Stories

#### Story 5.1: Task History API (2 points)
**As a** user  
**I want** to retrieve my historical task entries  
**So that** I can review and edit them

**Tasks:**
- [ ] Enhance `TaskViewSet` list endpoint with pagination
- [ ] Add filtering by date range, task type, interrupted status
- [ ] Add sorting options (start_time, duration)
- [ ] Return tasks with nested task_type info
- [ ] Add duration calculation in serializer
- [ ] Support PATCH for updating individual tasks
- [ ] Support DELETE for removing tasks
- [ ] Write tests for filtering and sorting
- [ ] Document query parameters

**Acceptance Criteria:**
- GET `/api/tasks/` returns paginated task list
- Can filter by `?start_date=`, `?end_date=`, `?task_type=`, `?interrupted=`
- Can sort by `?ordering=-start_time` or `?ordering=duration`
- PATCH `/api/tasks/{id}/` updates task
- DELETE `/api/tasks/{id}/` deletes task
- Changes reflected immediately in UI

---

#### Story 5.2: Task History List UI (2 points)
**As a** user  
**I want** to see a list of my recent task entries  
**So that** I can review what I've tracked

**Tasks:**
- [ ] Create `TaskHistoryPage` component
- [ ] Create `TaskEntryCard` component
- [ ] Display task type, start/end times, duration
- [ ] Show interrupted badge if applicable
- [ ] Add filter controls (date range, task type)
- [ ] Implement infinite scroll or pagination
- [ ] Add "Edit" button on each entry
- [ ] Add swipe-to-edit gesture on mobile
- [ ] Show loading states
- [ ] Handle empty state

**Acceptance Criteria:**
- Shows list of historical tasks
- Most recent tasks appear first
- Can filter by date and task type
- Each entry shows key information
- Edit button opens edit modal
- Swipe left reveals edit/delete on mobile
- Pagination/infinite scroll works
- Responsive design

---

#### Story 5.3: Task Entry Edit Modal (3 points)
**As a** user  
**I want** to edit task details  
**So that** I can correct mistakes

**Tasks:**
- [ ] Create `TaskEditModal` component
- [ ] Form fields: task type (dropdown), start time, end time, interrupted (checkbox), notes (textarea)
- [ ] Date/time picker components
- [ ] Real-time duration calculation
- [ ] Validation: end time > start time
- [ ] Save button calls PATCH API
- [ ] Delete button with confirmation
- [ ] Cancel button
- [ ] Show success/error notifications
- [ ] Make modal accessible (focus trap, ESC to close)
- [ ] Make responsive for mobile

**Acceptance Criteria:**
- Modal opens when edit button clicked
- All fields pre-filled with current values
- Can change task type via dropdown
- Can edit start and end times with pickers
- Duration updates in real-time
- Can toggle interrupted status
- Can add/edit notes
- Save updates the task successfully
- Delete removes the task (with confirmation)
- Cancel closes modal without changes
- Keyboard accessible (tab navigation, ESC to close)
- Mobile-friendly touch targets

---

## Sprint 6: Data Export (4-6 hours) [P0]

**Goal:** Implement CSV export functionality with email delivery and scheduled exports.

### Stories

#### Story 6.1: CSV Export API (2 points)
**As a** user  
**I want** to export my time tracking data as CSV  
**So that** I can analyze it elsewhere

**Tasks:**
- [ ] Create `/api/export/csv/` endpoint (POST)
- [ ] Accept parameters: start_date, end_date, email_to
- [ ] Generate CSV with columns: Date, Task Type, Start Time, End Time, Duration, Interrupted, Notes
- [ ] Convert times to user's timezone
- [ ] Format duration as HH:MM:SS
- [ ] Queue Celery task for email sending
- [ ] Send email with CSV attachment
- [ ] Create email template (HTML + plain text)
- [ ] Handle errors (invalid email, SMTP failure)
- [ ] Write tests

**Acceptance Criteria:**
- POST to endpoint triggers CSV generation
- CSV contains all tasks in date range
- Times displayed in user's timezone
- CSV attached to email
- Email sent to specified address
- User receives confirmation notification
- Errors handled gracefully

---

#### Story 6.2: Scheduled Exports (2 points)
**As a** user  
**I want** to schedule automatic exports  
**So that** I get regular reports without manual work

**Tasks:**
- [ ] Create `ScheduledExportViewSet`
- [ ] Create `ScheduledExportSerializer`
- [ ] CRUD endpoints for scheduled exports
- [ ] Create Celery periodic task to check scheduled exports
- [ ] Generate and send exports at scheduled times
- [ ] Update `last_sent` and `next_scheduled` fields
- [ ] Allow daily, weekly, monthly frequencies
- [ ] Write tests for scheduling logic

**Acceptance Criteria:**
- User can create scheduled export with frequency and email
- User can list, update, delete scheduled exports
- Exports sent automatically at scheduled times
- Next scheduled time calculated correctly
- User can enable/disable scheduled exports

---

#### Story 6.3: Export UI in Settings (2 points)
**As a** user  
**I want** a settings page for exports  
**So that** I can manage exports easily

**Tasks:**
- [ ] Create `ExportTab` in settings
- [ ] Create "Export Now" section with date range picker
- [ ] Create "Scheduled Exports" section
- [ ] List existing scheduled exports
- [ ] Create/edit scheduled export form
- [ ] Show last sent date for scheduled exports
- [ ] Add enable/disable toggle
- [ ] Show success notifications
- [ ] Handle errors

**Acceptance Criteria:**
- User can trigger immediate export with custom date range
- User can create new scheduled export
- User can edit existing scheduled exports
- User can enable/disable scheduled exports
- User can delete scheduled exports
- Feedback shown for all actions

---

## Sprint 7: API Keys & Extensibility (4-6 hours) [P0]

**Goal:** Enable user-generated API keys for automation and third-party integrations.

### Stories

#### Story 7.1: API Key Management Backend (3 points)
**As a** user  
**I want** to generate and manage API keys  
**So that** I can automate task tracking

**Tasks:**
- [ ] Create `APIKeyViewSet`
- [ ] Create `APIKeySerializer` (only show full key on creation)
- [ ] Implement key generation (secure random, hash storage)
- [ ] Store only hashed keys in database (SHA-256)
- [ ] Show key prefix for identification
- [ ] Track last_used timestamp
- [ ] Create custom authentication class for API keys
- [ ] Support API keys in Authorization header: `Api-Key <key>`
- [ ] Add rate limiting for API key requests
- [ ] Write tests for key generation and authentication
- [ ] Document API key usage

**Acceptance Criteria:**
- User can generate new API keys
- Full key shown only once (on creation)
- Keys hashed in database
- Can authenticate with API key header
- Can revoke (delete) API keys
- Last used timestamp updates on use
- Rate limiting active (100 req/min per key)

---

#### Story 7.2: API Key Management UI (2 points)
**As a** user  
**I want** a settings page to manage my API keys  
**So that** I can see and control my integrations

**Tasks:**
- [ ] Create `APIKeysTab` in settings
- [ ] Create "Generate New Key" button
- [ ] Create modal to name new key
- [ ] Show full key once after generation (with copy button)
- [ ] List existing keys (prefix only, name, created date, last used)
- [ ] Add revoke button per key (with confirmation)
- [ ] Add usage instructions/documentation link
- [ ] Show warning about keeping keys secret

**Acceptance Criteria:**
- User can generate new API key with custom name
- Full key displayed once with copy-to-clipboard button
- List shows all active keys (prefix only)
- User can revoke keys
- Clear documentation on how to use keys
- Warning about security displayed

---

#### Story 7.3: API Documentation (1 point)
**As a** developer integrating with MAGUS  
**I want** comprehensive API documentation  
**So that** I can build integrations

**Tasks:**
- [ ] Ensure OpenAPI schema complete
- [ ] Customize Swagger UI with branding
- [ ] Add examples for all endpoints
- [ ] Document authentication methods (JWT vs API key)
- [ ] Create "Getting Started" guide
- [ ] Add code examples (curl, Python, JavaScript)
- [ ] Document rate limits
- [ ] Document error responses

**Acceptance Criteria:**
- OpenAPI schema accurate and complete
- Swagger UI accessible at `/api/docs/`
- All endpoints documented with examples
- Authentication clearly explained
- Code samples provided
- Rate limits documented

---

## Sprint 8: PWA Features & Offline Support (4-6 hours) [P1]

**Goal:** Make the app installable as a PWA with offline capabilities.

### Stories

#### Story 8.1: PWA Manifest & Service Worker (3 points)
**As a** user  
**I want** to install MAGUS on my home screen  
**So that** it feels like a native app

**Tasks:**
- [ ] Create `manifest.json` with app metadata
- [ ] Add app icons (192x192, 512x512, maskable)
- [ ] Configure Workbox for service worker
- [ ] Cache app shell (HTML, CSS, JS)
- [ ] Cache API responses (with expiration)
- [ ] Implement offline fallback page
- [ ] Handle offline task start/stop (queue for sync)
- [ ] Test PWA install on iOS Safari
- [ ] Test PWA install on Chrome Android
- [ ] Add "Install App" prompt

**Acceptance Criteria:**
- App can be installed to home screen
- Works offline (shows cached data)
- Offline actions queued and synced when online
- App shell loads instantly on repeat visits
- Install prompt shown to users
- Passes Lighthouse PWA audit

---

#### Story 8.2: Background Sync & Notifications (2 points)
**As a** user  
**I want** notifications about my ongoing tasks  
**So that** I stay aware of my tracking

**Tasks:**
- [ ] Request notification permission
- [ ] Implement Web Push API
- [ ] Send notification when task reaches 1 hour (configurable)
- [ ] Show persistent notification with live timer (if browser supports)
- [ ] Add notification actions: "Stop", "Dismiss"
- [ ] Handle notification clicks (open app, stop task)
- [ ] Implement background sync for offline actions
- [ ] Test on iOS (limited support)
- [ ] Test on Android

**Acceptance Criteria:**
- User prompted for notification permission
- Notification sent after 1 hour of tracking
- Notification shows current duration (if supported)
- Notification actions work correctly
- Offline actions sync when back online

---

## Sprint 9: Polish & UX Enhancements (6-8 hours) [P1]

**Goal:** Add finishing touches, animations, themes, and improve overall experience.

### Stories

#### Story 9.1: Theme System Implementation (3 points)
**As a** user  
**I want** to choose between light and dark themes  
**So that** the app matches my preference

**Tasks:**
- [ ] Implement CSS custom properties for theming
- [ ] Create dark theme variables (default)
- [ ] Create light theme variables
- [ ] Add theme toggle in settings
- [ ] Persist theme choice to backend
- [ ] Apply theme on page load
- [ ] Add smooth theme transition
- [ ] Test all components in both themes
- [ ] Ensure sufficient color contrast
- [ ] Update Tailwind config for theme support

**Acceptance Criteria:**
- User can toggle between dark and light themes
- Theme persists across sessions
- All components styled correctly in both themes
- Smooth transition when changing themes
- Meets WCAG AA contrast requirements

---

#### Story 9.2: Animations & Transitions (2 points)
**As a** user  
**I want** smooth, delightful animations  
**So that** the app feels polished

**Tasks:**
- [ ] Add page transition animations
- [ ] Add card enter/exit animations
- [ ] Add loading skeletons (no spinners)
- [ ] Add success/error toast animations
- [ ] Add button press feedback (scale, opacity)
- [ ] Add long-press visual feedback (circular progress)
- [ ] Add scroll-based animations (fade-in)
- [ ] Respect `prefers-reduced-motion`
- [ ] Keep animations subtle and fast (<300ms)

**Acceptance Criteria:**
- All interactions have smooth feedback
- Page transitions feel seamless
- Loading states use skeleton screens
- Animations disabled if user prefers reduced motion
- No janky or slow animations

---

#### Story 9.3: Mobile Gestures & Touch Optimization (2 points)
**As a** mobile user  
**I want** intuitive touch gestures  
**So that** the app is easy to use on my phone

**Tasks:**
- [ ] Implement long-press for pin/unpin (with visual feedback)
- [ ] Implement swipe-to-edit on history entries
- [ ] Implement pull-to-refresh on dashboard
- [ ] Add momentum scrolling for horizontal task grid
- [ ] Increase touch targets to minimum 44x44px
- [ ] Add haptic feedback (if supported via vibration API)
- [ ] Test on iOS Safari
- [ ] Test on Chrome Android
- [ ] Optimize for one-handed use

**Acceptance Criteria:**
- Long-press (1.5s) pins/unpins tasks
- Swipe left on history entry reveals edit/delete
- Pull-to-refresh works on dashboard
- All touch targets meet accessibility minimums
- Haptic feedback on supported devices
- Smooth scrolling performance

---

## Sprint 10: Testing & Documentation (4-6 hours) [P1]

**Goal:** Write comprehensive tests, complete documentation, and ensure quality.

### Stories

#### Story 10.1: Backend Testing (2 points)
**As a** developer  
**I want** comprehensive backend tests  
**So that** I can refactor with confidence

**Tasks:**
- [ ] Write unit tests for all models
- [ ] Write tests for all API endpoints
- [ ] Write tests for authentication & permissions
- [ ] Write tests for Celery tasks
- [ ] Write tests for utility functions
- [ ] Aim for 80%+ coverage
- [ ] Set up coverage reporting
- [ ] Add tests to CI pipeline (if applicable)

**Acceptance Criteria:**
- 80%+ test coverage
- All critical paths tested
- All API endpoints have tests
- Authentication and permissions tested
- Celery tasks tested with mocked email

---

#### Story 10.2: Frontend Testing (2 points)
**As a** developer  
**I want** frontend tests for critical flows  
**So that** bugs don't reach production

**Tasks:**
- [ ] Write unit tests for utilities and hooks (Vitest)
- [ ] Write component tests for key components (React Testing Library)
- [ ] Write integration tests for critical flows (Playwright)
  - Login → Start task → Stop task → View summary
  - Create task type → Pin it → Start from quick grid
  - Edit task entry → Save changes
- [ ] Test accessibility with jest-axe
- [ ] Set up test scripts in package.json

**Acceptance Criteria:**
- Critical user flows tested end-to-end
- Component tests cover key interactions
- Accessibility tests pass
- Tests run in CI (if applicable)

---

#### Story 10.3: User Documentation (2 points)
**As a** user  
**I want** clear documentation  
**So that** I know how to use MAGUS

**Tasks:**
- [ ] Write comprehensive README.md
  - Project overview
  - Features list
  - Installation instructions
  - Usage guide
  - API documentation link
  - Troubleshooting
  - Contributing guidelines
- [ ] Create DOCKER.md with deployment guide
- [ ] Create API_GUIDE.md for developers
- [ ] Add screenshots/GIFs of key features
- [ ] Create FAQ section
- [ ] Add license file (choose license)

**Acceptance Criteria:**
- README clear and comprehensive
- Installation steps work for new users
- API guide helps developers integrate
- Screenshots illustrate key features
- License clearly stated

---

## Sprint 11: Deployment & Production Readiness (4-6 hours) [P0]

**Goal:** Prepare for production deployment with security, monitoring, and backups.

### Stories

#### Story 11.1: Production Configuration (2 points)
**As a** system administrator  
**I want** production-ready configuration  
**So that** MAGUS runs securely and reliably

**Tasks:**
- [ ] Create production `docker-compose.prod.yml`
- [ ] Configure environment variables for production
- [ ] Set DEBUG=False and proper SECRET_KEY
- [ ] Configure ALLOWED_HOSTS and CORS properly
- [ ] Set up static file serving via Nginx
- [ ] Configure PostgreSQL with persistence
- [ ] Set up Redis password authentication
- [ ] Configure email backend (SMTP)
- [ ] Add health check endpoints
- [ ] Set up logging to files/stdout

**Acceptance Criteria:**
- Production docker-compose works
- All secrets in environment variables
- Debug mode disabled
- Static files served efficiently
- Database data persists across restarts
- Logs accessible for debugging

---

#### Story 11.2: SSL/TLS Configuration (1 point)
**As a** system administrator  
**I want** HTTPS enabled  
**So that** data is encrypted in transit

**Tasks:**
- [ ] Configure Nginx for SSL
- [ ] Add Let's Encrypt/Certbot support (optional)
- [ ] Document manual certificate setup
- [ ] Redirect HTTP to HTTPS
- [ ] Set security headers (HSTS, CSP, etc.)
- [ ] Test SSL configuration

**Acceptance Criteria:**
- HTTPS works with valid certificate
- HTTP redirects to HTTPS
- Security headers set correctly
- SSL Labs grade A (if applicable)

---

#### Story 11.3: Backup & Recovery (2 points)
**As a** system administrator  
**I want** automated backups  
**So that** data is not lost

**Tasks:**
- [ ] Create backup script for PostgreSQL
- [ ] Schedule backups via cron or Celery Beat
- [ ] Store backups in persistent volume
- [ ] Implement backup rotation (keep last 30 days)
- [ ] Document restore procedure
- [ ] Test backup and restore
- [ ] Optional: Add S3/B2 backup upload

**Acceptance Criteria:**
- Daily automated backups
- Backups stored securely
- Old backups automatically deleted
- Restore procedure documented and tested

---

## Sprint 12 (Stretch): Retro Themes (8-10 hours) [P2]

**Goal:** Implement fun retro OS themes for delightful aesthetics.

### Stories

#### Story 12.1: Theme Infrastructure Expansion (3 points)
**As a** developer  
**I want** a robust theme system  
**So that** adding new themes is easy

**Tasks:**
- [ ] Expand CSS custom properties for advanced theming
- [ ] Create theme configuration objects
- [ ] Support theme-specific assets (textures, icons)
- [ ] Create theme preview in settings
- [ ] Add theme metadata (name, description, screenshot)

**Acceptance Criteria:**
- Theme system supports advanced customization
- Can swap assets per theme
- Preview shows theme before applying
- Easy to add new themes

---

#### Story 12.2: Aqua Theme (Mac OS X Leopard) (2 points)
**Tasks:**
- [ ] Source/create brushed metal texture
- [ ] Create blue lozenge button styles
- [ ] Style with unified toolbar aesthetic
- [ ] Add subtle gloss effects
- [ ] Test on all components

**Acceptance Criteria:**
- Looks like classic Mac OS X
- All components themed correctly
- Maintains usability

---

#### Story 12.3: Aero Theme (Windows 7) (2 points)
**Tasks:**
- [ ] Create glass blur effects (backdrop-filter)
- [ ] Blue/white color scheme
- [ ] Subtle gradients and shadows
- [ ] Window chrome styling
- [ ] Test browser support for blur effects

**Acceptance Criteria:**
- Captures Aero aesthetic
- Glass effects work on supported browsers
- Graceful degradation on unsupported browsers

---

#### Story 12.4: Metro Theme (Windows 8) (1 point)
**Tasks:**
- [ ] Flat design with no gradients
- [ ] Vibrant solid colors
- [ ] Typography-focused layouts
- [ ] Edge-to-edge content
- [ ] Square tiles for task buttons

**Acceptance Criteria:**
- Flat, modern design
- Bold colors and typography
- Tile-based layouts

---

#### Story 12.5: Luna Theme (Windows XP) (2 points)
**Tasks:**
- [ ] Blue/green gradient backgrounds
- [ ] Rounded corners on windows
- [ ] 3D-style button effects
- [ ] Classic Start button aesthetic
- [ ] Nostalgia overload

**Acceptance Criteria:**
- Looks like Windows XP
- Rounded, soft aesthetic
- 3D button effects

---

## Sprint 13 (Stretch): AI Insights (6-8 hours) [P3]

**Goal:** Integrate OpenAI for productivity insights and suggestions.

### Stories

#### Story 13.1: OpenAI Integration Backend (4 points)
**As a** user  
**I want** AI-generated insights about my time  
**So that** I can optimize my productivity

**Tasks:**
- [ ] Create OpenAI API client wrapper
- [ ] Encrypt user API keys in database
- [ ] Create `/api/analytics/insights/` endpoint
- [ ] Design prompt for time tracking analysis
- [ ] Structure output as JSON
- [ ] Cache insights (regenerate daily)
- [ ] Track token usage per user (optional)
- [ ] Handle API errors gracefully
- [ ] Write tests with mocked OpenAI responses

**Acceptance Criteria:**
- User can provide OpenAI API key in settings
- Insights generated from time tracking data
- Insights cached and refreshed daily
- Errors handled without crashing
- User's API key used (not yours)

---

#### Story 13.2: Insights Display UI (2 points)
**As a** user  
**I want** to see AI insights in my dashboard  
**So that** I can act on suggestions

**Tasks:**
- [ ] Create `InsightsCard` component
- [ ] Fetch insights from API
- [ ] Display pattern recognition insights
- [ ] Display optimization suggestions
- [ ] Display balance analysis
- [ ] Add "Regenerate Insights" button
- [ ] Handle loading and error states
- [ ] Make dismissible

**Acceptance Criteria:**
- Insights displayed on analytics page
- Formatted nicely with sections
- User can regenerate insights
- Loading state while generating
- Error shown if OpenAI key invalid

---

## Post-MVP Backlog (Future Sprints) [P3]

Ideas to implement after MVP is stable and deployed:

### User Experience
- [ ] Onboarding tutorial for new users
- [ ] Keyboard shortcuts for power users
- [ ] Customizable dashboard widgets
- [ ] Dark/light mode auto-switch based on time of day
- [ ] Custom color schemes (beyond preset themes)

### Features
- [ ] Task templates/sequences
- [ ] Goal setting with progress tracking
- [ ] Pomodoro timer integration
- [ ] Location-based auto-tracking (geofencing)
- [ ] Calendar integration (Google Cal, iCal)
- [ ] Team/family accounts (shared task types)

### Integrations
- [ ] Webhook support for automation
- [ ] Zapier/Make.com connectors
- [ ] iOS Shortcuts actions
- [ ] Apple Watch complication (requires native app)
- [ ] Google Assistant/Siri voice commands

### Analytics
- [ ] Predictive analytics (AI predicts task duration)
- [ ] Anomaly detection (unusual patterns)
- [ ] Comparative analysis (vs. past weeks/months)
- [ ] Export to Google Sheets/Excel
- [ ] Custom report builder

### Technical
- [ ] Native iOS app (Swift/SwiftUI)
- [ ] Native Android app (Kotlin)
- [ ] Desktop apps (Tauri or Electron)
- [ ] Internationalization (i18n)
- [ ] Multi-language support
- [ ] Public API marketplace
- [ ] Plugin system for extensions

---

## Definition of Done

For each story to be considered "done":

- [ ] Code written and follows style guidelines
- [ ] Unit tests written and passing
- [ ] Integration tests written (if applicable)
- [ ] Manually tested on desktop and mobile
- [ ] Responsive design verified
- [ ] Accessibility checked (ARIA, keyboard nav)
- [ ] API documented (if backend story)
- [ ] Code reviewed (self or pair)
- [ ] No linter errors
- [ ] No console errors
- [ ] Performance acceptable (no lag)
- [ ] Error handling implemented
- [ ] Loading states implemented
- [ ] Committed to feature branch with clear message

---

## Sprint Progress Tracking

Use this section to track progress as you work through sprints:

### Completed Sprints
- [ ] Sprint 0: Project Setup & Infrastructure
- [ ] Sprint 1: Authentication & User Management
- [ ] Sprint 2: Task Types Management
- [ ] Sprint 3: Task Tracking Core
- [ ] Sprint 4: Analytics & Visualizations
- [ ] Sprint 5: Manual Entry Editing
- [ ] Sprint 6: Data Export
- [ ] Sprint 7: API Keys & Extensibility
- [ ] Sprint 8: PWA Features & Offline Support
- [ ] Sprint 9: Polish & UX Enhancements
- [ ] Sprint 10: Testing & Documentation
- [ ] Sprint 11: Deployment & Production Readiness

### Stretch Goals
- [ ] Sprint 12: Retro Themes
- [ ] Sprint 13: AI Insights

---

## Velocity Estimates

**MVP (Sprints 0-11):** 70-90 story points ≈ 70-90 hours ≈ 9-11 full work days

**With Stretch Goals:** +20-30 hours

**Realistic Timeline:**
- **MVP in 2-3 intense days:** Possible if working 12-16 hour days, skipping some polish
- **MVP in 5-7 comfortable days:** More realistic pace with breaks and polish
- **Full implementation with stretch goals:** 10-12 days total

---

## Risk Mitigation

### Potential Blockers & Solutions

**Risk:** React + TypeScript learning curve  
**Solution:** Start with JavaScript, migrate to TypeScript later; use templates

**Risk:** Docker networking issues  
**Solution:** Use docker-compose which handles networking; thorough documentation

**Risk:** PWA installation issues on iOS  
**Solution:** Test early; document iOS-specific quirks; have fallback (just use browser)

**Risk:** Email sending failing in production  
**Solution:** Test SMTP configuration early; provide multiple provider examples

**Risk:** Scope creep (feature requests)  
**Solution:** Stick to MVP first; maintain backlog for future iterations

**Risk:** Data migration from old system  
**Solution:** Write and test migration script; keep old system running during transition

---

## Communication & Collaboration

Since this is primarily a solo project with AI pair programming:

- Commit frequently with clear messages
- Document decisions in code comments
- Keep this SPRINTS.md updated with progress
- Take breaks to avoid burnout
- Celebrate small wins!

---

## Next Steps

1. ✅ Review and approve PLAN.md and SPRINTS.md
2. ⬜ Set up development environment (Docker, etc.)
3. ⬜ Begin Sprint 0: Project Setup & Infrastructure
4. ⬜ Work through sprints sequentially
5. ⬜ Update this document as you go
6. ⬜ Deploy MVP and dogfood (use it yourself!)
7. ⬜ Iterate based on real usage

**Let's build something awesome! 🚀**

