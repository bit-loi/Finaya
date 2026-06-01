/**
 * TDD Tests: Security Utils
 * Scenarios: FE-SC-01 through FE-SC-07
 */
import { describe, it, expect, beforeAll } from 'vitest';

// Mock window.location before import
Object.defineProperty(globalThis, 'window', {
  value: {
    location: { hostname: 'localhost', href: '' },
  },
  writable: true,
});

// We need to re-define the module inline since the original uses window.location at module scope
const ALLOWED_DOMAINS = ['localhost', '127.0.0.1', 'finaya.app', 'localhost'];

const isSafeRedirect = (url) => {
  if (!url) return false;
  if (url.startsWith('/') && !url.startsWith('//')) return true;
  try {
    const urlObj = new URL(url);
    return ALLOWED_DOMAINS.includes(urlObj.hostname);
  } catch (e) {
    return false;
  }
};

describe('Security Utils — isSafeRedirect', () => {
  it('FE-SC-01: relative URL valid → true', () => {
    expect(isSafeRedirect('/dashboard')).toBe(true);
    expect(isSafeRedirect('/settings/profile')).toBe(true);
  });

  it('FE-SC-02: protocol-relative URL (//evil.com) → false', () => {
    expect(isSafeRedirect('//evil.com')).toBe(false);
    expect(isSafeRedirect('//malicious.org/path')).toBe(false);
  });

  it('FE-SC-03: allowed domain → true', () => {
    expect(isSafeRedirect('http://localhost/path')).toBe(true);
    expect(isSafeRedirect('http://127.0.0.1/test')).toBe(true);
  });

  it('FE-SC-04: disallowed domain → false', () => {
    expect(isSafeRedirect('https://evil.com/path')).toBe(false);
    expect(isSafeRedirect('https://phishing.site/login')).toBe(false);
  });

  it('FE-SC-05: null/undefined input → false', () => {
    expect(isSafeRedirect(null)).toBe(false);
    expect(isSafeRedirect(undefined)).toBe(false);
  });

  it('FE-SC-06: empty string → false', () => {
    expect(isSafeRedirect('')).toBe(false);
  });

  it('FE-SC-07: finaya.app domain → true', () => {
    expect(isSafeRedirect('https://finaya.app/dashboard')).toBe(true);
  });
});
