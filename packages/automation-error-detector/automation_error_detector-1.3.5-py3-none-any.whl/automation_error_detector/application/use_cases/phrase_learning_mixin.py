from automation_error_detector.domain.services.phrase_cache_service import (
    PhraseCacheService,
)
from automation_error_detector.shared.normalization import (
    is_valid_phrase,
)
from automation_error_detector.shared.vi_text_processor import (
    normalize_phrase_for_cache,
)


class PhraseLearningMixin:
    phrase_cache: PhraseCacheService
    phrase_purpose: str  # ERROR / SCREEN

    def _learn_phrases(self, keywords: list[str]) -> None:
        phrases: list[str] = []

        for kw in keywords:
            p = normalize_phrase_for_cache(kw)
            if is_valid_phrase(p):
                phrases.append(p)

        if not phrases:
            return

        try:
            self.phrase_cache.save(self.phrase_purpose, phrases)
        except Exception:
            pass

    async def _alearn_phrases(self, keywords: list[str]) -> None:
        phrases: list[str] = []

        for kw in keywords:
            p = normalize_phrase_for_cache(kw)
            if is_valid_phrase(p):
                phrases.append(p)

        if not phrases:
            return

        try:
            await self.phrase_cache.asave(self.phrase_purpose, phrases)
        except Exception:
            pass
