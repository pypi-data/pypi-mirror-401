import re
from typing import Optional, Set
import unicodedata

from automation_error_detector.domain.services.phrase_cache_service import (
    PhraseCacheService,
)


def remove_vietnamese_tone(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.replace("đ", "d").replace("Đ", "D")


def normalize_vi(text: str) -> str:
    text = text.lower()
    text = remove_vietnamese_tone(text)
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


STOPWORDS_VI = {
    "da",
    "dang",
    "se",
    "can",
    "vui",
    "long",
    "hay",
    "va",
    "la",
    "bi",
    "khi",
    "neu",
    "lai",
}


def extract_keywords_vi(
    text: str,
    purpose: str,
    phrase_cache: Optional[PhraseCacheService] = None,
) -> list[str]:
    text = normalize_vi(text)

    keywords: set[str] = set()

    # =========================
    # AUTH SIGNALS (login)
    # =========================
    AUTH_PHRASES = [
        "dang nhap",
        "phai dang nhap",
        "can dang nhap",
        "tao tai khoan",
        "mat khau",
        "email",
        "dien thoai",
        "dat gioi han tai",
    ]

    # =========================
    # BLOCK SIGNALS (permission)
    # =========================
    BLOCK_PHRASES = [
        "khong xem duoc",
        "khong hien thi",
        "bi han che",
        "theo yeu cau",
        "noi dung nay",
        "khong the xem",
    ]
    dynamic_phrases: Set[str] = set()

    # =========================
    # LOAD DYNAMIC PHRASES (optional)
    # =========================
    if phrase_cache:
        try:
            dynamic_phrases |= phrase_cache.load(purpose)
        except Exception:
            # Phrase cache is best-effort, never break detection
            pass

    all_phrases = list(dynamic_phrases) + AUTH_PHRASES + BLOCK_PHRASES
    # 1️⃣ Match PHRASES (highest priority)
    for phrase in all_phrases:
        if phrase in text:
            keywords.add(phrase)

    # 2️⃣ Fallback single-word signals (VERY limited)
    words = text.split()
    for w in words:
        if w in {"dang", "nhap", "mat", "khau"}:
            keywords.add("dang nhap")
        elif w in {"han", "che"}:
            keywords.add("bi han che")

    # 3️⃣ Safety fallback (ensure >= 2 keywords)
    if len(keywords) < 2:
        keywords.add("generic")
        keywords.add("screen")

    return sorted(keywords)


def normalize_phrase_for_cache(phrase: str) -> str:
    """
    Normalize phrase before saving into phrase cache.
    - Vietnamese: remove tone
    - English: lowercase + cleanup
    """
    phrase = phrase.strip().lower()

    # Nếu có ký tự unicode > ASCII → coi là tiếng Việt
    if any(ord(c) > 127 for c in phrase):
        phrase = normalize_vi(phrase)
    else:
        # English / ascii
        phrase = re.sub(r"[^a-z0-9 ]", " ", phrase)
        phrase = re.sub(r"\s+", " ", phrase).strip()

    return phrase
