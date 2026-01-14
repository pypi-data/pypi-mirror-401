from dataclasses import dataclass
from typing import Optional

@dataclass
class MToken:
    text: str
    tag: str
    whitespace: str
    phonemes: Optional[str] = None
    start_ts: Optional[float] = None
    end_ts: Optional[float] = None

    class Underscore(dict):
        def __getattr__(self, key):
            return self.get(key)

        def __setattr__(self, key, value):
            self[key] = value

    _: Optional[Underscore] = None
