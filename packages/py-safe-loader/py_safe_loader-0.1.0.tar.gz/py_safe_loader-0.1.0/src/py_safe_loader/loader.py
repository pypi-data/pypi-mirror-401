"""
SafeLoader - Reusable Module and Code Error Handler
====================================================
Import once, use everywhere in your codebase!

Usage:
    from safe_loader import SafeLoader
    
    loader = SafeLoader()
    modules = loader.load_modules(['module1', 'module2', 'module3'])
"""

import importlib
import sys
import traceback
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime
import os


class SafeLoader:
    """
    A reusable class for safe module loading and code execution
    that never terminates your program on errors.
    """
    
    def __init__(self, verbose=True, log_file=None):
        """
        Initialize SafeLoader
        
        Args:
            verbose (bool): Print detailed messages
            log_file (str): Optional file path to log errors
        """
        self.verbose = verbose
        self.log_file = log_file
        self.loaded_modules = {}
        self.failed_modules = {}
        self.execution_history = []
        
    def _log(self, message, level="INFO"):
        """Internal logging method"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        if self.verbose:
            print(log_entry)
        
        if self.log_file:
            try:
                with open(self.log_file, 'a') as f:
                    f.write(log_entry + "\n")
            except Exception as e:
                print(f"Warning: Could not write to log file: {e}")
    
    def load_module(self, module_name: str) -> Optional[Any]:
        """
        Safely load a single module
        
        Args:
            module_name (str): Name of the module to import
            
        Returns:
            Module object if successful, None if failed
        """
        try:
            module = importlib.import_module(module_name)
            self.loaded_modules[module_name] = module
            self._log(f"✓ Successfully loaded module: {module_name}", "SUCCESS")
            return module
            
        except ImportError as e:
            error_msg = f"Import error: {str(e)}"
            self.failed_modules[module_name] = error_msg
            self._log(f"✗ Failed to load {module_name}: {error_msg}", "ERROR")
            return None
            
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            self.failed_modules[module_name] = error_msg
            self._log(f"✗ Unexpected error loading {module_name}: {error_msg}", "ERROR")
            return None
    
    def load_modules(self, module_names: List[str]) -> Dict[str, Any]:
        """
        Safely load multiple modules
        
        Args:
            module_names (list): List of module names to import
            
        Returns:
            Dictionary of successfully loaded modules {name: module_object}
        """
        self._log(f"Loading {len(module_names)} modules...", "INFO")
        
        for module_name in module_names:
            self.load_module(module_name)
        
        self._log(
            f"Loaded {len(self.loaded_modules)}/{len(module_names)} modules successfully",
            "INFO"
        )
        
        return self.loaded_modules.copy()
    
    def safe_execute(self, func: Callable, *args, **kwargs) -> tuple:
        """
        Safely execute any function and catch all errors
        
        Args:
            func: Function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Tuple of (success: bool, result: Any, error: str)
        """
        func_name = func.__name__ if hasattr(func, '__name__') else str(func)
        
        try:
            self._log(f"Executing function: {func_name}", "INFO")
            result = func(*args, **kwargs)
            self._log(f"✓ {func_name} executed successfully", "SUCCESS")
            
            self.execution_history.append({
                'function': func_name,
                'status': 'success',
                'timestamp': datetime.now()
            })
            
            return (True, result, None)
            
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            tb = traceback.format_exc()
            
            self._log(f"✗ Error in {func_name}: {error_msg}", "ERROR")
            if self.verbose:
                self._log(f"Traceback:\n{tb}", "ERROR")
            
            self.execution_history.append({
                'function': func_name,
                'status': 'failed',
                'error': error_msg,
                'timestamp': datetime.now()
            })
            
            return (False, None, error_msg)
    
    def safe_exec_code(self, code: str, namespace: Optional[Dict] = None) -> tuple:
        """
        Safely execute code string using exec()
        
        Args:
            code (str): Python code to execute
            namespace (dict): Optional namespace dictionary
            
        Returns:
            Tuple of (success: bool, namespace: dict, error: str)
        """
        if namespace is None:
            namespace = {}
        
        try:
            self._log("Executing code block...", "INFO")
            exec(code, namespace)
            self._log("✓ Code executed successfully", "SUCCESS")
            return (True, namespace, None)
            
        except SyntaxError as e:
            error_msg = f"Syntax error at line {e.lineno}: {e.msg}"
            self._log(f"✗ {error_msg}", "ERROR")
            return (False, namespace, error_msg)
            
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            tb = traceback.format_exc()
            self._log(f"✗ Execution error: {error_msg}", "ERROR")
            if self.verbose:
                self._log(f"Traceback:\n{tb}", "ERROR")
            return (False, namespace, error_msg)
    
    def safe_exec_file(self, file_path: str, namespace: Optional[Dict] = None) -> tuple:
        """
        Safely execute a Python file
        
        Args:
            file_path (str): Path to Python file
            namespace (dict): Optional namespace dictionary
            
        Returns:
            Tuple of (success: bool, namespace: dict, error: str)
        """
        try:
            if not os.path.exists(file_path):
                error_msg = f"File not found: {file_path}"
                self._log(f"✗ {error_msg}", "ERROR")
                return (False, {}, error_msg)
            
            with open(file_path, 'r') as f:
                code = f.read()
            
            self._log(f"Executing file: {file_path}", "INFO")
            return self.safe_exec_code(code, namespace)
            
        except Exception as e:
            error_msg = f"Error reading file: {str(e)}"
            self._log(f"✗ {error_msg}", "ERROR")
            return (False, {}, error_msg)
    
    def try_import_or_install(self, package_name: str, import_name: Optional[str] = None) -> Optional[Any]:
        """
        Try to import a package, suggest installation if not found
        
        Args:
            package_name (str): Package name for pip install
            import_name (str): Import name if different from package name
            
        Returns:
            Module object if successful, None if failed
        """
        if import_name is None:
            import_name = package_name
        
        try:
            module = importlib.import_module(import_name)
            self.loaded_modules[import_name] = module
            self._log(f"✓ {import_name} is available", "SUCCESS")
            return module
            
        except ImportError:
            self._log(
                f"✗ {import_name} not found. Install with: pip install {package_name}",
                "WARNING"
            )
            return None
    
    def get_summary(self) -> Dict:
        """
        Get summary of all operations
        
        Returns:
            Dictionary with statistics and details
        """
        return {
            'total_modules_attempted': len(self.loaded_modules) + len(self.failed_modules),
            'modules_loaded': len(self.loaded_modules),
            'modules_failed': len(self.failed_modules),
            'loaded_module_names': list(self.loaded_modules.keys()),
            'failed_module_names': list(self.failed_modules.keys()),
            'failed_details': self.failed_modules.copy(),
            'execution_history': self.execution_history.copy()
        }
    
    def print_summary(self):
        """Print a formatted summary report"""
        summary = self.get_summary()
        
        print("\n" + "="*60)
        print("SAFELOADER SUMMARY REPORT")
        print("="*60)
        print(f"Total Modules Attempted: {summary['total_modules_attempted']}")
        print(f"Successfully Loaded: {summary['modules_loaded']}")
        print(f"Failed to Load: {summary['modules_failed']}")
        
        if summary['loaded_module_names']:
            print(f"\n✓ Loaded Modules:")
            for name in summary['loaded_module_names']:
                print(f"  - {name}")
        
        if summary['failed_module_names']:
            print(f"\n✗ Failed Modules:")
            for name in summary['failed_module_names']:
                print(f"  - {name}: {summary['failed_details'][name]}")
        
        if summary['execution_history']:
            print(f"\nExecution History ({len(summary['execution_history'])} operations):")
            for item in summary['execution_history'][-5:]:  # Show last 5
                status_icon = "✓" if item['status'] == 'success' else "✗"
                print(f"  {status_icon} {item['function']} - {item['timestamp'].strftime('%H:%M:%S')}")
        
        print("="*60 + "\n")
    
    def reset(self):
        """Reset all tracking data"""
        self.loaded_modules.clear()
        self.failed_modules.clear()
        self.execution_history.clear()
        self._log("SafeLoader reset", "INFO")
        
    def __enter__(self):
        """Enable context manager support - called when entering 'with' block"""
        self._log("SafeLoader context started", "INFO")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Enable context manager support - called when exiting 'with' block"""
        if exc_type is not None:
            self._log(f"Context exited with error: {exc_type.__name__}: {exc_val}", "ERROR")
        else:
            self._log("SafeLoader context completed successfully", "INFO")
        
        print("\n\n" + "="*60)
        print("FINAL SUMMARY - ALL OPERATIONS")
        print("="*60)
        
        self.print_summary()
        
        print("\n\n" + "="*60)
        print("SafeLoader context closed")
        print("="*60)
        
        self.reset()
        return False

# Convenience functions for quick use
def quick_load(*module_names, verbose=True) -> Dict[str, Any]:
    """
    Quick function to load modules without creating a SafeLoader instance
    
    Usage:
        modules = quick_load('requests', 'numpy', 'pandas')
    """
    loader = SafeLoader(verbose=verbose)
    return loader.load_modules(list(module_names))


def safe_run(func: Callable, *args, **kwargs) -> tuple:
    """
    Quick function to safely run any function
    
    Usage:
        success, result, error = safe_run(my_function, arg1, arg2)
    """
    loader = SafeLoader(verbose=False)
    return loader.safe_execute(func, *args, **kwargs)