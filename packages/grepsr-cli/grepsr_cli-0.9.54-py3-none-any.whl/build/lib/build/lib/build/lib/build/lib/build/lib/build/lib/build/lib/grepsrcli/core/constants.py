from dataclasses import dataclass
import re
from enum import Enum

PLATFORMS = ['php','node', 'php_next']
COMMENT_BLOCK_PATTERN = re.compile(r"(\/\*\*.?\n)(.*?)(\s*\*\/\s*\n)", re.DOTALL)
CLASS_DECLARATION_PATTERN = re.compile(r'class\s+\w+\s+extends\s(\w+)\b', re.DOTALL)

@dataclass
class LanguageTypeValue:
    index: int
    name: str
    template_name: str

class LanguageType(Enum):
    PHP = ('1', 'php')
    JAVASCRIPT = ('2', 'javascript')
    TYPESCRIPT = ('3', 'typescript')
    JAVASCRIPT_ES6 = ('4', 'javascript_es6')
    TYPESCRIPT_BASE_CLASS = ('5', 'typescript_base')

    def __new__(cls, value, display_name):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        if display_name in ['javascript', 'typescript', 'javascript_es6', 'typescript_base']:
            obj._template_name = 'node'
        else:
            obj._template_name = 'php'
        return obj
    
    @property
    def template_name(self) -> str:
        return self._template_name
    
TYPESCRIPT_LANGUAGE_TYPES = [
    LanguageType.TYPESCRIPT,
    LanguageType.TYPESCRIPT_BASE_CLASS,
]

BASE_CLASS_LANGUAGES = [
    LanguageType.TYPESCRIPT_BASE_CLASS,
]