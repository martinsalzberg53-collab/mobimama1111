import React, { createContext, useContext, useState, useCallback, type ReactNode } from "react";
import en from "../translations/en.json";
import tw from "../translations/tw.json";
import ga from "../translations/ga.json";
import ew from "../translations/ew.json";
import ha from "../translations/ha.json";

type Translations = typeof en;

const languages: Record<string, { label: string; data: Translations }> = {
  en: { label: "English", data: en },
  tw: { label: "Twi", data: tw },
  ga: { label: "Ga", data: ga },
  ew: { label: "Ewe", data: ew },
  ha: { label: "Hausa", data: ha },
};

type LanguageContextType = {
  language: string;
  setLanguage: (code: string) => void;
  t: (path: string) => string;
  languages: Record<string, { label: string }>;
};

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

function getNestedValue(obj: any, path: string): string {
  return path.split(".").reduce((acc, key) => acc?.[key], obj) ?? path;
}

export const LanguageProvider = ({ children }: { children: ReactNode }) => {
  const [language, setLangState] = useState<string>(
    () => localStorage.getItem("mobi_language") || "en"
  );

  const setLanguage = useCallback((code: string) => {
    if (languages[code]) {
      setLangState(code);
      localStorage.setItem("mobi_language", code);
    }
  }, []);

  const t = useCallback(
    (path: string): string => {
      const data = languages[language]?.data ?? languages.en.data;
      return getNestedValue(data, path);
    },
    [language]
  );

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t, languages }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) throw new Error("useLanguage must be used inside LanguageProvider");
  return context;
};
