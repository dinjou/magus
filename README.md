# gaebolg
Tools to quantify business deficiencies to plan a long-term solution.

---

# Time Tools
Tools to quantify deficiencies and patterns when you hear things like "there's not enough time." 

## Magus
### Package ID: `nayru.kronos.magus`

Designed to be a quick-and-dirty way of tracking when tasks start, stop, and are interrupted.

Server-side is a python+django webapp.
Client-side is an electron-wrapper pointed at the local webapp server.

### To Do:

- Add Clock-In and Clock-Out
- Add Users
- Create Daily Backup (probably just do this locally with cron and rsync)
- Add Midnight hard-cut of session logins

