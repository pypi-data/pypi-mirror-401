__version__ = '1.0.0'

import os
import re
from collections import Counter
from typing import Dict, Any
from sudachipy import dictionary, tokenizer

_tokenizer = None

_REPLACE_MAP = {
    'ッ': '', 'ー': '',
    'ャ': 'ヤ', 'ュ': 'ユ', 'ョ': 'ヨ',
    'ァ': 'ア', 'ィ': 'イ', 'ゥ': 'ウ', 'ェ': 'エ', 'ォ': 'オ'
}
_SYMBOL_PATTERN = re.compile(r'[。、,.！!・「」｣『』\s　]')


class Dajudge(int):
    def __new__(cls, score: float, phrase: str = "", reading_length: int = 0):
        is_dajare = score >= 1.2
        instance = super().__new__(cls, is_dajare)
        instance.score = round(score, 2)
        instance.is_dajare = is_dajare
        instance.phrase = phrase
        instance.reading_length = reading_length
        return instance

    def __repr__(self):
        return str(bool(self.is_dajare))


def _get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = dictionary.Dictionary().create()
    return _tokenizer


def _normalize_reading(text: str) -> str:
    text = _SYMBOL_PATTERN.sub('', text)
    for src, dst in _REPLACE_MAP.items():
        text = text.replace(src, dst)
    return text


def _compute_details(sentence: str) -> Dict[str, Any]:
    tokens = _get_tokenizer().tokenize(sentence, tokenizer.Tokenizer.SplitMode.C)
    word_list = []
    reading_parts = []
    
    for token in tokens:
        yomi = _normalize_reading(token.reading_form())
        if not yomi:
            continue
        word_list.append({
            'yomi': yomi,
            'surface': token.surface(),
            'norm': token.normalized_form()
        })
        reading_parts.append(yomi)

    full_reading = ''.join(reading_parts)
    total_length = len(full_reading)
    
    if total_length < 3:
        return {'score': 0.0, 'phrase': "", 'len': 0}

    best_score = 0.0
    best_phrase = ""
    best_len = 0

    for n in (2, 3, 4):
        if total_length < n:
            continue
        ngrams = [full_reading[i:i + n] for i in range(total_length - n + 1)]
        
        for phrase, count in Counter(ngrams).items():
            if count <= 1:
                continue

            matched_words = [w for w in word_list if phrase in w['yomi']]
            surfaces = {w['surface'] for w in matched_words}
            norms = {w['norm'] for w in matched_words}
            
            if not surfaces:
                continue

            if len(surfaces) >= 2:
                is_derivative = any(
                    a in b or b in a for a in surfaces for b in surfaces if a != b)
                if not is_derivative and len(norms) >= 2:
                    is_derivative = any(len(os.path.commonprefix(
                        [n1, n2])) >= 3 for n1 in norms for n2 in norms if n1 != n2)
                modifier = 0.05 if is_derivative else 2.5
            else:
                modifier = 0.2

            coverage = (len(phrase) * count) / total_length
            if coverage > 0.75:
                continue

            weight = 0.6 if n == 2 else 1.3
            score = (n * count) * weight * modifier
            normalized_score = score / (total_length * 0.15)

            if normalized_score > best_score:
                best_score = normalized_score
                best_phrase = phrase
                best_length = len(phrase)

    return {'score': best_score, 'phrase': best_phrase, 'length': best_length}


def dajudge(sentence: str) -> Dajudge:
    res = _compute_details(sentence)
    return Dajudge(res['score'], res['phrase'], res['length'])