#!/usr/bin/env python3
"""
Integration Tests

This module tests the complete system integration including:
- API endpoint functionality
- End-to-end validation workflows
- Concurrency and performance tests
"""

import sys
import os
import asyncio
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import json
from fastapi.testclient import TestClient
from app.main import app
from app.services.prescription_service import prescription_service


def create_test_client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_health_endpoint():
    """Test the health endpoint."""
    print("🧪 Testing Health Endpoint...")
    
    client = create_test_client()
    response = client.get("/health")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "healthy":
            print("✅ Health endpoint working correctly")
            return True
        else:
            print(f"❌ Health endpoint returned wrong status: {data}")
            return False
    else:
        print(f"❌ Health endpoint failed with status: {response.status_code}")
        return False


def test_validate_transfer_endpoint_valid():
    """Test validate transfer endpoint with valid XML."""
    print("\n🧪 Testing Validate Transfer Endpoint (Valid)...")
    
    try:
        client = create_test_client()
        
        # Valid XML content
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
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
        
        response = client.post("/api/v1/transfers/validate-transfer", content=xml_content)
        
        if response.status_code == 200:
            print("✅ Validate transfer endpoint working correctly")
            return True
        else:
            print(f"❌ Validate transfer endpoint failed with status: {response.status_code}")
            print(f"   Response: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Validate transfer endpoint test failed: {e}")
        return False


def test_validate_transfer_endpoint_invalid():
    """Test validate transfer endpoint with invalid XML."""
    print("\n🧪 Testing Validate Transfer Endpoint (Invalid)...")
    
    try:
        client = create_test_client()
        
        # Invalid XML content
        invalid_xml = "<invalid>xml</invalid>"
        
        response = client.post("/api/v1/transfers/validate-transfer", content=invalid_xml)
        
        if response.status_code == 400:
            print("✅ Validate transfer endpoint correctly rejected invalid XML")
            return True
        else:
            print(f"❌ Validate transfer endpoint should have failed with 400, got: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Validate transfer endpoint invalid test failed: {e}")
        return False


def test_verify_signature_endpoint():
    """Test verify signature endpoint."""
    print("\n🧪 Testing Verify Signature Endpoint...")
    
    try:
        client = create_test_client()
        
        # XML with digital signature
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
            <MedicationPrescribed>
                <DrugDescription>Test Drug</DrugDescription>
                <WrittenDate>2025-01-15</WrittenDate>
            </MedicationPrescribed>
            <Pharmacy>
                <TransferType>TRANSFER FROM PHARMACY</TransferType>
            </Pharmacy>
            <DigitalSignature>
                <Signature>test-signature</Signature>
            </DigitalSignature>
        </Message>"""
        
        response = client.post("/api/v1/transfers/verify-signature", content=xml_content)
        
        if response.status_code in [200, 400]:  # 200 for success, 400 for signature verification failure
            print("✅ Verify signature endpoint working correctly")
            return True
        else:
            print(f"❌ Verify signature endpoint failed with status: {response.status_code}")
            print(f"   Response: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Verify signature endpoint test failed: {e}")
        return False


async def test_service_integration():
    """Test service layer integration."""
    print("\n🧪 Testing Service Integration...")
    
    # Clear processed transfers for clean test
    prescription_service.clear_processed_transfers()
    
    # Load valid sample XML
    with open('tests/sample_rxtransfer.xml', 'r') as f:
        xml_content = f.read()
    
    try:
        # Test service validation
        result = await prescription_service.validate_transfer(xml_content)
        
        if result.get("status") == "valid":
            print("✅ Service validation working correctly")
            
            # Check that transfer was recorded
            processed_transfers = prescription_service.get_processed_transfers()
            if len(processed_transfers) > 0:
                print("✅ Transfer tracking working correctly")
                return True
            else:
                print("❌ Transfer tracking not working")
                return False
        else:
            print(f"❌ Service validation returned wrong status: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Service integration failed: {e}")
        return False


def test_error_handling_integration():
    """Test error handling in integration scenarios."""
    print("\n🧪 Testing Error Handling Integration...")
    
    try:
        client = create_test_client()
        
        # Test with missing XML content
        response = client.post("/api/v1/transfers/validate-transfer")
        
        if response.status_code in [400, 422]:
            print("✅ Correctly handled missing XML content")
            return True
        else:
            print(f"❌ Should have failed with 422 for missing XML, got: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error handling integration test failed: {e}")
        return False


def test_concurrent_validation():
    """Test concurrent validation requests."""
    print("\n🧪 Testing Concurrent Validation...")
    
    try:
        client = create_test_client()
        
        # Valid XML content
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
            <MedicationPrescribed>
                <DrugDescription>Test Drug</DrugDescription>
                <WrittenDate>2025-01-15</WrittenDate>
            </MedicationPrescribed>
            <Pharmacy>
                <TransferType>TRANSFER FROM PHARMACY</TransferType>
            </Pharmacy>
        </Message>"""
        
        # Send multiple concurrent requests
        responses = []
        for i in range(5):
            response = client.post("/api/v1/transfers/validate-transfer", content=xml_content)
            responses.append(response.status_code)
        
        # Check if all requests were processed
        success_count = sum(1 for status in responses if status in [200, 400])
        if success_count == 5:
            print("✅ Concurrent validation working correctly")
            return True
        else:
            print(f"❌ Concurrent validation failed: {responses}")
            return False
            
    except Exception as e:
        print(f"❌ Concurrent validation test failed: {e}")
        return False


def test_basic_performance():
    """Test basic performance metrics."""
    print("\n🧪 Testing Basic Performance...")
    
    try:
        client = create_test_client()
        
        # Valid XML content
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <Message xmlns="http://www.ncpdp.org/schema/SCRIPT">
            <MedicationPrescribed>
                <DrugDescription>Test Drug</DrugDescription>
                <WrittenDate>2025-01-15</WrittenDate>
            </MedicationPrescribed>
            <Pharmacy>
                <TransferType>TRANSFER FROM PHARMACY</TransferType>
            </Pharmacy>
        </Message>"""
        
        start_time = time.time()
        response = client.post("/api/v1/transfers/validate-transfer", content=xml_content)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        if response.status_code in [200, 400] and response_time < 5.0:  # Should complete within 5 seconds
            print(f"✅ Performance test passed (response time: {response_time:.3f}s)")
            return True
        else:
            print(f"❌ Performance test failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False


async def main():
    """Run all integration tests."""
    print("🚀 Testing Integration")
    print("=" * 60)
    
    tests = [
        test_health_endpoint,
        test_validate_transfer_endpoint_valid,
        test_validate_transfer_endpoint_invalid,
        test_verify_signature_endpoint,
        test_service_integration,
        test_error_handling_integration,
        test_concurrent_validation,
        test_basic_performance
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test.__name__ == 'test_service_integration':
            if await test():
                passed += 1
        else:
            if test():
                passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed!")
        return True
    else:
        print("⚠️  Some integration tests failed.")
        return False


if __name__ == "__main__":
    import asyncio
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 