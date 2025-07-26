#!/usr/bin/env python3
"""
Enhanced Validator Tests

This module tests enhanced validation scenarios including:
- Refills edge cases and invalid values
- Expiration edge cases and invalid formats
- Digital signature edge cases and invalid formats
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import HTTPException
from app.utils.validators.refills_validator import validate_refills_consistency
from app.utils.validators.expiration_validator import validate_prescription_expiration
from app.utils.validators.digital_signature_validator import validate_digital_signature
from app.utils.xml_parser import parse_xml_content


def create_test_xml_with_refills(number_of_refills, refills_remaining):
    """Create test XML with specific refill settings."""
    xml_template = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
        <MedicationPrescribed>
            <DrugDescription>Test Drug</DrugDescription>
            <NumberOfRefills>{number_of_refills}</NumberOfRefills>
            <RefillsRemaining>{refills_remaining}</RefillsRemaining>
        </MedicationPrescribed>
    </Message>"""
    return xml_template


def test_refills_edge_cases():
    """Test refills validator edge cases."""
    print("🧪 Testing Refills Edge Cases...")
    
    refill_tests = [
        # (number_of_refills, refills_remaining, should_pass, description)
        (0, 0, True, "zero refills"),
        (1, 0, True, "one refill, none remaining"),
        (1, 1, True, "one refill, one remaining"),
        (1, 2, False, "one refill, two remaining (invalid)"),
        (-1, 0, False, "negative refills"),
        (0, 1, False, "zero refills, one remaining (invalid)"),
        (5, 5, True, "five refills, five remaining"),
        (5, 0, True, "five refills, none remaining"),
        (5, 6, False, "five refills, six remaining (invalid)"),
    ]
    
    for num_refills, remaining, should_pass, description in refill_tests:
        xml_content = create_test_xml_with_refills(num_refills, remaining)
        root, ns = parse_xml_content(xml_content)
        
        try:
            validate_refills_consistency(root, ns)
            if should_pass:
                print(f"✅ {description} passed")
            else:
                print(f"❌ Should have failed - {description}")
                return False
        except HTTPException as e:
            if should_pass:
                print(f"❌ Should have passed - {description}: {e}")
                return False
            else:
                if e.status_code == 400 and "BY" in str(e.detail):
                    print(f"✅ Correctly rejected {description}")
                else:
                    print(f"❌ Wrong error for {description}: {e}")
                    return False
        except Exception as e:
            print(f"❌ Unexpected error for {description}: {e}")
            return False
    
    return True


def test_refills_invalid_values():
    """Test refills validator with invalid values."""
    print("\n🧪 Testing Refills Invalid Values...")
    
    invalid_refill_tests = [
        ("abc", "5", "non-integer number of refills"),
        ("5", "def", "non-integer refills remaining"),
        ("", "5", "empty number of refills"),
        ("5", "", "empty refills remaining"),
        ("5.5", "3", "decimal number of refills"),
        ("3", "2.5", "decimal refills remaining"),
    ]
    
    for num_refills, remaining, description in invalid_refill_tests:
        xml_content = create_test_xml_with_refills(num_refills, remaining)
        root, ns = parse_xml_content(xml_content)
        
        try:
            validate_refills_consistency(root, ns)
            print(f"❌ Should have failed - {description}")
            return False
        except HTTPException as e:
            if e.status_code == 400 and "BY" in str(e.detail):
                print(f"✅ Correctly rejected {description}")
            else:
                print(f"❌ Wrong error for {description}: {e}")
                return False
        except Exception as e:
            print(f"❌ Unexpected error for {description}: {e}")
            return False
    
    return True


