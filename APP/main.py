from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from ui import create_new_workspace, open_workspace

def main():
    app = QApplication([])
    main_window = QWidget()
    main_window.setWindowTitle("PyDAW Main Menu")
    main_window.setGeometry(200, 200, 600, 400)
    main_window.setWindowIcon(QIcon("icon.png"))
    
    layout = QVBoxLayout()
    layout.addWidget(QPushButton("Create Workspace", clicked=create_new_workspace))
    layout.addWidget(QPushButton("Open Workspace", clicked=open_workspace))
    
    exit_button = QPushButton("Exit")
    exit_button.clicked.connect(app.quit)
    layout.addWidget(exit_button)

    main_window.setLayout(layout)
    main_window.show()
    
    app.exec()

if __name__ == "__main__":
    main()
