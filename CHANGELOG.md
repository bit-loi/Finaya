# Changelog

All notable changes to the Finaya project are documented here, grouped by sprint.  
Format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [Sprint 4] - Enhancement & Polish (Feb 9 – Mar 31, 2026)

### Added
- Excel export with proper Rupiah formatting and multiple sheets
- AI Advisor conversation history persistence
- Guest mode navigation improvements and homepage CTA

### Changed
- Upgraded Gemini model to v3-flash-preview
- Cleaned up production logging

---

## [Sprint 3] - Production Deploy & Guest Mode (Feb 8–9, 2026)

### Added
- Guest mode with localStorage support for non-authenticated users
- Mock analysis endpoints for guest mode demo
- Clean production logging utility
- Critical alert for missing VITE_API_BASE_URL

### Fixed
- CORS preflight (OPTIONS) blocked by rate limiter
- Middleware ordering — CORS outer, SlowAPI inner
- Startup crash (502) by making config vars optional
- Lazy-loaded FinayaAgent to prevent Railway 502 from blocking port binding
- Missing Gemini API key graceful handling in AgentService
- Production API URL defaulting to Railway instance
- Removed residual mock analysis data from API service
- Dockerfile workdir and port configuration

### Infrastructure
- Configured explicit CORS origins for production
- Added Railway domain to CORS origins
- Updated Dockerfile for production deployment
- Set default API URL to production Railway instance

---

## [Sprint 2] - Platform Migration & AI Engine (Jan 26 – Feb 7, 2026)

### Added
- Google Gemini multimodal AI integration for map screenshot analysis
- Probabilistic traffic model based on junction analysis
- Weather Visitor Impact Coefficient (VIC) engine
- Firebase Firestore as persistent NoSQL database
- Firebase Authentication
- Docker configuration (Dockerfile + docker-compose.yml)
- Railway deployment configuration (railway.toml)
- Rate limiting with Redis and SlowAPI

### Changed
- Migrated database from Supabase to Firebase
- Clean reset of entire codebase for AI platform architecture
- Refactored imports to use absolute path aliases
- Consolidated utility functions

### Fixed
- Dashboard build error (duplicate key)
- Missing import path alias in GlowingEffect component
- Utils path unified for production build stability

### Infrastructure
- Added railway.toml for backend deployment
- Added docker-compose for multi-service orchestration
- Reverted Python version to 3.10 for compatibility

---

## [Sprint 1] - Foundation & Core Features (Oct 24 – Nov 6, 2025)

### Added
- Interactive map-based business location analysis
- Analysis form with business parameters (building width, operating hours, product price)
- Results panel with area distribution visualization
- Financial management features
- Multi-currency support (50+ currencies with flag icons)
- Dashboard with analytics charts
- GPS-based default location detection
- User authentication (register/login)
- SVG logo and flag assets
- README documentation

### Changed
- Migrated from Next.js to React + Vite
- Improved Navbar and Map Component design
- Improved Home page UI
- Refactored backend to modular architecture (repositories, services, schemas)

### Fixed
- Currency formatting for financial management and dashboard
- Backend and frontend integration issues
- Business Location Strategist feature bugs

### Removed
- Fake transaction features (removed in favor of real analysis data)
