/**
 * TDD Tests: Guest Storage Utility
 * Scenarios: FE-GS-01 through FE-GS-11
 */
import { describe, it, expect, beforeEach, vi } from 'vitest';

// Mock localStorage before imports
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: vi.fn((key) => store[key] || null),
    setItem: vi.fn((key, value) => { store[key] = value; }),
    removeItem: vi.fn((key) => { delete store[key]; }),
    clear: vi.fn(() => { store = {}; }),
    get _store() { return store; },
  };
})();

Object.defineProperty(globalThis, 'localStorage', { value: localStorageMock });

import {
  saveGuestAnalysis,
  getGuestAnalyses,
  getGuestAnalysisById,
  deleteGuestAnalysis,
  clearGuestAnalyses,
  hasGuestAnalyses,
  getGuestAnalysesCount,
} from '../guestStorage.js';

describe('Guest Storage Utility', () => {
  beforeEach(() => {
    localStorageMock.clear();
    vi.clearAllMocks();
  });

  it('FE-GS-01: saveGuestAnalysis returns object with guest_ ID', () => {
    const result = saveGuestAnalysis({ name: 'Test', location: 'Jakarta' });
    expect(result).toBeTruthy();
    expect(result.id).toMatch(/^guest_/);
    expect(result.isGuest).toBe(true);
    expect(result.created_at).toBeDefined();
  });

  it('FE-GS-02: getGuestAnalyses from empty storage returns []', () => {
    const result = getGuestAnalyses();
    expect(result).toEqual([]);
  });

  it('FE-GS-03: save then get returns saved data', () => {
    saveGuestAnalysis({ name: 'Test', location: 'Jakarta' });
    const result = getGuestAnalyses();
    expect(result).toHaveLength(1);
    expect(result[0].name).toBe('Test');
  });

  it('FE-GS-04: save exceeding limit (10) trims to 10', () => {
    for (let i = 0; i < 12; i++) {
      saveGuestAnalysis({ name: `Test ${i}`, location: 'Jakarta' });
    }
    const result = getGuestAnalyses();
    expect(result).toHaveLength(10);
  });

  it('FE-GS-05: deleteGuestAnalysis removes item by ID', () => {
    const saved = saveGuestAnalysis({ name: 'ToDelete', location: 'Jakarta' });
    expect(getGuestAnalyses()).toHaveLength(1);
    const deleted = deleteGuestAnalysis(saved.id);
    expect(deleted).toBe(true);
    expect(getGuestAnalyses()).toHaveLength(0);
  });

  it('FE-GS-06: clearGuestAnalyses removes all', () => {
    saveGuestAnalysis({ name: 'A', location: 'Jakarta' });
    saveGuestAnalysis({ name: 'B', location: 'Bandung' });
    expect(getGuestAnalyses()).toHaveLength(2);
    const cleared = clearGuestAnalyses();
    expect(cleared).toBe(true);
    expect(getGuestAnalyses()).toEqual([]);
  });

  it('FE-GS-07: hasGuestAnalyses returns false when empty', () => {
    expect(hasGuestAnalyses()).toBe(false);
  });

  it('FE-GS-08: hasGuestAnalyses returns true after save', () => {
    saveGuestAnalysis({ name: 'Test', location: 'Jakarta' });
    expect(hasGuestAnalyses()).toBe(true);
  });

  it('FE-GS-09: getGuestAnalysesCount returns correct count', () => {
    saveGuestAnalysis({ name: 'A', location: 'Jakarta' });
    saveGuestAnalysis({ name: 'B', location: 'Jakarta' });
    saveGuestAnalysis({ name: 'C', location: 'Jakarta' });
    expect(getGuestAnalysesCount()).toBe(3);
  });

  it('FE-GS-10: getGuestAnalysisById finds existing item', () => {
    const saved = saveGuestAnalysis({ name: 'Findable', location: 'Jakarta' });
    const found = getGuestAnalysisById(saved.id);
    expect(found).toBeTruthy();
    expect(found.name).toBe('Findable');
  });

  it('FE-GS-11: getGuestAnalysisById returns null for unknown ID', () => {
    const found = getGuestAnalysisById('nonexistent_id');
    expect(found).toBeNull();
  });
});
