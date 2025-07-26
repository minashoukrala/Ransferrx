#!/usr/bin/env python3
"""
XML Parser Utilities

This module provides XML parsing functionality for prescription validation,
including namespace handling and XML structure validation.
"""

import xml.etree.ElementTree as ET
from fastapi import HTTPException


def parse_xml_content(xml_content: str) -> tuple[ET.Element, dict]:
    """
    Parse XML content and extract root element with namespace mapping.
    
    **Functionality:**
    - Parses XML string content into ElementTree structure
    - Extracts and maps XML namespaces for proper element access
    - Validates basic XML structure and format
    - Returns root element and namespace mapping for validation use
    
    **Why this is important:**
    - Provides consistent XML parsing across all validation modules
    - Handles NCPDP SCRIPT namespace complexity
    - Ensures proper element access using namespace prefixes
    - Centralizes XML parsing logic and error handling
    
    **Technical Details:**
    - Uses xml.etree.ElementTree for parsing
    - Extracts all namespaces from XML document
    - Maps namespaces to 'ncpdp' prefix for consistent access
    - Handles malformed XML gracefully with descriptive errors
    
    **Error Handling:**
    - Catches XML parsing errors and converts to HTTPExceptions
    - Provides clear error messages for debugging
    - Maintains consistent error format across the application
    
    Args:
        xml_content (str): XML string content to parse
        
    Returns:
        tuple[ET.Element, dict]: Root element and namespace mapping
        
    Raises:
        HTTPException: Status 400 for malformed XML or parsing errors
    """
    try:
        # Parse XML content
        root = ET.fromstring(xml_content)
        
        # Extract namespaces from root element
        namespaces = {}
        if '}' in root.tag:
            namespace = root.tag.split('}')[0].strip('{')
            namespaces['ncpdp'] = namespace
        else:
            # Default namespace for NCPDP SCRIPT
            namespaces['ncpdp'] = 'http://www.ncpdp.org/schema/SCRIPT'
        
        return root, namespaces
        
    except ET.ParseError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "reason_code": "BY",
                "reason_description": f"Invalid XML format: {str(e)}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "reason_code": "BY",
                "reason_description": f"XML parsing error: {str(e)}"
            }
        )


def validate_xml_structure(root: ET.Element, ns: dict) -> None:
    """
    Validate basic XML structure for prescription transfer documents.
    
    **Checks performed:**
    - Validates root element is present and properly named
    - Ensures required top-level elements exist
    - Checks for basic NCPDP SCRIPT structure compliance
    - Validates required child elements within MedicationPrescribed
    
    **Why this is important:**
    - Ensures XML follows expected NCPDP SCRIPT format
    - Prevents processing of malformed or incomplete documents
    - Provides early validation before detailed business rule checks
    - Maintains data integrity and processing reliability
    
    Args:
        root (ET.Element): Root XML element
        ns (dict): XML namespace mapping
        
    Raises:
        HTTPException: Status 400 for structural validation failures
    """
    # Check if root element exists
    if root is None:
        raise HTTPException(
            status_code=400,
            detail={
                "reason_code": "BY",
                "reason_description": "Root element not found in XML document."
            }
        )
    
    # Check for required top-level elements (basic structure)
    required_elements = [
        './/ncpdp:MedicationPrescribed',
        './/ncpdp:Pharmacy'
    ]
    
    for element_path in required_elements:
        if root.find(element_path, ns) is None:
            raise HTTPException(
                status_code=400,
                detail={
                    "reason_code": "BY",
                    "reason_description": f"Required element not found: {element_path}"
                }
            )
    
    # Check for required elements within MedicationPrescribed
    medication_prescribed = root.find('.//ncpdp:MedicationPrescribed', ns)
    if medication_prescribed is not None:
        required_medication_elements = [
            'ncpdp:DrugDescription',
            'ncpdp:WrittenDate'
        ]
        
        for element_name in required_medication_elements:
            if medication_prescribed.find(element_name, ns) is None:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "reason_code": "BY",
                        "reason_description": f"Required element not found within MedicationPrescribed: {element_name}"
                    }
                ) 