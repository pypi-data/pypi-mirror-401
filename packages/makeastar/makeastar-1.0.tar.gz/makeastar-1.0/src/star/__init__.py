__version__ = "1.0"
__author__ = "Rheehose (Rhee Creative)"
__email__ = "rheehose@rheehose.com"

import sys
import re
from typing import Optional, Union

def _draw(lines) -> None:
    """Output lines with optimized I/O."""
    sys.stdout.write('\n'.join(lines) + '\n')

def _calc(w: int, h: int, i: int) -> int:
    """Calculate proportional width at step i."""
    return i if w == h else (w * i) // h

def _normalize_int(value: Union[int, float, str, None], default: Optional[int] = None) -> Optional[int]:
    """Normalize input to integer, handling various formats flexibly."""
    if value is None:
        return default
    try:
        # Handle string inputs with flexible parsing (remove spaces, convert comma/dot)
        if isinstance(value, str):
            value = value.strip().replace(' ', '')
        return int(float(value))
    except (ValueError, TypeError):
        return default

def triangle(width: Union[int, str], height: Union[int, str, None] = None, char: str = '*') -> None:
    """Left-aligned triangle (samgak)."""
    w = _normalize_int(width, 5)
    h = _normalize_int(height, w)
    if h == 0 or w == 0: return
    _draw(f"{char * _calc(w, h, i)}" for i in range(1, h + 1))

def right_triangle(width: Union[int, str], height: Union[int, str, None] = None, char: str = '*') -> None:
    """Right-aligned triangle (usamgak)."""
    w = _normalize_int(width, 5)
    h = _normalize_int(height, w)
    if h == 0 or w == 0: return
    _draw(f"{char * _calc(w, h, i):>{w}}" for i in range(1, h + 1))

def inverted(width: Union[int, str], height: Union[int, str, None] = None, char: str = '*') -> None:
    """Inverted left-aligned triangle (yeoksamgak)."""
    w = _normalize_int(width, 5)
    h = _normalize_int(height, w)
    if h == 0 or w == 0: return
    _draw(f"{char * _calc(w, h, i)}" for i in range(h, 0, -1))

def inverted_right(width: Union[int, str], height: Union[int, str, None] = None, char: str = '*') -> None:
    """Inverted right-aligned triangle (yeokusamgak)."""
    w = _normalize_int(width, 5)
    h = _normalize_int(height, w)
    if h == 0 or w == 0: return
    _draw(f"{char * _calc(w, h, i):>{w}}" for i in range(h, 0, -1))

def pyramid(n: Union[int, str] = 5, char: str = '*') -> None:
    """Centered pyramid."""
    size = _normalize_int(n, 5)
    if size == 0: return
    width = 2 * size - 1
    _draw(f"{char * (2 * i - 1):^{width}}".rstrip() for i in range(1, size + 1))

def diamond(n: Union[int, str] = 5, char: str = '*') -> None:
    """Diamond shape."""
    size = _normalize_int(n, 5)
    if size == 0: return
    width = 2 * size - 1
    top = [f"{char * (2 * i - 1):^{width}}".rstrip() for i in range(1, size + 1)]
    _draw(top + top[-2::-1])

def hourglass(n: Union[int, str] = 5, char: str = '*') -> None:
    """Hourglass shape."""
    size = _normalize_int(n, 5)
    if size == 0: return
    width = 2 * size - 1
    top = [f"{char * (2 * i - 1):^{width}}".rstrip() for i in range(size, 0, -1)]
    _draw(top + top[-2::-1])

def arrow(n: Union[int, str] = 5, char: str = '*') -> None:
    """Right-pointing arrow."""
    size = _normalize_int(n, 5)
    if size == 0: return
    part = [f"{char * i}" for i in range(1, size + 1)]
    _draw(part + part[-2::-1])

def draw(command: str) -> None:
    """
    Parse and execute a star pattern command from a string.
    Flexible parsing - handles spaces, commas, dots, etc.
    
    Examples:
        draw("triangle 5 10")
        draw("pyramid, 7")
        draw("diamond.3")
    """
    # Normalize: replace common separators with space
    normalized = re.sub(r'[,.\s]+', ' ', command.strip())
    parts = normalized.split()
    
    if not parts:
        return
    
    func_name = parts[0].lower()
    args = [_normalize_int(p, 5) for p in parts[1:]]
    
    # Map function names to actual functions
    func_map = {
        'triangle': triangle, 'tri': triangle, 'samgak': triangle,
        'right': right_triangle, 'rtri': right_triangle, 'usamgak': right_triangle,
        'inverted': inverted, 'inv': inverted, 'yeoksamgak': inverted,
        'inverted_right': inverted_right, 'rinv': inverted_right, 'rtinv': inverted_right,
        'pyramid': pyramid, 'pyra': pyramid,
        'diamond': diamond, 'dia': diamond,
        'hourglass': hourglass, 'morae': hourglass,
        'arrow': arrow, 'hwasal': arrow,
    }
    
    func = func_map.get(func_name)
    if func:
        func(*args)

# Aliases (Easy access & Korean phonetics)
samgak = tri = triangle
usamgak = rtri = right_triangle
yeoksamgak = inv = inverted
yeokusamgak = rinv = rtinv = inverted_right
pyra = pyramid
dia = diamond
morae = hourglass
hwasal = arrow

# Korean Hangul Aliases (Full)
삼각형 = triangle
우측삼각형 = 오른쪽삼각형 = right_triangle
역삼각형 = inverted
우측역삼각형 = 오른쪽역삼각형 = inverted_right
피라미드 = pyramid
다이아몬드 = 다이아 = diamond
모래시계 = hourglass
화살표 = arrow

# Korean Short Aliases (줄임말)
삼 = triangle
우삼 = right_triangle
역삼 = inverted
우역 = inverted_right
피라 = pyramid
다 = diamond
모 = hourglass
화 = arrow

# Korean Choseong Aliases (초성)
ㅅㄱ = ㅅㄱㅎ = triangle
ㅇㅅㄱ = ㅇㅊㅅㄱㅎ = ㅇㄹㅉㅅㄱㅎ = right_triangle
ㅇㅅ = ㅇㅅㄱㅎ = inverted
ㅇㅇ = ㅇㅊㅇㅅㄱㅎ = ㅇㄹㅉㅇㅅㄱㅎ = inverted_right
ㅍㄹ = ㅍㄹㅁㄷ = pyramid
ㄷㅇ = ㄷㅇㅇㅁㄷ = diamond
ㅁㄹ = ㅁㄹㅅㄱ = hourglass
ㅎㅅ = ㅎㅅㅍ = arrow
