"""
Duc Van Nguyen Package v6.0.0
Advanced Python utilities and tools for developers.
"""

__version__ = "6.0.0"
__author__ = "Duc Van Nguyen"

def hello():
    """Return a greeting message."""
    return "Hello from ducvannguyen package v6.0.0!"

def get_info():
    """Return package information."""
    return {
        "name": "ducvannguyen",
        "version": __version__,
        "author": __author__,
        "status": "Advanced utilities package"
    }

def string_utils():
    """String manipulation utilities."""
    return {
        "reverse": lambda s: s[::-1],
        "uppercase": lambda s: s.upper(),
        "lowercase": lambda s: s.lower(),
        "capitalize": lambda s: s.capitalize(),
        "word_count": lambda s: len(s.split()),
        "is_palindrome": lambda s: s.lower() == s.lower()[::-1]
    }

def math_utils():
    """Mathematical utilities."""
    import math
    return {
        "factorial": lambda n: math.factorial(n),
        "fibonacci": lambda n: sum(range(n)) if n <= 1 else sum(range(n)),
        "is_prime": lambda n: n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1)),
        "gcd": lambda a, b: math.gcd(a, b),
        "lcm": lambda a, b: abs(a * b) // math.gcd(a, b) if a and b else 0
    }

def list_utils():
    """List manipulation utilities."""
    return {
        "flatten": lambda lst: [item for sublist in lst for item in (sublist if isinstance(sublist, list) else [sublist])],
        "unique": lambda lst: list(dict.fromkeys(lst)),
        "chunk": lambda lst, size: [lst[i:i + size] for i in range(0, len(lst), size)],
        "shuffle": lambda lst: __import__('random').sample(lst, len(lst)),
        "sum_nested": lambda lst: sum(item if isinstance(item, (int, float)) else sum_nested(item) if isinstance(item, list) else 0 for item in lst)
    }

def file_utils():
    """File operation utilities."""
    import os
    return {
        "get_size": lambda path: os.path.getsize(path) if os.path.exists(path) else 0,
        "get_extension": lambda path: os.path.splitext(path)[1],
        "join_paths": lambda *paths: os.path.join(*paths),
        "is_file": lambda path: os.path.isfile(path),
        "is_dir": lambda path: os.path.isdir(path)
    }

def datetime_utils():
    """Date and time utilities."""
    from datetime import datetime, timedelta
    return {
        "now": lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "today": lambda: datetime.now().date(),
        "add_days": lambda days: (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d"),
        "format_timestamp": lambda ts: datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"),
        "days_between": lambda date1, date2: abs((datetime.strptime(date2, "%Y-%m-%d") - datetime.strptime(date1, "%Y-%m-%d")).days)
    }

def web_utils():
    """Web and URL utilities."""
    from urllib.parse import urlparse, parse_qs
    return {
        "parse_url": lambda url: urlparse(url),
        "get_domain": lambda url: urlparse(url).netloc,
        "is_valid_url": lambda url: bool(urlparse(url).scheme and urlparse(url).netloc),
        "extract_params": lambda url: parse_qs(urlparse(url).query)
    }

def random_utils():
    """Random generation utilities."""
    import random
    import string
    return {
        "random_string": lambda length: ''.join(random.choices(string.ascii_letters + string.digits, k=length)),
        "random_choice": lambda lst: random.choice(lst),
        "random_number": lambda min_val, max_val: random.randint(min_val, max_val),
        "uuid4": lambda: str(__import__('uuid').uuid4()),
        "shuffle_string": lambda s: ''.join(random.sample(s, len(s)))
    }

def validate_utils():
    """Data validation utilities."""
    import re
    return {
        "is_email": lambda email: bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)),
        "is_phone": lambda phone: bool(re.match(r'^\+?1?\d{9,15}$', phone)),
        "is_url": lambda url: bool(re.match(r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)?$', url)),
        "is_strong_password": lambda pwd: len(pwd) >= 8 and bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]', pwd))
    }

def all_utils():
    """Get all available utilities."""
    return {
        "string": string_utils(),
        "math": math_utils(),
        "list": list_utils(),
        "file": file_utils(),
        "datetime": datetime_utils(),
        "web": web_utils(),
        "random": random_utils(),
        "validate": validate_utils()
    }
