#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QSplitter, QWidget

from ..base.composite_widget import CompositeWidget


class HSplitterLayout(CompositeWidget):
    """
    動的に QSplitter を生成し、1:x の整数比率を保証するレイアウト。
    """

    def _setup_ui(self) -> None:
        """ベースとなるレイアウトと内部状態の初期化"""
        self.main_layout = QHBoxLayout(self)
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
        ウィジェットを追加します。
        stretch が (1, 整数) でない場合は (1, 2) にフォールバックします。
        """
        # バリデーションを実行して比率を確定
        self._stretch_factors = self._validate_stretch(stretch)

        if isinstance(widget_or_list, list):
            for w in widget_or_list:
                # 再帰的に単体追加メソッドを呼び出し
                self.addWidget(w, stretch=self._stretch_factors)
            return

        # 最大2個までの制限（3個目以降は無視）
        if len(self._added_widgets) >= 2:
            return

        self._added_widgets.append(widget_or_list)

        if len(self._added_widgets) == 1:
            # 1個目は直接レイアウトへ追加
            self.main_layout.addWidget(widget_or_list)
        elif len(self._added_widgets) == 2:
            # 2個目でスプリッター構造へ移行
            self._setup_splitter_connection()

    def _validate_stretch(self, stretch: object) -> tuple[int, int]:
        """
        1:x (xは正の整数) の形式を検証します。
        不適合な場合はデフォルトの (1, 2) を返します。
        """
        default = (1, 2)

        if not isinstance(stretch, tuple) or len(stretch) != 2:
            return default

        try:
            first, second = stretch
            # 1:x かつ x が整数であることを確認
            if first == 1 and isinstance(second, int) and second > 0:
                return (1, second)
        except (ValueError, TypeError):
            pass

        return default

    def _setup_splitter_connection(self) -> None:
        """QSplitter を生成し、1個目の退避と再配置を行います"""
        first_widget = self._added_widgets[0]
        second_widget = self._added_widgets[1]

        # 1個目を既存レイアウトから剥がす
        self.main_layout.removeWidget(first_widget)

        self._splitter = QSplitter(Qt.Orientation.Horizontal)
        self._splitter.addWidget(first_widget)
        self._splitter.addWidget(second_widget)

        # 比率を適用 (インデックス0と1にそれぞれ設定)
        self._splitter.setStretchFactor(0, self._stretch_factors[0])
        self._splitter.setStretchFactor(1, self._stretch_factors[1])

        self.main_layout.addWidget(self._splitter)

    def get_value(self) -> list[object]:
        """内包する CompositeWidget の値をリストで取得します"""
        return [
            w.get_value()
            for w in self._added_widgets
            if isinstance(w, CompositeWidget)
        ]

    def set_value(self, value: object) -> None:
        """値を順番に内包ウィジェットへセットします"""
        if not isinstance(value, list):
            return

        widgets = [
            w for w in self._added_widgets if isinstance(w, CompositeWidget)
        ]
        # zip を使って対応するウィジェットに値を配る
        for widget, val in zip(widgets, value):
            widget.set_value(val)
