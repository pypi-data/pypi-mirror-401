__author__ = "ziyan.yin"
__describe__ = ""


from libc.stdlib cimport strtol
from libc.string cimport memmove, strlen


cdef inline size_t _unquote(char* c_string, bint change_plus):
    cdef:
        int i = 0
        char[2] quote
        size_t n = strlen(c_string)

    while i < n:
        if c_string[i] == '+' and change_plus:
            c_string[i] = ' '
        elif c_string[i] == '%':
            quote[0] = c_string[i + 1]
            quote[1] = c_string[i + 2]
            c_string[i] = strtol(quote, NULL, 16)
            memmove(c_string + i + 1,  c_string + i + 3, n - i - 2)
            n -= 2
        i += 1
    return n


def unquote(val: bytes, encoding: str = "utf-8") -> str:
    return val[:_unquote(val, 0)].decode(encoding)


def unquote_plus(val: bytes, encoding: str = "utf-8") -> str:
    return val[:_unquote(val, 1)].decode(encoding)


def parse_qsl(qs: bytes, keep_blank_values: bool = False) -> list[tuple[str, str]]:
    query_args = qs.split(b'&') if qs else []
    r = []
    for name_value in query_args:
        if not name_value:
            continue
        nv = name_value.split(b'=')
        if len(nv) < 2:
            if not keep_blank_values:
                continue
            nv.append(b'')
        name = unquote_plus(nv[0])
        value = unquote_plus(nv[1])
        r.append((name, value))
    return r
