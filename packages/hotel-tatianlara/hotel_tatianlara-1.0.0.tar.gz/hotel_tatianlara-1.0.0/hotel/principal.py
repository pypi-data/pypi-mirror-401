import sys
from PySide6.QtWidgets import QApplication, QDialog

from hotel.vistas.vlogin import tl_VLogin
from hotel.vistas.vmenu import tl_VMenu


def main():
    app = QApplication(sys.argv)

    login = tl_VLogin()
    if login.exec() == QDialog.Accepted:
        menu = tl_VMenu()
        menu.exec()

    sys.exit(0)


if __name__ == "__main__":
    main()

