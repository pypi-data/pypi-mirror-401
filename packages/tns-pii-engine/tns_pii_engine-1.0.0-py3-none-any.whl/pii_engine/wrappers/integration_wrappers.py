#!/usr/bin/env python3
"""
Production Integration Wrapper Functions
For FastAPI service integration with dynamic fabricator-based processing
"""

from typing import Optional

def process_pii_fields(table_name: str, process: str, record_id: Optional[int], field_data: dict) -> dict:
    """
    Process multiple fields for insert/update - Compatible with service 2.py format
    
    Args:
        table_name: Database table name ("jobseekers" or "employers")
        process: "pseudo" or "mask" operation type  
        record_id: Record identifier (None during signup - user doesn't exist yet)
        field_data: Input JSON data
        
    Returns:
        Dict with 'fields' and 'tokenSet' keys as expected by service 2.py
    """
    from ..core.clean_processor import PIIProcessor
    
    # Print table being processed for debugging
    print(f">>> PROCESSING TABLE: {table_name} (process: {process})")
    
    pii_processor = PIIProcessor()
    processed_data = {}
    token_set = {}

    # Handle None record_id (use a temporary ID)
    if record_id is None:
        record_id = field_data.get('uid', 999999)

    # Get PII fields dynamically from fabricator.json
    cfg_keys = pii_processor.get_pii_fields_for_process(table_name, process)

    # Map config fields -> actual keys present in the payload
    pii_fields = cfg_keys.intersection(field_data.keys())

    for field_name, field_value in field_data.items():
        if field_name in pii_fields and field_value not in (None, "", "***"):
            if process == "pseudo":
                pseudo_value, token = pii_processor.process_field(
                    table_name, field_name, field_value, record_id
                )
                processed_data[field_name] = pseudo_value
                
                # Store token information for tokenSet
                token_set[field_name] = {
                    "original": field_value,
                    "pseudo": pseudo_value, 
                    "token": token
                }
            else:  # process == "mask"
                pseudo_value = pii_processor.process_field(
                    table_name, field_name, field_value, record_id
                )[0]  # Get only pseudo_value, ignore token
                processed_data[field_name] = pseudo_value
        else:
            processed_data[field_name] = field_value

    # Build TokenSet with tokens for PII fields and original values for non-PII fields
    token_set_output = {}
    for field_name, field_value in field_data.items():
        if field_name in token_set:
            # PII field - use token
            token_set_output[field_name] = token_set[field_name]['token']
        else:
            # Non-PII field - use original value
            token_set_output[field_name] = field_value
    
    # Return format expected by service 2.py - EXACT structure match
    return {
        'TokenSet': token_set_output,
        'fields': processed_data
    }

def retrieve_original_data(table_name: str, record_id: int, field_name: str) -> str:
    """
    Retrieve original PII data for admin access - Compatible with service 2.py
    
    Args:
        table_name: Database table name ("jobseekers" or "employers")
        record_id: Record identifier
        field_name: Field name to retrieve
        
    Returns:
        Original field value
    """
    from ..core.clean_processor import PIIProcessor
    
    pii_processor = PIIProcessor()
    return pii_processor.vault.retrieve_field_from_main_table(
        table_name, record_id, field_name
    )

def reverse_pii_fields(table_name: str, field_name: str, current_value: str, token_set_json: str) -> str:
    """
    Reverse PII field to get original value - Handles service 3.py TOKEN_SET format
    
    Args:
        table_name: Database table name ("employers", "jobseekers")
        field_name: Field name to reverse ("company_name", "first_name", etc.)
        current_value: Current pseudonymized value
        token_set_json: JSON string containing encrypted values
        
    Returns:
        Original field value or current value if reversal fails
    """
    import json
    import base64
    import os
    from cryptography.fernet import Fernet
    
    try:
        # Handle empty token_set
        if not token_set_json or token_set_json.strip() == "":
            print(f"REVERSE SKIPPED: {field_name} - empty token_set")
            return current_value
            
        # Parse token_set JSON
        try:
            token_data = json.loads(token_set_json)
        except json.JSONDecodeError as e:
            print(f"REVERSE FAILED: {field_name} - invalid JSON: {str(e)}")
            return current_value
            
        # Check if field exists in token_data
        if field_name not in token_data:
            print(f"REVERSE SKIPPED: {field_name} - field not in token_data")
            return current_value
            
        # Get encrypted value for this field
        encrypted_value = token_data[field_name]
        
        # Handle service 3.py format: "EE_base64_encrypted_data"
        if encrypted_value.startswith("EE_"):
            # Remove EE_ prefix and decode
            base64_data = encrypted_value[3:]  # Remove "EE_" prefix
            
            # Try to decrypt with current PII_ENC_KEY
            try:
                key = os.getenv('PII_ENC_KEY')
                if not key:
                    print(f"REVERSE FAILED: {field_name} - PII_ENC_KEY not found")
                    return current_value
                    
                fernet = Fernet(key.encode())
                encrypted_bytes = base64.b64decode(base64_data.encode())
                original_value = fernet.decrypt(encrypted_bytes).decode()
                print(f"REVERSE SUCCESS: {field_name} -> {original_value}")
                return original_value
                
            except Exception as decrypt_error:
                print(f"REVERSE FAILED: {field_name} {current_value} -> decryption failed")
                print(f"  Error: {str(decrypt_error)}")
                print(f"  Key used: {key[:20] if key else 'None'}...")
                print(f"  Token: {encrypted_value[:50]}...")
                return current_value
        else:
            # Non-encrypted field
            print(f"REVERSE SKIPPED: {field_name} - not encrypted (no EE_ prefix)")
            return current_value
        
    except Exception as e:
        print(f"REVERSE FAILED: {field_name} {current_value} -> {str(e)}")
        return current_value