import sys
import os
import yaml

from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QLabel,
    QFileDialog,
    QInputDialog,
)
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import (
    serialization,
    hashes,
    padding as padding2
)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key


class Window(QMainWindow):
    """The universal class"""

    def key_generation_func(
            self,
            symmetric_key_path: str,
            public_key_path: str,
            secret_key_path: str
    ) -> None:
        """
        The function generate a key for tasks
        symmetric_key_path - path to  symmetric key
        public_key_path - path to  public key
        secret_key_path - path to  secret key
        """
        symmetric_key = os.urandom(int(int(self.bit) / 8))
        keys = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        private_key = keys
        public_key = keys.public_key()
        public_pem = public_key_path + '\\publuc_key.pem'
        with open(public_pem, "wb") as public_out:
            public_out.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )
        private_pem = secret_key_path + '\\private_key.pem'
        with open(
                private_pem,
                'wb'
        ) as private_out:
            private_out.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )
        encrypted_symmetric_key = public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithms=hashes.SHA256(),
                label=None
            )
        )
        symmetric_file = symmetric_key_path + '\\sym_key.txt'
        with open(symmetric_file, 'wb') as key_file:
            key_file.write(encrypted_symmetric_key)

    def encrypt_data(
            self,
            initial_file_path: str,
            secret_key_path: str,
            symmetric_key_path: str,
            encrypted_file_path: str
    ) -> None:
        """
        The function encrypt data for tasks
        initial_file_path - path to file 
        secret_key_path - path to secret key       
        symmetric_key_path - path to symmetric key
        encrypted_file_path - path to  encrypted file
        """
        symmetric_file = symmetric_key_path + '\\sym_key.txt'
        with open(symmetric_file, mode='rb') as key_file:
            encrypted_symmetric_key = key_file.read()
        private_pem = secret_key_path + '\\private_key.pem'
        with open(private_pem, 'rb') as pem_in:
            private_bytes = pem_in.read()
        private_key = load_pem_private_key(private_bytes, password=None)
        d_symmetric_key = private_key.decrypt(
            encrypted_symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(), label=None)
        )
        initial_file = initial_file_path + '\\text.txt'
        with open(initial_file, 'r') as _file:
            initial_content = _file.read()
        padder = padding2.ANSIX923(256).padder()
        text = bytes(initial_content, 'UTF-8')
        padded_text = padder.update(text) + padder.finalize()
        iv = os.urandom(int(int(self.bit) / 8))
        cipher = Cipher(algorithms.AES(d_symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_text) + encryptor.finalize()
        dict_t = {'text': c_text, 'iv': iv}
        encrypted_file = encrypted_file_path + '\\secret_text.yaml'
        with open(encrypted_file, 'w') as _file:
            yaml.dump(dict_t, _file)

    def decrypting_data(
            self,
            encrypted_file_path: str,
            secret_key_path: str,
            symmetric_key_path: str,
            decrypted_file_path: str
    ) -> None:
        """
        The function decrypt data for tasks
        encrypted_file_path - path to decrypt file 
        secret_key_path - path to secret key     
        symmetric_key_path - path to symmetric key
        decrypted_file_path - path to  decrypt file 
        """
        symmetric_file = symmetric_key_path + '\\sym_key.txt'
        with open(symmetric_file, mode='rb') as key_file:
            encrypted_symmetric_key = key_file.read()
        private_pem = secret_key_path + '\\private_key.pem'
        with open(private_pem, 'rb') as pem_in:
            private_bytes = pem_in.read()
        private_key = load_pem_private_key(private_bytes, password=None)
        dsymmetric_key = private_key.decrypt(
            encrypted_symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None)
        )
        encrypted_file = encrypted_file_path + '\\secret_text.yaml'
        with open(encrypted_file) as _file:
            content_encrypted = yaml.safe_load(_file)
        text_enc = content_encrypted["text"]
        iv_enc = content_encrypted["iv"]
        cipher = Cipher(algorithms.AES(dsymmetric_key), modes.CBC(iv_enc))
        decryptor = cipher.decryptor()
        dc_text = decryptor.update(text_enc) + decryptor.finalize()
        unpadder = padding2.ANSIX923(256).unpadder()
        unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
        decrypted_file = decrypted_file_path + '\\finish_text.txt'
        with open(decrypted_file, 'w') as _file:
            _file.write(str(unpadded_dc_text))

    def button_first_field_click(self):
        """ The action when you click button near first field"""
        self.field_path_1 = QFileDialog.getExistingDirectory(
            self,
            "Выбрать папку",
            "."
        )
        self.field_first.setText(self.field_path_1)

    def button_second_field_click(self):
        """The action when you click button near second field"""
        self.field_path_2 = QFileDialog.getExistingDirectory(
            self,
            "Выбрать папку",
            "."
        )
        self.field_second.setText(self.field_path_2)

    def button_third_field_click(self):
        """The action when you click button near third field"""
        self.field_path_3 = QFileDialog.getExistingDirectory(
            self,
            "Выбрать папку",
            "."
        )
        self.field_third.setText(self.field_path_3)

    def button_fourth_field_click(self):
        """The action when you click button near fourth field"""
        self.field_path_4 = QFileDialog.getExistingDirectory(
            self,
            "Выбрать папку",
            "."
        )
        self.field_fourth.setText(self.field_path_3)

    def button_OK_click(self):
        """
        The action when you click button OK: hide a 
        field,
        button and show result tasks
        """
        try:
            if self.chose_task == 1:
                self.key_generation_func(
                    self.field_path_1,
                    self.field_path_2,
                    self.field_path_3
                )
            elif self.chose_task == 2:
                self.encrypt_data(
                    self.field_path_1,
                    self.field_path_2,
                    self.field_path_3,
                    self.fielt_path_4
                )
            else:
                self.decrypting_data(
                    self.field_path_1,
                    self.field_path_2,
                    self.field_path_3,
                    self.fielt_path_4
                )
            self.button_first_field.hide()
            self.button_second_field.hide()
            self.button_third_field.hide()
            self.button_fourth_field.hide()
            self.button_OK.hide()
            self.field_first.hide()
            self.field_second.hide()
            self.field_third.hide()
            self.field_fourth.hide()
            self.field_first.clear()
            self.field_second.clear()
            self.field_third.clear()
            self.field_fourth.clear()
            QMessageBox.about(self, "Внимание", "Успешно")
            self.label_bob.clear()
            self.label_bob.setText(
                """
                My name is Bob and i your helper\nPlease,chose:\n1)GenKeys\n
                2)Encryption\n3)Decryption
                """
            )
            self.label_bob.adjustSize()
            self.button_genkey.show()
            self.button_encryption.show()
            self.button_decryption.show()
        except FileNotFoundError:
            QMessageBox.about(self, "Внимание", "Проверьте введённые данные")

    def button_genkey_click(self):
        """The action when you click button genkey: open task 1"""
        self.chose_task = 1
        self.label_bob.clear()
        self.label_bob.setText("Task 1: Generation Keys")
        self.label_bob.adjustSize()
        self.button_genkey.hide()
        self.button_encryption.hide()
        self.button_decryption.hide()
        self.field_first.show()
        self.field_second.show()
        self.field_third.show()
        self.button_OK.show()
        self.button_first_field.show()
        self.button_second_field.show()
        self.button_third_field.show()
        self.field_first.setPlaceholderText("symmetric_key_path")
        self.field_second.setPlaceholderText("public_key_path")
        self.field_third.setPlaceholderText("secret_key_path")

    def button_encryption_click(self):
        """The action when you click button encryption: open task 2"""
        self.chose_task = 2
        self.label_bob.clear()
        self.label_bob.setText("Task 2: Encrypt data")
        self.label_bob.adjustSize()
        self.button_genkey.hide()
        self.button_encryption.hide()
        self.button_decryption.hide()
        self.field_first.show()
        self.field_second.show()
        self.field_third.show()
        self.field_fourth.show()
        self.button_OK.show()
        self.button_first_field.show()
        self.button_second_field.show()
        self.button_third_field.show()
        self.button_fourth_field.show()
        self.field_first.setPlaceholderText("initial_file_path")
        self.field_second.setPlaceholderText("secret_key_path")
        self.field_third.setPlaceholderText("symmetric_key_path")
        self.field_fourth.setPlaceholderText("encrypted_file_path")

    def button_decryption_click(self):
        """The action when you click  button decryption: open task 3"""
        self.chose_task = 3
        self.label_bob.clear()
        self.label_bob.setText("Task 3: Decrypt data")
        self.label_bob.adjustSize()
        self.button_genkey.hide()
        self.button_encryption.hide()
        self.button_decryption.hide()
        self.field_first.show()
        self.field_second.show()
        self.field_third.show()
        self.field_fourth.show()
        self.button_OK.show()
        self.button_first_field.show()
        self.button_second_field.show()
        self.button_third_field.show()
        self.button_fourth_field.show()
        self.field_first.setPlaceholderText("encrypted_file_path")
        self.field_second.setPlaceholderText("secret_key_path")
        self.field_third.setPlaceholderText("symmetric_key_path")
        self.field_fourth.setPlaceholderText("decrypted_file_path")

    def __init__(self) -> None:
        """"create a window object"""
        super(Window, self).__init__()
        self.label_bob = QLabel(self)
        self.button_genkey = QtWidgets.QPushButton(self)
        self.button_encryption = QtWidgets.QPushButton(self)
        self.button_decryption = QtWidgets.QPushButton(self)
        self.button_first_field = QtWidgets.QPushButton(self)
        self.button_second_field = QtWidgets.QPushButton(self)
        self.button_third_field = QtWidgets.QPushButton(self)
        self.button_fourth_field = QtWidgets.QPushButton(self)
        self.button_OK = QtWidgets.QPushButton(self)
        self.field_first = QtWidgets.QLineEdit(self)
        self.field_second = QtWidgets.QLineEdit(self)
        self.field_third = QtWidgets.QLineEdit(self)
        self.field_fourth = QtWidgets.QLineEdit(self)
        self.field_path_1 = (
            self.field_path_2
        ) = self.field_path_3 = self.fielt_path_4 = os.getcwd()

        self.chose_task = 1
        self.field_first.hide()
        self.field_second.hide()
        self.field_third.hide()
        self.field_fourth.hide()
        self.button_OK.hide()
        self.button_first_field.hide()
        self.button_second_field.hide()
        self.button_third_field.hide()
        self.button_fourth_field.hide()
        self.label_bob.setText(
            """
            Hello, my name is Bob and i your helper\nPlease,chose:\n1)GenKeys\n
            2)Encryption\n3)Decryption
            """
        )
        self.button_genkey.setText("1)GenKeys")
        self.button_encryption.setText("2)Encryption")
        self.button_decryption.setText("2)Decryption")
        self.button_first_field.setText("Choose")
        self.button_second_field.setText("Choose")
        self.button_third_field.setText("Choose")
        self.button_fourth_field.setText("Choose")
        self.button_OK.setText("OK")
        self.field_first.setFixedSize(150, 20)
        self.field_second.setFixedSize(150, 20)
        self.field_third.setFixedSize(150, 20)
        self.field_fourth.setFixedSize(150, 20)
        self.label_bob.setFont(QFont('Times', 10))
        self.label_bob.move(445, 58)
        self.button_genkey.move(445, 150)
        self.button_encryption.move(525, 150)
        self.button_decryption.move(605, 150)
        self.field_first.move(445, 72)
        self.field_second.move(445, 95)
        self.field_third.move(445, 118)
        self.field_fourth.move(445, 141)
        self.button_first_field.move(600, 72)
        self.button_second_field.move(600, 95)
        self.button_third_field.move(600, 118)
        self.button_fourth_field.move(600, 141)
        self.button_OK.move(520, 165)
        self.label_bob.adjustSize()
        self.button_genkey.adjustSize()
        self.button_encryption.adjustSize()
        self.button_decryption.adjustSize()
        self.button_first_field.adjustSize()
        self.button_second_field.adjustSize()
        self.button_third_field.adjustSize()
        self.button_fourth_field.adjustSize()
        self.button_OK.adjustSize()
        self.button_genkey.clicked.connect(self.button_genkey_click)
        self.button_first_field.clicked.connect(self.button_first_field_click)
        self.button_second_field.clicked.connect(self.button_second_field_click)
        self.button_third_field.clicked.connect(self.button_third_field_click)
        self.button_fourth_field.clicked.connect(self.button_fourth_field_click)
        self.button_OK.clicked.connect(self.button_OK_click)
        self.button_encryption.clicked.connect(self.button_encryption_click)
        self.button_decryption.clicked.connect(self.button_decryption_click)
        self.bit = '0'
        while self.bit != "128" and self.bit != "192" and self.bit != "256":
            text, ok = QInputDialog.getText(
                self, "Input Dialog", "Enter 128 or 192 or 256 bit:"
            )
            if ok:
                self.bit = str(text)
                print(self.bit)


def application() -> None:
    """"Start aplication mainwindow"""
    app = QApplication(sys.argv)
    window = Window()
    window.setObjectName("MainWindow")
    window.setMinimumSize(800, 600)
    window.setMaximumSize(800, 600)
    window.setStyleSheet("#MainWindow{border-image:url(phon.png)}")
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    print(__file__)
    application()
