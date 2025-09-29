#!/usr/bin/env python3
"""
Example usage of MetaGPT after virtual environment setup

This script demonstrates basic MetaGPT functionality that works
even with minimal dependencies installed.
"""

import sys
from pathlib import Path


def demonstrate_basic_imports():
    """Demonstrate that basic MetaGPT modules can be imported."""
    print("🧪 Testing basic MetaGPT imports...")
    
    try:
        import metagpt
        print("   ✅ metagpt - Core module")
        
        # Try to import some core components
        try:
            from metagpt.schema import Message
            print("   ✅ metagpt.schema.Message - Basic schema")
        except ImportError as e:
            print(f"   ⚠️  metagpt.schema.Message - {e}")
            
        try:
            from metagpt.config2 import Config
            print("   ✅ metagpt.config2.Config - Configuration")
        except ImportError as e:
            print(f"   ⚠️  metagpt.config2.Config - {e}")
            
        try:
            from metagpt.roles.role import Role
            print("   ✅ metagpt.roles.role.Role - Base role class")
        except ImportError as e:
            print(f"   ⚠️  metagpt.roles.role.Role - {e}")
            
    except ImportError as e:
        print(f"   ❌ Could not import metagpt: {e}")
        return False
    
    return True


def check_project_structure():
    """Check the project structure."""
    print("\n📁 Checking project structure...")
    
    important_dirs = [
        "metagpt",
        "tests", 
        "config",
        "docs",
        "examples"
    ]
    
    for dir_name in important_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            print(f"   ✅ {dir_name}/ - Found")
        else:
            print(f"   ❌ {dir_name}/ - Missing")
    
    # Check important files
    important_files = [
        "requirements.txt",
        "setup.py",
        "README.md",
        "setup_venv.sh",
        "verify_setup.py"
    ]
    
    for file_name in important_files:
        file_path = Path(file_name)
        if file_path.exists() and file_path.is_file():
            print(f"   ✅ {file_name} - Found")
        else:
            print(f"   ❌ {file_name} - Missing")


def demonstrate_config_loading():
    """Demonstrate configuration loading."""
    print("\n⚙️  Testing configuration loading...")
    
    config_paths = [
        Path.home() / ".metagpt" / "config2.yaml",
        Path("config") / "config2.yaml"
    ]
    
    for config_path in config_paths:
        if config_path.exists():
            print(f"   ✅ Config found: {config_path}")
            try:
                # Basic file reading test
                with open(config_path, 'r') as f:
                    content = f.read()
                    if len(content) > 0:
                        print(f"   ✅ Config readable ({len(content)} chars)")
                    else:
                        print("   ⚠️  Config file is empty")
                break
            except Exception as e:
                print(f"   ❌ Error reading config: {e}")
        else:
            print(f"   ⚠️  Config not found: {config_path}")


def show_next_steps():
    """Show what to do next."""
    print("\n🎯 Next Steps for Full Setup:")
    print("=" * 40)
    
    steps = [
        "1. Install dependencies:",
        "   pip install -r requirements.txt",
        "",
        "2. Install MetaGPT in development mode:",
        "   pip install -e .",
        "",
        "3. Set up configuration:",
        "   mkdir -p ~/.metagpt",
        "   cp config/config2.yaml ~/.metagpt/config2.yaml",
        "   # Edit ~/.metagpt/config2.yaml with your API keys",
        "",
        "4. Test the installation:",
        "   python verify_setup.py",
        "",
        "5. Run MetaGPT:",
        "   metagpt \"Create a simple Python calculator\"",
        "",
        "6. Optional: Install additional tools:",
        "   npm install -g @mermaid-js/mermaid-cli  # For diagrams",
        "   playwright install --with-deps chromium  # For web scraping"
    ]
    
    for step in steps:
        print(step)


def main():
    """Main function."""
    print("🚀 MetaGPT Usage Example")
    print("=" * 40)
    
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Python executable: {sys.executable}")
    print(f"Working directory: {Path.cwd()}")
    
    # Run demonstrations
    import_success = demonstrate_basic_imports()
    check_project_structure()
    demonstrate_config_loading()
    
    if import_success:
        print(f"\n✅ Basic MetaGPT structure is available!")
        print("The virtual environment is working correctly.")
    else:
        print(f"\n⚠️  MetaGPT imports failed - dependencies may need installation.")
    
    show_next_steps()
    
    return 0 if import_success else 1


if __name__ == "__main__":
    sys.exit(main())