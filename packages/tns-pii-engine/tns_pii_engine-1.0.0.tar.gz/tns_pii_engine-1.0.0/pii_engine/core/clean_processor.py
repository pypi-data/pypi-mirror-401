#!/usr/bin/env python3
"""
Clean Modular PII Processor
"""

from ..config.config import ConfigLoader
from .token_generator import TokenGenerator
from .pseudonymizer import Pseudonymizer
from ..utils.vault import VaultManager

class SchemaManager:
    """Simple schema manager for fabricator config"""
    
    def __init__(self, fabricator_config):
        self.fabricator_config = fabricator_config
    
    def get_maskable_fields(self, table_name):
        """Get fields that need masking for a table"""
        schema = self.fabricator_config.get('schema', [])
        for table_config in schema:
            if table_config.get('table') == table_name:
                maskable_fields = []
                for column in table_config.get('columns', []):
                    if column.get('mask', False) and column.get('pseudo', False):
                        maskable_fields.append(column['name'])
                return maskable_fields
        return []
    
    def get_table_config(self, table_name):
        """Get configuration for specific table"""
        schema = self.fabricator_config.get('schema', [])
        for table_config in schema:
            if table_config.get('table') == table_name:
                return table_config
        return None

class PIIProcessor:
    """Main PII processing engine - orchestrates all components."""
    
    def __init__(self, fabricator_config=None):
        # Load configuration
        self.fabricator = fabricator_config or ConfigLoader.load_fabricator()
        self.config = ConfigLoader.extract_product_config(self.fabricator)
        
        # Initialize components
        self.token_generator = TokenGenerator(
            prefix=self.config.get("prefix", "TKN"),
            token_size=int(self.config.get("token_size", "8"))
        )
        self.pseudonymizer = Pseudonymizer()
        self.schema_manager = SchemaManager(self.fabricator)
        self.vault = VaultManager()
    
    def process_record(self, table_name, record_data, record_id=None):
        """Process a single record - main entry point."""
        
        # Extract record_id if not provided
        if record_id is None:
            record_id = record_data.get('id')
        
        if record_id is None:
            raise ValueError("record_id is required for proper token mapping")
        
        # Check if record is already processed
        if self.vault.is_record_processed(table_name, record_id):
            #print(f"  Record {record_id} already processed - skipping")
            existing_token = self.vault.get_existing_token(table_name, record_id)
            return record_data, existing_token
        
        # Generate global token
        token = self.token_generator.generate_token(table_name, record_data)
        
        # Get maskable fields for this table
        maskable_fields = self.schema_manager.get_maskable_fields(table_name)
        
        # Process record
        processed_record = record_data.copy()
        original_mappings = {}
        
        for field_name, original_value in record_data.items():
            if field_name in maskable_fields:
                # Generate pseudonymized data
                pseudo_value = self.pseudonymizer.pseudonymize(original_value, field_name)
                processed_record[field_name] = pseudo_value
                original_mappings[field_name] = original_value
        
        # Store original data in vault
        if original_mappings:
            # self.vault.store_original_data(token, table_name, record_id, original_mappings)
            #print(f"STORED: {len(original_mappings)} fields for token {token}")
            print()
        
        # Add token to processed record
        processed_record['row_token'] = token
        
        return processed_record, token
    
    def process_field(self, table_name, field_name, field_value, record_id):
        """Process a single field - for field-level updates."""
        
        # Get maskable fields for this table
        maskable_fields = self.schema_manager.get_maskable_fields(table_name)
        
        if field_name not in maskable_fields:
            # Non-PII field - return as is
            return field_value, None
        
        # Check if field already processed - skip if exists
        existing_token = self.vault.get_field_token_from_json(table_name, record_id, field_name)
        if existing_token:
            existing_pseudo = self.vault.get_pseudonymized_value(table_name, record_id, field_name)
            return existing_pseudo or field_value, existing_token
        
        # Generate field-specific encrypted token for reversible decryption
        base_token = self.token_generator.generate_encrypted_token(field_value)
        field_token = base_token  # Encrypted token for security and reversibility
        
        # Generate pseudonymized value
        pseudo_value = self.pseudonymizer.pseudonymize(field_value, field_name)
        
        # Store original field data in main table (not separate vault)
        # self.vault.store_field_data_in_main_table(field_token, table_name, record_id, field_name, field_value)
        #print(f"STORED: {field_name} = {field_value} with token {field_token}")
        
        return pseudo_value, field_token
    
    def retrieve_original_data(self, token):
        """Retrieve original data using token (for admin access)."""
        return self.vault.retrieve_by_token(token)
    
    def retrieve_field_data(self, field_token):
        """Retrieve original field data using field token - searches across tables."""
        # For now, return None - field retrieval will be done by table/record/field
        # In production, implement token-to-record mapping if needed
        return None
    
    def get_original_data_by_record(self, table_name, record_id):
        """Get original data by table and record ID."""
        return self.vault.retrieve_by_record(table_name, record_id)
    
    def get_pii_fields_for_process(self, table_name, process):
        """Get PII fields for a table based on process type"""
        process = (process or "").strip().lower()
        if process not in ("pseudo", "mask"):
            raise ValueError("process must be either 'pseudo' or 'mask'")
        
        schema = self.fabricator.get('schema', [])
        for table_config in schema:
            if table_config.get('table') == table_name:
                pii_fields = set()
                for column in table_config.get('columns', []):
                    col_name = column.get('name')
                    if col_name and bool(column.get(process)) is True:
                        pii_fields.add(col_name)
                return pii_fields
        return set()
    
    # Legacy methods for backward compatibility
    def get_table_config(self, table_name):
        """Get configuration for specific table."""
        return self.schema_manager.get_table_config(table_name)
    
    def get_maskable_fields(self, table_name):
        """Get fields that need masking."""
        return self.schema_manager.get_maskable_fields(table_name)