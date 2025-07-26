#!/usr/bin/env python3
"""
Expiration Validator

This module handles validation of prescription expiration dates according to
regulatory timelines and business rules.
"""

import xml.etree.ElementTree as ET
from datetime import datetime, date
from fastapi import HTTPException
import re


def validate_prescription_expiration(root: ET.Element, ns: dict) -> None:
    """
    🟢 **5️⃣ Prescription Expiration Validation**
    
    Ensures prescriptions are current and valid according to regulatory timelines.
    
    **Checks performed:**
    - Compares `<WrittenDate>` to current date
    - If prescription is more than 1 year old, marks it as expired and rejects the transfer
    - Validates that WrittenDate is in correct format (YYYY-MM-DD)
    - Rejects future dates (prescriptions cannot be written in the future)
    - Rejects empty or whitespace-only dates
    
    **Why this is important:**
    - Ensures prescriptions are current and valid for dispensing
    - Helps meet state-specific laws about prescription expiration timelines
    - Prevents dispensing of outdated prescriptions that may no longer be clinically appropriate
    - Supports regulatory compliance with prescription validity requirements
    - Reduces risk of dispensing medications that may have changed or been discontinued
    
    **Business Rules:**
    - Prescriptions expire 1 year from the written date
    - WrittenDate must be in YYYY-MM-DD format with leading zeros
    - Expired prescriptions cannot be transferred
    - Future dates are not allowed (prescription cannot be written in the future)
    - Empty or whitespace-only dates are not allowed
    
    **Regulatory Considerations:**
    - Some jurisdictions require shorter windows (e.g., 6 months for controlled substances)
    - DEA Schedule-specific expiration rules may apply
    - Consider making expiration intervals configurable by medication type
    - Some states have specific rules for different drug classes
    
    **Example Scenarios:**
    - Valid: WrittenDate=2024-01-01 (current year)
    - Valid: WrittenDate=2023-12-31 (within 1 year)
    - Invalid: WrittenDate=2022-01-01 (more than 1 year old)
    - Invalid: WrittenDate=2025-01-01 (future date)
    - Invalid: WrittenDate=2025-1-5 (missing leading zeros)
    - Invalid: WrittenDate="" (empty date)
    
    Args:
        root (ET.Element): Root XML element
        ns (dict): XML namespace mapping
        
    Raises:
        HTTPException: Status 403 with reason_code "CW" for expired prescriptions
        HTTPException: Status 400 with reason_code "BY" for invalid date format
    """
    written_date_elem = root.find('.//ncpdp:WrittenDate', ns)
    
    if written_date_elem is not None:
        date_text = written_date_elem.text.strip() if written_date_elem.text else ""
        
        # Check if date is empty or whitespace-only
        if not date_text:
            raise HTTPException(
                status_code=400,
                detail={
                    "reason_code": "BY",
                    "reason_description": "WrittenDate cannot be empty or whitespace-only."
                }
            )
        
        # First check if the format is exactly YYYY-MM-DD with leading zeros
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_text):
            raise HTTPException(
                status_code=400,
                detail={
                    "reason_code": "BY",
                    "reason_description": "Invalid WrittenDate format. Expected YYYY-MM-DD with leading zeros."
                }
            )
        
        try:
            written_date = datetime.strptime(date_text, '%Y-%m-%d').date()
            today = date.today()
            
            # Check if prescription is in the future
            if written_date > today:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "reason_code": "BY",
                        "reason_description": "WrittenDate cannot be in the future."
                    }
                )
            
            # Check if prescription is more than 1 year old
            if (today - written_date).days > 365:
                raise HTTPException(
                    status_code=403,
                    detail={
                        "reason_code": "CW",
                        "reason_description": "Prescription has expired."
                    }
                )
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "reason_code": "BY",
                    "reason_description": "Invalid WrittenDate format. Expected YYYY-MM-DD."
                }
            ) 