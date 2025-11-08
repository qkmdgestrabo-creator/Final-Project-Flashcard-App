# FINAL PROJECT FLASHCARD APP / ui / components / pomodoro_timer.py

from PyQt6.QtCore import QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QSpinBox, QMessageBox, QWidget, QFrame)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtProperty, QEvent
from ui.visual.styles.styles import get_pomodoro_styles

class BreakOverlay(QWidget):
    def __init__(self, parent, session_info):
        super().__init__(parent)
        self.session_info = session_info
        self.styles = get_pomodoro_styles()
        self.setup_ui()
        
        # Install event filter on parent to track movement
        if parent:
            parent.installEventFilter(self)
        
    def setup_ui(self):
        # Make it a normal child widget
        self.setWindowFlags(Qt.WindowType.Widget)
        
        # Apply the light grey overlay style
        self.setStyleSheet(self.styles["break_overlay"])
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Create all labels
        break_label = QLabel("BREAK TIME")
        break_label.setStyleSheet(self.styles["break_label"])
        break_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        break_label.setWordWrap(True)
        
        messages = [
            "You're doing great! Your brain needs this rest.",
            "Well done! Taking breaks improves memory retention.",
            "Excellent work! This break will boost your focus.",
            "Amazing progress! Your mind is consolidating what you learned.",
            "Outstanding! This pause will enhance your learning."
        ]
        import random
        message = random.choice(messages)
        
        message_label = QLabel(message)
        message_label.setStyleSheet(self.styles["break_message"])
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setWordWrap(True)
        
        progress_label = QLabel(f"Session {self.session_info} completed!")
        progress_label.setStyleSheet(self.styles["break_progress"])
        progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_label.setWordWrap(True)
        
        self.timer_label = QLabel("05:00")
        self.timer_label.setStyleSheet(self.styles["break_timer"])
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        instruction_label = QLabel("Break in progress... Timer will auto-continue")
        instruction_label.setStyleSheet(self.styles["break_instruction"])
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_label.setWordWrap(True)
        
        # Add all widgets to layout
        layout.addWidget(break_label)
        layout.addWidget(message_label)
        layout.addWidget(progress_label)
        layout.addWidget(self.timer_label)
        layout.addWidget(instruction_label)
        
        # Set initial position
        self.update_position()
        
        # Fade in animation
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(800)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()
    
    def update_position(self):
        """Update to cover parent area"""
        if self.parent():
            # Always position at (0, 0) relative to parent and match size
            self.move(0, 0)
            self.resize(self.parent().width(), self.parent().height())
    
    def update_timer(self, minutes, seconds):
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")
    
    def eventFilter(self, obj, event):
        """Track parent window movement and resizing"""
        if obj == self.parent():
            if event.type() in [QEvent.Type.Move, QEvent.Type.Resize]:
                self.update_position()
        return super().eventFilter(obj, event)
    
    def resizeEvent(self, event):
        """Update when parent resizes"""
        self.update_position()
        super().resizeEvent(event)
    
    def showEvent(self, event):
        """Ensure proper positioning when shown"""
        self.update_position()
        super().showEvent(event)

