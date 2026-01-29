"""Internationalization support for Entropic Core."""

import json
import logging
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class Translator:
    """Translation manager."""

    def __init__(self, language: str = "en"):
        self.language = language
        self.translations: Dict[str, Dict[str, str]] = {}
        self.fallback_language = "en"
        self.logger = logging.getLogger("i18n.translator")

        # Load translations
        self._load_translations()

    def _load_translations(self) -> None:
        """Load translation files."""
        translations_dir = os.path.join(os.path.dirname(__file__), "locales")

        if not os.path.exists(translations_dir):
            self._initialize_default_translations()
            return

        for file in os.listdir(translations_dir):
            if file.endswith(".json"):
                lang_code = file[:-5]  # Remove .json
                file_path = os.path.join(translations_dir, file)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        self.translations[lang_code] = json.load(f)
                    self.logger.info(f"Loaded translations for: {lang_code}")
                except Exception as e:
                    self.logger.error(
                        f"Error loading translations for {lang_code}: {e}"
                    )

    def _initialize_default_translations(self) -> None:
        """Initialize default English translations."""
        self.translations["en"] = {
            # Status messages
            "status.optimal": "System in optimal state",
            "status.high_entropy": "High entropy detected",
            "status.low_entropy": "Low entropy detected",
            "status.stable": "System stable",
            "status.unstable": "System unstable",
            # Actions
            "action.reduce_chaos": "Reducing system chaos",
            "action.increase_chaos": "Increasing innovation",
            "action.maintain": "Maintaining homeostasis",
            # Alerts
            "alert.entropy_spike": "Entropy spike detected: {value:.2f}",
            "alert.system_collapse": "System collapse imminent",
            "alert.attack_detected": "Potential attack detected: {type}",
            # Dashboard
            "dashboard.title": "Entropic Core Dashboard",
            "dashboard.current_entropy": "Current Entropy",
            "dashboard.agents_count": "Active Agents",
            "dashboard.status": "System Status",
            "dashboard.alerts": "Alerts",
            # Reports
            "report.daily_title": "Daily Entropy Report - {date}",
            "report.system_health": "System Health",
            "report.recommendations": "Recommendations",
            "report.events": "Notable Events",
            # Errors
            "error.measurement_failed": "Entropy measurement failed",
            "error.regulation_failed": "Regulation action failed",
            "error.plugin_error": "Plugin error: {plugin}",
        }

        # Spanish translations
        self.translations["es"] = {
            "status.optimal": "Sistema en estado óptimo",
            "status.high_entropy": "Alta entropía detectada",
            "status.low_entropy": "Baja entropía detectada",
            "status.stable": "Sistema estable",
            "status.unstable": "Sistema inestable",
            "action.reduce_chaos": "Reduciendo caos del sistema",
            "action.increase_chaos": "Aumentando innovación",
            "action.maintain": "Manteniendo homeostasis",
            "alert.entropy_spike": "Pico de entropía detectado: {value:.2f}",
            "alert.system_collapse": "Colapso del sistema inminente",
            "alert.attack_detected": "Ataque potencial detectado: {type}",
            "dashboard.title": "Panel de Entropic Core",
            "dashboard.current_entropy": "Entropía Actual",
            "dashboard.agents_count": "Agentes Activos",
            "dashboard.status": "Estado del Sistema",
            "dashboard.alerts": "Alertas",
            "report.daily_title": "Reporte Diario de Entropía - {date}",
            "report.system_health": "Salud del Sistema",
            "report.recommendations": "Recomendaciones",
            "report.events": "Eventos Notables",
            "error.measurement_failed": "Falló la medición de entropía",
            "error.regulation_failed": "Falló la acción de regulación",
            "error.plugin_error": "Error de plugin: {plugin}",
        }

        # Japanese translations
        self.translations["ja"] = {
            "status.optimal": "システムは最適な状態です",
            "status.high_entropy": "高エントロピーを検出",
            "status.low_entropy": "低エントロピーを検出",
            "status.stable": "システム安定",
            "status.unstable": "システム不安定",
            "action.reduce_chaos": "システムの混乱を削減",
            "action.increase_chaos": "イノベーションを増加",
            "action.maintain": "ホメオスタシスを維持",
            "alert.entropy_spike": "エントロピースパイク検出: {value:.2f}",
            "alert.system_collapse": "システム崩壊が差し迫っています",
            "alert.attack_detected": "潜在的な攻撃を検出: {type}",
            "dashboard.title": "Entropic Core ダッシュボード",
            "dashboard.current_entropy": "現在のエントロピー",
            "dashboard.agents_count": "アクティブなエージェント",
            "dashboard.status": "システム状態",
            "dashboard.alerts": "アラート",
        }

    def translate(self, key: str, **kwargs) -> str:
        """Translate a key to current language."""
        # Try current language
        if self.language in self.translations:
            if key in self.translations[self.language]:
                text = self.translations[self.language][key]
                return text.format(**kwargs) if kwargs else text

        # Fallback to English
        if self.fallback_language in self.translations:
            if key in self.translations[self.fallback_language]:
                text = self.translations[self.fallback_language][key]
                return text.format(**kwargs) if kwargs else text

        # Return key if no translation found
        return key

    def set_language(self, language: str) -> None:
        """Change current language."""
        if language in self.translations:
            self.language = language
            self.logger.info(f"Language changed to: {language}")
        else:
            self.logger.warning(f"Language not available: {language}")

    def get_available_languages(self) -> list:
        """Get list of available languages."""
        return list(self.translations.keys())


# Global translator instance
_translator: Optional[Translator] = None


def get_translator(language: Optional[str] = None) -> Translator:
    """Get or create global translator instance."""
    global _translator

    if _translator is None:
        _translator = Translator(language or "en")
    elif language:
        _translator.set_language(language)

    return _translator


def set_language(language: str) -> None:
    """Set global language."""
    translator = get_translator()
    translator.set_language(language)


# Convenience function
def t(key: str, **kwargs) -> str:
    """Quick translation function."""
    return get_translator().translate(key, **kwargs)
