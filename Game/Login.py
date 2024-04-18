import sys
from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox
from GameUI import GameUI

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.role = None  # Add a role attribute
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Login')

        layout = QVBoxLayout()

        self.user_label = QLabel('Username:', self)
        layout.addWidget(self.user_label)

        self.user_input = QLineEdit(self)
        layout.addWidget(self.user_input)

        self.pass_label = QLabel('Password:', self)
        layout.addWidget(self.pass_label)

        self.pass_input = QLineEdit(self)
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pass_input)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()

        if self.authenticate(username, password):
            self.launch_game(username)
        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password')

    def authenticate(self, username, password):
        try:
            with open('credentials.txt', 'r') as file:
                credentials = file.readlines()
            credentials = [line.strip().split(':') for line in credentials]
            credentials_dict = {user: (pwd, role) for user, pwd, role in credentials}
            if username in credentials_dict and credentials_dict[username][0] == password:
                self.role = credentials_dict[username][1]  # Set the role attribute
                return True
            return False
        except FileNotFoundError:
            QMessageBox.critical(self, 'Error', 'Credentials file not found')
            return False

    def launch_game(self, username):
        if self.role == 'debugger':  # Check the role
            self.game_ui = GameUI(debug_mode=True)
        else:
            self.game_ui = GameUI()
        self.game_ui.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec())
