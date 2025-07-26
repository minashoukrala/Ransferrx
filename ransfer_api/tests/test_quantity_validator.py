#!/usr/bin/env python3
"""
Test Quantity Validator

Tests the quantity validation logic including quantity qualifiers
and relationships between original, remaining, and transferred quantities.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import xml.etree.ElementTree as ET
from fastapi import HTTPException
from app.utils.validators.quantity_validator import validate_quantity_qualifiers
from app.utils.xml_parser import parse_xml_content


def create_test_xml(quantities):
    """Create test XML with specific quantity settings."""
    quantity_elements = ""
    for qualifier, value in quantities:
        quantity_elements += f"""
            <Quantity>
                <CodeListQualifier>{qualifier}</CodeListQualifier>
                <Value>{value}</Value>
            </Quantity>"""
    
    xml_template = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
        <MedicationPrescribed>
            <DrugDescription>Test Drug</DrugDescription>
            {quantity_elements}
        </MedicationPrescribed>
    </Message>"""
    return xml_template


def test_valid_quantities():
    """Test valid quantity relationships."""
    print("🧪 Testing Valid Quantities...")
    
    # Original=180, Remaining=30, Transferred=30
    quantities = [("38", "180"), ("40", "30"), ("QT", "30")]
    xml_content = create_test_xml(quantities)
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_quantity_qualifiers(root, ns)
        print("✅ Valid quantities validation passed")
        return True
    except Exception as e:
        print(f"❌ Valid quantities validation failed: {e}")
        return False


def test_missing_quantity():
    """Test missing quantity qualifier."""
    print("🧪 Testing Missing Quantity...")
    
    # Missing QT qualifier
    quantities = [("38", "180"), ("40", "30")]
    xml_content = create_test_xml(quantities)
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_quantity_qualifiers(root, ns)
        print("❌ Should have failed - missing quantity qualifier")
        return False
    except HTTPException as e:
        if e.status_code == 400 and "BY" in str(e.detail):
            print("✅ Correctly rejected missing quantity qualifier")
            return True
        else:
            print(f"❌ Wrong error type: {e}")
            return False


def test_invalid_quantity_relationship():
    """Test invalid quantity relationship (Original < Remaining)."""
    print("🧪 Testing Invalid Quantity Relationship...")
    
    # Original=30, Remaining=180 (invalid: Original < Remaining)
    quantities = [("38", "30"), ("40", "180"), ("QT", "180")]
    xml_content = create_test_xml(quantities)
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_quantity_qualifiers(root, ns)
        print("❌ Should have failed - invalid quantity relationship")
        return False
    except HTTPException as e:
        if e.status_code == 400 and "BY" in str(e.detail):
            print("✅ Correctly rejected invalid quantity relationship")
            return True
        else:
            print(f"❌ Wrong error type: {e}")
            return False


def test_mismatched_transfer_quantity():
    """Test when transferred quantity doesn't match remaining quantity."""
    print("🧪 Testing Mismatched Transfer Quantity...")
    
    # Original=180, Remaining=30, Transferred=50 (should equal remaining)
    quantities = [("38", "180"), ("40", "30"), ("QT", "50")]
    xml_content = create_test_xml(quantities)
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_quantity_qualifiers(root, ns)
        print("❌ Should have failed - mismatched transfer quantity")
        return False
    except HTTPException as e:
        if e.status_code == 400 and "BY" in str(e.detail):
            print("✅ Correctly rejected mismatched transfer quantity")
            return True
        else:
            print(f"❌ Wrong error type: {e}")
            return False


def test_invalid_quantity_values():
    """Test invalid quantity values (non-integers)."""
    print("🧪 Testing Invalid Quantity Values...")
    
    # Non-integer values
    quantities = [("38", "abc"), ("40", "30"), ("QT", "30")]
    xml_content = create_test_xml(quantities)
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_quantity_qualifiers(root, ns)
        print("❌ Should have failed - invalid quantity values")
        return False
    except HTTPException as e:
        if e.status_code == 400 and "BY" in str(e.detail):
            print("✅ Correctly rejected invalid quantity values")
            return True
        else:
            print(f"❌ Wrong error type: {e}")
            return False


def test_duplicate_qualifiers():
    """Test duplicate quantity qualifiers."""
    print("🧪 Testing Duplicate Qualifiers...")
    
    # Duplicate 38 qualifier
    quantities = [("38", "180"), ("38", "200"), ("40", "30"), ("QT", "30")]
    xml_content = create_test_xml(quantities)
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_quantity_qualifiers(root, ns)
        print("❌ Should have failed - duplicate qualifiers")
        return False
    except HTTPException as e:
        if e.status_code == 400 and "BY" in str(e.detail):
            print("✅ Correctly rejected duplicate qualifiers")
            return True
        else:
            print(f"❌ Wrong error type: {e}")
            return False


def test_zero_quantities():
    """Test zero quantities (should be valid)."""
    print("🧪 Testing Zero Quantities...")
    
    # All zero quantities
    quantities = [("38", "0"), ("40", "0"), ("QT", "0")]
    xml_content = create_test_xml(quantities)
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_quantity_qualifiers(root, ns)
        print("✅ Zero quantities validation passed")
        return True
    except Exception as e:
        print(f"❌ Zero quantities validation failed: {e}")
        return False


def main():
    """Run all quantity validation tests."""
    print("🚀 Testing Quantity Validator")
    print("=" * 50)
    
    tests = [
        test_valid_quantities,
        test_missing_quantity,
        test_invalid_quantity_relationship,
        test_mismatched_transfer_quantity,
        test_invalid_quantity_values,
        test_duplicate_qualifiers,
        test_zero_quantities
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
        print("🎉 All quantity validation tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 