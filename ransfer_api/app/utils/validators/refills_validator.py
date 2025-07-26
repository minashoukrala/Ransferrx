#!/usr/bin/env python3
"""
Refills Validator

This module handles validation of prescription refills according to
NCPDP SCRIPT standards and business rules.
"""

import xml.etree.ElementTree as ET
from fastapi import HTTPException


def validate_refills_consistency(root: ET.Element, ns: dict) -> None:
    """
    🟢 **4️⃣ Refills Consistency Validation**
    
    Validates refill authorization and prevents over-dispensing beyond prescriber limits.
    
    **Checks performed:**
    - Ensures `<RefillsRemaining>` does not exceed `<NumberOfRefills>`
    - Validates that both values are valid integers
    - Checks for logical consistency between refill values
    - Rejects empty or whitespace-only values
    
    **Why this is important:**
    - Prevents over-dispensing beyond the prescriber's authorization
    - Supports state and federal refill rules and regulations
    - Ensures consistent pharmacy records and audit trails
    - Prevents unauthorized refills that could lead to medication abuse
    - Maintains compliance with prescription drug monitoring programs (PDMP)
    
    **Business Rules:**
    - RefillsRemaining ≤ NumberOfRefills (logical constraint)
    - Both values must be non-negative integers
    - Zero refills remaining is valid (prescription fully dispensed)
    - Empty or whitespace-only values are not allowed
    
    **State-Specific Considerations:**
    - Some states require at least 1 refill to allow transfer
    - Controlled substances may have stricter refill limitations
    - Consider making minimum refill requirements configurable
    
    **Example Scenarios:**
    - Valid: NumberOfRefills=3, RefillsRemaining=2
    - Valid: NumberOfRefills=3, RefillsRemaining=0 (fully dispensed)
    - Invalid: NumberOfRefills=3, RefillsRemaining="" (empty value)
    - Invalid: NumberOfRefills=3, RefillsRemaining=4 (exceeds authorization)
    
    Args:
        root (ET.Element): Root XML element
        ns (dict): XML namespace mapping
        
    Raises:
        HTTPException: Status 400 with reason_code "BY" for refill validation violations
    """
    number_of_refills = root.find('.//ncpdp:NumberOfRefills', ns)
    refills_remaining = root.find('.//ncpdp:RefillsRemaining', ns)
    
    # If both elements exist, validate their values
    if number_of_refills is not None and refills_remaining is not None:
        # Check for empty or whitespace-only values
        num_refills_text = number_of_refills.text.strip() if number_of_refills.text else ""
        remaining_text = refills_remaining.text.strip() if refills_remaining.text else ""
        
        if not num_refills_text or not remaining_text:
            raise HTTPException(
                status_code=400,
                detail={
                    "reason_code": "BY",
                    "reason_description": "Refill values cannot be empty or whitespace-only."
                }
            )
        
        try:
            # Convert to integers
            num_refills = int(num_refills_text)
            remaining = int(remaining_text)
            
            # Validate non-negative values
            if num_refills < 0 or remaining < 0:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "reason_code": "BY",
                        "reason_description": "Refill values must be non-negative integers."
                    }
                )
            
            # Check logical constraint
            if remaining > num_refills:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "reason_code": "BY",
                        "reason_description": "RefillsRemaining cannot exceed NumberOfRefills."
                    }
                )
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "reason_code": "BY",
                    "reason_description": "Invalid refill values - must be integers."
                }
            ) 