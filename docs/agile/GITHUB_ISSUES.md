# GitHub Issues — User Stories

> These issues are ready to be created on [github.com/JBL-987/Finaya/issues](https://github.com/JBL-987/Finaya/issues).  
> Since `gh` CLI is not available, create them manually or install `gh` and run the script at the bottom.

---

## Closed Issues (Completed Features)

### Issue #1: Interactive map-based location analysis
**Labels**: `enhancement`, `sprint-1`  
**Milestone**: Sprint 1  
**Description**:  
As a user, I want to analyze a business location on an interactive map, so that I can understand the profitability potential of that location.

**Acceptance Criteria**:
- [ ] Map component renders with interactive controls
- [ ] User can click on map to select location
- [ ] Analysis form accepts business parameters
- [ ] Results panel shows area distribution and metrics

---

### Issue #2: User registration and authentication
**Labels**: `enhancement`, `sprint-1`  
**Milestone**: Sprint 1  
**Description**:  
As a user, I want to register and log in to the platform, so that my analysis data is stored securely.

**Acceptance Criteria**:
- [ ] Registration with email and password
- [ ] Login with JWT token authentication
- [ ] Protected routes require authentication
- [ ] User profile accessible via /auth/me

---

### Issue #3: Revenue projection engine
**Labels**: `enhancement`, `sprint-1`  
**Milestone**: Sprint 1  
**Description**:  
As a user, I want to see daily, monthly, and yearly revenue projections, so that I can make data-driven business decisions.

**Acceptance Criteria**:
- [ ] Revenue calculated from business parameters
- [ ] Daily, monthly, and yearly breakdown displayed
- [ ] Cost analysis included
- [ ] ROI calculation displayed

---

### Issue #4: Multi-currency support
**Labels**: `enhancement`, `sprint-1`  
**Milestone**: Sprint 1  
**Description**:  
As a user, I want to choose from 50+ currencies, so that analysis results are relevant to my business location.

**Acceptance Criteria**:
- [ ] Currency selector with 50+ options
- [ ] Flag icons for each currency
- [ ] Revenue results displayed in selected currency
- [ ] Currency preference persisted per session

---

### Issue #5: Google Gemini AI map analysis
**Labels**: `enhancement`, `sprint-2`  
**Milestone**: Sprint 2  
**Description**:  
As a user, I want the system to use Google Gemini AI to analyze map screenshots, so that analysis is more accurate with computer vision.

**Acceptance Criteria**:
- [ ] Map screenshot automatically captured
- [ ] Gemini Vision API analyzes screenshot
- [ ] Area distribution extracted (residential, road, open space)
- [ ] Population density estimated

---

### Issue #6: Firebase migration
**Labels**: `infrastructure`, `sprint-2`  
**Milestone**: Sprint 2  
**Description**:  
As a developer, I want to migrate from Supabase to Firebase, so that authentication and data storage are unified under one platform.

**Acceptance Criteria**:
- [ ] Firebase Authentication replaces Supabase Auth
- [ ] Firestore replaces Supabase database
- [ ] All existing features work with new backend
- [ ] Firebase credentials properly secured

---

### Issue #7: Probabilistic traffic model
**Labels**: `enhancement`, `sprint-2`  
**Milestone**: Sprint 2  
**Description**:  
As a user, I want a probabilistic traffic model based on junction analysis, so that visitor estimates are more realistic.

**Acceptance Criteria**:
- [ ] Junction probability model (B/T) implemented
- [ ] Traffic flow simulated for storefront passing traffic
- [ ] Results integrated into revenue pipeline

---

### Issue #8: Weather impact coefficient (VIC)
**Labels**: `enhancement`, `sprint-2`  
**Milestone**: Sprint 2  
**Description**:  
As a user, I want weather impact calculated via the VIC coefficient, so that revenue projections account for weather conditions.

**Acceptance Criteria**:
- [ ] VIC model implemented
- [ ] Weather conditions reduce/increase visitor count
- [ ] Revenue adjusted before final calculation

---

### Issue #9: Guest mode
**Labels**: `enhancement`, `sprint-3`  
**Milestone**: Sprint 3  
**Description**:  
As a user, I want to access the platform without logging in, so that I can try out the features before registering.

**Acceptance Criteria**:
- [ ] Guest users can use analysis features
- [ ] Analysis data stored in localStorage
- [ ] Guest users see limited UI (no logout button)
- [ ] Smooth upgrade path from guest to registered user

---

### Issue #10: Production deployment on Railway
**Labels**: `infrastructure`, `sprint-3`  
**Milestone**: Sprint 3  
**Description**:  
As a user, I want the backend deployed and accessible in production, so that the platform can be used in a real environment.

**Acceptance Criteria**:
- [ ] Backend deployed on Railway
- [ ] CORS properly configured for production origins
- [ ] No 502 errors on startup
- [ ] Rate limiting works without blocking CORS preflight

---

### Issue #11: Excel export
**Labels**: `enhancement`, `sprint-4`  
**Milestone**: Sprint 4  
**Description**:  
As a user, I want to export analysis results to Excel with proper Rupiah formatting and multiple sheets, so that I can share reports with stakeholders.

**Acceptance Criteria**:
- [ ] Excel file generated with analysis results
- [ ] Rupiah currency properly formatted
- [ ] Multiple sheets for different data sections
- [ ] Download triggered from dashboard

---

### Issue #12: AI Advisor chatbot
**Labels**: `enhancement`, `sprint-4`  
**Milestone**: Sprint 4  
**Description**:  
As a user, I want to ask the AI Advisor about ROI, competition, and business pivots, so that I can get real-time strategic advice.

**Acceptance Criteria**:
- [ ] Conversational AI interface
- [ ] Conversation history persisted
- [ ] Context-aware responses based on analysis data
- [ ] Works for both guest and authenticated users

---

## Open Issues (Backlog)

### Issue #13: Side-by-side location comparison
**Labels**: `enhancement`, `backlog`  
**Description**:  
As a user, I want to compare multiple locations side-by-side, so that I can choose the best location.

---

### Issue #14: CI/CD pipeline with GitHub Actions
**Labels**: `infrastructure`, `backlog`  
**Description**:  
As a developer, I want a CI/CD pipeline with GitHub Actions, so that deployment is automated and tested.

---

### Issue #15: Admin usage analytics
**Labels**: `enhancement`, `backlog`  
**Description**:  
As an admin, I want to see platform usage analytics, so that I can understand user behavior.

---

## Quick Create Script (if `gh` CLI is installed later)

```bash
# Install gh CLI first: https://cli.github.com/
# Then run:

gh label create sprint-1 --color 0E8A16
gh label create sprint-2 --color 1D76DB
gh label create sprint-3 --color D93F0B
gh label create sprint-4 --color 5319E7
gh label create backlog --color FBCA04
gh label create infrastructure --color C5DEF5

gh issue create --title "Interactive map-based location analysis" --label "enhancement,sprint-1" --body "As a user, I want to analyze a business location on an interactive map."
gh issue create --title "User registration and authentication" --label "enhancement,sprint-1" --body "As a user, I want to register and log in to the platform."
gh issue create --title "Revenue projection engine" --label "enhancement,sprint-1" --body "As a user, I want to see daily, monthly, and yearly revenue projections."
gh issue create --title "Multi-currency support" --label "enhancement,sprint-1" --body "As a user, I want to choose from 50+ currencies."
gh issue create --title "Google Gemini AI map analysis" --label "enhancement,sprint-2" --body "As a user, I want the system to use Google Gemini AI to analyze map screenshots."
gh issue create --title "Firebase migration" --label "infrastructure,sprint-2" --body "As a developer, I want to migrate from Supabase to Firebase."
gh issue create --title "Probabilistic traffic model" --label "enhancement,sprint-2" --body "As a user, I want a probabilistic traffic model based on junction analysis."
gh issue create --title "Weather impact coefficient (VIC)" --label "enhancement,sprint-2" --body "As a user, I want weather impact calculated via VIC."
gh issue create --title "Guest mode" --label "enhancement,sprint-3" --body "As a user, I want to access the platform without logging in."
gh issue create --title "Production deployment on Railway" --label "infrastructure,sprint-3" --body "As a user, I want the backend deployed and accessible in production."
gh issue create --title "Excel export" --label "enhancement,sprint-4" --body "As a user, I want to export analysis results to Excel."
gh issue create --title "AI Advisor chatbot" --label "enhancement,sprint-4" --body "As a user, I want to ask the AI Advisor about ROI and strategy."
gh issue create --title "Side-by-side location comparison" --label "enhancement,backlog" --body "As a user, I want to compare multiple locations side-by-side."
gh issue create --title "CI/CD pipeline" --label "infrastructure,backlog" --body "As a developer, I want CI/CD with GitHub Actions."
gh issue create --title "Admin usage analytics" --label "enhancement,backlog" --body "As an admin, I want to see platform usage analytics."
```