class PomodoroTimer:
    def __init__(self, main_window):
        self.main_window = main_window
        self.styles = get_pomodoro_styles()
        self.time_remaining = 0
        self.timer_running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        
        # Session settings
        self.study_time = 25
        self.break_time = 5
        self.total_sessions = 4
        self.current_session = 0
        
        # State tracking
        self.is_break_time = False
        self.forced_break_mode = False
        self.sessions_completed = 0
        self.break_overlay = None
        
        # Initialize with study time
        self.time_remaining = self.study_time * 60
    
    def start_timer(self):
        if not self.timer_running and not self.forced_break_mode:
            if self.time_remaining <= 0:
                if not self.is_break_time:
                    self.time_remaining = self.study_time * 60
                    if self.current_session == 0:
                        self.current_session = 1
            
            self.timer_running = True
            self.timer.start(1000)
            self.update_display()
            return True
        return False
    
    def pause_timer(self):
        if self.timer_running and not self.forced_break_mode:
            self.timer_running = False
            self.timer.stop()
            self.update_display()
            return True
        return False
    
    def reset_timer(self):
        if not self.forced_break_mode:
            self.timer_running = False
            self.timer.stop()
            self.time_remaining = self.study_time * 60
            self.is_break_time = False
            self.forced_break_mode = False
            self.current_session = 0
            self.sessions_completed = 0
            self.remove_break_overlay()
            self.restore_window_resize()
            self.update_display()
            return True
        return False
    
    def update_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.update_display()
            
            if self.break_overlay:
                minutes = self.time_remaining // 60
                seconds = self.time_remaining % 60
                self.break_overlay.update_timer(minutes, seconds)
        else:
            self.timer_finished()
    
    def update_display(self):
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        
        if self.forced_break_mode:
            status = "FORCED BREAK"
        else:
            status = "Break" if self.is_break_time else "Study"
        
        session_info = f" ({self.current_session}/{self.total_sessions})"
        display_text = f"{status}{session_info}: {minutes:02d}:{seconds:02d}"
        
        if hasattr(self.main_window, 'update_timer_display'):
            self.main_window.update_timer_display(display_text)
        
        self.update_button_states()
    
    def update_button_states(self):
        if hasattr(self.main_window, 'pomodoro_btn'):
            if self.forced_break_mode:
                self.main_window.pomodoro_btn.setEnabled(False)
                self.main_window.pomodoro_btn.setText("⏸ Forced Break")
                self.main_window.pomodoro_btn.setStyleSheet(self.styles["timer_button_forced_break"])
                
                if hasattr(self.main_window, 'timer_settings_btn'):
                    self.main_window.timer_settings_btn.setEnabled(False)
            else:
                self.main_window.pomodoro_btn.setEnabled(True)
                if hasattr(self.main_window, 'timer_settings_btn'):
                    self.main_window.timer_settings_btn.setEnabled(True)
                    
                if self.timer_running:
                    self.main_window.pomodoro_btn.setText("⏸ Pause")
                    self.main_window.pomodoro_btn.setStyleSheet(self.styles["timer_button_running"])
                else:
                    self.main_window.pomodoro_btn.setText("▶ Start")
                    self.main_window.pomodoro_btn.setStyleSheet(self.styles["timer_button_stopped"])

    def show_break_overlay(self):
        """Show overlay as a child widget"""
        self.remove_break_overlay()
        
        session_info = f"{self.current_session}/{self.total_sessions}"
        self.break_overlay = BreakOverlay(self.main_window, session_info)
        self.break_overlay.show()
    
    def remove_break_overlay(self):
        if self.break_overlay:
            self.break_overlay.deleteLater()
            self.break_overlay = None
    
    def enforce_forced_break(self):
        """Make window non-resizable during break"""
        if hasattr(self.main_window, 'setFixedSize'):
            current_size = self.main_window.size()
            self.main_window.setFixedSize(current_size)

    def restore_window_resize(self):
        """Allow window resizing again after break"""
        if hasattr(self.main_window, 'setMinimumSize'):
            self.main_window.setMinimumSize(400, 300)
        if hasattr(self.main_window, 'setMaximumSize'):
            self.main_window.setMaximumSize(16777215, 16777215)

    def timer_finished(self):
        self.timer_running = False
        self.timer.stop()
        
        if not self.is_break_time:
            # STUDY TIME FINISHED - START FORCED BREAK
            self.sessions_completed += 1
            self.is_break_time = True
            self.forced_break_mode = True
            self.time_remaining = self.break_time * 60
            
            # ENFORCE non-resizable window
            self.enforce_forced_break()
            
            self.show_break_overlay()
            self.timer_running = True
            self.timer.start(1000)
            
        else:
            # BREAK TIME FINISHED
            self.is_break_time = False
            self.forced_break_mode = False
            
            # RESTORE window resizing
            self.restore_window_resize()
            
            self.remove_break_overlay()
            
            if self.current_session < self.total_sessions:
                self.current_session += 1
                self.time_remaining = self.study_time * 60
                
                QMessageBox.information(self.main_window, "Break Complete!", 
                                    f"Starting session {self.current_session}/{self.total_sessions} now!")
                
                self.timer_running = True
                self.timer.start(1000)
                self.update_display()
                
            else:
                self.time_remaining = 0
                self.current_session = 0
                self.sessions_completed = 0
                
                QMessageBox.information(self.main_window, "All Sessions Complete!", 
                                    f"Congratulations! You completed all {self.total_sessions} sessions! 🎉")
                self.update_display()
    
    def set_times(self, study_time, break_time, sessions):
        if not self.forced_break_mode:
            self.study_time = study_time
            self.break_time = break_time
            self.total_sessions = sessions
            
            if not self.timer_running:
                if not self.is_break_time:
                    self.time_remaining = self.study_time * 60
                else:
                    self.time_remaining = self.break_time * 60
                self.update_display()
            return True
        return False
    
    def show_settings(self, parent_widget):
        if self.forced_break_mode:
            QMessageBox.warning(parent_widget, "Settings Locked", 
                              "Cannot change settings during forced break!\n"
                              "Please wait for the break to complete.")
            return False
        
        settings_dialog = PomodoroSettings(parent_widget)
        settings_dialog.study_spin.setValue(self.study_time)
        settings_dialog.break_spin.setValue(self.break_time)
        settings_dialog.sessions_spin.setValue(self.total_sessions)
        
        if settings_dialog.exec() == QDialog.DialogCode.Accepted:
            return self.set_times(
                settings_dialog.study_spin.value(), 
                settings_dialog.break_spin.value(),
                settings_dialog.sessions_spin.value()
            )
        return False

