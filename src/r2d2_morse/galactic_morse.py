from typing import Dict, Optional, Tuple, List
import json
import re
from pathlib import Path


class InvalidCharacterError(Exception):
    """Raised when encountering unsupported characters during translation."""
    pass


class InvalidMorseCodeError(Exception):
    """Raised when encountering invalid Morse code patterns."""
    pass


class GalacticMorse:
    """
    R2-D2's Galactic Morse Code Translator
    
    A comprehensive bidirectional Morse code translator with Star Wars theming,
    supporting International Morse Code standards plus custom emoji mappings.
    """
    
    # Galactic Code Archive - Core Morse mappings
    _MORSE_MAP: Dict[str, str] = {
        # Letters
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..',
        
        # Numbers
        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
        '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
        
        # Punctuation
        '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
        '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
        ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
        '"': '.-..-.', '$': '...-..-', '@': '.--.-.',
        
        # Star Wars themed emoji mappings
        '⚡': '.-.-',     # Force lightning
        '🚀': '.--.',     # X-Wing fighter
        '🌟': '...',      # Death Star
        '🤖': '.-',       # R2-D2
        '⭐': '--',       # Imperial symbol
        '🔥': '..-',      # Lightsaber
        
        # Space character
        ' ': '/'
    }
    
    # Reverse mapping for Morse to text conversion
    _TEXT_MAP: Dict[str, str] = {morse: char for char, morse in _MORSE_MAP.items()}
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the Galactic Morse translator with custom mappings."""
        self.data_dir = Path(data_dir)
        self._load_custom_mappings()
    
    def _load_custom_mappings(self) -> None:
        """Load custom character mappings from Galactic Code Archive."""
        morse_file = self.data_dir / "morse_dictionary.json"
        if morse_file.exists():
            try:
                with open(morse_file, 'r', encoding='utf-8') as f:
                    custom_mappings = json.load(f)
                self._MORSE_MAP.update(custom_mappings)
                self._TEXT_MAP = {morse: char for char, morse in self._MORSE_MAP.items()}
            except Exception as e:
                print(f"[WARNING] Failed to load custom mappings: {e}")
    
    def text_to_morse(self, text: str, word_space: str = "/", char_space: str = " ") -> str:
        """
        Convert text to Morse code for Rebel transmissions.
        
        Args:
            text: Input text (A-Z, 0-9, punctuation, emojis)
            word_space: Word separator (default "/")
            char_space: Character separator (default " ")
            
        Returns:
            Morse code string
            
        Raises:
            InvalidCharacterError: For unsupported characters
            
        Example:
            >>> translator = GalacticMorse()
            >>> translator.text_to_morse("SOS")
            '... --- ...'
            >>> translator.text_to_morse("R2-D2")
            '.-. ..--- -.. ..---'
        """
        if not text:
            return ""
        
        morse_chars = []
        
        for char in text.upper():
            if char == ' ':
                morse_chars.append(word_space)
            elif char in self._MORSE_MAP:
                morse_chars.append(self._MORSE_MAP[char])
            else:
                raise InvalidCharacterError(
                    f"Imperial interference detected! Unsupported character: '{char}'"
                )
        
        return char_space.join(morse_chars)
    
    def morse_to_text(self, morse_code: str, strict: bool = False) -> str:
        """
        Decode Morse code into text for Rebel intelligence.
        
        Args:
            morse_code: Morse code string (dots, dashes, spaces)
            strict: Reject ambiguous codes if True
            
        Returns:
            Decoded text string
            
        Raises:
            InvalidMorseCodeError: For unrecognized patterns
            
        Example:
            >>> translator = GalacticMorse()
            >>> translator.morse_to_text("... --- ...")
            'SOS'
        """
        if not morse_code:
            return ""
        
        morse_code = morse_code.strip()
        words = morse_code.split('/')
        decoded_words = []
        
        for word in words:
            if not word.strip():
                decoded_words.append(' ')
                continue
                
            morse_chars = word.strip().split()
            decoded_chars = []
            
            for morse_char in morse_chars:
                if morse_char in self._TEXT_MAP:
                    decoded_chars.append(self._TEXT_MAP[morse_char])
                elif strict:
                    raise InvalidMorseCodeError(
                        f"Dark Side corruption detected! Invalid Morse pattern: '{morse_char}'"
                    )
                else:
                    decoded_chars.append('?')
            
            decoded_words.append(''.join(decoded_chars))
        
        return ' '.join(decoded_words).replace('  ', ' ').strip()
    
    def validate_morse_code(self, morse_code: str) -> Tuple[bool, str]:
        """
        Validate Morse code pattern integrity.
        
        Args:
            morse_code: Morse code string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not morse_code:
            return True, ""
        
        valid_chars = set('.- /')
        if not set(morse_code).issubset(valid_chars):
            invalid_chars = set(morse_code) - valid_chars
            return False, f"Invalid characters detected: {', '.join(invalid_chars)}"
        
        if morse_code.startswith(' ') or morse_code.endswith(' '):
            return False, "Morse code should not start or end with spaces"
        
        if '//' in morse_code:
            return False, "Double word separators not allowed"
        
        return True, ""
    
    def get_supported_characters(self) -> Dict[str, str]:
        """
        Get all supported character mappings from the Galactic Code Archive.
        
        Returns:
            Dictionary of character to Morse mappings
        """
        return self._MORSE_MAP.copy()
    
    def batch_translate(self, texts: List[str], to_morse: bool = True) -> List[Dict]:
        """
        Batch translate multiple texts for efficient Rebel operations.
        
        Args:
            texts: List of text strings to translate
            to_morse: True for text->morse, False for morse->text
            
        Returns:
            List of dictionaries with translation results
        """
        results = []
        
        for i, text in enumerate(texts):
            try:
                if to_morse:
                    translated = self.text_to_morse(text)
                    result = {
                        'index': i,
                        'input': text,
                        'output': translated,
                        'direction': 'text_to_morse',
                        'success': True,
                        'error': None
                    }
                else:
                    translated = self.morse_to_text(text)
                    result = {
                        'index': i,
                        'input': text,
                        'output': translated,
                        'direction': 'morse_to_text',
                        'success': True,
                        'error': None
                    }
            except (InvalidCharacterError, InvalidMorseCodeError) as e:
                result = {
                    'index': i,
                    'input': text,
                    'output': None,
                    'direction': 'text_to_morse' if to_morse else 'morse_to_text',
                    'success': False,
                    'error': str(e)
                }
            
            results.append(result)
        
        return results


