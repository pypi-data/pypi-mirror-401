"""
Example of debugging a specific module and function using geai-dbg.

This demonstrates how to use debug_module() to debug imported modules.
"""
from pygeai.dbg import debug_module


def example_simple_module():
    """Debug a simple built-in module."""
    print("Example: Debugging os.path.exists function")
    print("\nThis would set up a debugger for the os.path.exists function:")
    print("  dbg = debug_module('os.path', 'exists')")
    print("  dbg.run()")
    print("\nNote: This is for demonstration. Built-in functions may not be traceable.")


def example_pygeai_module():
    """Debug a PyGEAI module."""
    print("\nExample: Debugging PyGEAI modules")
    print("\nYou can debug any PyGEAI module function:")
    print("  from pygeai.dbg import debug_module")
    print("  ")
    print("  # Debug the chat module")
    print("  dbg = debug_module('pygeai.chat', 'send_message')")
    print("  dbg.add_breakpoint(module='pygeai.core.llm', function_name='get_completion')")
    print("  dbg.run()")


def example_cli_debugging():
    """Debug the geai CLI programmatically."""
    print("\nExample: Debugging geai CLI programmatically")
    print("\nInstead of using 'geai-dbg', you can set it up in code:")
    print("  from pygeai.dbg import debug_module")
    print("  ")
    print("  # Set up debugging with custom breakpoints")
    print("  dbg = debug_module('pygeai.cli.geai', 'main')")
    print("  dbg.add_breakpoint(module='pygeai.cli.commands', function_name='execute')")
    print("  dbg.run()")


def main():
    """Run all examples."""
    print("=" * 70)
    print("Module Debugging Examples")
    print("=" * 70)
    
    example_simple_module()
    example_pygeai_module()
    example_cli_debugging()
    
    print("\n" + "=" * 70)
    print("To use module debugging from the command line:")
    print("=" * 70)
    print("  geai-dbg -m pygeai.cli.geai:main")
    print("  geai-dbg -m pygeai.chat:send_message -b process_response")
    print("=" * 70)


if __name__ == "__main__":
    main()
