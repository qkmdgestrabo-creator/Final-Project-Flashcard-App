# ui/visual/app_styles.py

def get_sidebar_styles():
    return {
        "sidebar_collapsed": """
            QFrame {
                background-color: transparent;
                border: none;
            }
        """,
        "sidebar_expanded": """
            QFrame {
                background-color: #2c3e50;
                border: none;
            }
        """,
        "toggle_button": """
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1abc9c;
            }
        """,
        "nav_button_collapsed": """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                text-align: left;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgba(52, 73, 94, 0.7);
            }
        """,
        "nav_button_expanded": """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                text-align: left;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """
    }

def get_main_window_styles():
    return {
        "main_layout": """
            background-color: #ecf0f1;
        """
    }

