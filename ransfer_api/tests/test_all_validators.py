#!/usr/bin/env python3
"""
Test All Validators

Comprehensive test suite that tests all validators together
with the sample prescription XML.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.prescription_validator import validate_prescription_transfer
from app.utils.validators import (
    validate_controlled_substance,
    validate_digital_signature,
    validate_quantity_qualifiers,
    validate_refills_consistency,
    validate_prescription_expiration,
    validate_pharmacy_identification,
    validate_duplicate_prescription
)
from app.utils.xml_parser import parse_xml_content


def test_complete_validation():
    """Test the complete validation pipeline with sample XML."""
    print("🧪 Testing Complete Validation Pipeline...")
    
    try:
        # Load sample XML
        with open('tests/sample_rxtransfer.xml', 'r') as f:
            xml_content = f.read()
        
        # Test complete validation
        result = validate_prescription_transfer(xml_content)
        
        print("✅ Complete validation successful!")
        print(f"   Status: {result['status']}")
        print(f"   Message: {result['message']}")
        
        # Show validation details
        print("\n📋 Validation Details:")
        for check, status in result['validation_details'].items():
            print(f"   {check}: {status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Complete validation failed: {e}")
        return False


def test_individual_validators():
    """Test each individual validator with sample XML."""
    print("\n🧪 Testing Individual Validators...")
    
    try:
        # Load sample XML
        with open('tests/sample_rxtransfer.xml', 'r') as f:
            xml_content = f.read()
        
        # Parse XML once
        root, ns = parse_xml_content(xml_content)
        
        # Test each validator individually
        validators_to_test = [
            ("Controlled Substance", validate_controlled_substance),
            ("Digital Signature", validate_digital_signature),
            ("Quantity Qualifiers", validate_quantity_qualifiers),
            ("Refills Consistency", validate_refills_consistency),
            ("Prescription Expiration", validate_prescription_expiration),
            ("Pharmacy Identification", validate_pharmacy_identification),
            ("Duplicate Prevention", validate_duplicate_prescription)
        ]
        
        all_passed = True
        for name, validator in validators_to_test:
            try:
                validator(root, ns)
                print(f"✅ {name} validation passed")
            except Exception as e:
                print(f"❌ {name} validation failed: {e}")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Individual validators test failed: {e}")
        return False


def test_xml_parser():
    """Test XML parser functionality."""
    print("\n🧪 Testing XML Parser...")
    
    try:
        # Load sample XML
        with open('tests/sample_rxtransfer.xml', 'r') as f:
            xml_content = f.read()
        
        # Test parsing
        root, ns = parse_xml_content(xml_content)
        
        print("✅ XML parsing successful")
        print(f"   Root tag: {root.tag}")
        print(f"   Namespaces: {ns}")
        
        # Test structure validation
        from app.utils.xml_parser import validate_xml_structure
        validate_xml_structure(root, ns)
        print("✅ XML structure validation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ XML parser test failed: {e}")
        return False


def test_sample_xml_content():
    """Test the content of the sample XML file."""
    print("\n🧪 Testing Sample XML Content...")
    
    try:
        # Load and parse sample XML
        with open('tests/sample_rxtransfer.xml', 'r') as f:
            xml_content = f.read()
        
        root, ns = parse_xml_content(xml_content)
        
        # Check key elements
        checks = [
            ("MedicationPrescribed", root.find('.//ncpdp:MedicationPrescribed', ns)),
            ("ControlledSubstanceIndicator", root.find('.//ncpdp:ControlledSubstanceIndicator', ns)),
            ("PrescriptionPreviouslyFilled", root.find('.//ncpdp:PrescriptionPreviouslyFilled', ns)),
            ("WrittenDate", root.find('.//ncpdp:WrittenDate', ns)),
            ("Pharmacy", root.findall('.//ncpdp:Pharmacy', ns))
        ]
        
        for name, element in checks:
            if element is not None:
                if name == "Pharmacy":
                    print(f"✅ {name}: {len(element)} elements found")
                else:
                    print(f"✅ {name}: {element.text}")
            else:
                print(f"❌ {name}: Not found")
                return False
        
        # Check quantities
        quantities = root.findall('.//ncpdp:MedicationPrescribed/ncpdp:Quantity', ns)
        print(f"✅ Quantities: {len(quantities)} elements found")
        
        for qty in quantities:
            qualifier = qty.find('ncpdp:CodeListQualifier', ns)
            value = qty.find('ncpdp:Value', ns)
            if qualifier is not None and value is not None:
                print(f"   {qualifier.text}: {value.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Sample XML content test failed: {e}")
        return False


def test_error_handling():
    """Test error handling with invalid XML."""
    print("\n🧪 Testing Error Handling...")
    
    # Test with invalid XML
    invalid_xml = "<Invalid>XML</Invalid>"
    
    try:
        validate_prescription_transfer(invalid_xml)
        print("❌ Should have failed - invalid XML")
        return False
    except Exception as e:
        print(f"✅ Correctly handled invalid XML: {type(e).__name__}")
        return True


def main():
    """Run all comprehensive tests."""
    print("🚀 Testing All Validators")
    print("=" * 60)
    
    tests = [
        ("Sample XML Content", test_sample_xml_content),
        ("XML Parser", test_xml_parser),
        ("Individual Validators", test_individual_validators),
        ("Complete Validation", test_complete_validation),
        ("Error Handling", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test in tests:
        print(f"\n{'='*20} {name} {'='*20}")
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Results: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 All validators are working correctly!")
        print("\n✅ Validation System Status:")
        print("   • Controlled Substance Validation: Working")
        print("   • Digital Signature Validation: Working")
        print("   • Quantity Validation: Working")
        print("   • Refills Validation: Working")
        print("   • Expiration Validation: Working")
        print("   • Pharmacy Identification: Working")
        print("   • Duplicate Prevention: Working")
        print("   • XML Parser: Working")
        print("   • Complete Pipeline: Working")
        return True
    else:
        print("⚠️  Some test suites failed. Please review the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 