class PomodoroSettings(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.styles = get_pomodoro_styles()
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Timer Settings")
        
        # Apply dialog style first
        self.setStyleSheet(self.styles["settings_dialog"])
        
        # RESPONSIVE SIZING - Use percentage of screen size
        if self.parent():
            screen = self.parent().screen()
            screen_size = screen.availableGeometry()
            dialog_width = int(screen_size.width() * 0.25)
            dialog_height = int(screen_size.height() * 0.3)
            self.setMinimumSize(dialog_width, dialog_height)
        else:
            self.setMinimumSize(400, 300)
        
        # Main layout with proper spacing
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Study time
        study_layout = QHBoxLayout()
        study_label = QLabel("Study Time (minutes):")
        study_label.setStyleSheet(self.styles["settings_label"])
        study_layout.addWidget(study_label)
        
        study_layout.addStretch()
        
        self.study_spin = QSpinBox()
        self.study_spin.setStyleSheet(self.styles["spin_box"])
        self.study_spin.setRange(1, 60)
        self.study_spin.setValue(25)
        self.study_spin.setSuffix(" min")
        study_layout.addWidget(self.study_spin)
        layout.addLayout(study_layout)
        
        # Break time
        break_layout = QHBoxLayout()
        break_label = QLabel("Break Time (minutes):")
        break_label.setStyleSheet(self.styles["settings_label"])
        break_layout.addWidget(break_label)
        
        break_layout.addStretch()
        
        self.break_spin = QSpinBox()
        self.break_spin.setStyleSheet(self.styles["spin_box"])
        self.break_spin.setRange(1, 30)
        self.break_spin.setValue(5)
        self.break_spin.setSuffix(" min")
        break_layout.addWidget(self.break_spin)
        layout.addLayout(break_layout)
        
        # Sessions
        sessions_layout = QHBoxLayout()
        sessions_label = QLabel("Number of Sessions:")
        sessions_label.setStyleSheet(self.styles["settings_label"])
        sessions_layout.addWidget(sessions_label)
        
        sessions_layout.addStretch()
        
        self.sessions_spin = QSpinBox()
        self.sessions_spin.setStyleSheet(self.styles["spin_box"])
        self.sessions_spin.setRange(1, 10)
        self.sessions_spin.setValue(4)
        sessions_layout.addWidget(self.sessions_spin)
        layout.addLayout(sessions_layout)
        
        # Info label
        info_label = QLabel("💡 Note: All breaks between sessions are forced for your well-being and focus.")
        info_label.setStyleSheet(self.styles["settings_info"])
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        # Buttons with proper spacing
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setContentsMargins(0, 20, 0, 0)
        
        save_btn = QPushButton("💾 Save")
        save_btn.setStyleSheet(self.styles["save_button"])
        save_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.setStyleSheet(self.styles["cancel_button"])
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)