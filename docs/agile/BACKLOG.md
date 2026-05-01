# Product Backlog — Finaya

> **Product Owner**: JBL  
> **Last Updated**: 2026-03-31  
> **Methodology**: Scrum (2-week sprints)

---

## Epics

| ID | Epic | Description |
|----|------|-------------|
| E1 | Location Analysis Engine | Core AI-powered geospatial analysis |
| E2 | User Management & Auth | Authentication, profiles, preferences |
| E3 | Dashboard & Analytics | Data visualization, history, export |
| E4 | Guest Mode | Non-authenticated user experience |
| E5 | Deployment & Infrastructure | Docker, CI/CD, production readiness |
| E6 | AI Agent & Advisor | Conversational AI business consultant |
| E7 | Financial Tools | Revenue projection, currency support |

---

## User Stories (Prioritized by MoSCoW)

### Must Have

| ID | User Story | Epic | Sprint | Status |
|----|-----------|------|--------|--------|
| US-01 | As a **user**, I want to **analyze a business location on an interactive map**, so that I can **understand the profitability potential of that location**. | E1 | Sprint 1 | Done |
| US-02 | As a **user**, I want to **register and log in to the platform**, so that **my analysis data is stored securely**. | E2 | Sprint 1 | Done |
| US-03 | As a **user**, I want to **see analysis results showing area distribution (residential, roads, open spaces)**, so that I can **understand the location characteristics**. | E1 | Sprint 1 | Done |
| US-04 | As a **user**, I want to **see daily, monthly, and yearly revenue projections**, so that I can **make data-driven business decisions**. | E7 | Sprint 1 | Done |
| US-05 | As a **user**, I want the **system to use Google Gemini AI to analyze map screenshots**, so that **analysis is more accurate with computer vision**. | E1 | Sprint 2 | Done |
| US-06 | As a **user**, I want **my data stored in Firebase Firestore**, so that **my analyses are persistent and accessible later**. | E2 | Sprint 2 | Done |
| US-07 | As a **user**, I want to **access the platform without logging in (guest mode)**, so that I can **try out the features before registering**. | E4 | Sprint 3 | Done |
| US-08 | As a **user**, I want the **backend deployed and accessible in production**, so that **the platform can be used in a real environment**. | E5 | Sprint 3 | Done |

### Should Have

| ID | User Story | Epic | Sprint | Status |
|----|-----------|------|--------|--------|
| US-09 | As a **user**, I want to **see a dashboard with 12-month analytics charts**, so that I can **monitor usage trends**. | E3 | Sprint 1 | Done |
| US-10 | As a **user**, I want to **choose from 50+ currencies**, so that **analysis results are relevant to my business location**. | E7 | Sprint 1 | Done |
| US-11 | As a **user**, I want to **use automatic map screenshot capture**, so that **the analysis process is more seamless**. | E1 | Sprint 1 | Done |
| US-12 | As a **user**, I want to **export analysis results to Excel** with proper Rupiah formatting and multiple sheets, so that I can **share reports with stakeholders**. | E3 | Sprint 3 | Done |
| US-13 | As a **user**, I want to **ask the AI Advisor about ROI, competition, and business pivots**, so that I can **get real-time strategic advice**. | E6 | Sprint 3 | Done |
| US-14 | As a **user**, I want a **probabilistic traffic model based on junction analysis** to be used for simulation, so that **visitor estimates are more realistic**. | E1 | Sprint 2 | Done |
| US-15 | As a **user**, I want **weather impact calculated via the VIC coefficient**, so that **revenue projections account for weather conditions**. | E1 | Sprint 2 | Done |

### Could Have

| ID | User Story | Epic | Sprint | Status |
|----|-----------|------|--------|--------|
| US-16 | As a **user**, I want my **default location set based on my GPS**, so that **the map immediately shows the nearest area**. | E1 | Sprint 1 | Done |
| US-17 | As a **user**, I want an **attractive and professional homepage UI**, so that **the platform makes a positive first impression**. | E3 | Sprint 1 | Done |
| US-18 | As a **user**, I want the **platform to support 15+ languages**, so that **it can be used globally**. | E3 | Sprint 2 | Done |
| US-19 | As a **developer**, I want **clean production logging in the backend**, so that **debugging is easier without noise**. | E5 | Sprint 3 | Done |
| US-20 | As a **developer**, I want **rate limiting with Redis and SlowAPI**, so that **the API is protected from abuse**. | E5 | Sprint 2 | Done |

### Won't Have (This Release)

| ID | User Story | Epic | Sprint | Status |
|----|-----------|------|--------|--------|
| US-21 | As a **user**, I want to **compare multiple locations side-by-side**, so that I can **choose the best location**. | E1 | Backlog | Backlog |
| US-22 | As a **user**, I want to **receive notifications when significant changes occur in analyzed areas**, so that I **stay up-to-date**. | E1 | Backlog | Backlog |
| US-23 | As an **admin**, I want to **see platform usage analytics**, so that I can **understand user behavior**. | E3 | Backlog | Backlog |
| US-24 | As a **developer**, I want a **CI/CD pipeline with GitHub Actions**, so that **deployment is automated and tested**. | E5 | Backlog | Backlog |

---

## Definition of Done

Each user story is considered **Done** when it meets:

1. Feature works as described
2. No errors or crashes in production
3. Code committed with conventional commit message
4. Changes pushed to `main` branch
