#!/usr/bin/env python3
"""
Test Malformed Data Handling

Tests handling of malformed XML, invalid data formats, and edge cases
that could cause crashes or unexpected behavior.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import HTTPException
from app.utils.prescription_validator import validate_prescription_transfer
from app.utils.xml_parser import parse_xml_content


def test_malformed_xml_syntax():
    """Test handling of malformed XML syntax."""
    print("🧪 Testing Malformed XML Syntax...")
    
    malformed_xmls = [
        "<Invalid>XML</Invalid>",  # Wrong root element
        "<Message><UnclosedTag>",  # Unclosed tag
        "Not XML at all",  # Plain text
        "",  # Empty string
        "   ",  # Whitespace only
        "<?xml version='1.0'?><Message><Broken>",  # Incomplete XML
    ]
    
    for i, xml_content in enumerate(malformed_xmls):
        try:
            validate_prescription_transfer(xml_content)
            print(f"❌ Should have failed - malformed XML {i+1}")
            return False
        except Exception as e:
            if "400" in str(e) or "Invalid XML" in str(e):
                print(f"✅ Correctly rejected malformed XML {i+1}")
            else:
                print(f"❌ Wrong error for malformed XML {i+1}: {e}")
                return False
    
    return True


def test_invalid_date_formats():
    """Test handling of invalid date formats."""
    print("\n🧪 Testing Invalid Date Formats...")
    
    invalid_dates = [
        "2025-13-01",  # Invalid month
        "2025-12-32",  # Invalid day
        "2025/01/15",  # Wrong separator
        "01-15-2025",  # MM-DD-YYYY format
        "15-01-2025",  # DD-MM-YYYY format
        "2025-1-5",    # Missing leading zeros
        "2025-01-15T12:00:00",  # ISO format with time
        "invalid-date",  # Non-date string
        "",  # Empty date
        "2025-00-00",  # Zero values
    ]
    
    for date_format in invalid_dates:
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
            <MedicationPrescribed>
                <DrugDescription>Test Drug</DrugDescription>
                <Quantity>
                    <CodeListQualifier>38</CodeListQualifier>
                    <Value>180</Value>
                </Quantity>
                <Quantity>
                    <CodeListQualifier>40</CodeListQualifier>
                    <Value>30</Value>
                </Quantity>
                <Quantity>
                    <CodeListQualifier>QT</CodeListQualifier>
                    <Value>30</Value>
                </Quantity>
                <WrittenDate>{date_format}</WrittenDate>
            </MedicationPrescribed>
            <Pharmacy>
                <TransferType>TRANSFER FROM PHARMACY</TransferType>
            </Pharmacy>
            <Pharmacy>
                <TransferType>TRANSFER TO PHARMACY</TransferType>
            </Pharmacy>
        </Message>"""
        
        try:
            validate_prescription_transfer(xml_content)
            print(f"❌ Should have failed - invalid date: {date_format}")
            return False
        except Exception as e:
            if "400" in str(e) and "BY" in str(e):
                print(f"✅ Correctly rejected invalid date: {date_format}")
            else:
                print(f"❌ Wrong error for invalid date {date_format}: {e}")
                return False
    
    return True


