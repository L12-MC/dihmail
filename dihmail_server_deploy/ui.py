import sys
from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QLabel, QMessageBox
from PySide6.QtCore import *
import cli

alias = ""

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("DIH MAIL")
        self.inbox = QListWidget()
        self.message = QPlainTextEdit(readOnly=True, plainText="Select Message")
        self.myself = QLabel(f"{alias}:dih:dihmail.co")
        self.gen = QPushButton("Login")
        self.toplay = QHBoxLayout()
        self.refresher = QPushButton("Refresh")
        self.send = QPushButton("Send")
        self.toplay.addWidget(self.inbox)
        self.toplay.addWidget(self.message)
        self.mainlay = QVBoxLayout()
        self.bottom = QHBoxLayout()
        self.bottom.addWidget(self.refresher)
        self.bottom.addWidget(self.send)
        self.bottom.addWidget(self.myself)
        self.mainlay.addLayout(self.toplay)
        self.mainlay.addLayout(self.bottom)
        self.setLayout(self.mainlay)
        self.refresher.clicked.connect(self.refresh)
        self.inbox.itemClicked.connect(self.show_message)
        self.send.clicked.connect(self.open_send_dialog)
        self.load_inbox()
        
    def load_inbox(self):
        try:
            from mail import get_inbox
            messages = get_inbox(alias)
            self.inbox.clear()
            for msg in messages:
                mid, sender, recipient, created = msg
                self.inbox.addItem(f"[{mid}] From: {sender} - {created}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load inbox: {str(e)}")
    
    def refresh(self):
        self.load_inbox()
    
    def show_message(self, item):
        try:
            # Extract message ID from item text [123]
            text = item.text()
            mid = int(text.split('[')[1].split(']')[0])
            from mail import decrypt_message_id
            plaintext = decrypt_message_id(mid)
            # Replace literal \n with actual newlines
            plaintext = plaintext.replace('\\n', '\n')
            self.message.setPlainText(plaintext)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load message: {str(e)}")
    
    def open_send_dialog(self):
        send_dialog = SendDialog(alias, self)
        if send_dialog.exec() == QDialog.Accepted:
            self.refresh()


class SendDialog(QDialog):

    def __init__(self, sender_alias, parent=None):
        super(SendDialog, self).__init__(parent)
        self.sender_alias = sender_alias
        self.setWindowTitle("Send Message")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Recipient field
        layout.addWidget(QLabel("Recipient Address:"))
        self.recipient_input = QLineEdit()
        self.recipient_input.setPlaceholderText("username:dih:dihmail.co")
        layout.addWidget(self.recipient_input)
        
        # Message field
        layout.addWidget(QLabel("Message:"))
        self.message_input = QPlainTextEdit()
        self.message_input.setPlaceholderText("Enter your message here...")
        layout.addWidget(self.message_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        send_btn = QPushButton("Send")
        cancel_btn = QPushButton("Cancel")
        send_btn.clicked.connect(self.send_message)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(send_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def send_message(self):
        recipient = self.recipient_input.text().strip()
        message = self.message_input.toPlainText().strip()
        
        if not recipient or not message:
            QMessageBox.warning(self, "Error", "Both recipient and message are required!")
            return
        
        try:
            from mail import send_message
            result = send_message(self.sender_alias, recipient, message)
            QMessageBox.information(self, "Success", f"Message sent! ID: {result['message_id']}")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to send message: {str(e)}")


class LoginDialog(QDialog):

    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        self.setWindowTitle("Login / Register")
        self.setMinimumWidth(350)
        self.authenticated_user = None
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("DIH MAIL Authentication")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Username field
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username...")
        layout.addWidget(self.username_input)
        
        # Password field
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password...")
        layout.addWidget(self.password_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        login_btn = QPushButton("Login")
        register_btn = QPushButton("Register")
        login_btn.clicked.connect(self.login)
        register_btn.clicked.connect(self.register)
        button_layout.addWidget(login_btn)
        button_layout.addWidget(register_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and password are required!")
            return
        
        try:
            from auth import authenticate_user
            if authenticate_user(username, password):
                self.authenticated_user = username
                QMessageBox.information(self, "Success", f"Logged in as {username}")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Invalid username or password!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login failed: {str(e)}")
    
    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and password are required!")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters!")
            return
        
        try:
            from auth import register_user
            register_user(username, password)
            QMessageBox.information(self, "Success", f"User {username} registered successfully! You can now login.")
            # Auto-fill username for login
            self.password_input.clear()
            self.password_input.setFocus()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Registration failed: {str(e)}")
    

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    
    # Show login dialog
    login_dialog = LoginDialog()
    if login_dialog.exec() != QDialog.Accepted:
        sys.exit(0)  # User cancelled login
    
    # Get authenticated username
    alias = login_dialog.authenticated_user
    
    if not alias:
        QMessageBox.critical(None, "Error", "Authentication failed!")
        sys.exit(1)
    
    # Create and show the main form
    form = Form()
    form.show()
    form.myself.setText(f"{alias}:dih:dihmail.co")
    # Run the main Qt loop
    sys.exit(app.exec())