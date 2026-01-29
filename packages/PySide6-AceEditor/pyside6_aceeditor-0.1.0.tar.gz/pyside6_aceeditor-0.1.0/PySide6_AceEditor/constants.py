EDITOR_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ace Editor</title>
    <!-- 引入Ace编辑器库 -->
    <!--script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.32.6/ace.js"></script-->
    <script src="./ace.min.js"></script>
    <style>
        /* 确保页面没有边距和滚动条 */
        body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            overflow: hidden;
        }
        
        /* 编辑器容器占满整个页面 */
        #editor {
            position: absolute;
            top: 0;
            right: 0;
            bottom: 0;
            left: 0;
        }
    </style>
</head>
<body>
    <!-- 编辑器容器 -->
    <div id="editor"><!--// 这是Ace编辑器
function greet() {
    console.log("Hello, Ace Editor!");
}

// 尝试编辑这段代码
let message = "欢迎使用Ace编辑器";
console.log(message);--></div>

    <script>
    var annos_to_add = new Array();
    var annos_late_add = new Array();
    function getCursorAbsolutePosition(editor) {
    // 1. 获取光标行号和列号
    var cursor = editor.getCursorPosition(); // {row: 0, column: 5}
    var row = cursor.row;
    var column = cursor.column;

    // 2. 获取文档所有行
    //var lines = editor.session.getLines();
    let absolutePos = 0;

    // 3. 累加前 row 行的字符数（包括换行符，\n 算 1 个字符）
    for (let i = 0; i < row; i++) {
        // 每行内容的字符数 + 换行符（\n）的字符数
        absolutePos += editor.session.getLine(i).length + 1;
    }

    // 4. 加上当前行的列号
    absolutePos += column;

    return absolutePos;
}

// 调用示例
//const absoluteIndex = getCursorAbsolutePosition(editor);
//console.log("光标绝对索引：", absoluteIndex);
        // 初始化Ace编辑器
        const editor = ace.edit("editor");
        
        // 设置编辑器主题
        editor.setTheme("ace/theme/monokai");
        
        // 设置语言模式为JavaScript
        editor.session.setMode("ace/mode/javascript");
        
        // 设置一些基本配置
        editor.setShowPrintMargin(false); // 隐藏打印边距
        editor.setFontSize(14); // 设置字体大小
        
        var ws_connected=false
        window.onload = function(){
            window.ws=new WebSocket("ws://localhost:8765");
            ws.onopen=function(){
                console.log("connected");
                window.ws_connected=true;
            }
            editor.on("change",function(){
                    console.log("changed with ws connected:"+ws_connected);
                    if (ws_connected){
                        ws.send("changed");
                    };
                });
        }
    </script>
