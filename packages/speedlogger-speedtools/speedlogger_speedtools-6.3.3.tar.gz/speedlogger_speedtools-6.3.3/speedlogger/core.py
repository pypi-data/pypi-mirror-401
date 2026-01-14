"""
SpeedLogger - Fast Colored Logging Module
Version: 7.1.0
License: MIT License
Copyright (c) 2024 SpeedLogger Team

Description: Clean ASCII logging with global color control and consistent formatting.
"""

import sys
import time
import os
import re
from datetime import datetime
from typing import Optional, Any, List, Dict, Union
import getpass
import threading
from collections import deque

# ==================== COLORS ====================
class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Standard colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

# Color presets mapping
COLOR_PRESETS = {
    # Basic colors
    "BLACK": Colors.BLACK,
    "RED": Colors.RED,
    "GREEN": Colors.GREEN,
    "YELLOW": Colors.YELLOW,
    "BLUE": Colors.BLUE,
    "MAGENTA": Colors.MAGENTA,
    "CYAN": Colors.CYAN,
    "WHITE": Colors.WHITE,
    "GRAY": Colors.GRAY,
    
    # Bright colors
    "BRIGHT_RED": Colors.BRIGHT_RED,
    "BRIGHT_GREEN": Colors.BRIGHT_GREEN,
    "BRIGHT_YELLOW": Colors.BRIGHT_YELLOW,
    "BRIGHT_BLUE": Colors.BRIGHT_BLUE,
    "BRIGHT_MAGENTA": Colors.BRIGHT_MAGENTA,
    "BRIGHT_CYAN": Colors.BRIGHT_CYAN,
    "BRIGHT_WHITE": Colors.BRIGHT_WHITE,
    
    # Special
    "BOLD": Colors.BOLD,
    "DIM": Colors.DIM,
    "RESET": Colors.RESET,
}


