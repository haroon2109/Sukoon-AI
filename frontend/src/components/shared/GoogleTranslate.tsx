"use client";

import { useEffect } from "react";

const LANGUAGE_CODES: Record<string, string> = {
  English: "en",
  Hindi: "hi",
  Bengali: "bn",
  Kannada: "kn",
  Malayalam: "ml",
  Marathi: "mr",
  Tamil: "ta",
  Telugu: "te",
  Urdu: "ur",
};

export default function GoogleTranslate() {
  useEffect(() => {
    // 1. Get user language from localStorage
    const savedLang = localStorage.getItem("sukoon_language") || "English";
    const code = LANGUAGE_CODES[savedLang] || "en";

    // 2. Set googtrans cookie
    const cookieString = `/en/${code}`;
    document.cookie = `googtrans=${cookieString}; path=/`;
    document.cookie = `googtrans=${cookieString}; path=/; domain=${window.location.hostname}`;

    // 3. Define the init function
    // @ts-expect-error - Google Translate API is attached to window
    window.googleTranslateElementInit = () => {
      // @ts-expect-error - Google Translate API
      new window.google.translate.TranslateElement(
        {
          pageLanguage: "en",
          includedLanguages: "en,hi,bn,kn,ml,mr,ta,te,ur",
          autoDisplay: false,
        },
        "google_translate_element"
      );
    };

    // 4. Inject the script if not already present
    if (!document.getElementById("google-translate-script")) {
      const script = document.createElement("script");
      script.id = "google-translate-script";
      script.src = "//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
      script.async = true;
      document.body.appendChild(script);
    }
  }, []);

  return (
    <div id="google_translate_element" className="hidden" style={{ display: 'none' }}></div>
  );
}
