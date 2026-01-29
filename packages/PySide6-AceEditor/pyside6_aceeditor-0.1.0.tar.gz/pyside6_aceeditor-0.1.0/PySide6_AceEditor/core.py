from PySide6 import QtCore
import typing


class Annotation(QtCore.QObject):
    class Types:
        Error = "error"
        Warning = "warning"
        Info = "info"

    @typing.overload
    def __init__(self, annotations: typing.Self): ...
    @typing.overload
    def __init__(self, row: int, col: int, txt: str, type: str): ...
    @typing.overload
    def __init__(self, row: int, txt: str, type: str): ...
    def __init__(
        self, row_or_anno=None, col: int = 0, txt: str = None, type_: str = None
    ):
        super().__init__()
        if type(row_or_anno) == int:
            self._row = row_or_anno
            if type_ == None:
                type_ = txt
                txt = col
                col = 0
        elif type(row_or_anno) == type(self):
            self._row = row_or_anno.row()
            self._col = row_or_anno.column()
            self._type = row_or_anno.type()
            self._txt = row_or_anno.text()
            return
        self._col = col
        self._txt = txt
        self._type = type_

    def column(self) -> int:
        return self._col

    def row(self) -> int:
        return self._row

    def type(self) -> str:
        return self._type

    def text(self) -> str:
        return self._txt

    def setText(self, a0: str):
        self._txt = a0

    def setType(self, a0: str):
        self._type = a0

    def setColumn(self, a0: int):
        self._col = a0

    def setRow(self, a0: int | None):
        if a0 is None:
            a0 = 0
        self._row = a0

    def __str__(self):
        return f"{self.type()} @ {self.row()}:{'all'if not self.column() else self.column()} : {self.text()}"

    def __repr__(self):
        return str(self)

    def __iter__(self):
        dic = {
            "row": self.row(),
            "column": self.column(),
            "text": self.text(),
            "type": self.type(),
        }
        for i, j in dic.items():
            yield i, j

    @classmethod
    def fromDict(cls, dic: dict):
        props = ["row", "column", "text", "type"]
        k = []
        for i in props:
            if not i in dic.keys():
                k.append(None)
                continue
            k.append(dic[i])
        return cls(k[0], k[1], k[2], k[3])


if __name__ == "__main__":
    a1 = Annotation(1, 1, "test", "error")
    a2 = Annotation(2, "test", "error")
    a3 = Annotation(a1)
    a4 = Annotation(a2)
    a5 = Annotation.fromDict({"row": 0, "column": 1, "text": 2, "type": "error"})
    print(a1)
    print(a2)
    print(a3)
    print(a4)
    print(a5)
    print(dict(a1), dict(a2), dict(a3), dict(a4), dict(a5))
