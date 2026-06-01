export const ALLOWED_DOMAINS = [
  'localhost',
  '127.0.0.1',
  'finaya.app',
  globalThis.window?.location?.hostname
].filter(Boolean);

/**
 * Validates if a URL is safe for redirection.
 * @param {string} url - The URL to validate
 * @returns {boolean} - True if safe, false otherwise
 */
export const isSafeRedirect = (url) => {
  if (!url) return false;

  // 1. Allow relative URLs (must start with / but not //)
  if (url.startsWith('/') && !url.startsWith('//')) {
    return true;
  }

  // 2. Allow absolute URLs matching allowed domains
  try {
    const urlObj = new URL(url);
    return ALLOWED_DOMAINS.includes(urlObj.hostname);
  } catch (e) {
    return false;
  }
};

/**
 * Safely redirects the user. Blocks unsafe URLs.
 * @param {string} url - Target URL
 */
export const safeRedirect = (url) => {
  if (isSafeRedirect(url)) {
    const target = new URL(url, window.location.origin);

    if (target.origin === window.location.origin) {
      window.history.pushState({}, '', `${target.pathname}${target.search}${target.hash}`);
      const event = typeof PopStateEvent === 'function' ? new PopStateEvent('popstate') : new Event('popstate');
      window.dispatchEvent(event);
      return;
    }

    const link = document.createElement('a');
    link.href = encodeURI(target.href);
    link.rel = 'noopener noreferrer';
    link.target = '_self';
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } else {
    console.warn(`Blocked unsafe redirect to: ${url}`);
    window.history.pushState({}, '', '/');
    const event = typeof PopStateEvent === 'function' ? new PopStateEvent('popstate') : new Event('popstate');
    window.dispatchEvent(event);
  }
};
