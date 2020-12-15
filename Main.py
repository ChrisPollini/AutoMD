import sys

from PyQt5.QtWidgets import QApplication
from Presenter.MainPresenter import MainPresenter

def main():
    app = QApplication(sys.argv)

    MainPresenter()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
