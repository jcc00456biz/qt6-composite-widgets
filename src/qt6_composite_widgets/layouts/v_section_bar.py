#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from ..base.composite_widget import CompositeWidget
from .group_widgets import GroupWidgets


class VSectionBar(CompositeWidget):
    """見出しと区切り線で構成される垂直レイアウトコンテナ"""

    def _setup_ui(self) -> None:
        """初期レイアウトを構築します"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.section_data: list[list[GroupWidgets]] = []
        self._inner_composites: list[CompositeWidget] = []

    def add_widget(self, group_widgets: list[GroupWidgets]) -> None:
        """セクションデータ構造を追加し、UIを更新します"""
        if not isinstance(group_widgets, list):
            return
        if not all(isinstance(w, GroupWidgets) for w in group_widgets):
            return

        self.section_data.append(group_widgets)
        self.update_layout()

    def update_layout(self) -> None:
        """現在の保持データに基づいてセクションを再構築します"""
        self._clear_layout(self.main_layout)
        self._inner_composites.clear()

        for group_list in self.section_data:
            for g_widgets in group_list:
                # 1. 見出し (QLabel)
                # 翻訳が必要な場合は、ここで g_widgets.title をキーとして翻訳処理
                label = QLabel(g_widgets.title)
                label.setStyleSheet(
                    "font-weight: bold; font-size: 12px; color: #333;"
                )
                self.main_layout.addWidget(label)

                # 2. 区切り線 (QFrame)
                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setFrameShadow(QFrame.Shadow.Sunken)
                line.setStyleSheet("color: #ccc;")
                self.main_layout.addWidget(line)

                # 3. コンテンツウィジェットの追加
                for w in g_widgets.widgets:
                    self.main_layout.addWidget(w)
                    if isinstance(w, CompositeWidget):
                        self._inner_composites.append(w)

                # 4. セクション間の余白
                self.main_layout.addSpacing(15)

    def get_value(self) -> list:
        """内包する CompositeWidget の値を収集します"""
        return [w.get_value() for w in self._inner_composites]

    def set_value(self, value: object) -> None:
        """値を順番に分配します"""
        if isinstance(value, list):
            for widget, val in zip(self._inner_composites, value):
                widget.set_value(val)
