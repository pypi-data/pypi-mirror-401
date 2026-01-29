from setuptools import setup, find_packages
import os

# 你的包元信息
VERSION = "0.1.0"
RELEASE_NAME = "PySide6-AceEditor"  # pip install 的发布名称（可以带中横线）
PACKAGE_NAME = "PySide6_AceEditor"  # 源码文件夹的真实名称（必须是下划线，和你的文件夹一致！）

setup(
    name=RELEASE_NAME,
    version=VERSION,
    packages=find_packages(),  # 自动发现所有Python包
    #include_package_data=True,  # ✅ 关键1：开启「包含包内数据文件」
    package_data={
        # ✅ 关键2：声明需要打包的非Python文件
        # 格式：{"包名": ["要包含的文件/目录规则"]}
        PACKAGE_NAME: [
            "runtime/*",  # 包含runtime目录下所有文件
            "runtime/**/*",  # 递归包含runtime的所有子目录+文件（必须加！）
            # 如果你还有其他文件，比如ui文件/json文件，继续加
            # "*.ui", "*.json", "*.html"
        ]
    },
    install_requires=[
        "PySide6>=6.5.0",
        "websockets>=12.0",
        "pyperclip>=1.8.2",
    ],
    author="wry",
    author_email="wry_by01@outlook.com",
    description="基于PySide6的Ace编辑器组件，内置Ace Editor前端资源\nAce Editor widget based on PySide6 with Ace Editor frontend resources included",
    python_requires=">=3.8",
    url="https://github.com/wangruoyuyuyu/PySide6-AceEditor/",
    entry_points={
        "console_scripts": [
            # 语法规则：自定义命令名 = 包名.文件名:入口函数名
            "PySide6-AceEditor-Examples = PySide6_AceEditor.__main__:main",
        ]
    },
)
