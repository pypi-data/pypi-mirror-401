from PySide6 import QtWidgets, QtCore, QtWebEngineWidgets, QtGui
import os, typing
import sys, time, asyncio, websockets, pyperclip
import json

if sys.version_info.minor >= 9:
    from importlib import resources

    is_new_ver = True
else:
    import pkg_resources

    is_new_ver = False

try:
    from . import core, constants, utils
except (ImportError, ModuleNotFoundError):
    try:
        from PySide6_AceEditor import core, constants, utils
    except (ImportError, ModuleNotFoundError):
        import core, constants, utils

DEBUG = False


class AsyncioBridge(QtCore.QObject):
    """将asyncio事件循环嵌入到Qt事件循环的桥梁"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.loop = asyncio.get_event_loop()
        # 用QTimer定期唤醒asyncio事件循环（10ms一次）
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._process_asyncio_tasks)
        self.timer.start(10)  # 10ms检查一次asyncio任务

    def _process_asyncio_tasks(self):
        """处理asyncio的待执行任务"""
        # 执行一次事件循环迭代（非阻塞）
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.loop.run_forever()


class WebSocketServer(QtCore.QObject):
    def __init__(self, sig: QtCore.Signal, parent=None, host="0.0.0.0", port=8765):
        super().__init__(parent)
        self.sig = sig
        self.connected_clients = set()
        self.host = host
        self.port = port

    async def start_server(self):
        PORTS = (self.port, 5408, 2704, 54088, 9827, 1408, 1106)
        srv = None
        for i in PORTS:
            try:
                srv = websockets.serve(self._handle_client, self.host, i)
                async with srv as server:
                    self.server = server
                    # 保持服务运行（直到被停止）
                    await asyncio.Future()
                break
            except PermissionError:
                continue

    async def _handle_client(self, websocket: websockets.WebSocketServerProtocol):
        if DEBUG:
            print("regging")
        await self.register(websocket)
        if DEBUG:
            print("reged")
        async for message in websocket:
            if DEBUG:
                print(message)
            if str(message) == "changed":
                self.sig.emit()

    async def register(self, websocket: websockets.WebSocketServerProtocol):
        """注册新连接的客户端"""
        self.connected_clients.add(websocket)
        if DEBUG:
            print(f"新客户端连接，当前在线: {len(self.connected_clients)}")
        asyncio.ensure_future(self.wait(websocket))

    async def wait(self, websocket: websockets.WebSocketServerProtocol):
        try:
            # 保持连接（等待客户端断开）
            await websocket.wait_closed()
        finally:
            # 客户端断开后移除
            self.connected_clients.remove(websocket)
            if DEBUG:
                print(f"客户端断开，当前在线: {len(self.connected_clients)}")


class AceCodeWidget(QtWebEngineWidgets.QWebEngineView):
    textChanged = QtCore.Signal()

    class AnnotationTypes:
        Error = "error"
        Warning = "warning"
        Info = "info"

    def __init__(self, parent=None):
        # 关键：设置远程调试端口，这一行就足够启用调试
        if DEBUG:
            os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = "9222"

        super().__init__(parent=parent)

        self.loaded = False
        self._pre_run_code = str()
        self.do_set_text = False
        self.to_set_mode = False
        self.set_to = None
        self.set_to_mode = None
        self._got_txt = False
        self._txt = None
        self._first_txt = None
        self._got_thm = False
        self._thm = None
        self._got_mod = False
        self._mod = None
        self._to_set_anno = False
        self._anno = None
        self._first_thm = self._first_mod = None
        self.to_set_theme = False
        self._got_annos = False
        self._g_annos = None
        self._got_pos = False
        self._pos = None
        self._abs_pos = None
        self._got_abs_pos = False
        self._got_cur_selection = False
        self._cur_selection = None
        self._annos_to_set = list()
        self.page().loadFinished.connect(self.loadFinished2)

        self._cursor = QtGui.QTextCursor()

        self.asyncBrg = AsyncioBridge(self)
        self.wss = WebSocketServer(self.textChanged, self)
        asyncio.ensure_future(self.wss.start_server())

        # 设置初始尺寸
        self.resize(800, 600)

        try:
            if is_new_ver:
                self.runtime_dir = str(
                    resources.files("PySide6_AceEditor").joinpath("runtime")
                )
            else:
                self.runtime_dir = pkg_resources.resource_filename(
                    "PySide6_AceEditor", "runtime"
                )
        except ModuleNotFoundError:
            self.runtime_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "runtime"
            )
        self.base_url = QtCore.QUrl.fromLocalFile(self.runtime_dir + os.path.sep)

        # 加载初始内容
        self.setHtml(
            constants.EDITOR_HTML,
            baseUrl=self.base_url,
        )

        # 设置窗口标题
        self.setWindowTitle("Ace Code Widget (Debug on port 9222)")

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent):
        """重写右键菜单事件，控制菜单显示逻辑"""
        # 阻止默认菜单直接弹出
        event.accept()

        # 执行 JavaScript 判断点击的元素是否为文本输入区域
        # 逻辑：检查元素是否是 input/textarea，或具有 contenteditable 属性
        js_check = """
            (function() {
                const elem = document.elementFromPoint(%f, %f);
                if (!elem) return false;
                // 检查是否为 input 或 textarea
                if (elem.tagName === 'INPUT' || elem.tagName === 'TEXTAREA' || elem.className === 'ace_content') {
                    return true;
                }
                // 检查是否为可编辑元素（contenteditable="true"）
                if (elem.isContentEditable) {
                    return true;
                }
                return false;
            })()
        """ % (
            event.pos().x(),
            event.pos().y(),
        )  # 传入点击的坐标（相对网页的位置）
        ep = event.pos()

        # 执行 JS 并根据结果决定是否显示菜单
        self.page().runJavaScript(js_check, lambda i: self.show_menu_if_needed(i, ep))

    def show_menu_if_needed(self, is_editable: bool, pos: QtCore.QPoint):
        """根据元素类型决定是否显示右键菜单"""
        if DEBUG:
            print("editable:", is_editable)
        if is_editable:
            # 如果是文本框，显示默认右键菜单
            menu = self.createStandardContextMenu()
            menu.exec(self.mapToGlobal(pos))  # 弹出菜单
        else:
            # 非文本框区域，不显示菜单
            pass

    def setText(self, txt: str, select_after_set=False, isPrerun=False):
        if DEBUG:
            print(self.loaded)
        if not self.loaded:
            self.do_set_text = True
            self.set_to = txt
            self._first_txt = txt
            return
        a = "{"
        b = "}"
        js = f"""if(window.editor==undefined){a}
                                    window.onload=function(){a}
                                        editor.setValue("{utils.transText(txt)}");{'editor.selection.clearSelection();'if not select_after_set else str()}
                                  {b}
                                  {b}
                else{a}
                    editor.setValue("{utils.transText(txt)}");{'editor.selection.clearSelection();'if not select_after_set else str()}
                {b};"""
        if isPrerun:
            self._pre_run_code += js
            return
        self.page().runJavaScript(js)
        # print(js)

    def setMode(self, mode: str, isPrerun=False):
        if not self.loaded:
            self.to_set_mode = True
            self.set_to_mode = mode
            self._first_mod = mode
            return
        js = f'editor.session.setMode("{utils.transText(mode)}")'
        if isPrerun:
            self._pre_run_code += js + ";"
            return
        self.page().runJavaScript(js)

    def setTheme(self, theme: str, isPrerun=False):
        if not self.loaded:
            self.to_set_theme = True
            self.set_to_theme = theme
            self._first_thm = theme
            return
        js = f'editor.setTheme("{utils.transText(theme)}")'
        if isPrerun:
            self._pre_run_code += js + ";"
            return
        self.page().runJavaScript(js)

    def loadFinished2(self):
        if DEBUG:
            print("finished")
        self.loaded = True
        if self.do_set_text or self.to_set_mode:
            # 轮询检查editor是否初始化完成
            def check_editor():
                js = """window.editor !== undefined"""
                self.page().runJavaScript(
                    js, lambda result: self._on_editor_checked(result)
                )

            # 每隔10ms检查一次，最多检查100次（1秒）
            self.check_timer = QtCore.QTimer(self)
            self.check_timer.timeout.connect(check_editor)
            self.check_timer.start(10)
            self.check_count = 0

    def _on_editor_checked(self, result):
        if result or self.check_count >= 100:
            self.check_timer.stop()
            if result:
                self._pre_run_code += "annos_to_add=editor.session.getAnnotations();"
                if self.do_set_text:
                    self.setText(self.set_to, isPrerun=True)
                if self.to_set_mode:
                    self.setMode(self.set_to_mode, isPrerun=True)
                if self.to_set_theme:
                    self.setTheme(self.set_to_theme, isPrerun=True)
                if self._to_set_anno:
                    if DEBUG:
                        print("late add anno")
                        print("to_set_annos:", self._annos_to_set)
                    self.addAnnotations(self._annos_to_set, isPrerun=True)
                self._pre_run_code += "window.setTimeout(function(){editor.session.setAnnotations(annos_to_add);},1000);"  # TODO:解决由加载导致的问题
                if DEBUG:
                    print(
                        "------PreRunCode------\n"
                        + self._pre_run_code
                        + "\n------------"
                    )
                self.page().runJavaScript(self._pre_run_code)
            else:
                print("编辑器初始化超时，无法设置文本")
        else:
            self.check_count += 1

    def text(self, refresh_until_end=True) -> str:
        if self.loaded:
            self.page().runJavaScript("editor.getValue()", self._handle_txt)
            self._got_txt = False
            self._txt = None
            while not self._got_txt:
                if refresh_until_end:
                    QtWidgets.QApplication.processEvents()
                else:
                    time.sleep(0.000001)
            return self._txt
        if not self._first_txt:
            return ""
        return self._first_txt

    def theme(self, refresh_until_end=True) -> str:
        if self.loaded:
            self.page().runJavaScript("editor.getTheme()", self._handle_thm)
            self._got_thm = False
            self._thm = None
            while not self._got_thm:
                if refresh_until_end:
                    QtWidgets.QApplication.processEvents()
                else:
                    time.sleep(0.000001)
            return self._thm
        if not self._first_thm:
            return ""
        return self._first_thm

    def mode(self, refresh_until_end=True) -> str:
        if self.loaded:
            self.page().runJavaScript("editor.getMode()", self._handle_mod)
            self._got_mod = False
            self._mod = None
            while not self._got_mod:
                if refresh_until_end:
                    QtWidgets.QApplication.processEvents()
                else:
                    time.sleep(0.000001)
            return self._mod
        if not self._first_mod:
            return ""
        return self._first_mod

    def _handle_txt(self, txt: str):
        self._got_txt = True
        self._txt = txt

    def _handle_thm(self, thm: str):
        self._got_thm = True
        self._thm = thm

    def _handle_mod(self, mod: str):
        self._got_mod = True
        self._mod = mod

    def copy(self):
        self.page().runJavaScript(
            "editor.getSelectedText()", lambda t: pyperclip.copy(t)
        )

    def paste(self):
        self.page().runJavaScript(
            f'editor.insert("{utils.transText(pyperclip.paste())}")'
        )

    def setReadOnly(self, r: bool, isPrerun=False):
        if isPrerun:
            self._pre_run_code += f"editor.setReadOnly({utils.transBool(r)})"
            return
        self.page().runJavaScript(f"editor.setReadOnly({utils.transBool(r)})")

    def isReadOnly(self, refresh_until_end=True) -> bool:
        self._ro_got = False
        self._ro = None
        self.page().runJavaScript(f"editor.getReadOnly()", self._handle_ro)
        while not self._ro_got:
            if refresh_until_end:
                QtWidgets.QApplication.processEvents()
            else:
                time.sleep(0.000001)
        return self._ro

    def _handle_ro(self, ro: bool):
        self._ro = ro
        self._ro_got = True

    def clear(self):
        self.setText("")

    def clearAnnotations(self, isPrerun=False):
        self.page().runJavaScript(
            """if (window.editor!=undefined){
            editor.session.clearAnnotations()
        }"""
        )

    @typing.overload
    def addAnnotation(self, annotation: core.Annotation): ...
    @typing.overload
    def addAnnotation(self, row: int, col: int, txt: str, type: str): ...
    @typing.overload
    def addAnnotation(self, row: int, txt: str, type: str): ...
    def addAnnotation(
        self,
        anno_or_row: int | core.Annotation,
        col: int = None,
        txt: str = None,
        type_: str = None,
        isPrerun=False,
    ):
        if type(anno_or_row) == core.Annotation:
            row = anno_or_row.row()
            col = anno_or_row.column()
            txt = anno_or_row.text()
            type_ = anno_or_row.type()
        elif type(anno_or_row) == int:
            row = anno_or_row
            if type_ == None:
                type_ = txt
                txt = col
                col = 0
        if col is None:
            col = 0
        if not self.loaded:
            self._to_set_anno = True
            self._anno = core.Annotation(row, col, txt, type_)
            self._annos_to_set.append(self._anno)
            return
        anno = (
            """[{
                    row: {line_num},
                    column: {0},  // 列号（0 表示整行）
                    text: "{error_msg}",  // 错误信息
                    type: "{error}"  // 类型：error/warning/info
                }]""".replace(
                "{line_num}", str(row)
            )
            .replace("{0}", str(col))
            .replace("{error_msg}", utils.transText(txt))
            .replace("{error}", utils.transText(type_))
        )
        if DEBUG:
            print(anno)
        if isPrerun:
            self._pre_run_code += f"editor.session.setAnnotations({anno});"
            return
        self.page().runJavaScript(f"editor.session.setAnnotations({anno})")

    def _lateAddAnnotation(
        self,
        anno_or_row: int | core.Annotation,
        col: int = None,
        txt: str = None,
        type_: str = None,
        isPrerun=True,
    ):
        if type(anno_or_row) == core.Annotation:
            row = anno_or_row.row()
            col = anno_or_row.column()
            txt = anno_or_row.text()
            type_ = anno_or_row.type()
        elif type(anno_or_row) == int:
            row = anno_or_row
            if type_ == None:
                type_ = txt
                txt = col
                col = 0
        if col is None:
            col = 0
        if not self.loaded:
            self._to_set_anno = True
            self._anno = core.Annotation(row, col, txt, type_)
            return
        anno = (
            """[{
                    row: {line_num},
                    column: {0},  // 列号（0 表示整行）
                    text: "{error_msg}",  // 错误信息
                    type: "{error}"  // 类型：error/warning/info
                }]""".replace(
                "{line_num}", str(row)
            )
            .replace("{0}", str(col))
            .replace("{error_msg}", utils.transText(txt))
            .replace("{error}", utils.transText(type_))
        )
        if DEBUG:
            print(anno)
        if isPrerun:
            a = "{"
            b = "}"
            self._pre_run_code += f"window.setTimeout(function(){a}editor.session.setAnnotations({anno});{b},1000);"  # 后期改进再改用setValue回调吧
            return
        self.page().runJavaScript(f"editor.session.setAnnotations({anno})")

    def addAnnotations(
        self,
        annos: typing.List[core.Annotation],
        isPrerun=False,
    ):
        if not self.loaded:
            self._to_set_anno = True
            self._anno = core.Annotation(row, col, txt, type_)
            self._annos_to_set.append(self._anno)
            return
        if not isPrerun:
            self.page().runJavaScript(
                "annos_late_add = editor.session.getAnnotations();"
            )
        for i in annos:
            row = i.row()
            col = i.column()
            txt = i.text()
            type_ = i.type()
            anno = (
                """{
                    row: {line_num},
                    column: {0},  // 列号（0 表示整行）
                    text: "{error_msg}",  // 错误信息
                    type: "{error}"  // 类型：error/warning/info
                }""".replace(
                    "{line_num}", str(row)
                )
                .replace("{0}", str(col))
                .replace("{error_msg}", utils.transText(txt))
                .replace("{error}", utils.transText(type_))
            )
            if DEBUG:
                print(anno)
            if not isPrerun:
                self.page().runJavaScript(f"annos_late_add=[...annos_late_add,{anno}]")
            else:
                self._pre_run_code += f"annos_to_add=[...annos_to_add,{anno}];"
        if not isPrerun:
            self.page().runJavaScript("editor.session.setAnnotations(annos_late_add);")

    def annotations(self, refresh_until_end=True) -> typing.List[core.Annotation]:
        self.page().runJavaScript(
            "JSON.stringify(editor.session.getAnnotations())", self._handle_annotations
        )
        while not self._got_annos:
            if refresh_until_end:
                QtWidgets.QApplication.processEvents()
            else:
                time.sleep(0.000001)
        ret = list()
        for i in self._g_annos:
            ret.append(core.Annotation.fromDict(i))
        return ret

    def _handle_annotations(self, anno):
        anno = json.loads(anno)
        if DEBUG:
            print(anno, isinstance(anno, list), type(anno))
        self._got_annos = True
        self._g_annos = anno

    def textCursor(self, refresh_until_end=True) -> QtGui.QTextCursor:
        txt = self.text()
        self._doc = QtGui.QTextDocument()
        self._doc.setPlainText(txt)
        self._cursor = QtGui.QTextCursor(self._doc)

        # 1. 从Ace获取：锚点(anchor)的行列 + 光标(position)的行列
        ace_anchor_row, ace_anchor_col = self._get_selection(refresh_until_end)
        ace_cursor_row, ace_cursor_col = self._get_cursor_pos(refresh_until_end)
        ace_lines = txt.split("\n")

        # 2. 正确计算：锚点的绝对位置 + 光标的绝对位置
        anchor_abs = self._get_cursor_absolute_position_from_row_col(
            ace_anchor_row, ace_anchor_col, ace_lines
        )
        cursor_abs = self._get_cursor_absolute_position_from_row_col(
            ace_cursor_row, ace_cursor_col, ace_lines
        )

        # 3. 核心修复：生成Qt选区的正确逻辑（锚点固定，光标移动）
        self._cursor.setPosition(
            anchor_abs, QtGui.QTextCursor.MoveAnchor
        )  # 锚点=起始位
        self._cursor.setPosition(
            cursor_abs, QtGui.QTextCursor.KeepAnchor
        )  # 光标=结束位，保留锚点

        # 调试信息（可保留）
        if DEBUG:
            print(
                f"Ace同步到Qt → 锚点绝对位置: {anchor_abs}, 光标绝对位置: {cursor_abs}"
            )
            print(
                f"Ace行列 → 锚点:({ace_anchor_row},{ace_anchor_col}), 光标:({ace_cursor_row},{ace_cursor_col})"
            )
        return self._cursor

    def _get_cursor_pos(self, refresh_until_end=True):
        self._got_pos = False
        self.page().runJavaScript(
            "JSON.stringify(editor.getCursorPosition())", self._handle_cur_pos
        )
        while not self._got_pos:
            if refresh_until_end:
                QtWidgets.QApplication.processEvents()
            else:
                time.sleep(0.0000001)
        return self._pos

    def _get_cursor_abs_pos(self, refresh_until_end=True):
        self._got_abs_pos = False
        self.page().runJavaScript(
            "getCursorAbsolutePosition(editor)", self._handle_cur_abs_pos
        )
        while not self._got_abs_pos:
            if refresh_until_end:
                QtWidgets.QApplication.processEvents()
            else:
                time.sleep(0.0000001)
        print("position got:", self._abs_pos)
        return self._abs_pos

    def _get_selection(self, refresh_until_end=True):
        self._got_cur_selection = False
        self.page().runJavaScript(
            "JSON.stringify(editor.selection.getAnchor())", self._handle_selection
        )
        while not self._got_cur_selection:
            if refresh_until_end:
                QtWidgets.QApplication.processEvents()
            else:
                time.sleep(0.0000001)
        print("selection got:", self._cur_selection)
        return self._cur_selection

    def _handle_cur_pos(self, pos):
        if DEBUG:
            print(pos)
        if not pos:
            return None
        dic = json.loads(pos)
        self._pos = dic["row"], dic["column"]
        self._got_pos = True

    def _handle_selection(self, pos):
        if DEBUG:
            print(pos)
        if not pos:
            return None
        dic = json.loads(pos)
        self._cur_selection = dic["row"], dic["column"]
        self._got_cur_selection = True

    def _handle_cur_abs_pos(self, pos):
        if DEBUG:
            print(pos)
        self._abs_pos = int(float(pos))
        self._got_abs_pos = True

    def setTextCursor(self, cursor: QtGui.QTextCursor):
        # 1. 获取 选区结束点(lead) → Qt的cursor.position() 对应Ace的end
        end_row = cursor.blockNumber()
        end_col = cursor.position() - cursor.block().position()

        # 2. 获取 选区锚点(anchor) → Qt的cursor.anchor() 对应Ace的start
        anchor_cursor = QtGui.QTextCursor(cursor.document())
        anchor_cursor.setPosition(cursor.anchor())
        anchor_row = anchor_cursor.blockNumber()
        anchor_col = cursor.anchor() - anchor_cursor.block().position()

        # ========== 新增：防重合调试 ==========
        if DEBUG:
            print(
                f"Qt同步到Ace → 锚点:({anchor_row},{anchor_col}), 光标:({end_row},{end_col})"
            )
            if anchor_row == end_row and anchor_col == end_col:
                print("⚠️ 锚点和光标重合，无选区")

        # 3. 拼接Ace的正确选区API
        js_code = f"""
    editor.selection.setRange({{
        start: {{row: {anchor_row}, column: {anchor_col}}},
        end: {{row: {end_row}, column: {end_col}}}
    }});
    """
        self.page().runJavaScript(js_code)

    def document(self) -> QtGui.QTextDocument:
        self._doc = QtGui.QTextDocument()
        self._doc.setPlainText(self.text())
        return self._doc

    def selectAll(self):
        self.page().runJavaScript("editor.selectAll();")

    def _get_cursor_absolute_position_from_row_col(
        self, row: int, col: int, ace_lines: list
    ) -> int:
        """
        从 Ace Editor 的行号、列号计算光标绝对索引（对应原 JS 逻辑）
        :param row: Ace 编辑器的行号（从 0 开始）
        :param col: Ace 编辑器的列号（从 0 开始）
        :param ace_lines: Ace 编辑器的所有行内容（列表，每个元素是一行文本）
        :return: 绝对字符索引
        """
        absolute_pos = 0
        # 累加前 row 行的字符数（包含换行符 \n，算 1 个字符）
        for i in range(row):
            # 每行字符数 + 换行符的 1 个字符
            absolute_pos += len(ace_lines[i]) + 1
        # 加上当前行的列号
        absolute_pos += col
        return absolute_pos

    def setDocument(self, doc: QtGui.QTextDocument):
        self.setText(doc.toPlainText())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    acw = AceCodeWidget()
    acw.show()

    def test():
        acw.setText(
            """
def test(self):
                print(self)
test("0000")"""
        )
        acw.setMode(constants.BuiltinModes.PYTHON)
        acw.setTheme(constants.BuiltinThemes.CHAOS)
        # acw.clearAnnotations()
        acw.addAnnotation(core.Annotation(0, "Hello World!", acw.AnnotationTypes.Info))
        acw.addAnnotation(core.Annotation(1, "test", acw.AnnotationTypes.Warning))
        print("txt:", acw.text())
        print("thm:", acw.theme())
        print("mod:", acw.mode())
        acw.textChanged.connect(lambda: print(acw.text()))

    test()  # 现在初始调用也能生效了

    print("QWebEngineView 远程调试已启用")
    print(f"请在浏览器中访问: http://localhost:9222 进行调试")

    # 测试定时器（可选）
    test_qt = QtCore.QTimer()
    test_qt.timeout.connect(test)
    # test_qt.start(1000)  # 取消注释可测试定时更新

    sys.exit(app.exec())
