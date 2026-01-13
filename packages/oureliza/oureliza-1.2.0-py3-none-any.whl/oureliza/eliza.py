#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""ELIZA chatbot implementation."""

import re
import logging
from random import choice, randrange

from oureliza import DOCTOR_SCRIPT


class Key:
    def __init__(self, word, weight, decomps):
        self.word = word
        self.weight = weight
        self.decomps = decomps


class Decomp:
    def __init__(self, parts, save, reasmbs):
        self.parts = parts
        self.save = save
        self.reasmbs = reasmbs
        self.next_reasmb_index = 0


class Eliza:

    def __init__(self, script: str = None):
        self.logger = logging.getLogger(__name__)
        self.initials = []
        self.finals = []
        self.quits = []
        self.pres = {}
        self.posts = {}
        self.synons = {}
        self.keys = {}
        self.memory = []
        self._parse(script or DOCTOR_SCRIPT)

    def _parse(self, script: str):
        key = None
        decomp = None
        for line in script.splitlines():
            if not line.strip():
                continue

            tag, content = [part.strip() for part in line.split(':')]
            if tag == 'initial':
                self.initials.append(content)
            elif tag == 'final':
                self.finals.append(content)
            elif tag == 'quit':
                self.quits.append(content)
            elif tag == 'pre':
                parts = content.split(' ')
                self.pres[parts[0]] = parts[1:]
            elif tag == 'post':
                parts = content.split(' ')
                self.posts[parts[0]] = parts[1:]
            elif tag == 'synon':
                parts = content.split(' ')
                self.synons[parts[0]] = parts
            elif tag == 'key':
                parts = content.split(' ')
                word = parts[0]
                weight = int(parts[1]) if len(parts) > 1 else 1
                key = Key(word, weight, [])
                self.keys[word] = key
            elif tag == 'decomp':
                parts = content.split(' ')
                save = False
                if parts[0] == '$':
                    save = True
                    parts = parts[1:]
                decomp = Decomp(parts, save, [])
                key.decomps.append(decomp)
            elif tag == 'reasmb':
                parts = content.split(' ')
                decomp.reasmbs.append(parts)

    def _match_decomp_r(self, parts, words, results):
        if not parts and not words:
            return True
        if not parts or (not words and parts != ['*']):
            return False
        if parts[0] == '*':
            for index in range(len(words), -1, -1):
                results.append(words[:index])
                if self._match_decomp_r(parts[1:], words[index:], results):
                    return True
                results.pop()
            return False
        elif parts[0].startswith('@'):
            root = parts[0][1:]
            if root not in self.synons:
                raise ValueError(f'Unknown synonym root {root}')
            if words[0].lower() not in self.synons[root]:
                return False
            results.append([words[0]])
            return self._match_decomp_r(parts[1:], words[1:], results)
        elif parts[0].lower() != words[0].lower():
            return False
        else:
            return self._match_decomp_r(parts[1:], words[1:], results)

    def _match_decomp(self, parts, words):
        results = []
        if self._match_decomp_r(parts, words, results):
            return results
        return None

    def _next_reasmb(self, decomp):
        index = randrange(len(decomp.reasmbs))
        result = decomp.reasmbs[index % len(decomp.reasmbs)]
        decomp.next_reasmb_index = index + 1
        return result

    def _reassemble(self, reasmb, results):
        output = []
        for reword in reasmb:
            if not reword:
                continue
            # Handle placeholders like (1), (2), (2)?, (2)., etc.
            if reword[0] == '(' and ')' in reword:
                paren_end = reword.index(')')
                index = int(reword[1:paren_end])
                trailing = reword[paren_end + 1:]  # e.g., "?" from "(2)?"
                if index < 1 or index > len(results):
                    raise ValueError(f'Invalid result index {index}')
                insert = results[index - 1]
                for punct in [',', '.', ';']:
                    if punct in insert:
                        insert = insert[:insert.index(punct)]
                output.extend(insert)
                if trailing:
                    output.append(trailing)
            else:
                output.append(reword)
        return output

    def _sub(self, words, sub):
        output = []
        for word in words:
            word_lower = word.lower()
            if word_lower in sub:
                output.extend(sub[word_lower])
            else:
                output.append(word)
        return output

    def _match_key(self, words, key):
        for decomp in key.decomps:
            results = self._match_decomp(decomp.parts, words)
            if results is None:
                continue
            results = [self._sub(words, self.posts) for words in results]
            reasmb = self._next_reasmb(decomp)
            if reasmb[0] == 'goto':
                goto_key = reasmb[1]
                if goto_key not in self.keys:
                    raise ValueError(f'Invalid goto key {goto_key}')
                return self._match_key(words, self.keys[goto_key])
            output = self._reassemble(reasmb, results)
            if decomp.save:
                self.memory.append(output)
                continue
            return output
        return None

    def respond(self, text: str):
        if text.lower() in self.quits:
            return None

        text = re.sub(r'\s*\.+\s*', ' . ', text)
        text = re.sub(r'\s*,+\s*', ' , ', text)
        text = re.sub(r'\s*;+\s*', ' ; ', text)

        words = [w for w in text.split(' ') if w]
        words = self._sub(words, self.pres)

        keys = [self.keys[w.lower()] for w in words if w.lower() in self.keys]
        keys = sorted(keys, key=lambda k: -k.weight)

        output = None
        for key in keys:
            output = self._match_key(words, key)
            if output:
                break

        if not output:
            if self.memory:
                index = randrange(len(self.memory))
                output = self.memory.pop(index)
            else:
                output = self._next_reasmb(self.keys['xnone'].decomps[0])

        return ' '.join(output)

    def initial(self):
        return choice(self.initials)

    def final(self):
        return choice(self.finals)
