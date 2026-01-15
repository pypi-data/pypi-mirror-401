#!/usr/bin/env python3
"""
Production Integration Helper Functions
For FastAPI service integration with dynamic fabricator-based processing
"""

from typing import Optional

def process_pii_fields(table_name: str, process: str, record_id: Optional[int], field_data: dict) -> dict:
    """
    Process multiple fields for insert/update - Compatible with service 2.py format
    
    Args:
        table_name: Database table name
        process: "pseudo" or "mask" operation type  
        record_id: Record identifier (can be None)
        field_data: Input JSON data
        
    Returns:
        Dict with 'fields' and 'tokenSet' keys as expected by service 2.py
    """
    from ..core.clean_processor import PIIProcessor
    
    # Print table being processed for debugging
    #print(f">>> PROCESSING TABLE: {table_name} (process: {process})")
    
    pii_processor = PIIProcessor()
    processed_data = {}
    token_set = {}

    # Handle None record_id (use a temporary ID)
    if record_id is None:
        record_id = field_data.get('uid', 999999)

    # Get PII fields dynamically from fabricator
    cfg_keys = pii_processor.get_pii_fields_for_process(table_name, process)

    # Map config fields -> actual keys present in the payload
    pii_fields = cfg_keys.intersection(field_data.keys())

    # Store original values for later retrieval
    original_values_storage = {}
    
    # Store original values for later retrieval
    original_values_storage = {}
    
    for field_name, field_value in field_data.items():
        if field_name in pii_fields and field_value not in (None, "", "***"):
            if process == "pseudo":
                # Generate encrypted token and pseudonymized value
                encrypted_token = pii_processor.token_generator.generate_encrypted_token(field_value)
                pseudo_value = pii_processor.pseudonymizer.pseudonymize(field_value, field_name)
                
                processed_data[field_name] = pseudo_value
                token_set[field_name] = encrypted_token
                
                #print(f"PROCESSED: {field_name} = {field_value} -> Token: {encrypted_token}, Pseudo: {pseudo_value}")
            else:  # process == "mask"
                pseudo_value = pii_processor.pseudonymizer.pseudonymize(field_value, field_name)
                processed_data[field_name] = pseudo_value
        else:
            processed_data[field_name] = field_value
    
    # Store original values in a global mapping (in production, use database)
    if not hasattr(process_pii_fields, '_original_storage'):
        process_pii_fields._original_storage = {}
    process_pii_fields._original_storage.update(original_values_storage)
    
    # Store original values in a global mapping (in production, use database)
    if not hasattr(process_pii_fields, '_original_storage'):
        process_pii_fields._original_storage = {}
    process_pii_fields._original_storage.update(original_values_storage)

    # Build TokenSet with ONLY PII fields that have encrypted tokens
    token_set_output = {}
    for field_name, field_value in field_data.items():
        if field_name in token_set:
            # PII field that was processed - use encrypted token
            token_set_output[field_name] = token_set[field_name]
        # Do NOT include non-PII fields in TokenSet
    
    # Return format expected by service 2.py - EXACT structure match
    return {
        'TokenSet': token_set_output,
        'fields': processed_data
    }

def retrieve_original_data(table_name: str, record_id: int, field_name: str) -> str:
    """
    Retrieve original PII data for admin access - Compatible with service 2.py
    
    Args:
        table_name: Database table name
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

def reverse_pii_fields(table_name: str, field_name: str, field_value: str, token_set_json) -> str:
    """
    Phase 2: Reverse lookup - Convert single field back to original data
    NO FABRICATOR NEEDED - Pure token-based reversal
    
    Args:
        table_name: Database table name ("jobseekers" or "employers") - for compatibility only
        field_name: Field name to reverse (e.g., "company_name", "email")
        field_value: Current field value from database
        token_set_json: TokenSet as JSON string or dict containing tokens
        
    Returns:
        Original field value if token exists, otherwise raw field_value as-is
    """
    import json
    
    # Parse token_set if it's a JSON string
    try:
        if isinstance(token_set_json, str):
            token_set = json.loads(token_set_json)
        else:
            token_set = token_set_json or {}
    except (json.JSONDecodeError, TypeError):
        #print(f"Invalid token_set format for {field_name}")
        return field_value
    
    # SIMPLE LOGIC: If field_name in token_set → decrypt, else → return as-is
    if not isinstance(token_set, dict) or field_name not in token_set:
        # No token for this field → return pseudo value as-is (non-PII field)
        return field_value
    
    # Get encrypted token for this specific field
    encrypted_token = token_set.get(field_name)
    
    # Check if this field has an encrypted token (EE_ prefix)
    if encrypted_token and isinstance(encrypted_token, str) and encrypted_token.startswith('EE_'):
        try:
            # Decrypt token to get original value (NO FABRICATOR NEEDED)
            from ..core.token_generator import TokenGenerator
            token_gen = TokenGenerator()
            
            original_value = token_gen.decrypt_token(encrypted_token)
            
            if original_value:
                #print(f"REVERSE SUCCESS: {field_name} {field_value} -> {original_value}")
                return original_value
            else:
                #print(f"REVERSE FAILED: {field_name} {field_value} -> decryption failed")
                return field_value
                
        except Exception as e:
            #print(f"Error retrieving original value for {field_name}: {e}")
            return field_value
    else:
        # Field in token_set but no EE_ token → return pseudo value as-is
        return field_value

def get_pii_fields_for_table(table_name: str, process: str = None) -> set:
    """
    Get list of PII fields for a table (for validation)
    
    Args:
        table_name: Database table name
        process: "pseudo" or "mask" (optional)
        
    Returns:
        Set of field names that are marked as PII in fabricator.json
    """
    from ..core.clean_processor import PIIProcessor
    
    pii_processor = PIIProcessor()
    if process:
        return pii_processor.get_pii_fields_for_process(table_name, process)
    else:
        # Return all PII fields (both pseudo and mask)
        pseudo_fields = pii_processor.get_pii_fields_for_process(table_name, "pseudo")
        mask_fields = pii_processor.get_pii_fields_for_process(table_name, "mask")
        return pseudo_fields.union(mask_fields)