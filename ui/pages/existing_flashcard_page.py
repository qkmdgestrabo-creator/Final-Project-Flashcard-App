from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout
from PyQt6.QtCore import Qt

class ExistingFlashcard(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        self.setLayout(layout)
        
        # Title
        title = QLabel("Your Existing Flashcards")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Back button
        self.back_btn = QPushButton("← Back to Home")
        self.back_btn.clicked.connect(lambda: self.main_window.show_page(0))
        layout.addWidget(self.back_btn)
        
        # Scroll area for flashcards
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        self.cards_layout = QGridLayout(scroll_widget)
        
        # Sample flashcards - you can replace this with your actual data
        self.sample_flashcards = [
            {"question": "What is Python?", "answer": "A programming language"},
            {"question": "What is 2+2?", "answer": "4"},
            {"question": "Capital of France?", "answer": "Paris"},
            {"question": "Largest planet?", "answer": "Jupiter"},
        ]
        
        self.display_flashcards()
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
    
    def display_flashcards(self):
        # Clear existing cards
        for i in reversed(range(self.cards_layout.count())):
            self.cards_layout.itemAt(i).widget().setParent(None)
        
        # Display sample flashcards
        for i, card in enumerate(self.sample_flashcards):
            card_btn = QPushButton(f"Flashcard {i+1}: {card['question']}")
            card_btn.setMinimumHeight(60)
            card_btn.clicked.connect(lambda checked, idx=i: self.show_flashcard_details(idx))
            
            row = i // 2  # 2 cards per row
            col = i % 2
            self.cards_layout.addWidget(card_btn, row, col)
    
    def show_flashcard_details(self, card_index):
        card = self.sample_flashcards[card_index]
        print(f"Showing details for: {card['question']} - {card['answer']}")
        # Here you can implement a detailed view or flip card functionality