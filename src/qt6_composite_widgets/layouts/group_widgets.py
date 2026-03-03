#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from enum import IntEnum, auto

from PySide6.QtWidgets import QWidget


class LayoutDirection(IntEnum):
    """レイアウトの方向を定義するEnum"""

    HORIZONTAL = auto()
    VERTICAL = auto()


@dataclass
class GroupWidgets:
    title: str
    direction: LayoutDirection
    widgets: list[QWidget]
