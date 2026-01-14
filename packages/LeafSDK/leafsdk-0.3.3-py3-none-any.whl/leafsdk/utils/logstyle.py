#leafsdk/core/utils/logstyle.py

class LogIcons:
    """Centralized emoji icons for consistent logging style across the SDK."""
    SUCCESS = "✅"
    WARNING = "⚠️"
    ERROR = "❌"
    INFO = "ℹ️"
    RUN = "➡️"
    PAUSE = "⏸️"
    RESUME = "▶️"
    CANCEL = "🛑"
    PUBLISH = "📤"
    RECEIVE = "📥"

    @classmethod
    def all(cls) -> dict:
        """Return all icons as a dictionary."""
        return {
            "success": cls.SUCCESS,
            "warning": cls.WARNING,
            "error": cls.ERROR,
            "info": cls.INFO,
            "run": cls.RUN,
            "pause": cls.PAUSE,
            "resume": cls.RESUME,
            "cancel": cls.CANCEL,
            "publish": cls.PUBLISH,
            "receive": cls.RECEIVE,
        }