def test_empty_null_values():
    """Test handling of empty and null values."""
    print("\n🧪 Testing Empty/Null Values...")
    
    empty_value_tests = [
        ("<DrugDescription></DrugDescription>", "empty drug description"),
        ("<DrugDescription>   </DrugDescription>", "whitespace drug description"),
        ("<Value></Value>", "empty quantity value"),
        ("<Value>   </Value>", "whitespace quantity value"),
        ("<WrittenDate></WrittenDate>", "empty written date"),
        ("<TransferType></TransferType>", "empty transfer type"),
        ("<ControlledSubstanceIndicator></ControlledSubstanceIndicator>", "empty controlled substance indicator"),
    ]
    
    for element, description in empty_value_tests:
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
            <MedicationPrescribed>
                <DrugDescription>Test Drug</DrugDescription>
                <Quantity>
                    <CodeListQualifier>38</CodeListQualifier>
                    <Value>180</Value>
                </Quantity>
                <Quantity>
                    <CodeListQualifier>40</CodeListQualifier>
                    <Value>30</Value>
                </Quantity>
                <Quantity>
                    <CodeListQualifier>QT</CodeListQualifier>
                    <Value>30</Value>
                </Quantity>
                <WrittenDate>2025-01-15</WrittenDate>
                {element}
            </MedicationPrescribed>
            <Pharmacy>
                <TransferType>TRANSFER FROM PHARMACY</TransferType>
            </Pharmacy>
            <Pharmacy>
                <TransferType>TRANSFER TO PHARMACY</TransferType>
            </Pharmacy>
        </Message>"""
        
        try:
            validate_prescription_transfer(xml_content)
            print(f"✅ Handled {description} gracefully")
        except Exception as e:
            if "400" in str(e) and "BY" in str(e):
                print(f"✅ Correctly rejected {description}")
            else:
                print(f"❌ Unexpected error for {description}: {e}")
                return False
    
    return True


def test_special_characters():
    """Test handling of special characters and Unicode."""
    print("\n🧪 Testing Special Characters...")
    
    special_char_tests = [
        ("Dr. Smith's Rx", "apostrophe in name"),
        ("Médication Français", "accented characters"),
        ("Drug & More", "ampersand"),
        ("Drug < 10mg", "less than symbol"),
        ("Drug > 5mg", "greater than symbol"),
        ("Drug \"Special\"", "quotes"),
        ("Drug\nNewline", "newline character"),
        ("Drug\tTab", "tab character"),
        ("Drug with spaces ", "trailing spaces"),
        (" Drug with spaces", "leading spaces"),
    ]
    
    for test_value, description in special_char_tests:
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
            <MedicationPrescribed>
                <DrugDescription>{test_value}</DrugDescription>
                <Quantity>
                    <CodeListQualifier>38</CodeListQualifier>
                    <Value>180</Value>
                </Quantity>
                <Quantity>
                    <CodeListQualifier>40</CodeListQualifier>
                    <Value>30</Value>
                </Quantity>
                <Quantity>
                    <CodeListQualifier>QT</CodeListQualifier>
                    <Value>30</Value>
                </Quantity>
                <WrittenDate>2025-01-15</WrittenDate>
            </MedicationPrescribed>
            <Pharmacy>
                <TransferType>TRANSFER FROM PHARMACY</TransferType>
            </Pharmacy>
            <Pharmacy>
                <TransferType>TRANSFER TO PHARMACY</TransferType>
            </Pharmacy>
        </Message>"""
        
        try:
            validate_prescription_transfer(xml_content)
            # For ampersand and less than, this should not succeed (invalid XML)
            # Greater than is valid in XML text content
            if any(x in description for x in ["ampersand", "less than symbol"]):
                print(f"❌ Should have failed - {description}")
                return False
            print(f"✅ Handled {description} correctly")
        except Exception as e:
            # For ampersand and less than, expect a 400 error due to invalid XML
            if any(x in description for x in ["ampersand", "less than symbol"]):
                if "400" in str(e) and "BY" in str(e):
                    print(f"✅ Correctly rejected {description} (invalid XML)")
                else:
                    print(f"❌ Wrong error for {description}: {e}")
                    return False
            else:
                print(f"❌ Failed to handle {description}: {e}")
                return False
    
    return True