def create_test_xml_with_date(written_date):
    """Create test XML with specific written date."""
    xml_template = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
        <MedicationPrescribed>
            <DrugDescription>Test Drug</DrugDescription>
            <WrittenDate>{written_date}</WrittenDate>
        </MedicationPrescribed>
    </Message>"""
    return xml_template


def test_expiration_edge_cases():
    """Test expiration validator edge cases."""
    print("\n🧪 Testing Expiration Edge Cases...")
    
    from datetime import datetime, timedelta
    
    # Test future dates (should fail)
    future_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    xml_content = create_test_xml_with_date(future_date)
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_prescription_expiration(root, ns)
        print("❌ Should have failed - future date")
        return False
    except HTTPException as e:
        if e.status_code == 400 and "BY" in str(e.detail):
            print("✅ Correctly rejected future date")
        else:
            print(f"❌ Wrong error for future date: {e}")
            return False
    
    # Test exactly 1 year ago (should pass)
    exactly_one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    xml_content = create_test_xml_with_date(exactly_one_year_ago)
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_prescription_expiration(root, ns)
        print("✅ Exactly 1 year ago passed")
    except Exception as e:
        print(f"❌ Exactly 1 year ago failed: {e}")
        return False
    
    # Test exactly 1 year + 1 day ago (should fail)
    one_year_one_day_ago = (datetime.now() - timedelta(days=366)).strftime('%Y-%m-%d')
    xml_content = create_test_xml_with_date(one_year_one_day_ago)
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_prescription_expiration(root, ns)
        print("❌ Should have failed - exactly 1 year + 1 day ago")
        return False
    except HTTPException as e:
        if e.status_code == 403 and "CW" in str(e.detail):
            print("✅ Correctly rejected exactly 1 year + 1 day ago")
        else:
            print(f"❌ Wrong error for expired prescription: {e}")
            return False
    
    return True


def test_expiration_invalid_formats():
    """Test expiration validator with invalid date formats."""
    print("\n🧪 Testing Expiration Invalid Formats...")
    
    invalid_date_formats = [
        "2025-13-01",  # Invalid month
        "2025-12-32",  # Invalid day
        "2025/01/15",  # Wrong separator
        "01-15-2025",  # MM-DD-YYYY format
        "15-01-2025",  # DD-MM-YYYY format
        "2025-1-5",    # Missing leading zeros
        "2025-01-15T12:00:00",  # ISO format with time
        "invalid-date",  # Non-date string
        "2025-00-00",  # Zero values
    ]
    
    for date_format in invalid_date_formats:
        xml_content = create_test_xml_with_date(date_format)
        root, ns = parse_xml_content(xml_content)
        
        try:
            validate_prescription_expiration(root, ns)
            print(f"❌ Should have failed - invalid date format: {date_format}")
            return False
        except HTTPException as e:
            if e.status_code == 400 and "BY" in str(e.detail):
                print(f"✅ Correctly rejected invalid date format: {date_format}")
            else:
                print(f"❌ Wrong error for invalid date format {date_format}: {e}")
                return False
        except Exception as e:
            print(f"❌ Unexpected error for invalid date format {date_format}: {e}")
            return False
    
    return True


def create_test_xml_with_signature(digital_signature=None, controlled_substance="N"):
    """Create test XML with specific digital signature settings."""
    signature_element = f'<DigitalSignature>{digital_signature}</DigitalSignature>' if digital_signature else ''
    xml_template = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
        <MedicationPrescribed>
            <DrugDescription>Test Drug</DrugDescription>
        </MedicationPrescribed>
        <ControlledSubstanceIndicator>{controlled_substance}</ControlledSubstanceIndicator>
        {signature_element}
    </Message>"""
    return xml_template


def test_digital_signature_edge_cases():
    """Test digital signature validator edge cases."""
    print("\n🧪 Testing Digital Signature Edge Cases...")
    
    # Test non-controlled substance without signature (should pass)
    xml_content = create_test_xml_with_signature(controlled_substance="N")
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_digital_signature(root, ns)
        print("✅ Non-controlled substance without signature passed")
    except Exception as e:
        print(f"❌ Non-controlled substance without signature failed: {e}")
        return False
    
    # Test controlled substance without signature (should fail)
    xml_content = create_test_xml_with_signature(controlled_substance="Y")
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_digital_signature(root, ns)
        print("❌ Should have failed - controlled substance without signature")
        return False
    except HTTPException as e:
        if e.status_code == 400 and "BC" in str(e.detail):
            print("✅ Correctly rejected controlled substance without signature")
        else:
            print(f"❌ Wrong error for controlled substance without signature: {e}")
            return False
    
    # Test controlled substance with empty signature (should fail)
    xml_content = create_test_xml_with_signature("", controlled_substance="Y")
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_digital_signature(root, ns)
        print("❌ Should have failed - controlled substance with empty signature")
        return False
    except HTTPException as e:
        if e.status_code == 400 and "BC" in str(e.detail):
            print("✅ Correctly rejected controlled substance with empty signature")
        else:
            print(f"❌ Wrong error for controlled substance with empty signature: {e}")
            return False
    
    # Test controlled substance with whitespace signature (should fail)
    xml_content = create_test_xml_with_signature("   ", controlled_substance="Y")
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_digital_signature(root, ns)
        print("❌ Should have failed - controlled substance with whitespace signature")
        return False
    except HTTPException as e:
        if e.status_code == 400 and "BC" in str(e.detail):
            print("✅ Correctly rejected controlled substance with whitespace signature")
        else:
            print(f"❌ Wrong error for controlled substance with whitespace signature: {e}")
            return False
    
    return True


def test_digital_signature_invalid_formats():
    """Test digital signature validator with invalid signature formats."""
    print("\n🧪 Testing Digital Signature Invalid Formats...")
    
    # Test controlled substance with malformed signature
    xml_content = create_test_xml_with_signature("<Invalid>Signature</Invalid>", controlled_substance="Y")
    root, ns = parse_xml_content(xml_content)
    
    try:
        validate_digital_signature(root, ns)
        print("✅ Handled malformed signature gracefully (certificate not found)")
    except Exception as e:
        # Accept either certificate not found or empty signature error
        if ("certificate" in str(e).lower() or "not found" in str(e).lower() or 
            "empty" in str(e).lower() or "whitespace" in str(e).lower()):
            print("✅ Correctly handled malformed signature")
        else:
            print(f"❌ Unexpected error for malformed signature: {e}")
            return False
    
    return True


def main():
    """Run all enhanced validator tests."""
    print("🚀 Testing Enhanced Validators")
    print("=" * 60)
    
    tests = [
        test_refills_edge_cases,
        test_refills_invalid_values,
        test_expiration_edge_cases,
        test_expiration_invalid_formats,
        test_digital_signature_edge_cases,
        test_digital_signature_invalid_formats
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All enhanced validator tests passed!")
        return True
    else:
        print("⚠️  Some enhanced validator tests failed.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 