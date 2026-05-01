# Kanban Board — Finaya

> Replicate this board on [GitHub Projects](https://github.com/JBL-987/Finaya/projects) for live tracking.

---

## Board Structure

| Column | Purpose |
|--------|---------|
| Backlog | Prioritized but not yet scheduled |
| To Do | Committed for current sprint |
| In Progress | Actively being worked on |
| In Review | Code complete, awaiting review/test |
| Done | Merged to main and verified |

---

## Current Board State (as of Sprint 4)

### Backlog

| Card | Epic | Priority |
|------|------|----------|
| Side-by-side location comparison | E1 | Could Have |
| Push notifications for area changes | E1 | Won't Have |
| Admin usage analytics dashboard | E3 | Won't Have |
| CI/CD pipeline with GitHub Actions | E5 | Should Have |

### To Do

_(No items — between sprints)_

### In Progress

_(No items — between sprints)_

### In Review

_(No items)_

### Done

| Card | Epic | Sprint |
|------|------|--------|
| Interactive map-based location analysis | E1 | Sprint 1 |
| User registration and authentication | E2 | Sprint 1 |
| Area distribution results display | E1 | Sprint 1 |
| Revenue projection engine | E7 | Sprint 1 |
| Dashboard with analytics charts | E3 | Sprint 1 |
| Multi-currency support (50+) | E7 | Sprint 1 |
| Automatic map screenshot capture | E1 | Sprint 1 |
| GPS-based default location | E1 | Sprint 1 |
| Professional homepage UI | E3 | Sprint 1 |
| Google Gemini AI map analysis | E1 | Sprint 2 |
| Firebase Firestore storage | E2 | Sprint 2 |
| Probabilistic traffic model | E1 | Sprint 2 |
| Weather impact VIC coefficient | E1 | Sprint 2 |
| Multi-language support (15+) | E3 | Sprint 2 |
| Rate limiting (Redis + SlowAPI) | E5 | Sprint 2 |
| Guest mode (localStorage) | E4 | Sprint 3 |
| Production deployment (Railway) | E5 | Sprint 3 |
| Excel export with formatting | E3 | Sprint 3 |
| AI Advisor chatbot | E6 | Sprint 3 |
| Clean production logging | E5 | Sprint 3 |

---

## How to Replicate on GitHub Projects

1. Go to [github.com/JBL-987/Finaya](https://github.com/JBL-987/Finaya)
2. Click **Projects** tab > **New Project**
3. Select **Board** template
4. Create columns: `Backlog`, `To Do`, `In Progress`, `In Review`, `Done`
5. Add items from the tables above
6. Link each card to its corresponding GitHub Issue
7. Add sprint milestone labels for filtering

### Automation Rules (recommended)

| Trigger | Action |
|---------|--------|
| Issue opened | Move to Backlog |
| Issue assigned | Move to In Progress |
| PR opened linking issue | Move to In Review |
| PR merged | Move to Done |
