from __future__ import annotations

import os
from typing import List

from PySide6 import QtCore, QtGui, QtWidgets

from .sanity_runner import SanityStatus
from .sanity import SanityFailLevel


SANITY_STATUS_TO_COLOR = {
    SanityStatus.EXECUTION_FAIL: "#500a8c",
    SanityStatus.PASSED: "#0a8c0a",
}


SANITY_LEVEL_TO_COLOR = {
    SanityFailLevel.ERROR: "#8c0a0a",
    SanityFailLevel.WARNING: "#8c6e0a",
    SanityFailLevel.INFO: "#0059ff",
}


class MainUI(QtWidgets.QDialog):

    qmw_instance = None

    @classmethod
    def show_ui(cls):
        """
        Create new instance or show it, if it was hidden or dropped
        """
        if not cls.qmw_instance:
            cls.qmw_instance = MainUI()

        if cls.qmw_instance.isHidden():
            cls.qmw_instance.show()
        else:
            cls.qmw_instance.raise_()
            cls.qmw_instance.activateWindow()

    def __init__(self, parent=None):
        super().__init__(parent)

        # base settings for the window
        self.setWindowTitle("ELLIPSE SANITY")
        self.setMinimumSize(200, 200)
        self.resize(900, 800)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        # methods to build the UI
        self.create_widgets()
        self.create_layout()
        self.create_connection()

    def create_widgets(self):
        """
        Create widgets for main window.
        """

        self.report_view = QtWidgets.QTreeWidget()
        self.report_view.setHeaderLabels(["name", "sort_order"])
        self.report_view.setHeaderHidden(True)
        self.report_view.setColumnHidden(1, True)
        self.report_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.sanity_label = QtWidgets.QLabel("SANITY CHECK")
        self.sanity_label.setStyleSheet("font-size: 36px;")
        self.report_view.setMinimumWidth(400)
        self.expand_all_button = QtWidgets.QPushButton("Expand All")
        self.expand_all_button.setFixedSize(80, 30)
        self.collapse_all_button = QtWidgets.QPushButton("Collapse All")
        self.collapse_all_button.setFixedSize(80, 30)
        self.clear_all_button = QtWidgets.QPushButton("Clear All")
        self.clear_all_button.setFixedSize(80, 30)
        self.expand_report_view_button = QtWidgets.QPushButton("<<")
        self.expand_report_view_button.setFixedSize(30, 30)

        self.preset_dropdown = QtWidgets.QComboBox()
        self.preset_dropdown.setFixedSize(100, 30)

        self.uncheck_all_button = QtWidgets.QPushButton("Untick All")
        self.uncheck_all_button.setFixedSize(100, 30)
        self.check_all_button = QtWidgets.QPushButton("Tick All")
        self.check_all_button.setFixedSize(100, 30)
        self.run_all_checked = QtWidgets.QPushButton("Run All Ticked")
        self.run_all_checked.setFixedSize(100, 30)
        self.fix_all_checked = QtWidgets.QPushButton("Fix All Ticked")
        self.fix_all_checked.setFixedSize(100, 30)

    def create_layout(self):
        """
        Create layout for main window
        """

        main_layout = QtWidgets.QVBoxLayout(self)

        report_options_layout = QtWidgets.QHBoxLayout(self)
        report_options_layout.addSpacing(50)
        report_options_layout.addWidget(self.sanity_label)
        report_options_layout.addStretch()
        report_options_layout.addWidget(self.preset_dropdown)
        report_options_layout.addWidget(self.collapse_all_button)
        report_options_layout.addWidget(self.expand_all_button)
        report_options_layout.addWidget(self.clear_all_button)
        report_options_layout.addWidget(self.expand_report_view_button)
        main_layout.addLayout(report_options_layout)
        check_report_layout = QtWidgets.QHBoxLayout(self)

        categories_list_wdg = QtWidgets.QWidget()
        self.categories_listing_layout = QtWidgets.QVBoxLayout(categories_list_wdg)
        self.categories_listing_layout.setAlignment(QtCore.Qt.AlignTop)
        
        categories_list_scroll_area = QtWidgets.QScrollArea()
        categories_list_scroll_area.setMaximumWidth(450)
        categories_list_scroll_area.setWidgetResizable(True)
        categories_list_scroll_area.setWidget(categories_list_wdg)

        check_report_layout.addWidget(categories_list_scroll_area)
        check_report_layout.addWidget(self.report_view)

        main_layout.addLayout(check_report_layout)

        main_layout.addSpacing(10)
        run_layout = QtWidgets.QHBoxLayout(self)
        run_layout.addWidget(self.uncheck_all_button)
        run_layout.addWidget(self.check_all_button)
        run_layout.addStretch()
        run_layout.addWidget(self.run_all_checked)
        run_layout.addWidget(self.fix_all_checked)

        main_layout.addLayout(run_layout)


class MainTitle(QtWidgets.QWidget):
    def __init__(self, categorie_name, categorie_content, index, main_ui):
        super().__init__()
        
        self.categorie_name = categorie_name
        self.categorie_content = categorie_content
        self.main_ui = main_ui
        self.index = index*100

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        """
        Create widgets method
        """
        self.categorie_label = QtWidgets.QLabel(self.categorie_name)
        self.categorie_label.setStyleSheet("font-weight: bold; font-size: 24px; background-color: #737373;")
        self.categorie_label.setAlignment(QtCore.Qt.AlignCenter)
        self.categorie_label.setContentsMargins(0, 5, 0, 5)
        self.check_all_checkbox = QtWidgets.QCheckBox()

    def create_layout(self):
        """
        Create layout method
        """
        main_layout = QtWidgets.QVBoxLayout(self)

        categorie_layout = QtWidgets.QHBoxLayout(self)
        categorie_layout.addWidget(self.check_all_checkbox)
        categorie_layout.addWidget(self.categorie_label)
        main_layout.addWidget(self.categorie_label)

        self.check_listing_layout = QtWidgets.QVBoxLayout(self)
        # self.check_listing_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.addLayout(self.check_listing_layout)

    def showEvent(self, event):
        self.refresh_to_check_listing()


class ToCheckLine(QtWidgets.QWidget):
    def __init__(self, tech_name, check_content, index, parent_index, main_ui):
        super().__init__()

        self.tech_name = tech_name
        self.check_content = check_content
        self.check_state = self.check_content["default_checked"]
        self.label_state = "default"
        self.check_results = None
        self.main_ui = main_ui
        self.sort_order = parent_index + index
        self.has_been_run = False

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        """
        Create widgets method
        """
        self.check_label = QtWidgets.QLabel(self.check_content["nice_name"])
        self.check_label.setMinimumWidth(250)
        self.check_label.setContentsMargins(5, 0, 5, 0)
        self.run_button = QtWidgets.QPushButton("Run")
        self.run_button.setFixedWidth(40)
        self.fix_button = QtWidgets.QPushButton("Fix")

        if not self.check_content["resolve_func"]:
            self.fix_button.setDisabled(True)

        self.fix_button.setFixedWidth(40)
        self.check_checkbox = QtWidgets.QCheckBox()
        self.check_checkbox.setChecked(self.check_state)

    def create_layout(self):
        """
        Create layout method
        """
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addWidget(self.check_checkbox)
        main_layout.addWidget(self.check_label)
        main_layout.addStretch()
        main_layout.addWidget(self.run_button)
        main_layout.addWidget(self.fix_button)


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    wnd = MainUI()
    wnd.show_ui()
    app.exec()