from typing import Any, Dict, List

class NDCAParseError(Exception):
    pass

class NDCAParser:
    def __init__(self, text: str):
        self.text = text
        self.i = 0
        self.n = len(text)
        self.line = 1
        self.col = 1

    def _peek(self) -> str:
        if self.i < self.n:
            return self.text[self.i]
        return ""

    def _next(self) -> str:
        ch = self._peek()
        if ch:
            self.i += 1
            if ch == "\n":
                self.line += 1
                self.col = 1
            else:
                self.col += 1
        return ch

    def _error(self, msg: str) -> None:
        raise NDCAParseError(f"{msg} at line {self.line} col {self.col}")

    def _consume_comment(self) -> None:
        if self._next() != "*":
            self._error("expected '*' to start comment")
        while True:
            ch = self._next()
            if ch == "":
                self._error("unterminated comment")
            if ch == "*":
                return

    def _skip_ws(self) -> None:
        while True:
            ch = self._peek()
            if ch == "":
                return
            if ch.isspace():
                self._next()
                continue
            if ch == "*":
                self._consume_comment()
                continue
            return

    def parse(self) -> Dict[str, Any]:
        self._skip_ws()
        if self._peek() != "<":
            self._error("document must start with '<'")
        obj = self._parse_object()
        self._skip_ws()
        if self.i < self.n:
            rest = self.text[self.i:].strip()
            if rest != "":
                self._error("extra data after document")
        return obj

    def _parse_object(self) -> Dict[str, Any]:
        if self._next() != "<":
            self._error("expected '<' to start object")
        obj: Dict[str, Any] = {}
        self._skip_ws()
        while True:
            self._skip_ws()
            if self._peek() == ">":
                self._next()
                break
            if self._peek() != "[":
                self._error("expected '[' for key")
            key = self._parse_key()
            self._skip_ws()
            if self._next() != "=":
                self._error("expected '=' after key")
            self._skip_ws()
            val = self._parse_value()
            obj[key] = val
            self._skip_ws()
            if self._peek() == ";":
                self._next()
                self._skip_ws()
                continue
            elif self._peek() == ">":
                self._next()
                break
            else:
                self._error("expected ';' or '>' after value")
        return obj

    def _parse_key(self) -> str:
        if self._next() != "[":
            self._error("expected '[' to start key")
        start = self.i
        while True:
            ch = self._peek()
            if ch == "":
                self._error("unterminated key")
            if ch == "]":
                end = self.i
                self._next()
                break
            self._next()
        key = self.text[start:end]
        return key

    def _parse_value(self):
        self._skip_ws()
        ch = self._peek()
        if ch == "\"":
            return self._parse_string()
        if ch == "<":
            return self._parse_object()
        if ch == "(":
            return self._parse_list()
        if ch == "":
            self._error("unexpected EOF when parsing value")
        token = self._parse_token()
        if token in ("true", "false", "null"):
            if token == "true":
                return True
            if token == "false":
                return False
            return None
        try:
            if "." in token or "e" in token or "E" in token:
                return float(token)
            return int(token)
        except Exception:
            return token

    def _parse_string(self) -> str:
        if self._next() != "\"":
            self._error('expected \'"\' to start string')
        buf: List[str] = []
        while True:
            ch = self._next()
            if ch == "":
                self._error("unterminated string")
            if ch == "\\":
                esc = self._next()
                if esc == "":
                    self._error("unterminated escape sequence in string")
                if esc == "n":
                    buf.append("\n")
                elif esc == "r":
                    buf.append("\r")
                elif esc == "t":
                    buf.append("\t")
                elif esc == "\\":
                    buf.append("\\")
                elif esc == "\"":
                    buf.append("\"")
                else:
                    buf.append(esc)
            elif ch == "\"":
                break
            else:
                buf.append(ch)
        return "".join(buf)

    def _parse_list(self) -> List[Any]:
        if self._next() != "(":
            self._error("expected '(' to start list")
        arr: List[Any] = []
        self._skip_ws()
        while True:
            self._skip_ws()
            if self._peek() == ")":
                self._next()
                break
            val = self._parse_value()
            arr.append(val)
            self._skip_ws()
            if self._peek() == ";":
                self._next()
                self._skip_ws()
                continue
            elif self._peek() == ")":
                self._next()
                break
            else:
                self._error("expected ';' or ')' in list")
        return arr

    def _parse_token(self) -> str:
        self._skip_ws()
        start = self.i
        terminators = set(" \t\n\r;()<>]\"=")
        while True:
            ch = self._peek()
            if ch == "" or ch in terminators:
                break
            self._next()
        tok = self.text[start:self.i]
        if tok == "":
            self._error("expected token")
        return tok