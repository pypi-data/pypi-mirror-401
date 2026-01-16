"""
Example of debugging a standalone Python file using geai-dbg.

This demonstrates how to use debug_file() to debug any Python script.
"""
from pygeai.dbg import debug_file
import tempfile
import os


def create_sample_script():
    """Create a sample script to debug."""
    code = '''
def process_data(items):
    """Process a list of items."""
    result = []
    for item in items:
        result.append(item * 2)
    return result


def main():
    """Main entry point."""
    data = [1, 2, 3, 4, 5]
    processed = process_data(data)
    print(f"Processed: {processed}")
    return processed


if __name__ == "__main__":
    main()
'''
    
    fd, filepath = tempfile.mkstemp(suffix='.py', text=True)
    try:
        os.write(fd, code.encode())
    finally:
        os.close(fd)
    
    return filepath


def main():
    """Demonstrate file debugging."""
    print("Creating sample script...")
    script_path = create_sample_script()
    
    try:
        print(f"Script created at: {script_path}")
        print("\nSetting up debugger...")
        
        dbg = debug_file(script_path)
        dbg.add_breakpoint(function_name='process_data')
        
        print("Debugger configured with breakpoint on 'process_data'")
        print("\nTo run interactively, uncomment the line below:")
        print("# dbg.run()")
        print("\nCommands you can use:")
        print("  c     - continue")
        print("  s     - step into")
        print("  n     - next line")
        print("  p     - print variable (e.g., 'p items')")
        print("  l     - list source")
        print("  h     - help")
        
    finally:
        os.unlink(script_path)
        print(f"\nCleaned up {script_path}")


if __name__ == "__main__":
    main()
