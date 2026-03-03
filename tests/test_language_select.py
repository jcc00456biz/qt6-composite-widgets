#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from qt6_composite_widgets.widgets.language_select import (
    LanguageSelector,
    LanguageSelectorLanguage,
)


def test_initial_language_is_japanese(qtbot):
    """初期化時にデータクラスのデフォルト（日本語）が反映されているか"""
    widget = LanguageSelector()
    qtbot.addWidget(widget)  # テスト後に安全にクローズされるように登録

    # ラベルとコンボボックスの初期値をチェック
    assert widget.label.text() == "言語:"
    assert widget.combo.currentText() == "日本語"


def test_change_language_via_method(qtbot):
    """select_languageメソッドでUIが正しく更新されるか"""
    widget = LanguageSelector()
    qtbot.addWidget(widget)

    # 英語に変更
    widget.select_language(LanguageSelectorLanguage.EN)

    assert widget.label.text() == "Language:"
    # データクラスの定義に基づき、英語リスト内の「Japanese」などが含まれているか
    assert "Japanese" in [
        widget.combo.itemText(i) for i in range(widget.combo.count())
    ]


def test_value_changed_signal(qtbot):
    """ユーザーがコンボボックスを操作したときにシグナルが飛ぶか"""
    widget = LanguageSelector()
    qtbot.addWidget(widget)

    # シグナルの発火を監視
    with qtbot.waitSignal(widget.valueChanged, timeout=1000):
        # コンボボックスの選択を手動で変更
        widget.combo.setCurrentIndex(0)


def test_set_and_get_value(qtbot):
    """CompositeWidgetとしての基本機能が動作するか"""
    widget = LanguageSelector()
    qtbot.addWidget(widget)

    # 値をセット
    target_value = "英語"
    widget.set_value(target_value)

    assert widget.get_value() == target_value
    assert widget.combo.currentText() == target_value
