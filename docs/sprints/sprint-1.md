# Sprint 1: Foundation & Core Features

> **Sprint Period**: October 24 – November 6, 2025  
> **Sprint Goal**: Build the core platform with map-based analysis, financial tools, and basic UI  
> **Sprint Duration**: 2 weeks  
> **Velocity**: 8 story points completed

---

## Sprint Backlog

| ID | User Story | Story Points | Status |
|----|-----------|-------------|--------|
| US-01 | Analyze business location on interactive map | 5 | Done |
| US-02 | Register and log in to platform | 3 | Done |
| US-03 | View area distribution results | 3 | Done |
| US-04 | View daily/monthly/yearly revenue projections | 3 | Done |
| US-09 | Dashboard with analytics charts | 3 | Done |
| US-10 | Multi-currency support (50+ currencies) | 2 | Done |
| US-11 | Automatic map screenshot capture | 3 | Done |
| US-16 | GPS-based default location | 2 | Done |
| US-17 | Professional homepage UI | 2 | Done |

---

## Commits (16)

| Date | Hash | Message |
|------|------|---------|
| Oct 24 | `f25b1ed` | change from nextjs to react js |
| Oct 27 | `85d5f4b` | first step |
| Oct 27 | `aacccf3` | fix: analysisForm, resultPanel, map |
| Oct 28 | `0fb3b57` | ADD: financial management features |
| Oct 30 | `c69da5c` | Erase: Fake Transaction Features |
| Oct 31 | `a1731dc` | fix: backend and frontend integration, modular backend |
| Oct 31 | `ffc1483` | ADD: flags and svg logo |
| Oct 31 | `92153a1` | FIX: currency format for financial management and dashboard |
| Nov 02 | `eb68e84` | setup readme |
| Nov 02 | `b19ce72` | FIX: Business Location Strategist Feature |
| Nov 02 | `a8179b7` | Merge branch 'main' |
| Nov 02 | `cc1aafa` | fix: financial manage code |
| Nov 04 | `1e47934` | ADD: Multiple Currencies Format |
| Nov 05 | `389582e` | ADD: Default Location based on user's location |
| Nov 06 | `dfa4dd7` | CHANGES: Navbar and Map Component |
| Nov 06 | `87ffa66` | CHANGES: Improve Home UI |

---

## Sprint Review

### What was delivered
- Core map-based analysis interface with form and results panel
- Financial management features with multi-currency support
- User authentication and basic dashboard
- Modular backend architecture (repositories, services, schemas)
- Professional homepage and navbar

### What was not delivered
- AI-powered analysis (moved to Sprint 2)
- Persistent database storage (used local state)

---

## Sprint Retrospective

### What went well
- Rapid prototyping — full platform skeleton in 2 weeks
- Migration from Next.js to React+Vite improved development speed

### What could be improved
- Commit messages were inconsistent (mix of ALL CAPS, lowercase, no prefix convention)
- No branching strategy — all commits directly on main
- Financial management feature was added then partially removed ("Erase: Fake Transaction Features")

### Action items
- Adopt conventional commits (feat:, fix:, chore:)
- Plan features more carefully before implementing to avoid rollbacks
