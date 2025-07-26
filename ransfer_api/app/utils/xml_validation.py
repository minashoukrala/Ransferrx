import os
from xmlschema import XMLSchema, XMLSchemaValidationError


def validate_ncpdp_xml(xml_content: str) -> bool:
    """
    Validate XML content against NCPDP SCRIPT 2017071 XSD schema.
    
    Args:
        xml_content (str): The XML content to validate
        
    Returns:
        bool: True if validation passes
        
    Raises:
        XMLSchemaValidationError: If XML is invalid according to the schema
        FileNotFoundError: If the XSD schema file is not found
    """
    # Get the path to the XSD schema file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(current_dir, '..', 'schemas', 'NCPDP_SCRIPT_2017071.xsd')
    
    # Check if schema file exists
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"XSD schema file not found at: {schema_path}")
    
    # Load the schema
    schema = XMLSchema(schema_path)
    
    # Validate the XML content
    schema.validate(xml_content)
    
    return True 