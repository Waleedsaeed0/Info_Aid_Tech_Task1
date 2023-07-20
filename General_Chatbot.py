import sys
from nltk.chat.util import Chat, reflections
from datetime import datetime 
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QTextCursor, QTextCharFormat, QFont, QColor
from PyQt6.QtWidgets import *

# Get the current time and date
current_time = datetime.now().strftime("%H:%M:%S")  # Format: hours:minutes:seconds
current_date = datetime.now().strftime("%Y-%m-%d")  # Format: year-month-day
pairs = [
    [r"hi|hey|hello",
        ["Hello!", "Hey there!", "Hi!",]],
    [r"what is your name\?",
        ["You can call me Chatbot.", "I'm Chatbot.",]],
    [r"how are you\?",
        ["I'm doing well, thank you.", "I'm great, how about you?",]],
    [r"what can you do\?",
        ["I can  chat with you.",]],
    [r"tell me a joke",
        ["Why don't scientists trust atoms? Because they make up everything!", "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",]],
    [r"what is your favorite color\?",
        ["As an AI, I don't have the ability to perceive or have preferences for colors.",]],
    [r"what is your favorite food\?",
        ["As an AI, I don't consume food, so I don't have a favorite.",]],
    [r"what is the time\?",
        ["The current time is ",current_time]],  # You can add the actual time based on the location],
    [r"what is the date\?",
        ["The current date is ",current_date]],
    [r"tell me a fun fact",
        ["A sneeze travels at about 100 miles per hour.", "The world's oldest known vegetable is the pea.",]],
    [r"do you believe in ghosts\?",
        ["As an AI, I don't have beliefs or opinions.",]],
    [r"tell me a riddle",
        ["I can't think of a riddle at the moment, but here's one for you: What has keys but can't open locks? A piano!",]],
    [r"tell me a historical event",
        ["On July 20, 1969, Apollo 11 landed on the moon.",]],
    [r"tell me a famous quote",
        ["The only way to do great work is to love what you do. - Steve Jobs", "In the middle of every difficulty lies opportunity. - Albert Einstein",]],
    [r"how old are you\?",
        ["As an AI, I don't have an age.",]],
    [r"1",
     ["You're very smart!"]],
    [r"what is the meaning of life\?",
        ["The meaning of life is a subjective question and can vary for each individual.",]],
    [r"tell me a science fact",
        ["The speed of light is approximately 299,792,458 meters per second.", "Gravity is a force that attracts objects toward each other.",]],
    [r"tell me a technology fact",
        ["The first computer programmer was Ada Lovelace.", "The Internet was created in the late 1960s.",]],
    [r"what is your favorite movie\?",
        ["As an AI, I don't watch movies, so I don't have a favorite.",]],
    [r"tell me a book recommendation",
        ["One popular book recommendation is '1984' by George Orwell.",]],
    [r"tell me a music recommendation",
        ["One music recommendation is 'Bohemian Rhapsody' by Queen.",]],
    [r"tell me a sports fact",
        ["Basketball was invented by Dr. James Naismith in December 1891.", "Football (soccer) is the most popular sport in the world.",]],
    [r"what is the weather like today\?",
        ["I'm sorry, I don't have real-time weather information.",]],
    [r"tell me a travel destination",
        ["One popular travel destination is Paris, France.",]]]

def process_text(text):
    ChatbotWindow.append_to_chat_history(text, "You")

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
        self.append_to_chat_history("You have entered in General Chat (Press -1 to exit)", "AI")
        self.append_to_chat_history("How can I help you?", "AI")

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

    def send_message(self):
        # Handle send button click event
        message = self.text_input.toPlainText()
        if (message=="-1"):
            self.close()
        self.append_to_chat_history(message, "You")
        self.text_input.clear()
        chatbot = Chat(pairs, reflections)
        response = chatbot.respond(message)
        if response is None:
            response = "I'm sorry, I don't have an answer for that."
        self.append_to_chat_history(response, "AI")
        
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
