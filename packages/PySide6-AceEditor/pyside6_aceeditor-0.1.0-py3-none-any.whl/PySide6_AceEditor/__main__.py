try:
    from PySide6_AceEditor import testWindow
except (ImportError, ModuleNotFoundError):
    try:
        import testWindow
    except (ImportError, ModuleNotFoundError):
        from . import testWindow


def main():
    qa = testWindow.QtWidgets.QApplication(list())
    tw = testWindow.TestWindow()
    tw.show()
    qa.exec()


if __name__ == "__main__":
    main()
