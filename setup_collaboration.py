#!/usr/bin/env python3
"""
Quick Setup Script for QL Tracker Collaboration

This script helps you get started with the @track decorator immediately after
cloning the repository from GitHub. Run this script to set up your environment
and test the tracking functionality.
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    
    try:
        # Install the package in development mode
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], 
                      check=True, capture_output=True)
        print("✅ Package installed successfully")
        
        # Install additional dependencies if needed
        subprocess.run([sys.executable, "-m", "pip", "install", "rich", "tomli", "requests"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("💡 Try creating a virtual environment first:")
        print("   python3 -m venv venv")
        print("   source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("   Then run this script again.")
        return False
    
    return True


def create_config_file():
    """Create a basic configuration file."""
    config_content = """[tracker]
enable_logging = true
pretty_print = true
log_to_file = false
log_file_path = "logs/tracker.log"
log_level = "INFO"

[queue]
max_batch_size = 10
flush_interval_secs = 5

[storage]
backend = "jsonl"
output_path = "logs/ql-tracker.jsonl"
"""
    
    config_path = Path("trackconfig.toml")
    if not config_path.exists():
        with open(config_path, "w") as f:
            f.write(config_content)
        print("✅ Created trackconfig.toml")
    else:
        print("ℹ️ trackconfig.toml already exists")


def create_logs_directory():
    """Create logs directory if it doesn't exist."""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    print("✅ Logs directory ready")


def test_import():
    """Test if the package can be imported."""
    print("\n🧪 Testing imports...")
    
    try:
        from ql_tracker import track, initialize, shutdown
        print("✅ Successfully imported ql_tracker")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're in a virtual environment and the package is installed:")
        print("   python3 -m venv venv")
        print("   source venv/bin/activate")
        print("   pip install -e .")
        return False


def run_quick_test():
    """Run a quick test to verify everything works."""
    print("\n🚀 Running quick test...")
    
    try:
        from ql_tracker import track, initialize, shutdown
        
        # Initialize services
        initialize()
        
        # Test function
        @track
        def test_function(a, b):
            return a + b
        
        # Call the function
        result = test_function(5, 3)
        print(f"✅ Test function result: {result}")
        
        # Wait for background processing
        import time
        time.sleep(1)
        
        # Shutdown
        shutdown()
        print("✅ Quick test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 This might be due to missing dependencies or configuration issues.")
        print("   Check the logs for more details.")
        return False


def create_example_script():
    """Create a simple example script."""
    example_content = '''#!/usr/bin/env python3
"""
Simple example of using the @track decorator.

Run this script to see the tracking in action.
"""

from ql_tracker import track, initialize, shutdown

# Initialize services
initialize()

@track
def add_numbers(a, b):
    """Add two numbers with tracking."""
    return a + b

@track
def multiply_numbers(a, b):
    """Multiply two numbers with tracking."""
    return a * b

def main():
    print("🧮 Testing @track decorator...")
    
    # Test some functions
    result1 = add_numbers(10, 5)
    print(f"10 + 5 = {result1}")
    
    result2 = multiply_numbers(4, 7)
    print(f"4 * 7 = {result2}")
    
    # Wait for background processing
    import time
    time.sleep(2)
    
    # Shutdown
    shutdown()
    print("✅ Example completed!")

if __name__ == "__main__":
    main()
'''
    
    with open("quick_example.py", "w") as f:
        f.write(example_content)
    print("✅ Created quick_example.py")


def show_next_steps():
    """Show what to do next."""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the quick example:")
    print("   python quick_example.py")
    print("\n2. Check out the comprehensive example:")
    print("   python examples/collaboration_example.py")
    print("\n3. Read the setup guide:")
    print("   cat COLLABORATION_SETUP.md")
    print("\n4. View the logs:")
    print("   tail -f logs/ql-tracker.jsonl")
    print("\n💡 Basic usage:")
    print("   from ql_tracker import track, initialize")
    print("   initialize()")
    print("   @track")
    print("   def your_function():")
    print("       return 'Hello, World!'")


def main():
    """Main setup function."""
    print("🚀 QL Tracker - Collaboration Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create necessary files and directories
    create_config_file()
    create_logs_directory()
    
    # Test imports
    if not test_import():
        sys.exit(1)
    
    # Run quick test
    if not run_quick_test():
        print("⚠️ Quick test failed, but setup may still work")
    
    # Create example script
    create_example_script()
    
    # Show next steps
    show_next_steps()


if __name__ == "__main__":
    main() 