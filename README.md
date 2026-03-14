<div align="center">

# CodeXRay

### AI-Powered Codebase Intelligence Platform

Paste a GitHub repository URL and receive architecture insights, dependency graphs, and a structured engineering review within seconds.

**Live Demo**  
https://codexray-izf8.vercel.app

**Backend API Documentation**  
https://codexray-backend-47it.onrender.com/docs

</div>

---

## Overview

Understanding an unfamiliar codebase is one of the most time-consuming tasks in software engineering.  
Before contributing to a project, developers typically spend hours attempting to answer questions such as:

- How is the project structured?
- Which components depend on each other?
- What architectural pattern does the system follow?
- Where are the most important modules located?

CodeXRay automates this process.

Given a public GitHub repository, CodeXRay clones the project, analyzes its structure, extracts dependency relationships, and reconstructs the architecture of the system.

Instead of manually reading hundreds of files, developers receive a structured breakdown of the system within seconds.

---

## What CodeXRay Produces

CodeXRay performs several layers of analysis to reveal the internal structure of a repository.

### Architecture Detection

Automatically identifies architectural patterns present in the codebase, including:

- MVC
- Layered Architecture
- Microservices
- Monolithic Systems
- Event-Driven Architectures
- Serverless Systems

### Dependency Graph

Builds a directed graph showing how files import and depend on each other across the repository.

The visualization allows developers to quickly understand how modules interact.

### File Explorer

Indexes the entire file structure and allows inspection of dependency relationships for each file.

### Engineering Review

Generates a structured summary describing the strengths, weaknesses, and architectural characteristics of the project.

---

## Example Repositories to Analyze

You can test CodeXRay with well-known open source repositories such as:

- https://github.com/pallets/flask
- https://github.com/encode/starlette
- https://github.com/tiangolo/fastapi

Submitting one of these repositories will generate a full analysis dashboard.

---

## System Workflow

```
User submits GitHub repository URL
            │
            ▼
POST /repos/analyze
            │
            ▼
Repository record created and analysis job queued
            │
            ▼
Background worker pipeline

1. Clone repository
2. Recursively scan files
3. Detect programming languages
4. Extract dependencies using AST parsing
5. Build dependency graph
6. Detect architectural patterns
7. Generate engineering review
8. Persist results to PostgreSQL
9. Mark analysis status as completed

            │
            ▼
Frontend polls analysis status
            │
            ▼
Interactive dashboard renders results
```

---

## Technology Stack

### Backend

The backend service performs repository ingestion, analysis, and data persistence.

Core technologies include:

- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- asyncpg
- Python AST
- httpx

### Frontend

The frontend provides an interactive dashboard for exploring analysis results.

Core technologies include:

- Next.js 16 (App Router)
- TypeScript
- Tailwind CSS
- ReactFlow
- Zustand
- Axios

### Infrastructure

Deployment and infrastructure services:

- Render — backend hosting and PostgreSQL
- Vercel — frontend hosting
- Docker — local development database

---

## Project Structure

```
codexray/
│
├── backend/
│   ├── app/
│   │   ├── api/routes/          API route handlers
│   │   ├── pipeline/
│   │   │   ├── ingestion/       Repository cloning
│   │   │   ├── file_indexer/    File scanning and language detection
│   │   │   ├── parser/          AST dependency extraction
│   │   │   ├── graph_builder/   Dependency graph construction
│   │   │   ├── architecture/    Architecture detection
│   │   │   └── review/          Engineering review generation
│   │   ├── models/              SQLAlchemy ORM models
│   │   ├── db/                  Database configuration
│   │   └── workers/             Background analysis worker
│   └── main.py
│
└── frontend/
    ├── app/                     Next.js App Router pages
    ├── components/
    │   ├── dashboard/           Analysis panels
    │   ├── graph/               Dependency graph viewer
    │   ├── explorer/            File explorer
    │   └── shared/              Shared UI components
    ├── hooks/                   Custom React hooks
    ├── store/                   Zustand state management
    └── lib/                     API client utilities
```

---

## API Endpoints

| Method | Endpoint | Description |
|------|------|------|
| POST | `/repos/analyze` | Submit repository for analysis |
| GET | `/repos/{repo_id}/status` | Poll analysis status |
| GET | `/repos/{repo_id}/structure` | Retrieve indexed file list |
| GET | `/repos/{repo_id}/dependencies` | Retrieve dependency edges |
| GET | `/repos/{repo_id}/graph` | Retrieve dependency graph |
| GET | `/repos/{repo_id}/architecture` | Retrieve detected architecture |
| GET | `/repos/{repo_id}/review` | Retrieve engineering review |

Full interactive documentation is available at:

https://codexray-backend-47it.onrender.com/docs

---

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker

---

### Backend Setup

Start PostgreSQL

```
docker run --name codexray-db \
-e POSTGRES_PASSWORD=postgres \
-e POSTGRES_DB=codexray \
-p 5432:5432 \
-d postgres:16
```

Install dependencies

```
cd backend
pip install -r requirements.txt
```

Configure environment variables

```
cp .env.example .env
```

Add your GitHub API token to `.env`.

Start the backend server

```
uvicorn backend.main:app --reload
```

---

### Frontend Setup

```
cd frontend
npm install
```

Create environment configuration

```
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

Start the development server

```
npm run dev
```

Open the application at:

```
http://localhost:3000
```

---

## Environment Variables

### Backend (.env)

| Variable | Description |
|------|------|
| DATABASE_URL | PostgreSQL connection string |
| GITHUB_TOKEN | GitHub API token |
| ALLOWED_ORIGINS | Allowed CORS origins |
| WORKSPACE_ROOT | Directory for cloned repositories |
| ENV | Application environment |

---

## Author

Ujwal Shetty

GitHub:  
https://github.com/ujwalshetty625
