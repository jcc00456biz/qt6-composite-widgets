#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PySide6.QtCore import Signal, SignalInstance
from PySide6.QtWidgets import QLayout, QWidget


class CompositeWidget(QWidget):
    """
    複数のウィジェットを組み合わせて一つのコンポーネントを作るための基底クラス。
    値の保持、更新、通知のインターフェースを統一します。
    """

    # Pylance等の解析ツールがシグナルを属性として認識できるように型ヒントを明示
    # 実行時は Signal(object) として機能し、インスタンスでは SignalInstance 型になります
    valueChanged: SignalInstance = Signal(object)  # type: ignore

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        # UIの構築とシグナルの接続を実行
        self._setup_ui()
        self._setup_signals()

    def _setup_ui(self) -> None:
        """
        ウィジェットの配置とレイアウトの設定を行います。
        派生クラスで必ず実装してください。
        """
        raise NotImplementedError

    def _setup_signals(self) -> None:
        """
        内部ウィジェットのシグナルと、自身の値変更ロジックを接続します。
        """
        pass

    def _clear_layout(self, layout: QLayout | None) -> None:
        """レイアウト内のウィジェットを全て削除します"""
        if layout is None:
            return

        while layout.count() > 0:
            item = layout.takeAt(0)
            if item is None:
                continue

            if widget := item.widget():
                widget.setParent(None)
                widget.deleteLater()
            elif child_layout := item.layout():
                self._clear_layout(child_layout)

    def get_value(self) -> object:
        """
        ウィジェットの現在の値を返します。
        派生クラスで具体的な取得ロジックを実装してください。
        """
        raise NotImplementedError

    def set_value(self, value: object) -> None:
        """ウィジェットに値をセットします。"""
        raise NotImplementedError

    def emit_value_changed(self) -> None:
        """
        現在の値を外部へ通知します。
        内部ウィジェットの変更イベント（textChanged 等）から呼び出すことを想定しています。
        """
        # valueChanged は型ヒントにより SignalInstance として認識されます
        self.valueChanged.emit(self.get_value())
