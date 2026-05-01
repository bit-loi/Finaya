# Sprint 3: Production Deploy & Guest Mode

> **Sprint Period**: February 8 – February 9, 2026  
> **Sprint Goal**: Deploy to production, implement guest mode, fix CORS/middleware issues  
> **Sprint Duration**: 2 days (intensive sprint)  
> **Velocity**: 6 story points completed

---

## Sprint Backlog

| ID | User Story | Story Points | Status |
|----|-----------|-------------|--------|
| US-07 | Guest mode without login (localStorage) | 3 | Done |
| US-08 | Backend deployed and accessible in production | 5 | Done |
| US-12 | Excel export with Rupiah formatting | 3 | Done |
| US-13 | AI Advisor for ROI and strategy questions | 3 | Done |
| US-19 | Clean production logging | 1 | Done |

---

## Commits (32)

| Date | Hash | Message |
|------|------|---------|
| Feb 07 | `c0d0658` | chore: revert dockerfile copy strategy to standard practice |
| Feb 07 | `567d899` | Update backend configuration |
| Feb 07 | `5d3520b` | Add motor to requirements.txt |
| Feb 07 | `39c7ae1` | Update backend configuration, ignore firebase credentials |
| Feb 07 | `777b53c` | Revert python version back to 3.10 and update config |
| Feb 08 | `de9d06f` | feat: Add guest mode with local storage support |
| Feb 08 | `2674dd4` | fix(frontend): Add check for localhost API URL in production |
| Feb 08 | `925f292` | fix: Mock analysis endpoints for guest mode |
| Feb 08 | `229bf32` | chore(backend): Update Dockerfile for production |
| Feb 08 | `ad7d8d0` | fix(frontend): Enrich guest mode mock data |
| Feb 08 | `ed7eee9` | fix(frontend): Remove mock analysis data from API service |
| Feb 08 | `99d0635` | fix(frontend): Truly remove mock analysis data |
| Feb 08 | `7a7678c` | fix(frontend): Add critical alert for missing API URL |
| Feb 08 | `5382532` | fix(frontend): Set default API URL to production |
| Feb 08 | `d80b29a` | chore(frontend): Implement cleaner production logging |
| Feb 08 | `2b04fea` | fix(backend): Configure explicit CORS origins |
| Feb 08 | `3132a59` | fix(backend): Add Railway domain to CORS origins |
| Feb 08 | `59a0f99` | fix(backend): Force permissive CORS to unblock API |
| Feb 08 | `e4f40cd` | fix(backend): Optimize middleware order for CORS stability |
| Feb 08 | `0bee048` | fix(backend): Update CORS settings manually |
| Feb 08 | `4d8407f` | fix(backend): Update Dockerfile workdir and port |
| Feb 08 | `59731f6` | fix(backend): Bypass rate limiting for OPTIONS (CORS preflight) |
| Feb 08 | `6e1ce8a` | fix(backend): Correct middleware order — CORS outer, SlowAPI inner |
| Feb 08 | `969f9e4` | fix(backend): Add missing SlowAPIMiddleware import |
| Feb 08 | `2460a37` | fix(backend): Prevent startup crash (502) — optional config vars |
| Feb 08 | `1fd7ae6` | fix(backend): Soft-fail on startup initialization |
| Feb 08 | `f576145` | fix(backend): Handle missing Gemini API key gracefully |
| Feb 08 | `b827773` | fix(backend): Lazy-load FinayaAgent to prevent 502 |
| Feb 09 | `4a95771` | fix(backend): Fix CORS_ORIGINS parsing, OPTIONS middleware |
| Feb 09 | `a84c16e` | fix: production-ready config and Dockerfile |
| Feb 09 | `5b52b5e` | fix: Dockerfile CMD hardcode port |
| Feb 09 | `c11d740` | fix: hide logout for guest users |

---

## Sprint Review

### What was delivered
- Guest mode with localStorage persistence for non-authenticated users
- Full production deployment on Railway
- CORS middleware properly configured for cross-origin API access
- Clean production logging utility
- Graceful error handling for missing API keys and config vars
- Lazy-loading for heavy AI services to prevent 502 errors

### Production issues resolved this sprint
- CORS preflight (OPTIONS) blocked by rate limiter
- Middleware ordering conflicts (CORS vs SlowAPI)
- Startup crashes due to missing environment variables
- Railway 502 errors from blocking port binding

---

## Sprint Retrospective

### What went well
- All critical production blockers resolved within 2 days
- Conventional commit messages consistently adopted (fix(backend):, fix(frontend):, chore:)
- Scoped commits — each fix addresses one specific issue

### What could be improved
- 32 commits in 2 days indicates reactive debugging rather than proactive testing
- CORS issues required 10+ iterative fixes — a staging environment would have caught this earlier
- Guest mode went through add > mock > remove mock > re-add cycle

### Action items
- Set up a staging environment before deploying to production
- Add integration tests for CORS and middleware behavior
- Test deployment configuration locally with Docker before pushing
