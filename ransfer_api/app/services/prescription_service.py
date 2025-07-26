#!/usr/bin/env python3
"""
Prescription Service

This service orchestrates prescription transfer business logic,
coordinating between different utilities and providing a clean
interface for the API endpoints.
"""

from typing import Dict, Any, List, Optional
from fastapi import HTTPException
from app.utils.prescription_validator import validate_prescription_transfer
import xml.etree.ElementTree as ET


class PrescriptionService:
    """
    Service for handling prescription transfer operations.
    
    This service coordinates the business logic for prescription transfers,
    including validation, processing, and response formatting.
    """
    
    def __init__(self):
        """Initialize the prescription service."""
        # In production, this would connect to a database
        self.processed_transfers: List[str] = []
    
    async def validate_transfer(self, xml_content: str) -> Dict[str, Any]:
        """
        Validate a prescription transfer request.
        
        Args:
            xml_content (str): The XML content to validate
            
        Returns:
            Dict[str, Any]: Validation result with parsed data
            
        Raises:
            HTTPException: If validation fails
        """
        try:
            # Parse XML for response data
            parsed_data = self._parse_xml_for_response(xml_content)
            
            # Perform comprehensive validation
            validate_prescription_transfer(xml_content)
            
            # If validation passes, add to processed transfers
            if parsed_data.get('message_id'):
                self.processed_transfers.append(parsed_data['message_id'])
            
            return {
                "status": "valid",
                "message": "Transfer request validated successfully",
                "validation_categories": [
                    "Controlled Substance Validation",
                    "Digital Signature Validation", 
                    "Quantity Qualifiers Validation",
                    "Refills Consistency Validation",
                    "Prescription Expiration Validation",
                    "Pharmacy Identification Validation",
                    "Duplicate Transfer Validation"
                ],
                "data": parsed_data
            }
            
        except HTTPException:
            # Re-raise HTTP exceptions from validation
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Service error: {str(e)}")
    
    async def verify_signature(self, xml_content: str) -> Dict[str, Any]:
        """
        Verify digital signature in prescription XML.
        
        Args:
            xml_content (str): The XML content to verify
            
        Returns:
            Dict[str, Any]: Signature verification result
            
        Raises:
            HTTPException: If verification fails
        """
        try:
            # Parse XML for response data
            parsed_data = self._parse_xml_for_response(xml_content)
            
            # Perform validation (includes digital signature verification)
            validate_prescription_transfer(xml_content)
            
            return {
                "status": "signature_verified",
                "message": "Digital signature verification completed successfully",
                "data": parsed_data
            }
            
        except HTTPException:
            # Re-raise HTTP exceptions from validation
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Service error: {str(e)}")
    
    def _parse_xml_for_response(self, xml_content: str) -> Dict[str, Any]:
        """
        Parse NCPDP SCRIPT XML and extract relevant fields for response.
        
        Args:
            xml_content (str): The XML content to parse
            
        Returns:
            Dict[str, Any]: Parsed data for response
        """
        try:
            # Parse XML
            root = ET.fromstring(xml_content)
            
            # Define namespace
            ns = {'ncpdp': 'http://www.ncpdp.org/schema/SCRIPT'}
            
            # Extract patient information
            patient = root.find('.//ncpdp:Patient', ns)
            patient_name = None
            if patient is not None:
                first_name = patient.find('ncpdp:FirstName', ns)
                last_name = patient.find('ncpdp:LastName', ns)
                if first_name is not None and last_name is not None:
                    patient_name = f"{first_name.text} {last_name.text}"
            
            # Extract drug information
            drug_description = root.find('.//ncpdp:DrugDescription', ns)
            drug_name = drug_description.text if drug_description is not None else "Unknown"
            
            # Extract MessageId
            message_id = root.find('.//ncpdp:Header/ncpdp:MessageId', ns)
            message_id_value = message_id.text if message_id is not None else "Unknown"
            
            # Extract controlled substance indicator
            controlled_substance = root.find('.//ncpdp:ControlledSubstanceIndicator', ns)
            controlled_substance_value = controlled_substance.text if controlled_substance is not None else None
            
            # Extract pharmacy information
            pharmacies = root.findall('.//ncpdp:Pharmacy', ns)
            pharmacy_info = []
            for pharmacy in pharmacies:
                transfer_type = pharmacy.find('ncpdp:TransferType', ns)
                ncpdp_id = pharmacy.find('ncpdp:NCPDPID', ns)
                business_name = pharmacy.find('ncpdp:BusinessName', ns)
                
                pharmacy_info.append({
                    "transfer_type": transfer_type.text if transfer_type is not None else None,
                    "ncpdp_id": ncpdp_id.text if ncpdp_id is not None else None,
                    "business_name": business_name.text if business_name is not None else None
                })
            
            return {
                'message_id': message_id_value,
                'patient_name': patient_name,
                'drug_description': drug_name,
                'controlled_substance_indicator': controlled_substance_value,
                'pharmacies': pharmacy_info
            }
            
        except ET.ParseError as e:
            raise HTTPException(status_code=400, detail=f"Invalid XML format: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error parsing XML: {str(e)}")
    
    def get_processed_transfers(self) -> List[str]:
        """
        Get list of processed transfer MessageIds.
        
        Returns:
            List[str]: List of processed MessageIds
        """
        return self.processed_transfers.copy()
    
    def clear_processed_transfers(self) -> None:
        """Clear the list of processed transfers (for testing purposes)."""
        self.processed_transfers.clear()


# Create a singleton instance
prescription_service = PrescriptionService() 