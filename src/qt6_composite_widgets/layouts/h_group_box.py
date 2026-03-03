#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QLayout, QVBoxLayout

from ..base.composite_widget import CompositeWidget
from .group_widgets import GroupWidgets, LayoutDirection


class HGroupBox(CompositeWidget):
    """内部に動的な QGroupBox 群を生成・管理する複合ウィジェット"""

    def _setup_ui(self) -> None:
        """初期レイアウトを構築します"""
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.group_widgets: list[list[GroupWidgets]] = []
        self._inner_composites: list[CompositeWidget] = []

    def add_widget(self, group_widgets: list[GroupWidgets]) -> None:
        """データ構造を追加し、UIを更新します"""
        if not isinstance(group_widgets, list):
            return
        if not all(isinstance(w, GroupWidgets) for w in group_widgets):
            return

        self.group_widgets.append(group_widgets)
        self.update_layout()

    def update_layout(self) -> None:
        """現在の保持データに基づいてレイアウトを再構築します"""
        self._clear_layout(self.main_layout)
        self._inner_composites.clear()

        for group_list in self.group_widgets:
            for g_widgets in group_list:
                group = QGroupBox(g_widgets.title)

                # layout_cls に「QLayout の型」であることを明示
                layout_cls: type[QLayout] = (
                    QHBoxLayout
                    if g_widgets.direction == LayoutDirection.HORIZONTAL
                    else QVBoxLayout
                )

                group_layout = layout_cls(group)
                group_layout.setContentsMargins(10, 10, 10, 10)
                group_layout.setSpacing(10)

                for w in g_widgets.widgets:
                    group_layout.addWidget(w)
                    if isinstance(w, CompositeWidget):
                        self._inner_composites.append(w)

                self.main_layout.addWidget(group)

        # 余白調整
        self.main_layout.addStretch()

    def get_value(self) -> list:
        """内包する全 CompositeWidget の値を収集します"""
        return [w.get_value() for w in self._inner_composites]

    def set_value(self, value: object) -> None:
        """値を順番に分配します"""
        # 実行時に list であることを確認する
        if isinstance(value, list):
            for widget, val in zip(self._inner_composites, value):
                widget.set_value(val)
