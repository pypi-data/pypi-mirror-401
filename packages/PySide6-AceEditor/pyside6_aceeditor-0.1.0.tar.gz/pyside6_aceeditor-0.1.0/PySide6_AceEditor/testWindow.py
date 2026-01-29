try:
    from PySide6_AceEditor import ui_testWindow
except (ImportError, ModuleNotFoundError):
    try:
        from . import ui_testWindow
    except (ImportError, ModuleNotFoundError):
        import ui_testWindow
from PySide6 import QtWidgets, QtGui
import pyperclip, typing

testCode = """// 这是Ace编辑器
function greet() {
    console.log("Hello, Ace Editor!");
}

// 尝试编辑这段代码
let message = "欢迎使用Ace编辑器";
console.log(message);"""


class TestWindow(QtWidgets.QMainWindow, ui_testWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.ss = QtGui.QTextCursor.MoveMode.MoveAnchor
        self.anchor_cache = None  # 缓存选区的「原始锚点绝对位置」

        self.widget.setText(testCode)
        self.connectSignals()

    def connectSignals(self):
        self.pushButton_copy.clicked.connect(self.copy_txt)
        self.pushButton_paste.clicked.connect(self.paste_txt)
        self.checkBox_readonly.stateChanged.connect(self.setRo)
        self.pushButton_cpro.clicked.connect(self.cpro)

        self.pushButton_addanno.clicked.connect(self.aan)
        self.pushButton_clr_anno.clicked.connect(self.can)
        self.pushButton_copyanno.clicked.connect(self.cpan)

        self.pushButton_copy_cur_pos.clicked.connect(self.ccp)
        self.pushButton_cur_right.clicked.connect(self.crt)
        self.pushButton_cur_left.clicked.connect(self.clt)
        self.pushButton_cur_up.clicked.connect(self.cup)
        self.pushButton_cur_down.clicked.connect(self.cdn)
        self.pushButton_copy_anch_pos.clicked.connect(self.cap)

        self.checkBox_selecting.stateChanged.connect(self.css)

    def css(self, state):
        if state == 2:
            self.ss = QtGui.QTextCursor.MoveMode.KeepAnchor
            # 勾选时：初始化锚点缓存 = 当前光标位置（第一次移动的起始锚点）
            cur = self.widget.textCursor()
            self.anchor_cache = cur.position()
            print(f"勾选选区模式 → 初始化锚点缓存: {self.anchor_cache}")
        else:
            self.ss = QtGui.QTextCursor.MoveMode.MoveAnchor
            # 取消勾选时：清空锚点缓存，恢复纯光标移动
            self.anchor_cache = None
            print(f"取消选区模式 → 清空锚点缓存")
        print(
            f"当前模式: {'选区扩展(KeepAnchor)' if self.ss == QtGui.QTextCursor.MoveMode.KeepAnchor else '纯光标移动(MoveAnchor)'}"
        )

    def get_anchor_row_column(
        self, text_cur: QtGui.QTextCursor
    ) -> typing.Tuple[int, int]:
        """
        获取 QTextEdit 中选区锚点（anchor）的行号和列号（均从 0 开始计数）
        :param text_edit: QTextEdit 实例
        :return: (anchor_row, anchor_column) 锚点的行号和列号
        """
        # 1. 获取 QTextEdit 的光标对象
        main_cursor = text_cur

        # 2. 获取锚点的绝对字符位置
        anchor_abs_pos = main_cursor.anchor()

        # 3. 创建锚点专属的临时 QTextCursor，用于计算行/列
        anchor_cursor = QtGui.QTextCursor(main_cursor.document())
        anchor_cursor.setPosition(anchor_abs_pos)  # 将临时光标移动到锚点位置

        # 4. 计算锚点的行号（直接获取）
        anchor_row = anchor_cursor.blockNumber()  # 行号从 0 开始

        # 5. 计算锚点的列号（当前锚点位置 - 所在行的行首位置）
        line_start_pos = (
            anchor_cursor.block().position()
        )  # 获取锚点所在行的行首绝对位置
        anchor_column = anchor_abs_pos - line_start_pos  # 列号从 0 开始

        return anchor_row, anchor_column

    def cap(self):
        cur = self.widget.textCursor()
        print("pos:", cur.anchor())
        pyperclip.copy(
            str(
                (self.get_anchor_row_column(cur)[0], self.get_anchor_row_column(cur)[1])
            )
        )

    def cup(self):
        cur = self.widget.textCursor()
        cur_col = cur.position() - cur.block().position()
        cur_block_num = cur.blockNumber()
        prev_block = cur.document().findBlockByNumber(cur_block_num - 1)
        if not prev_block.isValid():
            return
        target_col = min(cur_col, len(prev_block.text()))
        target_pos = prev_block.position() + target_col

        # ========== 接入锚点缓存 ==========
        if self.anchor_cache is not None:
            # 勾选状态：锚点=缓存值，光标=目标值，生成选区
            cur.setPosition(self.anchor_cache, QtGui.QTextCursor.MoveAnchor)
            cur.setPosition(target_pos, QtGui.QTextCursor.KeepAnchor)
        else:
            # 未勾选：纯光标移动
            cur.setPosition(target_pos, self.ss)
        self.widget.setTextCursor(cur)

    def cdn(self):
        cur = self.widget.textCursor()
        cur_col = cur.position() - cur.block().position()
        cur_block_num = cur.blockNumber()
        next_block = cur.document().findBlockByNumber(cur_block_num + 1)
        if not next_block.isValid():
            return
        target_col = min(cur_col, len(next_block.text()))
        target_pos = next_block.position() + target_col

        # ========== 接入锚点缓存 ==========
        if self.anchor_cache is not None:
            cur.setPosition(self.anchor_cache, QtGui.QTextCursor.MoveAnchor)
            cur.setPosition(target_pos, QtGui.QTextCursor.KeepAnchor)
        else:
            cur.setPosition(target_pos, self.ss)
        self.widget.setTextCursor(cur)

    def crt(self):
        cur = self.widget.textCursor()
        if cur.position() + 1 > cur.document().characterCount():
            return
        target_pos = cur.position() + 1

        # ========== 接入锚点缓存 ==========
        if self.anchor_cache is not None:
            cur.setPosition(self.anchor_cache, QtGui.QTextCursor.MoveAnchor)
            cur.setPosition(target_pos, QtGui.QTextCursor.KeepAnchor)
        else:
            cur.setPosition(target_pos, self.ss)
        self.widget.setTextCursor(cur)

    def clt(self):
        cur = self.widget.textCursor()
        if cur.position() - 1 < 0:
            return
        target_pos = cur.position() - 1

        # ========== 接入锚点缓存 ==========
        if self.anchor_cache is not None:
            cur.setPosition(self.anchor_cache, QtGui.QTextCursor.MoveAnchor)
            cur.setPosition(target_pos, QtGui.QTextCursor.KeepAnchor)
        else:
            cur.setPosition(target_pos, self.ss)
        self.widget.setTextCursor(cur)

    def ccp(self):
        cur = self.widget.textCursor()
        print("pos:", cur.position())
        pyperclip.copy(
            str((cur.blockNumber(), cur.position() - cur.block().position()))
        )

    def cpan(self):
        pyperclip.copy(str(self.widget.annotations()))

    def can(self):
        self.widget.clearAnnotations()

    def aan(self):
        l = [
            self.widget.AnnotationTypes.Error,
            self.widget.AnnotationTypes.Warning,
            self.widget.AnnotationTypes.Info,
        ]
        self.widget.addAnnotation(
            self.spinBox_row.value(),
            self.spinBox_col.value(),
            self.lineEdit_anno.text(),
            l[self.comboBox_annotype.currentIndex()],
        )

    def copy_txt(self):
        self.widget.copy()

    def paste_txt(self):
        self.widget.paste()

    def setRo(self):
        self.widget.setReadOnly(self.checkBox_readonly.isChecked())

    def cpro(self):
        pyperclip.copy(str(self.widget.isReadOnly()))


qa = QtWidgets.QApplication(list())
tw = TestWindow()
tw.show()
qa.exec()
