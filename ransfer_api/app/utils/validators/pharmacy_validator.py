#!/usr/bin/env python3
"""
Pharmacy Validator

This module handles validation of pharmacy identification and transfer types
according to NCPDP SCRIPT standards.
"""

import xml.etree.ElementTree as ET
from fastapi import HTTPException


def validate_pharmacy_identification(root: ET.Element, ns: dict) -> None:
    """
    🟢 **6️⃣ Pharmacy Identification Validation**
    
    Establishes clear source and destination for prescription transfers.
    
    **Checks performed:**
    - Validates there are exactly 2 `<Pharmacy>` elements
    - Ensures one pharmacy has `TransferType="TRANSFER FROM PHARMACY"`
    - Ensures one pharmacy has `TransferType="TRANSFER TO PHARMACY"`
    - Validates that both transfer types are present and unique
    
    **Why this is important:**
    - Establishes clear source and destination for the transfer
    - Complies with NCPDP SCRIPT transaction format requirements
    - Ensures traceability of prescription movement between pharmacies
    - Supports audit trails for regulatory compliance
    - Prevents ambiguous transfer directions that could lead to dispensing errors
    - Enables proper routing and processing of transfer requests
    
    **Business Rules:**
    - Exactly 2 pharmacy elements required (source and destination)
    - TransferType values must be "TRANSFER FROM PHARMACY" and "TRANSFER TO PHARMACY"
    - Both transfer types must be present and unique
    - No duplicate transfer types allowed
    
    **Additional Validation Opportunities:**
    - Optionally validate that each pharmacy entry includes both NPI and NCPDPID
    - Verify pharmacy identifiers are valid and active
    - Check that source and destination pharmacies are different
    - Validate pharmacy business names and addresses
    
    **Example Structure:**
    ```xml
    <Pharmacy>
        <TransferType>TRANSFER FROM PHARMACY</TransferType>
        <NCPDPID>1234567</NCPDPID>
        <NPI>1234567890</NPI>
    </Pharmacy>
    <Pharmacy>
        <TransferType>TRANSFER TO PHARMACY</TransferType>
        <NCPDPID>7654321</NCPDPID>
        <NPI>0987654321</NPI>
    </Pharmacy>
    ```
    
    Args:
        root (ET.Element): Root XML element
        ns (dict): XML namespace mapping
        
    Raises:
        HTTPException: Status 400 with reason_code "CA" for pharmacy identification violations
    """
    pharmacies = root.findall('.//ncpdp:Pharmacy', ns)
    
    if len(pharmacies) != 2:
        raise HTTPException(
            status_code=400,
            detail={
                "reason_code": "CA",
                "reason_description": "Both source and destination pharmacy information is required."
            }
        )
    
    transfer_types = []
    for pharmacy in pharmacies:
        transfer_type = pharmacy.find('ncpdp:TransferType', ns)
        if transfer_type is not None and transfer_type.text:
            transfer_types.append(transfer_type.text)
    
    required_types = {"TRANSFER TO PHARMACY", "TRANSFER FROM PHARMACY"}
    if set(transfer_types) != required_types:
        raise HTTPException(
            status_code=400,
            detail={
                "reason_code": "CA",
                "reason_description": "Both source and destination pharmacy information is required."
            }
        ) 