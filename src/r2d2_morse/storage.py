import json
from pathlib import Path
from typing import Dict, List, Optional
from .galactic_morse import GalacticMorse


class GalacticCodeArchive:
    """Manages the Galactic Code Archive for storing Morse mappings and preferences."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.morse_file = self.data_dir / "morse_dictionary.json"
        self.prefs_file = self.data_dir / "user_preferences.json"
        self.samples_file = self.data_dir / "sample_messages.json"
        
        # Initialize default mappings if not exists
        self._initialize_default_files()
    
    def _initialize_default_files(self) -> None:
        """Initialize JSON files with default data if they don't exist."""
        if not self.morse_file.exists():
            with open(self.morse_file, 'w', encoding='utf-8') as f:
                json.dump(GalacticMorse._MORSE_MAP, f, indent=2, ensure_ascii=False)
        
        if not self.prefs_file.exists():
            default_prefs = {
                "theme": "dark",
                "sound_enabled": False,
                "auto_copy": True
            }
            with open(self.prefs_file, 'w', encoding='utf-8') as f:
                json.dump(default_prefs, f, indent=2)
        
        if not self.samples_file.exists():
            default_samples = [
                {
                    "text": "SOS",
                    "morse": "... --- ...",
                    "description": "Rebel distress signal"
                },
                {
                    "text": "MAYTHEFORCE",
                    "morse": "-- .- -.-- - .... . ..-. --- .-. -.-. .",
                    "description": "Jedi blessing"
                },
                {
                    "text": "HELP ME OBI-WAN",
                    "morse": ".... . .-.. .--. / -- . / --- -... .. .-.. .- -.",
                    "description": "Leia's distress call"
                }
            ]
            with open(self.samples_file, 'w', encoding='utf-8') as f:
                json.dump(default_samples, f, indent=2, ensure_ascii=False)
    
    def load_morse_mappings(self) -> Dict[str, str]:
        """Load Morse code mappings from JSON file."""
        try:
            with open(self.morse_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Failed to load Galactic Code Archive: {e}")
    
    def save_morse_mappings(self, mappings: Dict[str, str]) -> None:
        """Save Morse code mappings to JSON file."""
        try:
            with open(self.morse_file, 'w', encoding='utf-8') as f:
                json.dump(mappings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Failed to save Galactic Code Archive: {e}")
    
    def load_user_preferences(self) -> Dict[str, any]:
        """Load user preferences from JSON file."""
        try:
            with open(self.prefs_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Failed to load user preferences: {e}")
    
    def save_user_preferences(self, preferences: Dict[str, any]) -> None:
        """Save user preferences to JSON file."""
        try:
            with open(self.prefs_file, 'w', encoding='utf-8') as f:
                json.dump(preferences, f, indent=2)
        except Exception as e:
            raise Exception(f"Failed to save user preferences: {e}")
    
    def load_sample_messages(self) -> List[Dict[str, str]]:
        """Load sample messages from JSON file."""
        try:
            with open(self.samples_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Failed to load sample messages: {e}")