from typing import TypedDict


class ASRWord(TypedDict):
    word: str
    start_ms: int
    end_ms: int


class ASRSegment(TypedDict):
    text: str
    start_ms: int
    end_ms: int
    words: list[ASRWord]


class ASRRawData(TypedDict):
    chunks: list[str]
    words: list[ASRWord]
