#!/usr/bin/env python3
"""
Test Controlled Substance Validator

Tests the controlled substance validation logic including DEA compliance
and safety checks for prescription transfers.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import xml.etree.ElementTree as ET
from fastapi import HTTPException
from app.utils.validators.controlled_substance_validator import validate_controlled_substance
from app.utils.xml_parser import parse_xml_content


def create_test_xml(controlled_substance="N", do_not_fill="N", previously_filled="false", digital_signature=None):
    """Create test XML with specific controlled substance settings."""
    xml_template = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
        <MedicationPrescribed>
            <DrugDescription>Test Drug</DrugDescription>
        </MedicationPrescribed>
        <ControlledSubstanceIndicator>{controlled_substance}</ControlledSubstanceIndicator>
        <DoNotFill>{do_not_fill}</DoNotFill>
        <PrescriptionPreviouslyFilled>{previously_filled}</PrescriptionPreviouslyFilled>
        {f'<DigitalSignature>{digital_signature}</DigitalSignature>' if digital_signature else ''}
    </Message>"""
    return xml_template


def test_non_controlled_substance():
    """Test validation of non-controlled substances."""
    print("🧪 Testing Non-Controlled Substance...")
    
    xml_content = create_test_xml(controlled_substance="N")
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_controlled_substance(root, ns)
        print("✅ Non-controlled substance validation passed")
        return True
    except Exception as e:
        print(f"❌ Non-controlled substance validation failed: {e}")
        return False


def test_controlled_substance_with_do_not_fill():
    """Test controlled substance with proper DoNotFill setting."""
    print("🧪 Testing Controlled Substance with DoNotFill='Y'...")
    
    xml_content = create_test_xml(
        controlled_substance="Y",
        do_not_fill="Y",
        digital_signature="SampleSignature"
    )
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_controlled_substance(root, ns)
        print("✅ Controlled substance with DoNotFill='Y' validation passed")
        return True
    except Exception as e:
        print(f"❌ Controlled substance with DoNotFill='Y' validation failed: {e}")
        return False


def test_controlled_substance_without_do_not_fill():
    """Test controlled substance without proper DoNotFill setting."""
    print("🧪 Testing Controlled Substance without DoNotFill='Y'...")
    
    xml_content = create_test_xml(
        controlled_substance="Y",
        do_not_fill="N",
        digital_signature="SampleSignature"
    )
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_controlled_substance(root, ns)
        print("❌ Should have failed - controlled substance without DoNotFill='Y'")
        return False
    except HTTPException as e:
        if e.status_code == 403 and "CX" in str(e.detail):
            print("✅ Correctly rejected controlled substance without DoNotFill='Y'")
            return True
        else:
            print(f"❌ Wrong error type: {e}")
            return False


def test_controlled_substance_without_digital_signature():
    """Test controlled substance without digital signature."""
    print("🧪 Testing Controlled Substance without Digital Signature...")
    
    xml_content = create_test_xml(
        controlled_substance="Y",
        do_not_fill="Y"
        # No digital signature
    )
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_controlled_substance(root, ns)
        print("❌ Should have failed - controlled substance without digital signature")
        return False
    except HTTPException as e:
        if e.status_code == 400 and "BC" in str(e.detail):
            print("✅ Correctly rejected controlled substance without digital signature")
            return True
        else:
            print(f"❌ Wrong error type: {e}")
            return False


def test_previously_filled_controlled_substance():
    """Test previously filled controlled substance."""
    print("🧪 Testing Previously Filled Controlled Substance...")
    
    xml_content = create_test_xml(
        controlled_substance="Y",
        do_not_fill="Y",
        previously_filled="true",
        digital_signature="SampleSignature"
    )
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_controlled_substance(root, ns)
        print("❌ Should have failed - previously filled controlled substance")
        return False
    except HTTPException as e:
        if e.status_code == 403 and "CX" in str(e.detail):
            print("✅ Correctly rejected previously filled controlled substance")
            return True
        else:
            print(f"❌ Wrong error type: {e}")
            return False


def main():
    """Run all controlled substance validation tests."""
    print("🚀 Testing Controlled Substance Validator")
    print("=" * 50)
    
    tests = [
        test_non_controlled_substance,
        test_controlled_substance_with_do_not_fill,
        test_controlled_substance_without_do_not_fill,
        test_controlled_substance_without_digital_signature,
        test_previously_filled_controlled_substance
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
        print("🎉 All controlled substance validation tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 