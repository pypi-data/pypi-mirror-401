from typing import TextIO, Union, Tuple

def detect_language(code: Union[str, TextIO]) -> Tuple[str, int]:
    """
    Erkennt die Programmiersprache anhand von Schlüsselwörtern in einem größeren Codeausschnitt.

    Parameter:
        code (str | TextIO): Quellcode als String oder Dateiobjekt.

    Returns:
        Tuple[str, int]: Vermutete Sprache und Score (Anzahl gefundener Schlüsselwörter).

    Hinweis:
        - Analyse basiert auf mehreren Schlüsselwörtern pro Sprache.
        - Maximal 5 MB werden aus Dateiobjekten gelesen, um Speicher zu schonen.
    """
    MAX_READ_SIZE = 5 * 1024 * 1024  # 5 MB

    if code is None:
        return "unknown", 0

    # Code aus Dateiobjekt lesen
    if hasattr(code, "read"):
        try:
            code_content = code.read(MAX_READ_SIZE)
        except Exception:
            return "unknown", 0
        code = code_content

    if not isinstance(code, str):
        raise TypeError(f"code muss str oder TextIO sein, nicht {type(code).__name__}")

    if not code.strip():
        return "unknown", 0

    code_lower = code.lower()

    # Schlüsselwörter für verschiedene Sprachen
    keywords = {
        # =========================
        # Skript- & Hochsprachen
        # =========================
        "python": [
            "def ", "import ", "class ", "print(", "self",
            "elif ", "except ", "lambda ", "__init__", "yield "
        ],

        "javascript": [
            "function ", "console.log", "var ", "let ", "const ",
            "=>", "document.", "window.", "async ", "await "
        ],

        "typescript": [
            "interface ", "type ", "implements ", "readonly ",
            "public ", "private ", "import ", "export "
        ],

        "java": [
            "public class", "System.out.println",
            "import java", "extends ", "implements ",
            "static void", "@Override"
        ],

        "c": [
            "#include", "int ", "printf(", "scanf(",
            "void ", "struct ", "malloc(", "sizeof("
        ],

        "c++": [
            "#include", "std::", "cout", "cin",
            "template ", "namespace ", "class ", "::"
        ],

        "c#": [
            "using System", "namespace ", "public class",
            "Console.WriteLine", "get;", "set;", "async ", "await "
        ],

        "go": [
            "package ", "func ", "import ", "defer ",
            "go ", "chan ", "struct ", "interface{}"
        ],

        "rust": [
            "fn ", "let ", "mut ", "pub ",
            "impl ", "struct ", "enum ", "match "
        ],

        "ruby": [
            "def ", "end", "puts ",
            "class ", "module ", "require ",
            "@@", "attr_"
        ],

        "php": [
            "<?php", "echo ", "$",
            "function ", "namespace ",
            "use ", "->", "::"
        ],

        # =========================
        # Web / Markup
        # =========================
        "html": [
            "<!DOCTYPE html", "<html", "<head", "<body",
            "<div", "<span", "<a ", "<script", "<style"
        ],

        "css": [
            "{", "}", ":", ";",
            "display:", "position:", "flex",
            "grid", "@media"
        ],

        "xml": [
            "<?xml", "</", "/>", "<tag", "xmlns"
        ],

        "json": [
            "{", "}", ":", "[", "]", "\""
        ],

        "yaml": [
            "---", ":", "- ", "#"
        ],

        # =========================
        # System / Scripting
        # =========================
        "bash": [
            "#!/bin/bash", "echo ", "fi", "then",
            "$(", "chmod ", "export ", "sudo "
        ],

        "powershell": [
            "Write-Host", "Get-Item", "Set-Item",
            "$_", "param(", "function ", "-Name"
        ],

        "batch": [
            "@echo off", "set ", "if ", "goto ",
            "%1", "%~dp0"
        ],

        # =========================
        # Mobile / Enterprise
        # =========================
        "kotlin": [
            "fun ", "val ", "var ",
            "data class", "when ", "object "
        ],

        "swift": [
            "func ", "let ", "var ",
            "class ", "struct ", "enum ",
            "import UIKit"
        ],

        "dart": [
            "void main", "import ",
            "class ", "final ", "async ", "await "
        ],

        # =========================
        # Daten / Wissenschaft
        # =========================
        "r": [
            "<-", "library(", "data.frame",
            "ggplot", "function(", "NA"
        ],

        "matlab": [
            "function ", "end",
            "plot(", "zeros(", "ones(", "%"
        ],

        "julia": [
            "function ", "end",
            "using ", "struct ", "::"
        ],

        # =========================
        # Sonstige / Spezial
        # =========================
        "lua": [
            "function ", "end",
            "local ", "nil", "then "
        ],

        "haskell": [
            "::", "->", "where ",
            "let ", "data ", "deriving "
        ],

        "assembly": [
            "mov ", "jmp ", "call ",
            "ret", "eax", "ebx"
        ],

        "sql": [
            "SELECT ", "FROM ", "WHERE ",
            "INSERT ", "UPDATE ", "DELETE ",
            "JOIN ", "CREATE TABLE"
        ],

        "markdown": [
            "# ", "## ", "```", "- ",
            "* ", "> ", "[", "]("
        ]
    }

    scores = {lang: 0 for lang in keywords}

    for lang, keys in keywords.items():
        for key in keys:
            scores[lang] += code_lower.count(key)

    best_lang = max(scores, key=scores.get)
    best_score = scores[best_lang]

    if best_score == 0:
        return "unknown", 0

    return best_lang, best_score
