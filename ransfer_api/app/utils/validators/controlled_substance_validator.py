#!/usr/bin/env python3
"""
Controlled Substance Validator

This module handles validation of controlled substance prescriptions
according to DEA and NCPDP SCRIPT requirements.
"""

import xml.etree.ElementTree as ET
from fastapi import HTTPException


def validate_controlled_substance(root: ET.Element, ns: dict) -> None:
    """
    🟢 **1️⃣ Controlled Substance Validation**
    
    Enforces DEA and NCPDP SCRIPT requirements for controlled substance transfers.
    
    **Checks performed:**
    - Validates that `<ControlledSubstanceIndicator>` is present and equals "Y" or "N"
    - If controlled substance (indicator = "Y"):
      - Requires `<DoNotFill>` to be present and set to "Y" (mandatory for informational transfers)
      - Checks that `<PrescriptionPreviouslyFilled>` is not "true" (dispensed controlled substances cannot be transferred)
    
    **Why this is important:**
    - Prevents illegal transfers of controlled substances
    - Enforces DEA and NCPDP SCRIPT requirements for safe handling
    - Ensures that if the transfer is informational only, the receiving pharmacy does not dispense
    - Complies with 21 CFR 1311 regulations for electronic prescriptions for controlled substances (EPCS)
    
    **Business Rules:**
    - Controlled substances must be sent with DoNotFill='Y' if transferred electronically
    - Previously filled controlled substances cannot be transferred
    - Digital signature validation is handled separately by the digital signature validator
    
    Args:
        root (ET.Element): Root XML element
        ns (dict): XML namespace mapping
        
    Raises:
        HTTPException: Status 403 with reason_code "CX" for controlled substance violations
    """
    controlled_indicator = root.find('.//ncpdp:ControlledSubstanceIndicator', ns)
    
    if controlled_indicator is not None and controlled_indicator.text == "Y":
        # Check DoNotFill
        do_not_fill = root.find('.//ncpdp:DoNotFill', ns)
        if do_not_fill is None or do_not_fill.text != "Y":
            raise HTTPException(
                status_code=403,
                detail={
                    "reason_code": "CX",
                    "reason_description": "Controlled substance prescriptions must be sent with DoNotFill='Y' if transferred electronically."
                }
            )
        
        # Check PrescriptionPreviouslyFilled
        previously_filled = root.find('.//ncpdp:PrescriptionPreviouslyFilled', ns)
        if previously_filled is not None and previously_filled.text == "true":
            raise HTTPException(
                status_code=403,
                detail={
                    "reason_code": "CX",
                    "reason_description": "Controlled substances previously filled cannot be transferred."
                }
            ) 