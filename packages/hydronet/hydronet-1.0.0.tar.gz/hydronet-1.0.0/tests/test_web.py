"""
Test Web Interfaces
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_web_files():
    """Check if web interface files exist"""
    web_files = [
        'Web_Interfaces/index.html',
        'Web_Interfaces/web_app.py'
    ]
    
    all_exist = True
    for file in web_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"⚠️  {file} not found")
            all_exist = False
    
    return all_exist

if __name__ == "__main__":
    print("Testing Web Interfaces...")
    test_web_files()
    print("✅ Web interface tests completed")
