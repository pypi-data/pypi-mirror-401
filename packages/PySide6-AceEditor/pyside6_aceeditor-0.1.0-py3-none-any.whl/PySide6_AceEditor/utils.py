def transText(txt: str):
    a = txt.replace('"', '\\"').replace("'", "\\'")
    b = a.replace("\n", "\\\n\\n")
    return b


def transBool(bool_: bool):
    return str(bool_).lower()
