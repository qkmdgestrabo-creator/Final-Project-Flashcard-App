from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton

class AllCards(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("<h1>All Cards</h1>")
        
        
        # Buttons
        button_layout = QVBoxLayout()
     

        
        layout.addWidget(title)
