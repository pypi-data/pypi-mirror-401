"""
DucVanNguyen Core Class - Professional Python Toolkit
Advanced utilities and tools for developers.
"""

import os
import re
import json
import uuid
import random
import string
import hashlib
import base64
import secrets
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from typing import Any, Dict, List, Optional, Union, Callable


class DucVanNguyen:
    """
    Professional Python toolkit with advanced utilities.
    
    This class provides comprehensive tools for:
    - String manipulation and validation
    - Mathematical operations
    - File and directory operations
    - Web and URL utilities
    - Random generation
    - Data validation
    - Encryption and encoding
    - API utilities
    """
    
    def __init__(self, name: str = "DucVanNguyen", version: str = "7.0.0"):
        self.name = name
        self.version = version
        self._created_at = datetime.now()
        self._session_id = str(uuid.uuid4())
        
    def __str__(self):
        return f"{self.name} v{self.version} - Professional Python Toolkit"
    
    def __repr__(self):
        return f"DucVanNguyen(name='{self.name}', version='{self.version}')"
    
    def info(self) -> Dict[str, Any]:
        """Get toolkit information."""
        return {
            "name": self.name,
            "version": self.version,
            "created_at": self._created_at.isoformat(),
            "session_id": self._session_id,
            "author": "Duc Van Nguyen",
            "description": "Professional Python toolkit with advanced utilities"
        }
    
    # String Utilities
    def reverse_string(self, text: str) -> str:
        """Reverse a string."""
        return text[::-1]
    
    def is_palindrome(self, text: str) -> bool:
        """Check if string is palindrome."""
        cleaned = re.sub(r'[^a-zA-Z0-9]', '', text.lower())
        return cleaned == cleaned[::-1]
    
    def word_count(self, text: str) -> int:
        """Count words in text."""
        return len(text.split())
    
    def char_count(self, text: str, include_spaces: bool = True) -> int:
        """Count characters in text."""
        if include_spaces:
            return len(text)
        return len(text.replace(" ", ""))
    
    def capitalize_words(self, text: str) -> str:
        """Capitalize first letter of each word."""
        return ' '.join(word.capitalize() for word in text.split())
    
    def remove_duplicates(self, text: str) -> str:
        """Remove duplicate characters from string."""
        seen = set()
        result = []
        for char in text:
            if char not in seen:
                seen.add(char)
                result.append(char)
        return ''.join(result)
    
    # Math Utilities
    def factorial(self, n: int) -> int:
        """Calculate factorial."""
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        if n == 0:
            return 1
        return n * self.factorial(n - 1)
    
    def is_prime(self, n: int) -> bool:
        """Check if number is prime."""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        w = 2
        while i * i <= n:
            if n % i == 0:
                return False
            i += w
            w = 6 - w
        return True
    
    def fibonacci(self, n: int) -> int:
        """Calculate nth Fibonacci number."""
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b
    
    def gcd(self, a: int, b: int) -> int:
        """Calculate greatest common divisor."""
        while b:
            a, b = b, a % b
        return a
    
    def lcm(self, a: int, b: int) -> int:
        """Calculate least common multiple."""
        return abs(a * b) // self.gcd(a, b) if a and b else 0
    
    # List Utilities
    def flatten_list(self, lst: List[Any]) -> List[Any]:
        """Flatten nested list."""
        result = []
        for item in lst:
            if isinstance(item, list):
                result.extend(self.flatten_list(item))
            else:
                result.append(item)
        return result
    
    def unique_list(self, lst: List[Any]) -> List[Any]:
        """Remove duplicates from list while preserving order."""
        seen = set()
        result = []
        for item in lst:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    
    def chunk_list(self, lst: List[Any], size: int) -> List[List[Any]]:
        """Split list into chunks of specified size."""
        return [lst[i:i + size] for i in range(0, len(lst), size)]
    
    def shuffle_list(self, lst: List[Any]) -> List[Any]:
        """Shuffle list randomly."""
        return random.sample(lst, len(lst))
    
    # File Utilities
    def get_file_size(self, path: str) -> int:
        """Get file size in bytes."""
        return os.path.getsize(path) if os.path.exists(path) else 0
    
    def get_file_extension(self, path: str) -> str:
        """Get file extension."""
        return os.path.splitext(path)[1]
    
    def join_paths(self, *paths: str) -> str:
        """Join multiple paths."""
        return os.path.join(*paths)
    
    def is_file(self, path: str) -> bool:
        """Check if path is a file."""
        return os.path.isfile(path)
    
    def is_directory(self, path: str) -> bool:
        """Check if path is a directory."""
        return os.path.isdir(path)
    
    # DateTime Utilities
    def now(self, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Get current time formatted."""
        return datetime.now().strftime(format_str)
    
    def today(self) -> str:
        """Get today's date."""
        return datetime.now().date().isoformat()
    
    def add_days(self, days: int, format_str: str = "%Y-%m-%d") -> str:
        """Add days to current date."""
        return (datetime.now() + timedelta(days=days)).strftime(format_str)
    
    def days_between(self, date1: str, date2: str, format_str: str = "%Y-%m-%d") -> int:
        """Calculate days between two dates."""
        d1 = datetime.strptime(date1, format_str)
        d2 = datetime.strptime(date2, format_str)
        return abs((d2 - d1).days)
    
    # Web Utilities
    def parse_url(self, url: str) -> Dict[str, str]:
        """Parse URL into components."""
        parsed = urlparse(url)
        return {
            "scheme": parsed.scheme,
            "netloc": parsed.netloc,
            "path": parsed.path,
            "params": parsed.params,
            "query": parsed.query,
            "fragment": parsed.fragment
        }
    
    def get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        return urlparse(url).netloc
    
    def is_valid_url(self, url: str) -> bool:
        """Validate URL format."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def extract_query_params(self, url: str) -> Dict[str, List[str]]:
        """Extract query parameters from URL."""
        return parse_qs(urlparse(url).query)
    
    # Random Utilities
    def random_string(self, length: int = 10, include_digits: bool = True, 
                    include_symbols: bool = False) -> str:
        """Generate random string."""
        chars = string.ascii_letters
        if include_digits:
            chars += string.digits
        if include_symbols:
            chars += "!@#$%^&*"
        return ''.join(random.choices(chars, k=length))
    
    def random_number(self, min_val: int = 0, max_val: int = 100) -> int:
        """Generate random number in range."""
        return random.randint(min_val, max_val)
    
    def random_choice(self, items: List[Any]) -> Any:
        """Choose random item from list."""
        return random.choice(items)
    
    def generate_uuid(self) -> str:
        """Generate UUID4."""
        return str(uuid.uuid4())
    
    def generate_token(self, length: int = 32) -> str:
        """Generate secure token."""
        return secrets.token_urlsafe(length)
    
    # Validation Utilities
    def is_email(self, email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def is_phone(self, phone: str) -> bool:
        """Validate phone number."""
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, phone))
    
    def is_strong_password(self, password: str) -> bool:
        """Validate strong password."""
        if len(password) < 8:
            return False
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]'
        return bool(re.match(pattern, password))
    
    def is_username(self, username: str) -> bool:
        """Validate username (3-20 chars, alphanumeric and underscore)."""
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return bool(re.match(pattern, username))
    
    # Encryption & Encoding
    def md5_hash(self, text: str) -> str:
        """Generate MD5 hash."""
        return hashlib.md5(text.encode()).hexdigest()
    
    def sha256_hash(self, text: str) -> str:
        """Generate SHA256 hash."""
        return hashlib.sha256(text.encode()).hexdigest()
    
    def base64_encode(self, text: str) -> str:
        """Encode text to base64."""
        return base64.b64encode(text.encode()).decode()
    
    def base64_decode(self, encoded_text: str) -> str:
        """Decode base64 to text."""
        return base64.b64decode(encoded_text).decode()
    
    # API Utilities
    def create_response(self, data: Any, status: str = "success", 
                       message: str = "", code: int = 200) -> Dict[str, Any]:
        """Create standardized API response."""
        return {
            "status": status,
            "code": code,
            "message": message,
            "data": data,
            "timestamp": self.now(),
            "toolkit": f"{self.name} v{self.version}"
        }
    
    def validate_json(self, json_str: str) -> bool:
        """Validate JSON string."""
        try:
            json.loads(json_str)
            return True
        except:
            return False
    
    def format_json(self, data: Any, indent: int = 2) -> str:
        """Format data as pretty JSON."""
        return json.dumps(data, indent=indent, ensure_ascii=False)
    
    # Performance Utilities
    def timer(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Time function execution."""
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        execution_time = (end - start).total_seconds()
        
        return {
            "result": result,
            "execution_time": execution_time,
            "start_time": start.isoformat(),
            "end_time": end.isoformat()
        }
    
    def benchmark(self, func: Callable, iterations: int = 1000, *args, **kwargs) -> Dict[str, Any]:
        """Benchmark function performance."""
        times = []
        for _ in range(iterations):
            start = datetime.now()
            func(*args, **kwargs)
            end = datetime.now()
            times.append((end - start).total_seconds())
        
        return {
            "iterations": iterations,
            "total_time": sum(times),
            "average_time": sum(times) / len(times),
            "min_time": min(times),
            "max_time": max(times),
            "toolkit": f"{self.name} v{self.version}"
        }
    
    # Advanced Features
    def chain(self, *functions) -> Callable:
        """Chain multiple functions together."""
        def chained(x):
            result = x
            for func in functions:
                result = func(result)
            return result
        return chained
    
    def pipe(self, data: Any, *operations) -> Any:
        """Pipe data through multiple operations."""
        result = data
        for operation in operations:
            if callable(operation):
                result = operation(result)
            else:
                raise ValueError("Operation must be callable")
        return result
    
    def memoize(self, func: Callable) -> Callable:
        """Memoize function results."""
        cache = {}
        def wrapper(*args):
            if args in cache:
                return cache[args]
            result = func(*args)
            cache[args] = result
            return result
        return wrapper
    
    def get_all_methods(self) -> List[str]:
        """Get all available methods."""
        return [method for method in dir(self) if not method.startswith('_') and callable(getattr(self, method))]
    
    def help(self, method_name: Optional[str] = None) -> Union[str, Dict[str, str]]:
        """Get help for methods."""
        if method_name:
            if hasattr(self, method_name) and callable(getattr(self, method_name)):
                return getattr(self, method_name).__doc__ or "No documentation available"
            else:
                return f"Method '{method_name}' not found"
        
        methods = self.get_all_methods()
        help_dict = {}
        for method in methods:
            doc = getattr(self, method).__doc__
            help_dict[method] = doc or "No documentation available"
        
        return help_dict


# Create default instance
ducvannguyen = DucVanNguyen()

# Export commonly used functions for backward compatibility
def hello():
    return ducvannguyen.__str__()

def get_info():
    return ducvannguyen.info()

def string_utils():
    return {
        "reverse": ducvannguyen.reverse_string,
        "uppercase": lambda s: s.upper(),
        "lowercase": lambda s: s.lower(),
        "capitalize": ducvannguyen.capitalize_words,
        "word_count": ducvannguyen.word_count,
        "is_palindrome": ducvannguyen.is_palindrome
    }

def math_utils():
    return {
        "factorial": ducvannguyen.factorial,
        "fibonacci": ducvannguyen.fibonacci,
        "is_prime": ducvannguyen.is_prime,
        "gcd": ducvannguyen.gcd,
        "lcm": ducvannguyen.lcm
    }

def list_utils():
    return {
        "flatten": ducvannguyen.flatten_list,
        "unique": ducvannguyen.unique_list,
        "chunk": ducvannguyen.chunk_list,
        "shuffle": ducvannguyen.shuffle_list,
        "sum_nested": lambda lst: sum(item if isinstance(item, (int, float)) else ducvannguyen.flatten_list([item]) if isinstance(item, list) else 0 for item in lst)
    }

def file_utils():
    return {
        "get_size": ducvannguyen.get_file_size,
        "get_extension": ducvannguyen.get_file_extension,
        "join_paths": ducvannguyen.join_paths,
        "is_file": ducvannguyen.is_file,
        "is_dir": ducvannguyen.is_directory
    }

def datetime_utils():
    return {
        "now": ducvannguyen.now,
        "today": ducvannguyen.today,
        "add_days": ducvannguyen.add_days,
        "format_timestamp": lambda ts: datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"),
        "days_between": ducvannguyen.days_between
    }

def web_utils():
    return {
        "parse_url": ducvannguyen.parse_url,
        "get_domain": ducvannguyen.get_domain,
        "is_valid_url": ducvannguyen.is_valid_url,
        "extract_params": ducvannguyen.extract_query_params
    }

def random_utils():
    return {
        "random_string": ducvannguyen.random_string,
        "random_choice": ducvannguyen.random_choice,
        "random_number": ducvannguyen.random_number,
        "uuid4": ducvannguyen.generate_uuid,
        "shuffle_string": lambda s: ''.join(random.sample(s, len(s)))
    }

def validate_utils():
    return {
        "is_email": ducvannguyen.is_email,
        "is_phone": ducvannguyen.is_phone,
        "is_url": ducvannguyen.is_valid_url,
        "is_strong_password": ducvannguyen.is_strong_password
    }

def all_utils():
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
