from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from app.services.prescription_service import prescription_service

router = APIRouter()





@router.post("/validate-transfer")
async def validate_transfer(request: Request):
    """
    Validate NCPDP SCRIPT transfer request using comprehensive validation.
    
    This endpoint performs complete validation including:
    - Controlled substance validation
    - Digital signature verification
    - Quantity qualifiers validation
    - Refills consistency validation
    - Prescription expiration validation
    - Pharmacy identification validation
    - Duplicate transfer validation
    
    Expected request body: XML content
    """
    try:
        # Get XML content from request body
        xml_content = await request.body()
        xml_content_str = xml_content.decode('utf-8')
        
        # Use the prescription service to validate the transfer
        result = await prescription_service.validate_transfer(xml_content_str)
        
        # Return the validation result
        return JSONResponse(status_code=200, content=result)
        
    except HTTPException:
        # Re-raise HTTP exceptions from validation
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/verify-signature")
async def verify_signature(request: Request):
    """
    Verify digital signature in NCPDP SCRIPT XML.
    
    This endpoint specifically focuses on digital signature verification
    as part of the comprehensive validation process.
    
    Expected request body: XML content
    """
    try:
        # Get XML content from request body
        xml_content = await request.body()
        xml_content_str = xml_content.decode('utf-8')
        
        # Use the prescription service to verify the signature
        result = await prescription_service.verify_signature(xml_content_str)
        
        # Return the verification result
        return JSONResponse(status_code=200, content=result)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint for the transfers router."""
    return {"status": "ok", "service": "transfers"} 