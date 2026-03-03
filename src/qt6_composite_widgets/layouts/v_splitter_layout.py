#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSplitter, QVBoxLayout, QWidget

from ..base.composite_widget import CompositeWidget


class VSplitterLayout(CompositeWidget):
    """
    2つのウィジェットを垂直方向に比率指定で分割配置するレイアウト。
    """

    def _setup_ui(self) -> None:
        """垂直ベースレイアウトの初期化"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self._added_widgets: list[QWidget] = []
        self._splitter: QSplitter | None = None
        self._stretch_factors: tuple[int, int] = (1, 2)

    def addWidget(
        self,
        widget_or_list: QWidget | list[QWidget],
        stretch: tuple[int, int] = (1, 2),
    ) -> None:
        """
        ウィジェットを垂直方向に追加します。
        2個目の追加時に QSplitter (Vertical) を生成します。
        """
        self._stretch_factors = self._validate_stretch(stretch)

        if isinstance(widget_or_list, list):
            for w in widget_or_list:
                self.addWidget(w, stretch=self._stretch_factors)
            return

        if len(self._added_widgets) >= 2:
            return

        self._added_widgets.append(widget_or_list)

        if len(self._added_widgets) == 1:
            self.main_layout.addWidget(widget_or_list)
        elif len(self._added_widgets) == 2:
            self._setup_splitter_connection()

    def _validate_stretch(self, stretch: object) -> tuple[int, int]:
        """1:x の比率バリデーション"""
        default = (1, 2)
        if not isinstance(stretch, tuple) or len(stretch) != 2:
            return default

        try:
            first, second = stretch
            if first == 1 and isinstance(second, int) and second > 0:
                return (1, second)
        except (ValueError, TypeError):
            pass
        return default

    def _setup_splitter_connection(self) -> None:
        """垂直スプリッターの構築"""
        first_widget = self._added_widgets[0]
        second_widget = self._added_widgets[1]

        self.main_layout.removeWidget(first_widget)

        # Orientation を Vertical に設定
        self._splitter = QSplitter(Qt.Orientation.Vertical)
        self._splitter.addWidget(first_widget)
        self._splitter.addWidget(second_widget)

        # 比率を反映
        self._splitter.setStretchFactor(0, self._stretch_factors[0])
        self._splitter.setStretchFactor(1, self._stretch_factors[1])

        self.main_layout.addWidget(self._splitter)

    def get_value(self) -> list[object]:
        """内包ウィジェットの値をリストで返却"""
        return [
            w.get_value()
            for w in self._added_widgets
            if isinstance(w, CompositeWidget)
        ]

    def set_value(self, value: object) -> None:
        """
        値をセットします。
        基底クラスとの互換性のため引数名を value とし、内部でリストとして扱います。
        """
        if not isinstance(value, list):
            return

        widgets = [
            w for w in self._added_widgets if isinstance(w, CompositeWidget)
        ]
        for widget, val in zip(widgets, value):
            widget.set_value(val)
