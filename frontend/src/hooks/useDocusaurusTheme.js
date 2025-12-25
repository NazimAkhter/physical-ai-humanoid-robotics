import { useState, useEffect } from 'react';

/**
 * Custom hook to access Docusaurus theme (light/dark mode)
 * Uses CSS data-theme attribute to avoid SSR issues with useColorMode
 * @returns {Object} Theme state with colorMode ('light' | 'dark')
 */
export function useDocusaurusTheme() {
  const [colorMode, setColorMode] = useState('light');

  useEffect(() => {
    // Get theme from data-theme attribute on document element
    const getTheme = () => {
      if (typeof document !== 'undefined') {
        return document.documentElement.getAttribute('data-theme') || 'light';
      }
      return 'light';
    };

    // Set initial theme
    setColorMode(getTheme());

    // Watch for theme changes
    const observer = new MutationObserver(() => {
      setColorMode(getTheme());
    });

    if (typeof document !== 'undefined') {
      observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ['data-theme']
      });
    }

    return () => observer.disconnect();
  }, []);

  return {
    colorMode  // 'light' or 'dark'
  };
}