</body>
</html>
"""


class BuiltinThemes:
    """
    Ace编辑器内置主题常量类
    对应文件：theme-xxx.js，值为Ace加载主题时的路径
    """

    # 基础主题
    AMBIANCE = "ace/theme/ambiance"
    CHAOS = "ace/theme/chaos"
    CHROME = "ace/theme/chrome"
    CLOUDS = "ace/theme/clouds"
    CLOUDS_MIDNIGHT = "ace/theme/clouds_midnight"
    COBALT = "ace/theme/cobalt"
    CRIMSON_EDITOR = "ace/theme/crimson_editor"
    DAWN = "ace/theme/dawn"
    DRACULA = "ace/theme/dracula"
    DREAMWEAVER = "ace/theme/dreamweaver"
    ECLIPSE = "ace/theme/eclipse"
    GITHUB = "ace/theme/github"
    GITHUB_DARK = "ace/theme/github_dark"
    GITHUB_LIGHT_DEFAULT = "ace/theme/github_light_default"
    GOB = "ace/theme/gob"
    GRUVBOX = "ace/theme/gruvbox"
    GRUVBOX_DARK_HARD = "ace/theme/gruvbox_dark_hard"
    GRUVBOX_LIGHT_HARD = "ace/theme/gruvbox_light_hard"
    IDLE_FINGERS = "ace/theme/idle_fingers"
    IPLASTIC = "ace/theme/iplastic"
    KATZENMILCH = "ace/theme/katzenmilch"
    KR_THEME = "ace/theme/kr_theme"
    KUROIR = "ace/theme/kuroir"
    MERBIVORE = "ace/theme/merbivore"
    MERBIVORE_SOFT = "ace/theme/merbivore_soft"
    MONO_INDUSTRIAL = "ace/theme/mono_industrial"
    MONOKAI = "ace/theme/monokai"  # 你之前使用的主题
    NORD_DARK = "ace/theme/nord_dark"
    ONE_DARK = "ace/theme/one_dark"
    PASTEL_ON_DARK = "ace/theme/pastel_on_dark"
    SOLARIZED_DARK = "ace/theme/solarized_dark"
    SOLARIZED_LIGHT = "ace/theme/solarized_light"
    SQLSERVER = "ace/theme/sqlserver"
    TERMINAL = "ace/theme/terminal"
    TEXTMATE = "ace/theme/textmate"
    TOMORROW = "ace/theme/tomorrow"
    TOMORROW_NIGHT = "ace/theme/tomorrow_night"
    TOMORROW_NIGHT_BLUE = "ace/theme/tomorrow_night_blue"
    TOMORROW_NIGHT_BRIGHT = "ace/theme/tomorrow_night_bright"
    TOMORROW_NIGHT_EIGHTIES = "ace/theme/tomorrow_night_eighties"
    TWILIGHT = "ace/theme/twilight"
    VIBRANT_INK = "ace/theme/vibrant_ink"
    XCODE = "ace/theme/xcode"
    # Cloud9系列主题
    CLOUD9_DAY = "ace/theme/cloud9_day"
    CLOUD9_NIGHT = "ace/theme/cloud9_night"
    CLOUD9_NIGHT_LOW_COLOR = "ace/theme/cloud9_night_low_color"
    # 新增Cloud Editor主题
    CLOUD_EDITOR = "ace/theme/cloud_editor"
    CLOUD_EDITOR_DARK = "ace/theme/cloud_editor_dark"


class BuiltinModes:
    """
    Ace编辑器内置语言模式常量类
    对应文件：mode-xxx.js，值为Ace加载语言模式时的路径
    """

    # 常用编程语言
    PYTHON = "ace/mode/python"  # 你可能需要的Python模式
    JAVASCRIPT = "ace/mode/javascript"
    TYPESCRIPT = "ace/mode/typescript"
    JSX = "ace/mode/jsx"
    TSX = "ace/mode/tsx"
    JAVA = "ace/mode/java"
    C_CPP = "ace/mode/c_cpp"  # C/C++模式
    CSHARP = "ace/mode/csharp"
    GO = "ace/mode/golang"  # Go语言
    RUBY = "ace/mode/ruby"
    PHP = "ace/mode/php"
    PHP_LARAVEL_BLADE = "ace/mode/php_laravel_blade"
    SWIFT = "ace/mode/swift"
    KOTLIN = "ace/mode/kotlin"
    RUST = "ace/mode/rust"
    DART = "ace/mode/dart"
    LUA = "ace/mode/lua"
    R = "ace/mode/r"
    PERL = "ace/mode/perl"
    SCALA = "ace/mode/scala"
    CLOJURE = "ace/mode/clojure"
    ELIXIR = "ace/mode/elixir"
    RAKU = "ace/mode/raku"
    JULIA = "ace/mode/julia"
    ODIN = "ace/mode/odin"
    ZIG = "ace/mode/zig"

    # 脚本/配置文件
    BASH = "ace/mode/sh"  # Shell/Bash模式
    POWERSHELL = "ace/mode/powershell"
    BATCHFILE = "ace/mode/batchfile"
    MAKEFILE = "ace/mode/makefile"
    JSON = "ace/mode/json"
    JSON5 = "ace/mode/json5"
    YAML = "ace/mode/yaml"
    TOML = "ace/mode/toml"
    INI = "ace/mode/ini"
    CSV = "ace/mode/csv"
    TSV = "ace/mode/tsv"

    # Web相关
    HTML = "ace/mode/html"
    CSS = "ace/mode/css"
    SCSS = "ace/mode/scss"
    SASS = "ace/mode/sass"
    LESS = "ace/mode/less"
    STYLUS = "ace/mode/stylus"
    VUE = "ace/mode/vue"
    ASTRO = "ace/mode/astro"
    EJS = "ace/mode/ejs"
    HANDLEBARS = "ace/mode/handlebars"
    JADE = "ace/mode/jade"
    SLIM = "ace/mode/slim"
    NUNJUCKS = "ace/mode/nunjucks"
    TWIG = "ace/mode/twig"

    # 数据库相关
    SQL = "ace/mode/sql"
    MYSQL = "ace/mode/mysql"
    PGSQL = "ace/mode/pgsql"
    SQLSERVER = "ace/mode/sqlserver"
    REDSHIFT = "ace/mode/redshift"
    SPARQL = "ace/mode/sparql"

    # 文档相关
    MARKDOWN = "ace/mode/markdown"
    RST = "ace/mode/rst"
    LATEX = "ace/mode/latex"
    TEX = "ace/mode/tex"
    PLAIN_TEXT = "ace/mode/plain_text"  # 纯文本模式

    # 其他常用模式
    XML = "ace/mode/xml"
    XQUERY = "ace/mode/xquery"
    DIFF = "ace/mode/diff"
    PROTOBUF = "ace/mode/protobuf"
    TERRAFORM = "ace/mode/terraform"
    PRQL = "ace/mode/prql"
    LOGIQL = "ace/mode/logiql"
    PARTIQL = "ace/mode/partiql"
