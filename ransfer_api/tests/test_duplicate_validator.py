#!/usr/bin/env python3
"""
Test Duplicate Validator

Tests the duplicate prescription validation logic to prevent
duplicate transfers and ensure data integrity.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import xml.etree.ElementTree as ET
from fastapi import HTTPException
from app.utils.validators.duplicate_validator import validate_duplicate_prescription
from app.utils.xml_parser import parse_xml_content


def create_test_xml(previously_filled="false"):
    """Create test XML with specific previously filled setting."""
    xml_template = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
        <MedicationPrescribed>
            <DrugDescription>Test Drug</DrugDescription>
        </MedicationPrescribed>
        <PrescriptionPreviouslyFilled>{previously_filled}</PrescriptionPreviouslyFilled>
    </Message>"""
    return xml_template


def test_not_previously_filled():
    """Test prescription that has not been previously filled."""
    print("🧪 Testing Not Previously Filled...")
    
    xml_content = create_test_xml(previously_filled="false")
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_duplicate_prescription(root, ns)
        print("✅ Not previously filled validation passed")
        return True
    except Exception as e:
        print(f"❌ Not previously filled validation failed: {e}")
        return False


def test_previously_filled():
    """Test prescription that has been previously filled."""
    print("🧪 Testing Previously Filled...")
    
    xml_content = create_test_xml(previously_filled="true")
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_duplicate_prescription(root, ns)
        print("❌ Should have failed - previously filled prescription")
        return False
    except HTTPException as e:
        if e.status_code == 403 and "CX" in str(e.detail):
            print("✅ Correctly rejected previously filled prescription")
            return True
        else:
            print(f"❌ Wrong error type: {e}")
            return False


def test_missing_previously_filled():
    """Test prescription with missing previously filled indicator."""
    print("🧪 Testing Missing Previously Filled...")
    
    xml_template = """<?xml version="1.0" encoding="UTF-8"?>
    <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
        <MedicationPrescribed>
            <DrugDescription>Test Drug</DrugDescription>
        </MedicationPrescribed>
    </Message>"""
    
    root, ns = parse_xml_content(xml_template)
    
    try:
        validate_duplicate_prescription(root, ns)
        print("✅ Missing previously filled validation passed")
        return True
    except Exception as e:
        print(f"❌ Missing previously filled validation failed: {e}")
        return False


def test_case_sensitive_previously_filled():
    """Test case sensitivity of previously filled values."""
    print("🧪 Testing Case Sensitivity...")
    
    # Test "TRUE" (uppercase) - should be rejected
    xml_content = create_test_xml(previously_filled="TRUE")
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_duplicate_prescription(root, ns)
        print("❌ Should have failed - uppercase TRUE")
        return False
    except HTTPException as e:
        if e.status_code == 403 and "CX" in str(e.detail):
            print("✅ Correctly rejected uppercase TRUE")
        else:
            print(f"❌ Wrong error type for uppercase TRUE: {e}")
            return False
    
    # Test "True" (title case) - should be rejected
    xml_content = create_test_xml(previously_filled="True")
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_duplicate_prescription(root, ns)
        print("❌ Should have failed - title case True")
        return False
    except HTTPException as e:
        if e.status_code == 403 and "CX" in str(e.detail):
            print("✅ Correctly rejected title case True")
            return True
        else:
            print(f"❌ Wrong error type for title case True: {e}")
            return False


def test_other_false_values():
    """Test other false values that should pass validation."""
    print("🧪 Testing Other False Values...")
    
    false_values = ["FALSE", "False", "no", "NO", "0", ""]
    
    for value in false_values:
        xml_content = create_test_xml(previously_filled=value)
        root, ns = parse_xml_content(xml_content)
        
        try:
            validate_duplicate_prescription(root, ns)
            print(f"✅ '{value}' validation passed")
        except Exception as e:
            print(f"❌ '{value}' validation failed: {e}")
            return False
    
    return True


def main():
    """Run all duplicate validation tests."""
    print("🚀 Testing Duplicate Validator")
    print("=" * 50)
    
    tests = [
        test_not_previously_filled,
        test_previously_filled,
        test_missing_previously_filled,
        test_case_sensitive_previously_filled,
        test_other_false_values
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All duplicate validation tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 