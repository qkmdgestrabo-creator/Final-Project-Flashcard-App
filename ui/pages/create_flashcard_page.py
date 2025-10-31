from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt

class CreateFlashcard(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        self.setLayout(layout)
        
        # Title
        title = QLabel("Create New Flashcard")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Question input
        question_label = QLabel("Question:")
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("Enter your question here...")
        
        # Answer input  
        answer_label = QLabel("Answer:")
        self.answer_input = QTextEdit()
        self.answer_input.setPlaceholderText("Enter the answer here...")
        self.answer_input.setMaximumHeight(100)
        
        # Buttons
        self.save_btn = QPushButton("Save Flashcard")
        self.cancel_btn = QPushButton("Cancel")
        
        # Add widgets to layout
        layout.addWidget(question_label)
        layout.addWidget(self.question_input)
        layout.addWidget(answer_label)
        layout.addWidget(self.answer_input)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.cancel_btn)
        layout.addStretch()
        
        # Connect buttons
        self.save_btn.clicked.connect(self.save_flashcard)
        self.cancel_btn.clicked.connect(self.go_back)
    
    def save_flashcard(self):
        question = self.question_input.text().strip()
        answer = self.answer_input.toPlainText().strip()
        
        if question and answer:
            print(f"Saved flashcard - Q: {question}, A: {answer}")
            # Here you can add logic to save to database/file
            self.clear_form()
        else:
            print("Please fill both question and answer")
    
    def clear_form(self):
        self.question_input.clear()
        self.answer_input.clear()
    
    def go_back(self):
        self.main_window.show_page(0)  # Go back to home page