/**
 * useLanguageArray — Operator-configured active languages for this deployment.
 *
 * Stored in localStorage as 'eve-lang-array'. Default: [current UI language].
 * The announcement system scopes NLLB translations and Kokoro TTS to this array
 * instead of crawling all 41 NLLB locales.
 *
 * Usage:
 *   const { langs, setLangs, AVAILABLE_LANGS } = useLanguageArray();
 */
import { useState, useCallback } from 'react';

/** All NLLB-supported locales with human-readable labels */
export const AVAILABLE_LANGS: { code: string; label: string }[] = [
    { code: 'en', label: 'English' },
    { code: 'am', label: 'Amharic' },
    { code: 'ar', label: 'Arabic' },
    { code: 'bn', label: 'Bengali' },
    { code: 'de', label: 'German' },
    { code: 'es', label: 'Spanish' },
    { code: 'fa', label: 'Farsi' },
    { code: 'fr', label: 'French' },
    { code: 'ha', label: 'Hausa' },
    { code: 'he', label: 'Hebrew' },
    { code: 'hi', label: 'Hindi' },
    { code: 'id', label: 'Indonesian' },
    { code: 'ig', label: 'Igbo' },
    { code: 'it', label: 'Italian' },
    { code: 'ja', label: 'Japanese' },
    { code: 'jw', label: 'Javanese' },
    { code: 'km', label: 'Khmer' },
    { code: 'ko', label: 'Korean' },
    { code: 'ku', label: 'Kurdish' },
    { code: 'la', label: 'Latin' },
    { code: 'mg', label: 'Malagasy' },
    { code: 'mr', label: 'Marathi' },
    { code: 'my', label: 'Burmese' },
    { code: 'nl', label: 'Dutch' },
    { code: 'pl', label: 'Polish' },
    { code: 'ps', label: 'Pashto' },
    { code: 'pt', label: 'Portuguese' },
    { code: 'ru', label: 'Russian' },
    { code: 'so', label: 'Somali' },
    { code: 'sw', label: 'Swahili' },
    { code: 'ta', label: 'Tamil' },
    { code: 'te', label: 'Telugu' },
    { code: 'th', label: 'Thai' },
    { code: 'tl', label: 'Tagalog' },
    { code: 'tr', label: 'Turkish' },
    { code: 'uk', label: 'Ukrainian' },
    { code: 'ur', label: 'Urdu' },
    { code: 'vi', label: 'Vietnamese' },
    { code: 'xh', label: 'Xhosa' },
    { code: 'yo', label: 'Yoruba' },
    { code: 'zh', label: 'Chinese' },
    { code: 'zu', label: 'Zulu' },
];

const STORAGE_KEY = 'eve-lang-array';

export function useLanguageArray() {
    const [langs, _setLangs] = useState<string[]>(() => {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            if (saved) {
                const parsed = JSON.parse(saved);
                if (Array.isArray(parsed) && parsed.length > 0) return parsed;
            }
        } catch { /* bad JSON */ }
        return [localStorage.getItem('eve-lang') || 'en'];
    });

    const setLangs = useCallback((newLangs: string[]) => {
        const unique = [...new Set(newLangs)].filter(Boolean);
        const final = unique.length > 0 ? unique : ['en'];
        localStorage.setItem(STORAGE_KEY, JSON.stringify(final));
        _setLangs(final);
    }, []);

    const toggleLang = useCallback((code: string) => {
        _setLangs(prev => {
            const next = prev.includes(code)
                ? prev.filter(l => l !== code)
                : [...prev, code];
            // Must keep at least one language
            const final = next.length > 0 ? next : ['en'];
            localStorage.setItem(STORAGE_KEY, JSON.stringify(final));
            return final;
        });
    }, []);

    return { langs, setLangs, toggleLang, AVAILABLE_LANGS };
}
