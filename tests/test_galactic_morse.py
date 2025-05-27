import pytest
from hypothesis import given, strategies as st
from r2d2_morse.galactic_morse import GalacticMorse, InvalidCharacterError, InvalidMorseCodeError
from r2d2_morse.storage import GalacticCodeArchive


@pytest.fixture
def morse(tmp_path):
    """Fixture for GalacticMorse instance with temporary data directory."""
    return GalacticMorse(data_dir=str(tmp_path))


@pytest.fixture
def archive(tmp_path):
    """Fixture for GalacticCodeArchive instance with temporary data directory."""
    return GalacticCodeArchive(data_dir=str(tmp_path))


def test_text_to_morse_basic(morse):
    """Test basic text to Morse conversion."""
    assert morse.text_to_morse("SOS") == "... --- ..."
    assert morse.text_to_morse("R2-D2") == ".-. ..--- -.. ..---"
    assert morse.text_to_morse("⚡") == ".-.-"


def test_morse_to_text_basic(morse):
    """Test basic Morse to text conversion."""
    assert morse.morse_to_text("... --- ...") == "SOS"
    assert morse.morse_to_text(".-. ..--- -.. ..---") == "R2D2"
    assert morse.morse_to_text(".-.-") == "⚡"


def test_invalid_character(morse):
    """Test handling of invalid characters."""
    with pytest.raises(InvalidCharacterError, match="Unsupported character: '世'"):
        morse.text_to_morse("Hello 世界")


def test_invalid_morse_strict(morse):
    """Test strict mode for invalid Morse patterns."""
    with pytest.raises(InvalidMorseCodeError, match="Invalid Morse pattern: 'XXX'"):
        morse.morse_to_text("XXX", strict=True)


@given(st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ⚡🚀🌟🤖⭐🔥"))
def test_bijective_conversion(text):
    """Property-based test for bidirectional conversion consistency."""
    morse = GalacticMorse()
    morse_code = morse.text_to_morse(text)
    decoded = morse.morse_to_text(morse_code)
    assert decoded.replace(" ", "") == text.replace(" ", "").upper()


def test_validate_morse_code(morse):
    """Test Morse code validation."""
    assert morse.validate_morse_code("... --- ...")[0] is True
    assert morse.validate_morse_code("... --- ...")[1] == ""
    assert morse.validate_morse_code("... X ...")[0] is False
    assert "Invalid characters detected: X" in morse.validate_morse_code("... X ...")[1]
    assert morse.validate_morse_code(" // ")[0] is False
    assert "Morse code should not start or end with spaces" in morse.validate_morse_code(" // ")[1]


def test_batch_translation(morse):
    """Test batch translation functionality."""
    inputs = ["SOS", "R2-D2", "INVALID"]
    results = morse.batch_translate(inputs, to_morse=True)
    assert len(results) == 3
    assert results[0]["output"] == "... --- ..."
    assert results[1]["output"] == ".-. ..--- -.. ..---"
    assert not results[2]["success"]
    assert "Unsupported character" in results[2]["error"]


def test_storage_initialization(archive):
    """Test Galactic Code Archive initialization."""
    assert (archive.data_dir / "morse_dictionary.json").exists()
    assert (archive.data_dir / "user_preferences.json").exists()
    assert (archive.data_dir / "sample_messages.json").exists()


def test_storage_load_save_morse_mappings(archive):
    """Test loading and saving Morse mappings."""
    mappings = archive.load_morse_mappings()
    assert mappings["A"] == ".-"
    assert mappings["⚡"] == ".-.-"
    
    new_mappings = {"🧙": "...-"}  # Yoda emoji
    archive.save_morse_mappings(new_mappings)
    loaded = archive.load_morse_mappings()
    assert loaded["🧙"] == "...-"


def test_storage_load_save_preferences(archive):
    """Test loading and saving user preferences."""
    prefs = archive.load_user_preferences()
    assert prefs["theme"] == "dark"
    assert prefs["auto_copy"] is True
    
    new_prefs = {"theme": "light", "sound_enabled": True, "auto_copy": False}
    archive.save_user_preferences(new_prefs)
    loaded = archive.load_user_preferences()
    assert loaded["theme"] == "light"
    assert loaded["sound_enabled"] is True


def test_storage_load_sample_messages(archive):
    """Test loading sample messages."""
    samples = archive.load_sample_messages()
    assert len(samples) >= 3
    assert any(s["text"] == "SOS" for s in samples)
    assert any(s["text"] == "HELP ME OBI-WAN" for s in samples)