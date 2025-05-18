

import sys
import os
from PyQt5.QtCore import Qt, QFileInfo
from PyQt5.QtGui import QIcon, QFont, QKeySequence
from PyQt5.QtWidgets import (QApplication, QAction, QMainWindow, QTextEdit, 
                            QMessageBox, QFileDialog, QLabel, QStatusBar)

DEFAULT_TITLE = "Untitled"
APP_NAME = "HandyNote"
SUPPORTED_FORMATS = "Handy note (*.hnote);;Text File (*.txt);;All Files (*)"

class HandyNoteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.init_ui()
        self.check_arguments()
        
    def init_ui(self):
        self.setGeometry(100, 100, 600, 570)
        self.setWindowTitle(f"{APP_NAME} - {DEFAULT_TITLE}")
        self.setWindowIcon(QIcon("images/nameOrderError.png"))
        
        self.create_widgets()
        self.create_toolbar()
        self.create_status_bar()
        
    def create_widgets(self):
        self.text_edit = QTextEdit(self)
        self.text_edit.setTabStopDistance(20)
        self.text_edit.setStyleSheet("""
            background-color: white;
            color: black;
            border: 3px solid #2E2E2E;
            font-style: bold;
        """)
        self.text_edit.setFont(QFont("Segoe UI", 12))
        self.setCentralWidget(self.text_edit)
        
    def create_toolbar(self):
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.setStyleSheet("background-color: #2E2E2E;")
        toolbar.setMovable(False)

        actions = [
            ("New", "images/new.png", "Ctrl+N", self.new_note),
            ("Open", "images/open.png", "Ctrl+O", self.open_note),
            ("Save", "images/fileSave.png", "Ctrl+S", self.save_note),
            ("About", "images/help.png", None, self.show_about)
        ]
        
        for text, icon, shortcut, handler in actions:
            action = QAction(QIcon(icon), text, self)
            if shortcut:
                action.setShortcut(shortcut)
            action.triggered.connect(handler)
            toolbar.addAction(action)
            
    def create_status_bar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready", 3000)

    def check_arguments(self):
        if len(sys.argv) == 2:
            file_path = sys.argv[1]
            self.open_file(file_path)

    def new_note(self):
        if self.check_unsaved_changes():
            self.text_edit.clear()
            self.current_file = None
            self.update_window_title()

    def open_note(self):
        if self.check_unsaved_changes():
            file_name, _ = QFileDialog.getOpenFileName(
                self, "Open File", "", SUPPORTED_FORMATS)
            if file_name:
                self.open_file(file_name)

    def save_note(self):
        if self.current_file:
            self.save_file(self.current_file)
        else:
            self.save_as()

    def save_as(self):
        file_name, selected_filter = QFileDialog.getSaveFileName(
            self, "Save File", "", SUPPORTED_FORMATS)
        if file_name:
            # Add proper extension if missing
            if selected_filter == "Handy note (*.hnote)" and not file_name.endswith(".hnote"):
                file_name += ".hnote"
            elif selected_filter == "Text File (*.txt)" and not file_name.endswith(".txt"):
                file_name += ".txt"
                
            self.save_file(file_name)
            self.current_file = file_name
            self.update_window_title()

    def check_unsaved_changes(self):
        if self.text_edit.document().isModified():
            response = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Do you want to continue?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if response == QMessageBox.Save:
                self.save_note()
                return True
            elif response == QMessageBox.Discard:
                return True
            else:
                return False
        return True

    def open_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.text_edit.setText(file.read())
                self.current_file = file_path
                self.update_window_title()
                self.status.showMessage(f"Opened: {file_path}", 3000)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open file:\n{str(e)}")

    def save_file(self, file_path):
        try:
            with open(file_path, 'w') as file:
                file.write(self.text_edit.toPlainText())
                self.text_edit.document().setModified(False)
                self.status.showMessage(f"Saved: {file_path}", 3000)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not save file:\n{str(e)}")

    def update_window_title(self):
        title = DEFAULT_TITLE
        if self.current_file:
            title = QFileInfo(self.current_file).fileName()
        self.setWindowTitle(f"{APP_NAME} - {title}")

    def show_about(self):
        about_text = f"""About {APP_NAME}:
Version: 1.1
Contact: realmuhammed70@gmail.com

A simple and efficient note-taking application."""
        QMessageBox.information(self, f"About {APP_NAME}", about_text)

    def closeEvent(self, event):
        if self.check_unsaved_changes():
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = HandyNoteApp()
    window.show()
    sys.exit(app.exec_())