class SpeedLogger:
    """
    Main SpeedLogger class with clean ASCII output and global color control.
    
    Features:
    - Clean ASCII symbols only
    - Global color settings for all log types
    - Consistent spacing and formatting
    - Rate limiting
    - Input methods with prompts
    - Progress bars and animations
    
    Format: [SYMBOL]          [TIME]    [PREFIX]    |   message
    
    Args:
        show_time (bool): Show timestamp in logs (default: True)
        show_prefix (bool): Show prefix in logs (default: True)
        symbol_padding (int): Padding after symbol (default: 10)
        time_padding (int): Padding after time (default: 2)
    """
    
    def __init__(self, show_time: bool = True, show_prefix: bool = True,
                 symbol_padding: int = 10, time_padding: int = 2):
        self.show_time = show_time
        self.show_prefix = show_prefix
        self.symbol_padding = symbol_padding
        self.time_padding = time_padding
        
        self._screen_width = self._get_terminal_width()
        self._log_count = 0
        self._rate_limit = 0
        self._rate_limit_queue = deque()
        self._lock = threading.Lock()
        
        # Global color settings
        self._symbol_color = Colors.BRIGHT_CYAN      # Color for all symbols
        self._time_color = Colors.BRIGHT_WHITE       # Color for time
        self._prefix_color = Colors.BRIGHT_BLUE      # Color for prefixes
        self._message_color = Colors.WHITE           # Color for messages
        self._border_color = Colors.GRAY             # Color for borders
        self._input_color = Colors.BRIGHT_MAGENTA    # Color for input prompts
        
        # Symbol mapping
        self._symbols = {
            # Core logging
            "info": "[+]",
            "success": "[√]",
            "warning": "[!]",
            "error": "[X]",
            "debug": "[*]",
            "critical": "[#]",
            
            # Input/Interaction
            "input": "[?]",
            "password": "[?]",
            "confirm": "[$]",
            "choice": "[?]",
            
            # Visual elements
            "separator": "[=]",
            "title": "[#]",
            "section": "[=]",
            
            # Status/Progress
            "progress": "[P]",
            "loading": "[L]",
            "spinner": "[S]",
            "waiting": "[~]",
            
            # Data display
            "list": "[>]",
            "item": "[>]",
            "table": "[T]",
            "key_value": "[K]",
        }
    
    # ==================== COLOR CONFIGURATION ====================
    
    def color(self, element_type: str, color: str):
        """
        Set color for all elements of a specific type.
        
        Args:
            element_type (str): Type of element to color. Options:
                - "SYMBOL": All symbols ([+], [!], etc.)
                - "TIME": Timestamps
                - "PREFIX": Prefix text
                - "MESSAGE": Message text
                - "BORDER": Borders/separators
                - "INPUT": Input prompts
            color (str): Color name from COLOR_PRESETS or direct ANSI code.
            
        Examples:
            >>> log.color("SYMBOL", "BRIGHT_GREEN")
            >>> log.color("MESSAGE", Colors.YELLOW)
            >>> log.color("PREFIX", "BRIGHT_MAGENTA")
        """
        color_code = self._resolve_color(color)
        if not color_code:
            return
            
        element_type = element_type.upper()
        
        if element_type == "SYMBOL":
            self._symbol_color = color_code
        elif element_type == "TIME":
            self._time_color = color_code
        elif element_type == "PREFIX":
            self._prefix_color = color_code
        elif element_type == "MESSAGE":
            self._message_color = color_code
        elif element_type == "BORDER":
            self._border_color = color_code
        elif element_type == "INPUT":
            self._input_color = color_code
    
    def set_colors(self, symbol: str = None, time: str = None, prefix: str = None,
                   message: str = None, border: str = None, input_color: str = None):
        """
        Set multiple colors at once.
        
        Args:
            symbol: Color for all symbols
            time: Color for timestamps
            prefix: Color for prefixes
            message: Color for messages
            border: Color for borders
            input_color: Color for input prompts
        """
        if symbol:
            self.color("SYMBOL", symbol)
        if time:
            self.color("TIME", time)
        if prefix:
            self.color("PREFIX", prefix)
        if message:
            self.color("MESSAGE", message)
        if border:
            self.color("BORDER", border)
        if input_color:
            self.color("INPUT", input_color)
    
    def reset_colors(self):
        """Reset all colors to defaults."""
        self._symbol_color = Colors.BRIGHT_CYAN
        self._time_color = Colors.BRIGHT_WHITE
        self._prefix_color = Colors.BRIGHT_BLUE
        self._message_color = Colors.WHITE
        self._border_color = Colors.GRAY
        self._input_color = Colors.BRIGHT_MAGENTA
    
    def _resolve_color(self, color: str) -> Optional[str]:
        """Resolve color string to ANSI code."""
        if color is None:
            return None
        elif color.startswith('\033'):
            return color
        elif color.upper() in COLOR_PRESETS:
            return COLOR_PRESETS[color.upper()]
        return None
    
    # ==================== UTILITY METHODS ====================
    
    def _get_terminal_width(self) -> int:
        """Get terminal width."""
        try:
            return os.get_terminal_size().columns
        except:
            return 80
    
    def _clean_ansi(self, text: str) -> str:
        """Remove ANSI codes from text."""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
    
    def _visible_length(self, text: str) -> int:
        """Get visible length (without ANSI codes)."""
        return len(self._clean_ansi(text))
    
    def _format_time(self) -> str:
        """Format current time as HH:MM:SS."""
        return datetime.now().strftime("%H:%M:%S")
    
    def _center_text(self, text: str) -> str:
        """Center text based on screen width."""
        visible_len = self._visible_length(text)
        padding = max(0, (self._screen_width - visible_len) // 2)
        return ' ' * padding + text
    
    def _print_line(self, text: str):
        """Print line."""
        print(text)
    
    def _check_rate_limit(self) -> bool:
        """Check if rate limit is exceeded."""
        if self._rate_limit <= 0:
            return True
            
        current_time = time.time()
        with self._lock:
            while self._rate_limit_queue and current_time - self._rate_limit_queue[0] > 1.0:
                self._rate_limit_queue.popleft()
            
            if len(self._rate_limit_queue) < self._rate_limit:
                self._rate_limit_queue.append(current_time)
                return True
            return False
    
    # ==================== CORE LOGGING ====================
    
    def _format_line(self, symbol: str, prefix: str = None, message: str = "") -> str:
        """
        Format log line with consistent spacing.
        
        Format: [SYMBOL]          [TIME]    [PREFIX]    |   message
        """
        # Symbol part
        symbol_part = f"{self._symbol_color}{symbol}{Colors.RESET}"
        
        # Time part
        if self.show_time:
            time_part = f"{self._time_color}[{self._format_time()}]{Colors.RESET}"
        else:
            time_part = ""
        
        # Prefix part
        if self.show_prefix and prefix:
            prefix_part = f"{self._prefix_color}[{prefix.upper()}]{Colors.RESET}"
        else:
            prefix_part = ""
        
        # Build line with consistent spacing
        parts = []
        
        # Symbol with padding
        symbol_str = f"{symbol_part:<{self.symbol_padding + len(symbol) - 2}}"
        parts.append(symbol_str)
        
        # Time with padding
        if time_part:
            time_str = f"{time_part:<{len(time_part) + self.time_padding}}"
            parts.append(time_str)
        
        # Prefix
        if prefix_part:
            prefix_str = f"{prefix_part:<{len(prefix_part) + 4}}"
            parts.append(prefix_str)
        
        # Message
        message_part = f"{self._message_color}{message}{Colors.RESET}"
        
        # Combine
        if prefix_part:
            line = ''.join(parts) + f"|   {message_part}"
        else:
            line = ''.join(parts) + f"{message_part}"
        
        return line
    
    def _log(self, symbol_type: str, prefix: str, message: str):
        """Core logging method."""
        if not self._check_rate_limit():
            return
            
        self._log_count += 1
        
        symbol = self._symbols.get(symbol_type, "[*]")
        line = self._format_line(symbol, prefix, message)
        self._print_line(line)
    
    # ==================== LOG METHODS ====================
    
    def info(self, prefix: str, message: str):
        """Info log: [+]"""
        self._log("info", prefix, message)
    
    def success(self, prefix: str, message: str):
        """Success log: [√]"""
        self._log("success", prefix, message)
    
    def warning(self, prefix: str, message: str):
        """Warning log: [!]"""
        self._log("warning", prefix, message)
    
    def error(self, prefix: str, message: str):
        """Error log: [X]"""
        self._log("error", prefix, message)
    
    def debug(self, prefix: str, message: str):
        """Debug log: [*]"""
        self._log("debug", prefix, message)
    
    def critical(self, prefix: str, message: str):
        """Critical log: [#]"""
        self._log("critical", prefix, message)
    
    # ==================== INPUT METHODS ====================
    
    def inp(self, prompt: str, prefix: str = "INPUT") -> str:
        """
        Get user input with prompt.
        
        Format: [?]          [TIME]    Enter your email  [>]
        """
        if not self._check_rate_limit():
            return ""
        
        # Show prompt
        symbol = self._symbols["input"]
        time_part = f"{self._time_color}[{self._format_time()}]{Colors.RESET}" if self.show_time else ""
        
        # Build prompt display
        prompt_display = f"{self._input_color}{prompt}{Colors.RESET}  {self._symbol_color}[>]{Colors.RESET}"
        
        # Format line
        symbol_part = f"{self._symbol_color}{symbol}{Colors.RESET}"
        symbol_str = f"{symbol_part:<{self.symbol_padding + len(symbol) - 2}}"
        
        line_parts = [symbol_str]
        
        if time_part:
            time_str = f"{time_part:<{len(time_part) + self.time_padding}}"
            line_parts.append(time_str)
        
        line_parts.append(prompt_display)
        prompt_line = ''.join(line_parts)
        
        # Print prompt and get input
        print(prompt_line, end=' ')
        return input()
    
    def password(self, prompt: str = "Password", prefix: str = "AUTH") -> str:
        """Get password input (hidden)."""
        if not self._check_rate_limit():
            return ""
        
        # Show prompt
        symbol = self._symbols["password"]
        time_part = f"{self._time_color}[{self._format_time()}]{Colors.RESET}" if self.show_time else ""
        
        prompt_display = f"{self._input_color}{prompt}{Colors.RESET}  {self._symbol_color}[>]{Colors.RESET}"
        
        symbol_part = f"{self._symbol_color}{symbol}{Colors.RESET}"
        symbol_str = f"{symbol_part:<{self.symbol_padding + len(symbol) - 2}}"
        
        line_parts = [symbol_str]
        
        if time_part:
            time_str = f"{time_part:<{len(time_part) + self.time_padding}}"
            line_parts.append(time_str)
        
        line_parts.append(prompt_display)
        prompt_line = ''.join(line_parts)
        
        # Print prompt
        print(prompt_line, end=' ', flush=True)
        
        # Get password
        try:
            import msvcrt
            password_chars = []
            
            while True:
                char = msvcrt.getch()
                
                if char in [b'\r', b'\n']:
                    print()
                    break
                
                elif char == b'\x08':
                    if password_chars:
                        password_chars.pop()
                        print('\b \b', end='', flush=True)
                
                elif 32 <= ord(char) <= 126:
                    password_chars.append(char.decode('utf-8'))
                    print('*', end='', flush=True)
            
            return ''.join(password_chars)
            
        except ImportError:
            # Unix fallback
            return getpass.getpass('')
    
    def confirm(self, question: str, prefix: str = "CONFIRM") -> bool:
        """Get yes/no confirmation."""
        prompt = f"{question} (y/n)  {self._symbol_color}[>]{Colors.RESET}"
        response = self.inp(prompt, prefix).lower()
        return response in ['y', 'yes', '1', 't', 'true']
    
    def choice(self, prompt: str, options: List[str], prefix: str = "CHOICE") -> int:
        """Get choice from multiple options."""
        # Show prompt
        self.info(prefix, prompt)
        
        # Show options
        for i, option in enumerate(options, 1):
            option_line = f"   {self._symbol_color}{i}.{Colors.RESET}  {self._message_color}{option}{Colors.RESET}"
            print(option_line)
        
        # Get choice
        while True:
            choice_prompt = f"Select (1-{len(options)})  {self._symbol_color}[>]{Colors.RESET}"
            choice_input = input(f"   {choice_prompt} ").strip()
            
            try:
                choice_num = int(choice_input)
                if 1 <= choice_num <= len(options):
                    return choice_num - 1
                else:
                    self.error("INPUT", f"Please enter 1-{len(options)}")
            except ValueError:
                self.error("INPUT", "Please enter a valid number")
    
    # ==================== VISUAL ELEMENTS ====================
    
    def separator(self, length: int = 60, char: str = "-"):
        """Print a separator line."""
        if not self._check_rate_limit():
            return
        
        line = char * length
        symbol = self._symbols["separator"]
        
        time_part = f"{self._time_color}[{self._format_time()}]{Colors.RESET}" if self.show_time else ""
        
        # Format separator line
        symbol_part = f"{self._border_color}{symbol}{Colors.RESET}"
        symbol_str = f"{symbol_part:<{self.symbol_padding + len(symbol) - 2}}"
        
        line_parts = [symbol_str]
        
        if time_part:
            time_str = f"{time_part:<{len(time_part) + self.time_padding}}"
            line_parts.append(time_str)
        
        separator_text = f"{self._border_color}{line}{Colors.RESET}"
        line_parts.append(separator_text)
        
        separator_line = ''.join(line_parts)
        self._print_line(separator_line)
    
    def title(self, text: str):
        """Print a centered title with borders."""
        border = "=" * (len(text) + 4)
        
        # Top border
        self.separator(len(border), "=")
        
        # Title line
        symbol = self._symbols["title"]
        time_part = f"{self._time_color}[{self._format_time()}]{Colors.RESET}" if self.show_time else ""
        
        symbol_part = f"{self._symbol_color}{symbol}{Colors.RESET}"
        symbol_str = f"{symbol_part:<{self.symbol_padding + len(symbol) - 2}}"
        
        line_parts = [symbol_str]
        
        if time_part:
            time_str = f"{time_part:<{len(time_part) + self.time_padding}}"
            line_parts.append(time_str)
        
        title_text = f"{self._message_color}{text.upper()}{Colors.RESET}"
        line_parts.append(title_text)
        
        title_line = ''.join(line_parts)
        self._print_line(title_line)
        
        # Bottom border
        self.separator(len(border), "=")
    
    def section(self, text: str):
        """Print a section header."""
        self.separator(len(text) + 6, "-")
        self.info("SECTION", text)
        self.separator(len(text) + 6, "-")
    
    # ==================== PROGRESS & ANIMATIONS ====================
    
    def progress_bar(self, current: int, total: int, length: int = 40, label: str = ""):
        """Display a progress bar."""
        if not self._check_rate_limit():
            return
        
        percent = current / total if total > 0 else 0
        filled = int(length * percent)
        
        # Build bar
        bar = f"{self._symbol_color}█{Colors.RESET}" * filled + \
              f"{self._border_color}░{Colors.RESET}" * (length - filled)
        
        percent_text = f"{percent*100:6.1f}%"
        
        # Build message
        message = f"{bar}   {percent_text}   ({current}/{total})"
        if label:
            message = f"{label}: {message}"
        
        # Show progress
        symbol = self._symbols["progress"]
        line = self._format_line(symbol, "PROGRESS", message)
        
        print(line, end='\r')
        
        if current == total:
            print()
            self.success("PROGRESS", "Complete")
    
    def loading(self, message: str = "Loading", duration: float = 2.0):
        """Display loading animation."""
        frames = ["|   ", "/   ", "-   ", "\\   "]
        start_time = time.time()
        
        while time.time() - start_time < duration:
            if not self._check_rate_limit():
                time.sleep(0.1)
                continue
            
            elapsed = time.time() - start_time
            frame_idx = int(elapsed * 4) % len(frames)
            
            symbol = f"[{frames[frame_idx]}]"
            line = self._format_line(symbol, "LOADING", message)
            
            print(line, end='\r')
            time.sleep(0.1)
        
        # Clear line
        print(' ' * self._screen_width, end='\r')
        self.success("LOADING", f"{message} complete")
    
    def waiting(self, message: str = "Waiting", duration: float = 1.0):
        """Display waiting animation with dots."""
        start_time = time.time()
        dots = 0
        
        while time.time() - start_time < duration:
            if not self._check_rate_limit():
                time.sleep(0.5)
                continue
            
            dots = (dots + 1) % 4
            dot_str = "." * dots + " " * (3 - dots)
            
            symbol = f"[{dot_str}]"
            line = self._format_line(symbol, "WAITING", message)
            
            print(line, end='\r')
            time.sleep(0.5)
        
        print(' ' * self._screen_width, end='\r')
    
    # ==================== DATA DISPLAY ====================
    
    def list_items(self, items: List[str], title: Optional[str] = None):
        """Display a list of items."""
        if not self._check_rate_limit():
            return
        
        if title:
            self.info("LIST", title)
        
        for item in items:
            if not self._check_rate_limit():
                continue
            
            symbol = self._symbols["item"]
            line = self._format_line(symbol, "", f"  {item}")
            self._print_line(line)
    
    def key_value(self, data: Dict[str, Any], title: Optional[str] = None):
        """Display key-value pairs."""
        if not self._check_rate_limit():
            return
        
        if title:
            self.info("DATA", title)
        
        max_key_len = max(len(str(k)) for k in data.keys())
        
        for key, value in data.items():
            if not self._check_rate_limit():
                continue
            
            symbol = self._symbols["key_value"]
            key_part = f"{self._prefix_color}{key}{Colors.RESET}"
            key_str = f"{key_part:<{max_key_len + 2}}"
            
            value_str = f"{self._message_color}{value}{Colors.RESET}"
            
            line = f"{self._symbol_color}{symbol}{Colors.RESET}" + \
                   f"{' ' * (self.symbol_padding - 3)}" + \
                   f"{key_str}:  {value_str}"
            
            self._print_line(line)
    
    def table(self, data: List[List[Any]], headers: Optional[List[str]] = None):
        """Display data in a simple table."""
        if not data:
            return
        
        if not self._check_rate_limit():
            return
        
        # Calculate column widths
        all_rows = data.copy()
        if headers:
            all_rows.insert(0, headers)
        
        col_count = len(all_rows[0])
        col_widths = [0] * col_count
        
        for row in all_rows:
            for i, cell in enumerate(row):
                visible_len = len(str(cell))
                col_widths[i] = max(col_widths[i], visible_len)
        
        # Display table
        if headers:
            # Headers
            header_parts = []
            for i, header in enumerate(headers):
                header_text = f"{self._prefix_color}{header}{Colors.RESET}"
                header_parts.append(f"{header_text:<{col_widths[i] + 2}}")
            
            header_line = "   ".join(header_parts)
            print(f"{' ' * (self.symbol_padding + 2)}{header_line}")
            
            # Separator
            sep_parts = []
            for width in col_widths:
                sep_parts.append("-" * (width + 2))
            sep_line = "---".join(sep_parts)
            print(f"{' ' * (self.symbol_padding + 2)}{self._border_color}{sep_line}{Colors.RESET}")
        
        # Data rows
        for row in data:
            row_parts = []
            for i, cell in enumerate(row):
                row_parts.append(f"{self._message_color}{str(cell):<{col_widths[i] + 2}}{Colors.RESET}")
            
            row_line = "   ".join(row_parts)
            print(f"{' ' * (self.symbol_padding + 2)}{row_line}")
    
    # ==================== CONFIGURATION ====================
    
    def set_show_time(self, show_time: bool):
        """Enable/disable timestamp display."""
        self.show_time = show_time
    
    def set_show_prefix(self, show_prefix: bool):
        """Enable/disable prefix display."""
        self.show_prefix = show_prefix
    
    def set_padding(self, symbol_padding: int = None, time_padding: int = None):
        """Set padding values."""
        if symbol_padding is not None:
            self.symbol_padding = symbol_padding
        if time_padding is not None:
            self.time_padding = time_padding
    
    def set_rate_limit(self, limit: int):
        """Set rate limit (logs per second, 0 = no limit)."""
        self._rate_limit = max(0, limit)
    
    def get_log_count(self):
        """Get total log count."""
        return self._log_count
    
    def reset_count(self):
        """Reset log counter."""
        self._log_count = 0


# ==================== GLOBAL INSTANCE ====================
logger = SpeedLogger()

# ==================== GLOBAL FUNCTIONS ====================

def color(element_type: str, color: str):
    """Global: Set color for all elements of a type."""
    logger.color(element_type, color)

def set_colors(symbol: str = None, time: str = None, prefix: str = None,
               message: str = None, border: str = None, input_color: str = None):
    """Global: Set multiple colors at once."""
    logger.set_colors(symbol, time, prefix, message, border, input_color)

def reset_colors():
    """Global: Reset all colors to defaults."""
    logger.reset_colors()

def set_show_time(show_time: bool):
    """Global: Enable/disable timestamp display."""
    logger.set_show_time(show_time)

def set_show_prefix(show_prefix: bool):
    """Global: Enable/disable prefix display."""
    logger.set_show_prefix(show_prefix)

def set_padding(symbol_padding: int = None, time_padding: int = None):
    """Global: Set padding values."""
    logger.set_padding(symbol_padding, time_padding)

def set_rate_limit(limit: int):
    """Global: Set rate limit."""
    logger.set_rate_limit(limit)

# Core logging
def info(prefix: str, message: str):
    logger.info(prefix, message)

def success(prefix: str, message: str):
    logger.success(prefix, message)

def warning(prefix: str, message: str):
    logger.warning(prefix, message)

def error(prefix: str, message: str):
    logger.error(prefix, message)

def debug(prefix: str, message: str):
    logger.debug(prefix, message)

def critical(prefix: str, message: str):
    logger.critical(prefix, message)

# Input methods
def inp(prompt: str, prefix: str = "INPUT") -> str:
    return logger.inp(prompt, prefix)

def password(prompt: str = "Password", prefix: str = "AUTH") -> str:
    return logger.password(prompt, prefix)

def confirm(question: str, prefix: str = "CONFIRM") -> bool:
    return logger.confirm(question, prefix)

def choice(prompt: str, options: List[str], prefix: str = "CHOICE") -> int:
    return logger.choice(prompt, options, prefix)

# Visual elements
def separator(length: int = 60, char: str = "-"):
    logger.separator(length, char)

def title(text: str):
    logger.title(text)

def section(text: str):
    logger.section(text)

# Progress & animations
def progress_bar(current: int, total: int, length: int = 40, label: str = ""):
    logger.progress_bar(current, total, length, label)

def loading(message: str = "Loading", duration: float = 2.0):
    logger.loading(message, duration)

def waiting(message: str = "Waiting", duration: float = 1.0):
    logger.waiting(message, duration)

# Data display
def list_items(items: List[str], title: Optional[str] = None):
    logger.list_items(items, title)

def key_value(data: Dict[str, Any], title: Optional[str] = None):
    logger.key_value(data, title)

def table(data: List[List[Any]], headers: Optional[List[str]] = None):
    logger.table(data, headers)

# Global instance
log = SpeedLogger()