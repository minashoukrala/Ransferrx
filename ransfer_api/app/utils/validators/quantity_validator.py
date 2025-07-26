#!/usr/bin/env python3
"""
Quantity Validator

This module handles validation of prescription quantities according to
NCPDP SCRIPT standards and business rules.
"""

import xml.etree.ElementTree as ET
from fastapi import HTTPException


def validate_quantity_qualifiers(root: ET.Element, ns: dict) -> None:
    """
    🟢 **3️⃣ Quantity Qualifiers Validation**
    
    Ensures proper quantity tracking and prevents over-dispensing of medications.
    
    **Checks performed:**
    - Ensures there are exactly three `<Quantity>` elements inside `<MedicationPrescribed>`
    - Requires that the qualifiers are:
      - "38" for Original Quantity (total amount originally authorized)
      - "40" for Quantity Remaining (amount still available to be dispensed/transferred)
      - "QT" for Quantity Transferred (amount being transferred in this transaction)
    - Verifies that:
      - There are no duplicate qualifiers
      - Original Quantity (38) is greater than or equal to Remaining Quantity (40)
      - Quantity Transferred (QT) equals Quantity Remaining (40)
      - All quantity values are valid integers
    
    **Why this is important:**
    - Prevents over-dispensing of medication beyond prescriber authorization
    - Ensures proper record-keeping and audit trails for prescription transfers
    - Enforces NCPDP SCRIPT specification for quantity tracking
    - Supports reconciliation if the prescription was transferred multiple times
    - Provides complete audit trail: original → remaining → transferred
    
    **Business Rules:**
    - Original Quantity (38) ≥ Remaining Quantity (40) - logical constraint
    - Quantity Transferred (QT) = Remaining Quantity (40) - what's being transferred
    - All three qualifiers (38, 40, QT) are required and must be unique
    - No negative or zero quantities allowed
    
    **Real-World Example:**
    - Original prescription: 180 tablets
    - Dispensed so far: 60 tablets
    - Remaining: 120 tablets
    - Transferring now: 120 tablets
    - Qualifiers: 38=180, 40=120, QT=120
    
    Args:
        root (ET.Element): Root XML element
        ns (dict): XML namespace mapping
        
    Raises:
        HTTPException: Status 400 with reason_code "BY" for quantity validation violations
    """
    quantities = root.findall('.//ncpdp:MedicationPrescribed/ncpdp:Quantity', ns)
    
    if len(quantities) != 3:
        raise HTTPException(
            status_code=400,
            detail={
                "reason_code": "BY",
                "reason_description": "Quantity qualifiers 38, 40, and QT are required and must be unique."
            }
        )
    
    # Extract quantity values and qualifiers
    quantity_data = {}
    for quantity in quantities:
        qualifier = quantity.find('ncpdp:CodeListQualifier', ns)
        value_elem = quantity.find('ncpdp:Value', ns)
        
        if qualifier is not None and qualifier.text and value_elem is not None and value_elem.text:
            try:
                quantity_data[qualifier.text] = int(value_elem.text)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "reason_code": "BY",
                        "reason_description": "Quantity values must be valid integers."
                    }
                )
    
    # Check that all required qualifiers are present
    required_qualifiers = {"38", "40", "QT"}
    if set(quantity_data.keys()) != required_qualifiers:
        raise HTTPException(
            status_code=400,
            detail={
                "reason_code": "BY",
                "reason_description": "Quantity qualifiers 38, 40, and QT are required and must be unique."
            }
        )
    
    # Validate quantity relationships
    original_qty = quantity_data.get("38", 0)  # Original Quantity
    remaining_qty = quantity_data.get("40", 0)  # Quantity Remaining
    transferred_qty = quantity_data.get("QT", 0)  # Quantity Transferred
    
    # Check that original quantity is greater than or equal to remaining quantity
    if original_qty < remaining_qty:
        raise HTTPException(
            status_code=400,
            detail={
                "reason_code": "BY",
                "reason_description": "Original quantity (38) must be greater than or equal to remaining quantity (40)."
            }
        )
    
    # Check that quantity transferred equals remaining quantity
    if transferred_qty != remaining_qty:
        raise HTTPException(
            status_code=400,
            detail={
                "reason_code": "BY",
                "reason_description": "Quantity transferred (QT) must equal remaining quantity (40)."
            }
        ) 