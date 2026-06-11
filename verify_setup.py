#!/usr/bin/env python3
"""
MetaGPT Setup Verification Script

This script verifies that the virtual environment is properly set up
and all core dependencies are available.
"""

import importlib
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Check if Python version meets requirements."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 9:
        print("   ✅ Python version is compatible")
        return True
    else:
        print(f"   ❌ Python 3.9+ required, found {version.major}.{version.minor}")
        return False


def check_virtual_env():
    """Check if running in virtual environment."""
    print("\n🔧 Checking virtual environment...")
    
    # Check if in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("   ✅ Running in virtual environment")
        print(f"   📍 Python executable: {sys.executable}")
        return True
    else:
        print("   ⚠️  Not running in virtual environment")
        print("   💡 Activate with: source venv/bin/activate")
        return False


def check_package_import(package_name, description=""):
    """Check if a package can be imported."""
    try:
        importlib.import_module(package_name)
        print(f"   ✅ {package_name} {description}")
        return True
    except ImportError:
        print(f"   ❌ {package_name} {description} - not available")
        return False


def check_core_dependencies():
    """Check core dependencies."""
    print("\n📦 Checking core dependencies...")
    
    dependencies = [
        ("sys", "- Python standard library"),
        ("pathlib", "- Path utilities"),
        ("subprocess", "- Process management"),
        ("importlib", "- Import utilities"),
    ]
    
    # Try to check some common packages
    optional_deps = [
        ("numpy", "- Numerical computing"),
        ("pandas", "- Data manipulation"),
        ("pydantic", "- Data validation"),
        ("aiohttp", "- Async HTTP client"),
        ("openai", "- OpenAI API client"),
        ("typer", "- CLI framework"),
        ("rich", "- Rich text formatting"),
        ("loguru", "- Enhanced logging"),
    ]
    
    # Check required deps
    all_good = True
    for package, desc in dependencies:
        if not check_package_import(package, desc):
            all_good = False
    
    # Check optional deps
    optional_count = 0
    for package, desc in optional_deps:
        if check_package_import(package, desc):
            optional_count += 1
    
    print(f"\n   📊 Optional dependencies: {optional_count}/{len(optional_deps)} available")
    return all_good


def check_metagpt():
    """Check if MetaGPT can be imported."""
    print("\n🤖 Checking MetaGPT installation...")
    
    try:
        import metagpt
        print("   ✅ MetaGPT module can be imported")
        
        # Try to get version info
        try:
            # Check if version is available
            if hasattr(metagpt, '__version__'):
                print(f"   📍 Version: {metagpt.__version__}")
            else:
                print("   📍 Version: Development (no version attribute)")
        except:
            print("   📍 Version: Unknown")
            
        return True
        
    except ImportError as e:
        print(f"   ❌ MetaGPT module not available: {e}")
        print("   💡 Try: pip install -e .")
        return False


def check_console_script():
    """Check if metagpt console script is available."""
    print("\n🎯 Checking console script...")
    
    try:
        result = subprocess.run(['metagpt', '--help'], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        if result.returncode == 0:
            print("   ✅ 'metagpt' command is available")
            return True
        else:
            print("   ❌ 'metagpt' command failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("   ❌ 'metagpt' command not found")
        print("   💡 Install with: pip install -e .")
        return False


def check_config_files():
    """Check for configuration files."""
    print("\n⚙️  Checking configuration...")
    
    config_locations = [
        Path.home() / ".metagpt" / "config2.yaml",
        Path("config") / "config2.yaml",
    ]
    
    found_config = False
    for config_path in config_locations:
        if config_path.exists():
            print(f"   ✅ Config found: {config_path}")
            found_config = True
        else:
            print(f"   ❌ Config not found: {config_path}")
    
    if not found_config:
        print("   💡 Setup config with:")
        print("      mkdir -p ~/.metagpt")
        print("      cp config/config2.yaml ~/.metagpt/config2.yaml")
        print("      # Edit ~/.metagpt/config2.yaml with your API keys")
    
    return found_config


def check_optional_tools():
    """Check for optional tools."""
    print("\n🛠️  Checking optional tools...")
    
    # Check Node.js and npm for mermaid-cli
    try:
        result = subprocess.run(['npm', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print(f"   ✅ npm available (version {result.stdout.strip()})")
            
            # Check mermaid-cli
            try:
                result = subprocess.run(['mmdc', '--version'], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=5)
                if result.returncode == 0:
                    print("   ✅ mermaid-cli available")
                else:
                    print("   ❌ mermaid-cli not available")
                    print("   💡 Install with: npm install -g @mermaid-js/mermaid-cli")
            except FileNotFoundError:
                print("   ❌ mermaid-cli not available")
                print("   💡 Install with: npm install -g @mermaid-js/mermaid-cli")
                
        else:
            print("   ❌ npm not working properly")
    except FileNotFoundError:
        print("   ❌ npm not found")
        print("   💡 Install Node.js from: https://nodejs.org/")
    
    # Check playwright
    try:
        result = subprocess.run(['playwright', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print("   ✅ Playwright available")
        else:
            print("   ❌ Playwright not available")
    except FileNotFoundError:
        print("   ❌ Playwright not available")
        print("   💡 Install browsers with: playwright install --with-deps chromium")


def main():
    """Main verification function."""
    print("🚀 MetaGPT Setup Verification")
    print("=" * 40)
    
    checks = [
        check_python_version(),
        check_virtual_env(),
        check_core_dependencies(),
        check_metagpt(),
        check_console_script(),
        check_config_files(),
    ]
    
    # Optional checks (don't affect overall status)
    check_optional_tools()
    
    print("\n" + "=" * 40)
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print("🎉 All checks passed! MetaGPT setup is ready.")
        return 0
    else:
        print(f"⚠️  {passed}/{total} checks passed. Setup needs attention.")
        print("\n💡 Next steps:")
        print("1. Ensure virtual environment is activated: source venv/bin/activate")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Install MetaGPT: pip install -e .")
        print("4. Setup configuration files as shown above")
        return 1


if __name__ == "__main__":
    sys.exit(main())