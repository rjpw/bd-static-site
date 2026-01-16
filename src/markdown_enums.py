from enum import StrEnum, auto

class TextType(StrEnum):
    TEXT   = auto()
    BOLD   = auto()
    ITALIC = auto()
    CODE   = auto()
    LINK   = auto()
    IMAGE  = auto()

class BlockType(StrEnum):
    PARAGRAPH       = auto()
    HEADING         = auto()
    CODE            = auto()
    QUOTE           = auto()
    UNORDERED_LIST  = auto()
    ORDERED_LIST    = auto()
