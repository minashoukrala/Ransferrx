#!/usr/bin/env python3
"""
Test Pharmacy Validator

Tests the pharmacy identification validation logic including
transfer types and pharmacy information requirements.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import xml.etree.ElementTree as ET
from fastapi import HTTPException
from app.utils.validators.pharmacy_validator import validate_pharmacy_identification
from app.utils.xml_parser import parse_xml_content


def create_test_xml(pharmacies):
    """Create test XML with specific pharmacy settings."""
    pharmacy_elements = ""
    for transfer_type in pharmacies:
        pharmacy_elements += f"""
        <Pharmacy>
            <NCPDPID>1234567</NCPDPID>
            <NPI>1234567890</NPI>
            <BusinessName>Test Pharmacy</BusinessName>
            <TransferType>{transfer_type}</TransferType>
        </Pharmacy>"""
    
    xml_template = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
        <MedicationPrescribed>
            <DrugDescription>Test Drug</DrugDescription>
        </MedicationPrescribed>
        {pharmacy_elements}
    </Message>"""
    return xml_template


def test_valid_pharmacy_identification():
    """Test valid pharmacy identification with both transfer types."""
    print("🧪 Testing Valid Pharmacy Identification...")
    
    pharmacies = ["TRANSFER FROM PHARMACY", "TRANSFER TO PHARMACY"]
    xml_content = create_test_xml(pharmacies)
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_pharmacy_identification(root, ns)
        print("✅ Valid pharmacy identification passed")
        return True
    except Exception as e:
        print(f"❌ Valid pharmacy identification failed: {e}")
        return False


def test_missing_pharmacy():
    """Test missing pharmacy information."""
    print("🧪 Testing Missing Pharmacy...")
    
    xml_template = """<?xml version="1.0" encoding="UTF-8"?>
    <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
        <MedicationPrescribed>
            <DrugDescription>Test Drug</DrugDescription>
        </MedicationPrescribed>
    </Message>"""
    
    root, ns = parse_xml_content(xml_template)
    
    try:
        validate_pharmacy_identification(root, ns)
        print("❌ Should have failed - missing pharmacy information")
        return False
    except HTTPException as e:
        if e.status_code == 400 and "CA" in str(e.detail):
            print("✅ Correctly rejected missing pharmacy information")
            return True
        else:
            print(f"❌ Wrong error type: {e}")
            return False


def test_single_pharmacy():
    """Test single pharmacy (should fail - need both)."""
    print("🧪 Testing Single Pharmacy...")
    
    pharmacies = ["TRANSFER FROM PHARMACY"]
    xml_content = create_test_xml(pharmacies)
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_pharmacy_identification(root, ns)
        print("❌ Should have failed - single pharmacy")
        return False
    except HTTPException as e:
        if e.status_code == 400 and "CA" in str(e.detail):
            print("✅ Correctly rejected single pharmacy")
            return True
        else:
            print(f"❌ Wrong error type: {e}")
            return False


def test_duplicate_transfer_types():
    """Test duplicate transfer types."""
    print("🧪 Testing Duplicate Transfer Types...")
    
    pharmacies = ["TRANSFER FROM PHARMACY", "TRANSFER FROM PHARMACY"]
    xml_content = create_test_xml(pharmacies)
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_pharmacy_identification(root, ns)
        print("❌ Should have failed - duplicate transfer types")
        return False
    except HTTPException as e:
        if e.status_code == 400 and "CA" in str(e.detail):
            print("✅ Correctly rejected duplicate transfer types")
            return True
        else:
            print(f"❌ Wrong error type: {e}")
            return False


def test_invalid_transfer_types():
    """Test invalid transfer types."""
    print("🧪 Testing Invalid Transfer Types...")
    
    pharmacies = ["TRANSFER FROM PHARMACY", "INVALID TRANSFER TYPE"]
    xml_content = create_test_xml(pharmacies)
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_pharmacy_identification(root, ns)
        print("❌ Should have failed - invalid transfer types")
        return False
    except HTTPException as e:
        if e.status_code == 400 and "CA" in str(e.detail):
            print("✅ Correctly rejected invalid transfer types")
            return True
        else:
            print(f"❌ Wrong error type: {e}")
            return False


def test_three_pharmacies():
    """Test three pharmacies (should fail - need exactly 2)."""
    print("🧪 Testing Three Pharmacies...")
    
    pharmacies = ["TRANSFER FROM PHARMACY", "TRANSFER TO PHARMACY", "TRANSFER FROM PHARMACY"]
    xml_content = create_test_xml(pharmacies)
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_pharmacy_identification(root, ns)
        print("❌ Should have failed - three pharmacies")
        return False
    except HTTPException as e:
        if e.status_code == 400 and "CA" in str(e.detail):
            print("✅ Correctly rejected three pharmacies")
            return True
        else:
            print(f"❌ Wrong error type: {e}")
            return False


def test_case_sensitive_transfer_types():
    """Test case sensitivity of transfer types."""
    print("🧪 Testing Case Sensitivity...")
    
    pharmacies = ["TRANSFER FROM PHARMACY", "transfer to pharmacy"]
    xml_content = create_test_xml(pharmacies)
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_pharmacy_identification(root, ns)
        print("❌ Should have failed - case sensitive transfer types")
        return False
    except HTTPException as e:
        if e.status_code == 400 and "CA" in str(e.detail):
            print("✅ Correctly rejected case sensitive transfer types")
            return True
        else:
            print(f"❌ Wrong error type: {e}")
            return False


def main():
    """Run all pharmacy validation tests."""
    print("🚀 Testing Pharmacy Validator")
    print("=" * 50)
    
    tests = [
        test_valid_pharmacy_identification,
        test_missing_pharmacy,
        test_single_pharmacy,
        test_duplicate_transfer_types,
        test_invalid_transfer_types,
        test_three_pharmacies,
        test_case_sensitive_transfer_types
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
        print("🎉 All pharmacy validation tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 