if __name__ == "__main__":
    # Initialize the Galactic Morse translator
    r2d2 = GalacticMorse()
    
    print("🤖 R2-D2 Galactic Communicator: Ready for Transmission!")
    print("=" * 60)
    
    # Test basic functionality
    test_messages = [
        "SOS",
        "HELP ME OBI-WAN",
        "MAY THE FORCE BE WITH YOU",
        "R2-D2",
        "USE THE FORCE ⚡🚀"
    ]
    
    print("\n📡 Testing Rebel Transmissions:")
    for msg in test_messages:
        try:
            morse = r2d2.text_to_morse(msg)
            decoded = r2d2.morse_to_text(morse)
            
            print(f"\n[Original] {msg}")
            print(f"[Morse]    {morse}")
            print(f"[Decoded]  {decoded}")
            print(f"[Status]   {'✅ Success' if decoded.replace(' ', '') == msg.replace(' ', '') else '❌ Failed'}")
            
        except Exception as e:
            print(f"\n[Original] {msg}")
            print(f"[Error]    {e}")
    
    print("\n🚨 Testing Imperial Interference Detection:")
    try:
        r2d2.text_to_morse("Hello 世界!")  # Contains unsupported character
    except InvalidCharacterError as e:
        print(f"[Error Caught] {e}")
    
    print("\n🎯 All systems operational. May the Force be with you!")