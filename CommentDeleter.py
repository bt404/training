#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re

PATTERN_LINE = re.compile(r'//.*')
PATTERN_BLOCK = re.compile(r'/*.**/', re.S)


def counter(content):
    num_line = re.findAll(PATTERN_LINE, content)
    num_block = re.findAll(PATTERN_BLOCK, content)
    return len(num_line) + len(num_block)


def delete(content):
    content = re.sub(PATTERN_LINE, '', content)
    content = re.sub(PATTERN_BLOCK, '', content)
    return content


def clear():
    pass
