# PROJECT_STATE: cock-tail

> **System Directive for PM-Architect:**
> You are acting as the Lead PM-Architect for this project. Treat this document as the single source of truth. 
> When re-primed with this file, update Section 4 (Master Implementation Roadmap) and Section 5 (Current Active Execution Unit) based on recent progress, and output the exact instructions for the Worker LLM for the next step.

---

## 1. Project Overview & Core Vision
* **Project Name:** cock-tail
* **Target Directory:** `~/projects/cock-tail/`
* **Core Objective:** A modern, minimalistic, and visually vibrant web application categorizing cocktails by their base liquor. Features expanding image cards with integrated recipes and "under construction" placeholders for incomplete entries.
* **Target Output:** A responsive web application (Astro/Tailwind Frontend) hosted initially on GitHub Pages, designed for modular expansion to a dedicated server and backend API.

---

## 2. Technical Architecture & Tech Stack

### Core Stack
* **OS / Runtime Environment:** Linux / Node.js 20 (Frontend)
* **Frameworks & Core Libraries:** Astro, Tailwind CSS, Alpine.js (for UI interactions)
* **CI/CD & Hosting (Phase 1):** GitHub Actions, GitHub Pages
* **Backend Pipeline (Phase 3 - Future):** FastAPI, Pydantic, SQLAlchemy, Debian target deployment

### Directory Structure Blueprint
```text
cock-tail/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── docs/
│   └── PROJECT_STATE.md
├── frontend/
│   ├── public/
│   ├── src/
│   ├── astro.config.mjs
│   ├── tailwind.config.cjs
│   └── package.json
├── backend/ 
│   ├── alembic/
│   ├── api/
│   ├── core/
│   │   └── database.py
│   ├── models/
│   ├── schemas/
│   ├── alembic.ini
│   ├── main.py
│   └── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Architectural Directives & Coding Rules

* Modularity: Maintain strict separation of concerns. UI components must be reusable.

* Design Language: Vibrant, modern, minimalistic. Use ample whitespace, high-contrast typography, and fluid transitions.

* Deployment Agility: The Astro configuration must use dynamic environment variables for site and base paths to ensure a seamless migration from GitHub Pages to a custom domain later.

* Environment & Secrets: No hardcoding sensitive data.

## 3. Environment & Configuration Rules

* **Required Prerequisites:** Node.js 20+, Git, GitHub Repository

* **Required .env Variables (Local):**

        APP_ENV (development | production)

* **Build / Execution Commands (Frontend):**

        Setup: npm install

        Run Dev Server: npm run dev

        Build for Production: npm run build

## 4. Master Implementation Roadmap

    Status Legend: [ ] Not Started | [/] In Progress | [x] Completed

### Phase 1: Environment Setup & CI/CD Pipeline ###

    [x] **Step 1.1:** Initialize the Astro project with Tailwind CSS, set up the directory layout, and configure `astro.config.mjs` for GitHub Pages compatibility.
    [x] **Step 1.2:** Write the GitHub Actions `deploy.yml` workflow to automate static builds and deployments to the `gh-pages` branch.
    [x] **Step 1.3:** Configure the base layout template (`Layout.astro`) with global vibrant/minimalistic styling.
    [x] **Step 1.4:** Create the JSON data structure for the base liquors and the sample White Russian cocktail.

### Phase 2: UI/UX Component Development ###

    [x] **Step 2.1:** Build the base liquor category landing page layout.
    [x] **Step 2.2:** Build the interactive, expandable Cocktail Card component (handling the image click-to-enlarge and recipe reveal).
    [x] **Step 2.3:** Implement the "Under Construction" placeholder logic for non-hero cocktails.

### Phase 3: Future Expansion Scaffolding ###

    [x] **Step 3.1:** Scaffold initial FastAPI backend directory structure for future migration off GitHub Pages.
    [x] **Step 3.2:** Configure PostgreSQL database connection pool and initialize Alembic for schema migrations.
    [x] **Step 3.3:** Provision local PostgreSQL database via Docker Compose (port 5433) and establish SQLAlchemy models (`Category`, `Cocktail`).
    [x] **Step 3.4:** Generate and apply initial Alembic migrations, and fully Dockerize the entire stack (Frontend, Backend, and Database) for local development.
    [ ] **Step 3.5:** Build Pydantic schemas and implement FastAPI CRUD endpoints to interact with the database.

---

## 5. Current Active Execution Unit

* **Current Step ID:** Step 3.5
* **Status:** `[ ] Not Started`
* **Target Files:** `backend/api/`, `backend/schemas/cocktail.py`, `backend/main.py`
* **Objective:** Build out the Pydantic schemas and FastAPI CRUD endpoints to serve the cocktail data dynamically from the PostgreSQL database, preparing the API for frontend integration.

---

## 6. Audit Trail & Progress Log

* **2026-08-08:** Project blueprint updated to reflect `cock-tail` repository name.
* **2026-08-08:** Step 1.1 completed: Astro/Tailwind frontend initialized and verified with successful production build.
* **2026-08-08:** Step 1.2 completed: GitHub Actions workflow created for automated GitHub Pages deployment.
* **2026-08-09:** Step 1.3 completed: Base layout template (`Layout.astro`) created with vibrant, modern Tailwind styling.
* **2026-08-09:** Step 1.4 completed: Structured `cocktails.json` dataset created containing base liquor categories and cocktail details.
* **2026-08-09:** Step 2.1 completed: Primary landing page layout built with base liquor category grids.
* **2026-08-09:** Step 2.2 completed: Interactive, responsive CocktailCard component implemented using native HTML `<dialog>`.
* **2026-08-09:** Step 2.3 completed: "Under Construction" conditional rendering and visual overlays added to non-active cocktail cards.
* **2026-08-09:** Step 3.1 completed: Scaffolded the FastAPI backend directory structure and initialized the core application entry point.
* **2026-08-09:** Step 3.2 completed: PostgreSQL connection logic (SQLAlchemy) and Alembic migration environment configured. Intentionally left without an active database to maintain strict project isolation.
* **2026-08-15:** Step 3.3 & 3.4 completed: Full-stack Dockerization achieved. Configured `docker-compose.yml` for Astro frontend, FastAPI backend, and PostgreSQL (bound to 5433 to prevent local conflicts). Created SQLAlchemy models, successfully generated and applied initial Alembic migrations, and cleaned up redundant local Python artifacts.