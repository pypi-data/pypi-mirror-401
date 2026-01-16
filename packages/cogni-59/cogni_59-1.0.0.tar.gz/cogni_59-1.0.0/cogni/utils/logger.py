"""Optional logging utility with ANSI color support."""


class Logger:
    """Logger class with optional verbose output and ANSI colors."""
    
    # ANSI color codes
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
    GREY = '\033[90m'
    PURPLE = '\033[95m'
    
    def __init__(self, verbose=False):
        """
        Initialize logger.
        
        Args:
            verbose (bool): If True, enable logging output. If False, all logs are silent.
        """
        self.verbose = verbose
    
    def info(self, message):
        """Log an info message."""
        if self.verbose:
            print(f"{self.CYAN}[INFO] {message}{self.RESET}")
    
    def debug(self, message):
        """Log a debug message."""
        if self.verbose:
            print(f"{self.GREY}[DEBUG] {message}{self.RESET}")
    
    def warning(self, message):
        """Log a warning message."""
        if self.verbose:
            print(f"{self.YELLOW}[WARNING] {message}{self.RESET}")
    
    def error(self, message):
        """Log an error message."""
        if self.verbose:
            print(f"{self.RED}[ERROR] {message}{self.RESET}")
    
    def success(self, message):
        """Log a success message."""
        if self.verbose:
            print(f"{self.GREEN}[SUCCESS] {message}{self.RESET}")
    
    def engine_log(self, message):
        """Log an engine-specific message."""
        if self.verbose:
            print(f"{self.CYAN}[ENGINE LOG] {message}{self.RESET}")
    
    def social_log(self, message):
        """Log a social dynamics message."""
        if self.verbose:
            print(f"{self.PURPLE}[SOCIAL ENGINE] {message}{self.RESET}")

