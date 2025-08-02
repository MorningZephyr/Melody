#!/usr/bin/env python3
"""
Test script for Piano Technique Master
Verifies that all components are working correctly
"""

import sys
import os
import requests
import subprocess
import time

def test_dependencies():
    """Test if all required packages are installed"""
    print("🔍 Testing dependencies...")
    
    try:
        import music21
        import numpy
        import flask
        import flask_cors
        print("✅ All dependencies installed correctly")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def test_midi_parsing():
    """Test MIDI parsing functionality"""
    print("🎵 Testing MIDI parsing...")
    
    try:
        from parse_midi import parse_midi_file, analyze_difficulty
        
        # Test with the sample file
        if os.path.exists("Alla_Turca_Mozart.mid"):
            notes = parse_midi_file("Alla_Turca_Mozart.mid")
            difficulty = analyze_difficulty(notes)
            
            print(f"✅ MIDI parsing successful")
            print(f"   📊 Notes found: {len(notes)}")
            print(f"   📈 Difficulty: {difficulty['level']}")
            return True
        else:
            print("❌ Sample MIDI file not found")
            return False
            
    except Exception as e:
        print(f"❌ MIDI parsing failed: {e}")
        return False

def test_backend_api():
    """Test if backend API is accessible"""
    print("🌐 Testing backend API...")
    
    try:
        # Check if backend is running
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API is running")
            return True
        else:
            print("❌ Backend API returned error")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Backend not running (this is normal if not started yet)")
        return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_frontend_files():
    """Test if frontend files exist"""
    print("🖥️  Testing frontend files...")
    
    frontend_files = [
        "frontend/index.html",
        "frontend/styles.css", 
        "frontend/script.js"
    ]
    
    all_exist = True
    for file in frontend_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("🎹 Piano Technique Master - System Test")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("MIDI Parsing", test_midi_parsing), 
        ("Frontend Files", test_frontend_files),
        ("Backend API", test_backend_api)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! The system is ready to use.")
        print("\n🚀 To start the application:")
        print("   1. Run: python backend/app.py")
        print("   2. Open: frontend/index.html in your browser")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        print("\n🔧 Common solutions:")
        print("   - Run: pip install -r requirements.txt")
        print("   - Run: pip install -r backend/requirements.txt")
        print("   - Make sure you're in the correct directory")

if __name__ == "__main__":
    main()