def test_boundary_values():
    """Test boundary values and edge cases."""
    print("\n🧪 Testing Boundary Values...")
    
    # Test exactly 1 year old prescription (should pass)
    from datetime import datetime, timedelta
    exactly_one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
        <MedicationPrescribed>
            <DrugDescription>Test Drug</DrugDescription>
            <Quantity>
                <CodeListQualifier>38</CodeListQualifier>
                <Value>180</Value>
            </Quantity>
            <Quantity>
                <CodeListQualifier>40</CodeListQualifier>
                <Value>30</Value>
            </Quantity>
            <Quantity>
                <CodeListQualifier>QT</CodeListQualifier>
                <Value>30</Value>
            </Quantity>
            <WrittenDate>{exactly_one_year_ago}</WrittenDate>
        </MedicationPrescribed>
        <Pharmacy>
            <TransferType>TRANSFER FROM PHARMACY</TransferType>
        </Pharmacy>
        <Pharmacy>
            <TransferType>TRANSFER TO PHARMACY</TransferType>
        </Pharmacy>
    </Message>"""
    
    try:
        validate_prescription_transfer(xml_content)
        print("✅ Exactly 1 year old prescription passed")
    except Exception as e:
        print(f"❌ Exactly 1 year old prescription failed: {e}")
        return False
    
    # Test exactly 1 year + 1 day old prescription (should fail)
    one_year_one_day_ago = (datetime.now() - timedelta(days=366)).strftime('%Y-%m-%d')
    
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
        <MedicationPrescribed>
            <DrugDescription>Test Drug</DrugDescription>
            <Quantity>
                <CodeListQualifier>38</CodeListQualifier>
                <Value>180</Value>
            </Quantity>
            <Quantity>
                <CodeListQualifier>40</CodeListQualifier>
                <Value>30</Value>
            </Quantity>
            <Quantity>
                <CodeListQualifier>QT</CodeListQualifier>
                <Value>30</Value>
            </Quantity>
            <WrittenDate>{one_year_one_day_ago}</WrittenDate>
        </MedicationPrescribed>
        <Pharmacy>
            <TransferType>TRANSFER FROM PHARMACY</TransferType>
        </Pharmacy>
        <Pharmacy>
            <TransferType>TRANSFER TO PHARMACY</TransferType>
        </Pharmacy>
    </Message>"""
    
    try:
        validate_prescription_transfer(xml_content)
        print("❌ Should have failed - exactly 1 year + 1 day old")
        return False
    except Exception as e:
        if "403" in str(e) and "CW" in str(e):
            print("✅ Correctly rejected exactly 1 year + 1 day old prescription")
        else:
            print(f"❌ Wrong error for expired prescription: {e}")
            return False
    
    return True


def test_missing_required_elements():
    """Test handling of missing required elements."""
    print("\n🧪 Testing Missing Required Elements...")
    
    missing_element_tests = [
        ("<MedicationPrescribed>", "missing MedicationPrescribed"),
        ("<Quantity>", "missing Quantity elements"),
        ("<Pharmacy>", "missing Pharmacy elements"),
        ("<WrittenDate>", "missing WrittenDate"),
        ("<DrugDescription>", "missing DrugDescription"),
    ]
    
    for element, description in missing_element_tests:
        # Create XML without the specified element
        xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
            <MedicationPrescribed>
                <DrugDescription>Test Drug</DrugDescription>
                <Quantity>
                    <CodeListQualifier>38</CodeListQualifier>
                    <Value>180</Value>
                </Quantity>
                <Quantity>
                    <CodeListQualifier>40</CodeListQualifier>
                    <Value>30</Value>
                </Quantity>
                <Quantity>
                    <CodeListQualifier>QT</CodeListQualifier>
                    <Value>30</Value>
                </Quantity>
                <WrittenDate>2025-01-15</WrittenDate>
            </MedicationPrescribed>
            <Pharmacy>
                <TransferType>TRANSFER FROM PHARMACY</TransferType>
            </Pharmacy>
            <Pharmacy>
                <TransferType>TRANSFER TO PHARMACY</TransferType>
            </Pharmacy>
        </Message>"""
        
        # Remove the element being tested
        if "MedicationPrescribed" in description:
            xml_content = xml_content.replace("<MedicationPrescribed>", "").replace("</MedicationPrescribed>", "")
        elif "Quantity" in description:
            xml_content = xml_content.replace("<Quantity>", "").replace("</Quantity>", "")
        elif "Pharmacy" in description:
            xml_content = xml_content.replace("<Pharmacy>", "").replace("</Pharmacy>", "")
        elif "WrittenDate" in description:
            xml_content = xml_content.replace("<WrittenDate>2025-01-15</WrittenDate>", "")
        elif "DrugDescription" in description:
            xml_content = xml_content.replace("<DrugDescription>Test Drug</DrugDescription>", "")
        
        try:
            validate_prescription_transfer(xml_content)
            print(f"❌ Should have failed - {description}")
            return False
        except Exception as e:
            if "400" in str(e) and "BY" in str(e):
                print(f"✅ Correctly rejected {description}")
            else:
                print(f"❌ Wrong error for {description}: {e}")
                return False
    
    return True


def main():
    """Run all malformed data tests."""
    print("🚀 Testing Malformed Data Handling")
    print("=" * 60)
    
    tests = [
        test_malformed_xml_syntax,
        test_invalid_date_formats,
        test_empty_null_values,
        test_special_characters,
        test_boundary_values,
        test_missing_required_elements
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
        print("🎉 All malformed data tests passed!")
        return True
    else:
        print("⚠️  Some malformed data tests failed.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 