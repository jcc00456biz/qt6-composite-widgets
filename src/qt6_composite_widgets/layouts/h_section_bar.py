#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ..base.composite_widget import CompositeWidget
from .group_widgets import GroupWidgets


class HSectionBar(CompositeWidget):
    """見出しと垂直区切り線で構成される水平レイアウトコンテナ"""

    def _setup_ui(self) -> None:
        """初期レイアウトを構築します"""
        # メインは水平レイアウト
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)
        # 左詰めに設定
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

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
                # セクション内の要素（ラベル、線、ウィジェット）を垂直に並べるためのコンテナ
                section_container = QWidget()
                section_layout = QVBoxLayout(section_container)
                section_layout.setContentsMargins(0, 0, 0, 0)
                section_layout.setSpacing(5)

                # 1. 見出し
                label = QLabel(g_widgets.title)
                label.setStyleSheet(
                    "font-weight: bold; font-size: 12px; color: #333;"
                )
                section_layout.addWidget(label)

                # 2. 区切り線（水平バー内なので、見出しの下の短い線）
                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setFrameShadow(QFrame.Shadow.Sunken)
                line.setStyleSheet("color: #ccc;")
                section_layout.addWidget(line)

                # 3. コンテンツウィジェット
                for w in g_widgets.widgets:
                    section_layout.addWidget(w)
                    if isinstance(w, CompositeWidget):
                        self._inner_composites.append(w)

                # セクション全体をメインの水平レイアウトに追加
                self.main_layout.addWidget(section_container)

                # 4. セクション間の「垂直」な区切り線（最後の要素以外）
                # 必要に応じて追加してください。ここでは間隔（Spacing）で調整
                self.main_layout.addSpacing(20)

        # 右側にストレッチを入れて左に寄せる
        self.main_layout.addStretch()

    def get_value(self) -> list:
        """値を収集します"""
        return [w.get_value() for w in self._inner_composites]

    def set_value(self, value: object) -> None:
        """値を分配します"""
        if isinstance(value, list):
            for widget, val in zip(self._inner_composites, value):
                widget.set_value(val)
