# MAGUS ![magus icon](https://github.com/Hyliana/gaebolg/blob/c370d729505a8ee35047fe2385bf7cf7794cda2f/krono/magus/static/magus/favicon.ico)
*(formerly known as gaebolg)*

MAGUS is a full-stack Django Webapp written in Python to streamline self-reported task-tracking in a reactive environment.

**Q: What problem does this solve?**

**A:** MAGUS keeps me from having to do copious amounts of data cleaning. Agents simply click "Start" or "Stop" on the type of event they are reporting, and MAGUS handles the data-entry.

## Features

- **Authentication**: User accounts ensure that agents do not need to self-report their identity for data-entry.
- **Activity-aware Reporting**: Agents are warned when trying to stop tasks that they haven't started, and are asked to verify if a previous task has been interrupted when starting another while they have an ongoing task.
- **Heartbeat**: Ongoing tasks are killed to keep timestamps reasonably accurate if an agent closes the program without stopping a task.
- **Django Admin Console:** Admin users can manually correct erroneous entries without needing to manually update the PostgreSQL15 database.

## Context

My current team is tasked with response to real-time events. For various reasons, we needed to demonstrate the ways our time is used. 

I already had a working understanding of SQL, Python, and Web-Development, so I was able to quickly develop the core of MAGUS over a weekend a few months ago. My friend @Malathair and ChatGPT helped fill in the gaps in my knowledge, and I was able to get this from concept to deployment in about three days.

Server-side is a python+django webapp built on PostgreSQL and Redis.
Client-side is an electron-wrapper pointed at the local webapp server.

> [!NOTE]
> Designed to be a quick-and-dirty fix, this is not intended for long-term deployment. 

## What's Next:

I have a few ideas about ways I can use this code-base, but for right now it's just living here doing nothing much. 

## Questions?

Send me a message on github. I think that's a thing you can do, anyway?
