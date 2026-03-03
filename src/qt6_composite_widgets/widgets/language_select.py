#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel

# 基底クラスをインポート
from ..base.composite_widget import CompositeWidget


class LanguageSelectorLanguage(Enum):
    JA = "ja"  # 日本語
    EN = "en"  # 英語
    DE = "de"  # ドイツ語
    IT = "it"  # イタリア語
    FR = "fr"  # フランス語


@dataclass
class LanguageSelectorData:
    # 言語選択（デフォルトは日本語）
    select_language: LanguageSelectorLanguage = LanguageSelectorLanguage.JA

    # ラベル定義
    label: dict[LanguageSelectorLanguage, str] = field(
        default_factory=lambda: {
            LanguageSelectorLanguage.JA: "言語:",
            LanguageSelectorLanguage.EN: "Language:",
            LanguageSelectorLanguage.DE: "Sprache:",
            LanguageSelectorLanguage.IT: "Lingua:",
            LanguageSelectorLanguage.FR: "Langue:",
        }
    )

    # コンボボックスアイテム定義
    combo_box_item: dict[LanguageSelectorLanguage, list[str]] = field(
        default_factory=lambda: {
            LanguageSelectorLanguage.JA: [
                "英語",
                "日本語",
                "ドイツ語",
                "イタリア語",
                "フランス語",
            ],
            LanguageSelectorLanguage.EN: [
                "English",
                "Japanese",
                "German",
                "Italian",
                "French",
            ],
            LanguageSelectorLanguage.DE: [
                "Englisch",
                "Japanisch",
                "Deutsch",
                "Italienisch",
                "Französisch",
            ],
            LanguageSelectorLanguage.IT: [
                "Inglese",
                "Giapponese",
                "Tedesco",
                "Italiano",
                "Francese",
            ],
            LanguageSelectorLanguage.FR: [
                "Anglais",
                "Japonais",
                "Allemand",
                "Italien",
                "Français",
            ],
        }
    )

    def get_label(self) -> str:
        return self.label[self.select_language]

    def get_combo_items(self) -> list[str]:
        return self.combo_box_item[self.select_language]


class LanguageSelector(CompositeWidget):
    """言語を選択するためのコンポジットウィジェット"""

    def _setup_ui(self) -> None:
        """初期UIの構築とデータ同期を行います"""
        # データクラスのインスタンス化（デフォルト値が注入される）
        self._lang_selector_data = LanguageSelectorData()

        # ウィジェット初期化
        self.label = QLabel(self._lang_selector_data.get_label())
        self.combo = QComboBox()

        # アイテムの追加と初期インデックスの同期
        self._refresh_combo_contents()
        self._sync_combo_to_data()

        # レイアウト構築
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        layout.addWidget(self.combo, 1)

        # 最後に接続することで、初期設定時のシグナル発火を抑制
        self.combo.currentIndexChanged.connect(self.emit_value_changed)

    def _refresh_combo_contents(self) -> None:
        """データクラスからコンボボックスのアイテムリストを更新します"""
        self.combo.clear()
        self.combo.addItems(self._lang_selector_data.get_combo_items())

    def _sync_combo_to_data(self) -> None:
        """データクラスの現在の設定に合わせてコンボボックスのインデックスを合わせます"""
        lang_type = self._lang_selector_data.select_language
        # 該当する言語の表示用文字列を取得（例: LanguageSelectorLanguage.JA なら「日本語」）
        # 各言語リストの並び順が固定（EN=0, JA=1...）であることを前提とした安全な取得
        target_text = self._lang_selector_data.combo_box_item[lang_type][1]

        index = self.combo.findText(target_text)
        if index >= 0:
            self.combo.setCurrentIndex(index)

    def _update_ui(self) -> None:
        """内部データを UI 表示に反映させます"""
        self.label.blockSignals(True)
        self.combo.blockSignals(True)

        # ラベル更新
        self.label.setText(self._lang_selector_data.get_label())

        # コンボボックス更新
        self._refresh_combo_contents()
        self._sync_combo_to_data()

        self.combo.blockSignals(False)
        self.label.blockSignals(False)

    def select_language(
        self, select_language: LanguageSelectorLanguage
    ) -> bool:
        """外部から特定の言語コードを指定して変更します"""
        if not isinstance(select_language, LanguageSelectorLanguage):
            return False
        if self._lang_selector_data.select_language == select_language:
            return False

        self._lang_selector_data.select_language = select_language
        self._update_ui()
        return True

    def change_languages_data(
        self, language_selector_data: LanguageSelectorData
    ) -> bool:
        """データクラス自体を差し替えて UI を更新します"""
        if not isinstance(language_selector_data, LanguageSelectorData):
            return False

        self._lang_selector_data = language_selector_data
        self._update_ui()
        return True

    def get_value(self) -> object:
        """Pylance警告対策: 戻り値を object に設定"""
        return self.combo.currentText()

    def set_value(self, value: object) -> None:
        """Pylance警告対策: 引数を object に設定"""
        index = self.combo.findText(str(value))
        if index >= 0:
            self.combo.setCurrentIndex(index)
