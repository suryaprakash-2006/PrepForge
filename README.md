# PrepForge

> **12-Week Internship Preparation & Progress Tracker**

---

## Description

PrepForge is a full-stack web application designed to help students systematically manage and track their internship preparation over a structured 12-week timeline.

The application is intended to support preparation across multiple technical areas:

- **Programming** — Python, C++
- **Data Structures & Algorithms** — DSA problem tracking
- **Databases** — SQL, DBMS, MongoDB
- **Core Computer Science** — OOP, Operating Systems, Computer Networks, Computer Architecture, Software Engineering
- **Data Science & AI/ML** — topic-by-topic progress
- **SDE Preparation** — system design, coding patterns
- **Projects** — defence preparation
- **Assessments** — practice test tracking
- **Mock Interviews** — session logging and feedback
- **Weakness Management** — identify and close knowledge gaps
- **Revision** — spaced repetition tracking
- **Progress Analytics** — visual dashboards

> **Note:** The features listed above represent the full planned scope. The project is currently in the **initial bootstrap phase** — no application functionality has been implemented yet.

---

## Planned Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite (JavaScript) |
| Backend | FastAPI (Python) |
| Database | MongoDB |
| API Style | REST |
| Auth | JWT (JSON Web Tokens) |
| Version Control | Git + GitHub |

---

## Architecture

```
Browser
  └── React / Vite (frontend)
          ↓  REST API calls
      FastAPI (backend / Python)
          ↓  async queries
        MongoDB (database)
```

---

## Development Principles

PrepForge is built with the following principles:

- **Free-first** — no mandatory paid services, APIs, or infrastructure
- **Open-source-first** — all dependencies are open-source
- **No mandatory paid AI APIs** — AI features, if any, must be optional and free-tier compatible
- **Portable** — runs fully on a local machine with no cloud dependency during development
- **Simple, maintainable architecture** — monorepo, flat module structure, no unnecessary abstractions
- **Security-conscious** — multi-user design, user-data isolation, proper JWT handling, hashed passwords from day one

---

## Current Status

```
Phase 1 — Repository Bootstrap
Status:  IN PROGRESS
```

| Phase | Description | Status |
|---|---|---|
| 1 | Repository bootstrap | 🔄 In Progress |
| 2 | Backend scaffold + FastAPI + MongoDB connectivity | ⏳ Planned |
| 3 | Frontend scaffold + Vite + React shell | ⏳ Planned |
| 4 | Authentication — Register, Login, Logout, JWT | ⏳ Planned |
| 5 | Dashboard + Roadmap + Tasks (MVP core) | ⏳ Planned |

---

## Planned MVP

The first usable version of PrepForge will include only:

- [ ] User registration
- [ ] User login
- [ ] User logout
- [ ] Protected dashboard (authenticated users only)
- [ ] 12-week roadmap display
- [ ] Daily task management
- [ ] Task completion tracking
- [ ] Basic progress percentage
- [ ] User-specific data storage (isolated per user)

Advanced modules (DSA tracker, SQL tracker, analytics, mock interviews, etc.) will be implemented after the MVP is stable.

---

## Repository Structure

```
PrepForge/
├── frontend/       # React + Vite application (not yet scaffolded)
├── backend/        # FastAPI application (not yet scaffolded)
├── docs/           # Project documentation
├── .env.example    # Environment variable template — copy to .env and fill in values
├── .gitignore      # Prevents secrets and generated files from being committed
└── README.md       # This file
```

---

## Getting Started

> Setup instructions will be added in Phase 2 (Backend Scaffold) and Phase 3 (Frontend Scaffold).

---

## Environment Configuration

Copy `.env.example` and fill in the required values before running any part of the application:

```bash
# For the backend
cp .env.example backend/.env
```

See `.env.example` for documentation on each variable.

**Never commit a real `.env` file.** It is listed in `.gitignore`.

---

## Contributing

This is a personal portfolio project. Contributions are not currently open, but the repository is public for reference.

---

## License

No license has been selected yet.
