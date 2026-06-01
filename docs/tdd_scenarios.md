# TDD Test Scenarios -- Finaya Project

> **Dokumen ini berisi skenario Test-Driven Development (TDD) untuk project Finaya.**
> Setiap skenario didefinisikan sebelum implementasi test, mengikuti prinsip **Red -> Green -> Refactor**.

---

## Daftar Isi

1. [Backend -- Unit Tests: Traffic Probability](#1-traffic-probability-service)
2. [Backend -- Unit Tests: Weather Probability](#2-weather-probability-service)
3. [Backend -- Unit Tests: Gemini Service (JSON Extract & Business Metrics)](#3-gemini-service-analysis)
4. [Backend -- Unit Tests: Security Manager](#4-security-manager)
5. [Backend -- Unit Tests: Custom Exceptions](#5-custom-exceptions)
6. [Backend -- Unit Tests: Pydantic Schemas](#6-pydantic-schemas)
7. [Backend -- Unit Tests: Analysis Service (CRUD)](#7-analysis-service)
8. [Backend -- Unit Tests: User Service](#8-user-service)
9. [Backend -- Integration Tests: Middleware](#9-middleware)
10. [Backend -- Integration Tests: Rate Limiter](#10-rate-limiter)
11. [Backend -- Integration Tests: API Endpoints](#11-api-endpoints)
12. [Frontend -- Unit Tests: Guest Storage](#12-guest-storage)
13. [Frontend -- Unit Tests: Security Utils](#13-security-utils)

---

## 1. Traffic Probability Service

**File:** `backend/app/services/traffic_probability.py`
**Test File:** `backend/tests/test_traffic_probability.py`

| ID | Skenario | Input | Expected Output | Tipe |
|----|----------|-------|-----------------|------|
| TP-01 | Junction type "B" (belokan) menghasilkan probabilitas 0.5 | `junction_probability("B")` | `0.5` | Unit |
| TP-02 | Junction type "P" (T-junction) menghasilkan probabilitas 1/3 | `junction_probability("P")` | `0.333...` | Unit |
| TP-03 | Junction type "JK" (jalan kecil) menghasilkan probabilitas 0.4 | `junction_probability("JK")` | `0.4` | Unit |
| TP-04 | Junction type unknown menghasilkan default probabilitas 0.8 | `junction_probability("X")` | `0.8` | Unit |
| TP-05 | Probabilistic traffic dengan multiple junctions | `probabilistic_traffic(1000, ["B", "P", "B"])` | `1000 x 0.5 x 0.333 x 0.5 = 83.33` | Unit |
| TP-06 | Traffic dengan junction list kosong, traffic tidak berubah | `probabilistic_traffic(1000, [])` | `1000.0` | Edge |
| TP-07 | Traffic dengan single junction "B" | `probabilistic_traffic(500, ["B"])` | `250.0` | Unit |
| TP-08 | Traffic awal 0 tetap 0 berapapun junction | `probabilistic_traffic(0, ["B", "P"])` | `0.0` | Edge |

---

## 2. Weather Probability Service

**File:** `backend/app/services/weather_probability.py`
**Test File:** `backend/tests/test_weather_probability.py`

| ID | Skenario | Input | Expected Output | Tipe |
|----|----------|-------|-----------------|------|
| WP-01 | WMO code 0 dipetakan ke clear | `get_wmo_weather_state(0)` | `"clear"` | Unit |
| WP-02 | WMO code 1 dipetakan ke clear | `get_wmo_weather_state(1)` | `"clear"` | Unit |
| WP-03 | WMO code 2 dipetakan ke cloudy | `get_wmo_weather_state(2)` | `"cloudy"` | Unit |
| WP-04 | WMO code 3 dipetakan ke cloudy | `get_wmo_weather_state(3)` | `"cloudy"` | Unit |
| WP-05 | WMO code 51 dipetakan ke light_rain | `get_wmo_weather_state(51)` | `"light_rain"` | Unit |
| WP-06 | WMO code 65 dipetakan ke light_rain (boundary) | `get_wmo_weather_state(65)` | `"light_rain"` | Edge |
| WP-07 | WMO code 80 dipetakan ke heavy_rain | `get_wmo_weather_state(80)` | `"heavy_rain"` | Edge |
| WP-08 | WMO code 82 dipetakan ke heavy_rain | `get_wmo_weather_state(82)` | `"heavy_rain"` | Unit |
| WP-09 | WMO code 95 dipetakan ke storm | `get_wmo_weather_state(95)` | `"storm"` | Unit |
| WP-10 | WMO code 99 dipetakan ke storm | `get_wmo_weather_state(99)` | `"storm"` | Unit |
| WP-11 | apply_weather clear menghasilkan APT x 1.0 | `apply_weather_to_apt(1000)` + mock clear | `(1000, "clear")` | Unit |
| WP-12 | apply_weather heavy_rain menghasilkan APT x 0.6 | `apply_weather_to_apt(1000)` + mock heavy_rain | `(600, "heavy_rain")` | Unit |
| WP-13 | apply_weather storm menghasilkan APT x 0.4 | `apply_weather_to_apt(1000)` + mock storm | `(400, "storm")` | Unit |
| WP-14 | apply_weather tanpa koordinat, fallback ke random | `apply_weather_to_apt(1000, None, None)` | `tuple (float, str)` | Edge |

---

## 3. Gemini Service Analysis

**File:** `backend/app/services/gemini_service_analysis.py`
**Test File:** `backend/tests/test_gemini_service.py`

| ID | Skenario | Input | Expected Output | Tipe |
|----|----------|-------|-----------------|------|
| GS-01 | Extract JSON dari plain JSON string | `'{"key": "val"}'` | `{"key": "val"}` | Unit |
| GS-02 | Extract JSON dari markdown code block | `'json {"a":1} '` | `{"a": 1}` | Unit |
| GS-03 | Extract JSON dari teks campuran | `'Blah blah {"x": 10} more text'` | `{"x": 10}` | Unit |
| GS-04 | Extract JSON dari string tanpa JSON, raise error | `'no json here'` | `ValueError` | Edge |
| GS-05 | Extract JSON invalid, raise error | `'{"broken": '` | `ValueError` / `json.JSONDecodeError` | Edge |
| GS-06 | Business metrics -- revenue calculation valid | Mocked AreaDistribution + business params | Contains `monthlyRevenue`, `yearlyRevenue`, `locationScore` | Unit |
| GS-07 | Business metrics -- low buyers, score penalty | Config sehingga buyers < 20 | `locationScore` adjusted (x 0.85) | Unit |
| GS-08 | Business metrics -- competitor "low", factor 1.0 | `competitor_density_estimate="low"` | `competitor_factor = 1.0` in scoring | Unit |
| GS-09 | Business metrics -- competitor "high", factor 0.3 | `competitor_density_estimate="high"` | `competitor_factor = 0.3` in scoring | Unit |
| GS-10 | Business metrics -- confidence "High" ketika density > 100 dan road > 0 | Valid area distribution data | `confidenceLevel == "High"` | Unit |
| GS-11 | Business metrics -- confidence "Low" ketika reasoning berisi "Fallback" | Reasoning = "Fallback: ..." | `confidenceLevel == "Low"` | Unit |
| GS-12 | Business metrics -- score capped at 9.5 | Extremely high revenue scenario | `locationScore <= 9.5` | Edge |
| GS-13 | Business metrics -- score minimum 1.0 | Extremely low revenue scenario | `locationScore >= 1.0` | Edge |

---

## 4. Security Manager

**File:** `backend/app/core/security.py`
**Test File:** `backend/tests/test_security.py`

| ID | Skenario | Input | Expected Output | Tipe |
|----|----------|-------|-----------------|------|
| SC-01 | Sanitize input menghapus karakter `<>{}$` | `"<script>alert(1)</script>"` | `"scriptalert(1)/script"` | Unit |
| SC-02 | Sanitize input string normal tetap sama | `"Hello World"` | `"Hello World"` | Unit |
| SC-03 | Sanitize input string kosong menghasilkan kosong | `""` | `""` | Edge |
| SC-04 | Validate Google API key format valid | `"AIzaXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"` | `True` | Unit |
| SC-05 | Validate Google API key format invalid | `"invalid_key"` | `False` | Unit |
| SC-06 | Validate API key non-google, selalu true | `validate_api_key_format("any", "other")` | `True` | Unit |
| SC-07 | Koordinat valid menghasilkan True | `(-6.2, 106.8)` | `True` | Unit |
| SC-08 | Latitude out of range, raise HTTPException | `(91, 0)` | `HTTPException 400` | Edge |
| SC-09 | Longitude out of range, raise HTTPException | `(0, 181)` | `HTTPException 400` | Edge |
| SC-10 | Email masking normal | `"john@gmail.com"` | `"j***@gmail.com"` | Unit |
| SC-11 | Email masking invalid format | `"invalid"` | `"invalid_email"` | Edge |

---

## 5. Custom Exceptions

**File:** `backend/app/core/exceptions.py`
**Test File:** `backend/tests/test_exceptions.py`

| ID | Skenario | Input | Expected Output | Tipe |
|----|----------|-------|-----------------|------|
| EX-01 | FinayaException default status code | `FinayaException("err")` | `status_code == 500` | Unit |
| EX-02 | AuthenticationError status code | `AuthenticationError()` | `status_code == 401` | Unit |
| EX-03 | AuthorizationError status code | `AuthorizationError()` | `status_code == 403` | Unit |
| EX-04 | ValidationError status code | `ValidationError()` | `status_code == 422` | Unit |
| EX-05 | NotFoundError status code | `NotFoundError()` | `status_code == 404` | Unit |
| EX-06 | DatabaseError status code | `DatabaseError()` | `status_code == 500` | Unit |
| EX-07 | ExternalServiceError status code | `ExternalServiceError()` | `status_code == 502` | Unit |
| EX-08 | Exception inheritance chain | Semua custom exception | `isinstance(..., FinayaException)` | Unit |
| EX-09 | Custom message tersimpan | `AuthenticationError("custom msg")` | `message == "custom msg"` | Unit |

---

## 6. Pydantic Schemas

**File:** `backend/app/schemas/schemas.py`
**Test File:** `backend/tests/test_schemas.py`

| ID | Skenario | Input | Expected Output | Tipe |
|----|----------|-------|-----------------|------|
| SM-01 | AreaDistribution valid construction | Semua field terisi | Object valid | Unit |
| SM-02 | AreaDistribution missing field, raise ValidationError | Tanpa `residential` | `ValidationError` | Edge |
| SM-03 | AnalysisCreate valid construction | Semua required fields | Object valid | Unit |
| SM-04 | AnalysisCreate optional gemini_analysis default None | Tanpa `gemini_analysis` | `gemini_analysis == None` | Unit |
| SM-05 | UserCreate membutuhkan password | Data lengkap | Object valid | Unit |
| SM-06 | FirebaseLogin membutuhkan email + token | Data lengkap | Object valid | Unit |
| SM-07 | Token schema valid | `access_token + token_type` | Object valid | Unit |

---

## 7. Analysis Service

**File:** `backend/app/services/analysis_service.py`
**Test File:** `backend/tests/test_analysis_service.py`

| ID | Skenario | Input | Expected Output | Tipe |
|----|----------|-------|-----------------|------|
| AS-01 | Create analysis sukses | Valid `AnalysisCreate` + mocked repo | `Analysis` object returned | Unit |
| AS-02 | Create analysis tanpa name, raise ValidationError | `name=""` | `ValidationError` raised | Edge |
| AS-03 | Create analysis repo gagal, raise DatabaseError | Mocked repo return None | `DatabaseError` raised | Edge |
| AS-04 | Get analysis sukses | Valid ID + mocked repo | `Analysis` object returned | Unit |
| AS-05 | Get analysis not found, return None | Unknown ID + mocked repo return None | `None` | Unit |
| AS-06 | Get user analyses empty list | Mocked repo return [] | `[]` | Unit |
| AS-07 | Delete analysis sukses | Valid ID | `True` | Unit |
| AS-08 | Delete analysis gagal, raise DatabaseError | Mocked repo raise Exception | `DatabaseError` raised | Edge |

---

## 8. User Service

**File:** `backend/app/services/user_service.py`
**Test File:** `backend/tests/test_user_service.py`

| ID | Skenario | Input | Expected Output | Tipe |
|----|----------|-------|-----------------|------|
| US-01 | Create user sukses | Valid UserCreate | `User` object returned | Unit |
| US-02 | Create user email sudah ada, raise ValidationError | Existing email | `ValidationError` raised | Edge |
| US-03 | Create user DB gagal, raise DatabaseError | Mocked repo return None | `DatabaseError` raised | Edge |
| US-04 | Authenticate dengan firebase-managed account, raise AuthenticationError | Password login on firebase account | `AuthenticationError` raised | Unit |
| US-05 | Authenticate user not found, return None | Unknown email | `None` | Unit |
| US-06 | Get user by email found | Existing email + mocked repo | `User` object returned | Unit |
| US-07 | Get user by email not found | Unknown email + mocked repo | `None` | Unit |

---

## 9. Middleware

**File:** `backend/app/core/middleware.py`
**Test File:** `backend/tests/test_middleware.py` (sudah ada, diperluas)

| ID | Skenario | Input | Expected Output | Tipe |
|----|----------|-------|-----------------|------|
| MW-01 | OPTIONS request mendapat response 200 | `OPTIONS /test` | `200` | Integration |
| MW-02 | GET request mendapat response 200 + X-Process-Time header | `GET /test` | Header exists | Integration |
| MW-03 | OPTIONS request tidak menghasilkan log entry | `OPTIONS /test` | No log for OPTIONS | Integration |

---

## 10. Rate Limiter

**File:** `backend/app/core/ratelimiter.py`
**Test File:** `backend/tests/test_ratelimiter.py` (sudah ada, diperluas)

| ID | Skenario | Input | Expected Output | Tipe |
|----|----------|-------|-----------------|------|
| RL-01 | Initialization fallback ke in-memory tanpa Redis | No Redis | `_initialized == True` | Unit |
| RL-02 | RateLimitConfig: auth path menggunakan AUTH rule | `/api/v1/auth/login` | `AUTH` config | Unit |
| RL-03 | RateLimitConfig: write operations menggunakan WRITE rule | `/api/v1/places/create` | `WRITE` config | Unit |
| RL-04 | RateLimitConfig: analysis path menggunakan ANALYSIS rule | `/api/v1/analysis/insight` | `ANALYSIS` config | Unit |
| RL-05 | RateLimitConfig: fallback menggunakan GENERAL rule | `/api/v1/health` | `GENERAL` config | Unit |

---

## 11. API Endpoints

**File:** `backend/main.py`, `backend/app/api/v1/*.py`
**Test File:** `backend/tests/test_main.py`, `backend/tests/test_analysis.py` (sudah ada)

| ID | Skenario | Input | Expected Output | Tipe |
|----|----------|-------|-----------------|------|
| API-01 | Health check mendapat 200 healthy | `GET /health` | `{"status": "healthy"}` | Integration |
| API-02 | Root endpoint mendapat 200 welcome | `GET /` | `{"message": "Welcome to Finaya API"}` | Integration |
| API-03 | Analyze endpoint mendapat 200 + metrics (mocked) | `POST /api/v1/analysis/analyze` | `success: true, metrics, area_distribution` | Integration |
| API-04 | Calculate endpoint mendapat 200 + analysis_id (mocked) | `POST /api/v1/analysis/calculate` | `success: true, analysis_id` | Integration |
| API-05 | Get analysis not found mendapat 404 | `GET /api/v1/analysis/unknown_id` | `404` | Integration |
| API-06 | Get user analyses empty mendapat 200 [] | `GET /api/v1/analysis/` | `[]` | Integration |

---

## 12. Guest Storage (Frontend)

**File:** `frontend/src/utils/guestStorage.js`
**Test File:** `frontend/src/utils/__tests__/guestStorage.test.js`

| ID | Skenario | Input | Expected Output | Tipe |
|----|----------|-------|-----------------|------|
| FE-GS-01 | Save guest analysis mengembalikan object dengan ID | Valid data | Object dengan `id` yang dimulai `guest_` | Unit |
| FE-GS-02 | Get guest analyses dari storage kosong | Empty localStorage | `[]` | Unit |
| FE-GS-03 | Save + Get, data tersimpan benar | Save lalu Get | Array berisi 1 item | Unit |
| FE-GS-04 | Save melebihi limit (10), trim ke 10 | Save 12 items | `length === 10` | Edge |
| FE-GS-05 | Delete guest analysis by ID | Save lalu Delete | `length === 0` | Unit |
| FE-GS-06 | Clear all guest analyses | Save beberapa lalu Clear | `[]` | Unit |
| FE-GS-07 | hasGuestAnalyses mengembalikan false jika kosong | Empty storage | `false` | Unit |
| FE-GS-08 | hasGuestAnalyses mengembalikan true jika ada data | After save | `true` | Unit |
| FE-GS-09 | getGuestAnalysesCount mengembalikan jumlah benar | Save 3 items | `3` | Unit |
| FE-GS-10 | getGuestAnalysisById, item ditemukan | Save lalu get by ID | Object matching | Unit |
| FE-GS-11 | getGuestAnalysisById, item tidak ditemukan | Unknown ID | `null` | Edge |

---

## 13. Security Utils (Frontend)

**File:** `frontend/src/utils/security.js`
**Test File:** `frontend/src/utils/__tests__/security.test.js`

| ID | Skenario | Input | Expected Output | Tipe |
|----|----------|-------|-----------------|------|
| FE-SC-01 | Relative URL valid, return true | `"/dashboard"` | `true` | Unit |
| FE-SC-02 | Protocol-relative URL (`//evil.com`), return false | `"//evil.com"` | `false` | Unit |
| FE-SC-03 | Allowed domain, return true | `"http://localhost/path"` | `true` | Unit |
| FE-SC-04 | Disallowed domain, return false | `"https://evil.com/path"` | `false` | Unit |
| FE-SC-05 | Null/undefined input, return false | `null` | `false` | Edge |
| FE-SC-06 | Empty string, return false | `""` | `false` | Edge |
| FE-SC-07 | Finaya domain, return true | `"https://finaya.app/dashboard"` | `true` | Unit |

---

## Summary

| Kategori | Jumlah Test Case |
|----------|:----------------:|
| Traffic Probability | 8 |
| Weather Probability | 14 |
| Gemini Service | 13 |
| Security Manager | 11 |
| Custom Exceptions | 9 |
| Pydantic Schemas | 7 |
| Analysis Service | 8 |
| User Service | 7 |
| Middleware | 3 |
| Rate Limiter | 5 |
| API Endpoints | 6 |
| Frontend Guest Storage | 11 |
| Frontend Security | 7 |
| **TOTAL** | **109** |

---

> **Catatan TDD:**
> 1. **Red** -- Tulis test terlebih dahulu (skenario di atas)
> 2. **Green** -- Implementasi minimal untuk pass
> 3. **Refactor** -- Perbaiki code quality sambil memastikan test tetap green
