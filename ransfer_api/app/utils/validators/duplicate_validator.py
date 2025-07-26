#!/usr/bin/env python3
"""
Duplicate Validator

This module handles validation to prevent duplicate prescription transfers
and ensure data integrity.
"""

import xml.etree.ElementTree as ET
from fastapi import HTTPException


def validate_duplicate_prescription(root: ET.Element, ns: dict) -> None:
    """
    🟢 **7️⃣ Duplicate Prescription Validation**
    
    Prevents duplicate transfers and ensures data integrity.
    
    **Checks performed:**
    - Validates that `<PrescriptionPreviouslyFilled>` is not "true"
    - Ensures prescription has not been previously dispensed
    - Prevents duplicate processing of the same prescription
    
    **Why this is important:**
    - Prevents double-dispensing of the same prescription
    - Ensures prescription integrity and prevents medication errors
    - Supports regulatory compliance with prescription transfer rules
    - Prevents potential fraud or abuse through duplicate transfers
    - Maintains accurate pharmacy records and audit trails
    
    **Business Rules:**
    - PrescriptionPreviouslyFilled must not be "true"
    - Previously filled prescriptions cannot be transferred
    - This prevents duplicate dispensing and potential medication errors
    
    **Regulatory Considerations:**
    - Most jurisdictions prohibit transferring already-dispensed prescriptions
    - Controlled substances have stricter rules about transfer limitations
    - Some states allow partial transfers with specific documentation
    - Consider state-specific rules for prescription transfer limitations
    
    **Example Scenarios:**
    - Valid: PrescriptionPreviouslyFilled="false" or not present
    - Invalid: PrescriptionPreviouslyFilled="true" (already dispensed)
    
    **Additional Validation Opportunities:**
    - Check for duplicate prescription IDs across multiple transfers
    - Validate against a database of previously processed prescriptions
    - Implement time-based duplicate detection (e.g., same prescription within 24 hours)
    - Consider implementing a prescription transfer registry
    
    Args:
        root (ET.Element): Root XML element
        ns (dict): XML namespace mapping
        
    Raises:
        HTTPException: Status 403 with reason_code "CX" for duplicate prescription violations
    """
    previously_filled = root.find('.//ncpdp:PrescriptionPreviouslyFilled', ns)
    
    if previously_filled is not None and previously_filled.text and previously_filled.text.lower() == "true":
        raise HTTPException(
            status_code=403,
            detail={
                "reason_code": "CX",
                "reason_description": "Prescription has already been filled and cannot be transferred."
            }
        ) 