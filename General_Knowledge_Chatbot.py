import sys
import wikipedia
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QTextCursor, QTextCharFormat, QFont, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QPushButton, QMessageBox

class ChatbotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Chatbot")
        self.setGeometry(100, 100, 700, 400)

        # Create chat history
        self.chat_history = QTextEdit(self)
        self.chat_history.setStyleSheet("background-color: #C3B1E1;")
        self.chat_history.setReadOnly(True)
        self.chat_history.setFontPointSize(12)
        self.append_to_chat_history("Type any General Knowledge question(Press -1 to exit)", "AI")

        # Create text input
        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Type your message...")
        self.text_input.setFont(QFont("Helvetica", 12))  # Set the desired font with desired size
        self.text_input.setFixedHeight(50)  # Initial height

        # Create send button
        self.button = QPushButton()
        self.button.setIcon(QIcon("G:\Practice\Meesage.png"))
        self.button.setFixedSize(50, 50)
        self.button.setIconSize(QSize(35, 35))
        self.button.clicked.connect(self.send_message)
        self.button.setStyleSheet(
            "QPushButton {border-radius: 25px; background-color: #800080;}"
            "QPushButton:hover { background-color: #A040A0;}"
            "QPushButton:pressed { background-color:#a881af;}")

        self.button.move(self.width() - self.button.width() - 20, self.height() - self.button.height() - 60)
        self.text_input.textChanged.connect(self.check_text)


        # Create layout
        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(self.button)
        layout.addWidget(self.chat_history)
        layout.addLayout(input_layout)

        # Create main widget
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def check_text(self):
        # Enable the button if there is text in the QTextEdit, otherwise disable it
        text = self.text_input.toPlainText()
        self.button.setEnabled(bool(text))

    def append_to_chat_history(self, text, sender):
        # Get the current cursor position
        cursor = self.chat_history.textCursor()
        # Move the cursor to the end of the document
        cursor.movePosition(QTextCursor.MoveOperation.End)
        # Set the alignment based on the sender
        alignment = Qt.AlignmentFlag.AlignRight if sender == "You" else Qt.AlignmentFlag.AlignLeft
        self.chat_history.setAlignment(alignment)
        # Create a text char format for styling
        char_format = QTextCharFormat()
        char_format.setBackground(QColor("#C3B1E1"))  # Set the desired background color
        char_format.setFontPointSize(12)
        # Insert the text at the cursor position with the applied format
        cursor.setCharFormat(char_format)
        if sender == "You":
            cursor.insertText(f"{sender}: {text}\n")
        else:
            cursor.insertText(f"{sender}: {text}\n")
        # Insert the formatted message to the chat history
        cursor.setCharFormat(char_format)

        # Set the cursor back to the original position
        self.chat_history.setTextCursor(cursor)
        # Scroll to the bottom to show the new text
        self.chat_history.ensureCursorVisible()
        return 
    
    def get_answer(self, question):
        try:
            if question.strip() == "":
                raise ValueError("Question is empty.")
            answer = wikipedia.summary(question, sentences=3)
        except wikipedia.exceptions.PageError:
            answer = "Sorry, I couldn't find any information related to your question."
        except wikipedia.exceptions.WikipediaException as e:
            answer = f"An unknown error occurred: {str(e)}"
        return answer
    
    def send_message(self):
        # Handle send button click event
        message = self.text_input.toPlainText()
        if (message=="-1"):
            self.close()
        self.append_to_chat_history(message, "You")
        self.text_input.clear()
        answer = self.get_answer(message)
        self.append_to_chat_history(answer,"AI")
        
    def closeEvent(self, event):
        # Override close event to confirm before closing the window
        reply = QMessageBox.question(self, 'Confirm Exit', 'Are you sure you want to exit?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatbotWindow()
    window.show()
    sys.exit(app.exec())
