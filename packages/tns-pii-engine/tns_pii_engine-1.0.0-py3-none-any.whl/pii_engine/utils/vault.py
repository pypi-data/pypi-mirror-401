#!/usr/bin/env python3
"""
Vault operations for PII Engine
"""

import os
import json
import base64
import time
import mysql.connector
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'test_db')
}

class VaultManager:
    """Manage encrypted storage and retrieval of original PII data."""
    
    def __init__(self):
        self.key = os.getenv('PII_ENC_KEY')
        if not self.key:
            raise ValueError("PII_ENC_KEY not found")
        self.fernet = Fernet(self.key.encode())
        self.connection = None  # Reuse connection
    
    def store_original_data(self, token, table_name, record_id, field_mappings):
        """Store encrypted original data in vault."""
        try:
            # Encrypt field mappings
            encrypted_mappings = {}
            for field, original_value in field_mappings.items():
                encrypted_value = self.fernet.encrypt(str(original_value).encode())
                encrypted_mappings[field] = base64.b64encode(encrypted_value).decode()
            
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()
            
            # Delete old entry first
            cursor.execute("""
                DELETE FROM pii_vault 
                WHERE table_name = %s AND record_id = %s
            """, (table_name, record_id))
            
            # Insert new entry
            cursor.execute("""
                INSERT INTO pii_vault (token, table_name, record_id, field_mappings) 
                VALUES (%s, %s, %s, %s)
            """, (token, table_name, record_id, json.dumps(encrypted_mappings)))
            
            connection.commit()
            connection.close()
            
        except Exception as e:
            #print(f"Error storing in vault: {e}")
            raise
    
    def retrieve_by_token(self, token):
        """Retrieve original data using token."""
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT table_name, field_mappings 
                FROM pii_vault 
                WHERE token = %s
            """, (token,))
            
            result = cursor.fetchone()
            connection.close()
            
            if not result:
                return None
            
            table_name, encrypted_mappings_json = result
            encrypted_mappings = json.loads(encrypted_mappings_json)
            
            # Decrypt data
            original_data = {}
            for field, encrypted_b64 in encrypted_mappings.items():
                encrypted_data = base64.b64decode(encrypted_b64.encode())
                original_value = self.fernet.decrypt(encrypted_data).decode()
                original_data[field] = original_value
            
            return {
                'table_name': table_name,
                'original_data': original_data
            }
            
        except Exception as e:
            #print(f"Error retrieving original data: {e}")
            return None
    
    def retrieve_by_record(self, table_name, record_id):
        """Retrieve original data by table and record ID."""
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT token FROM pii_vault 
                WHERE table_name = %s AND record_id = %s
            """, (table_name, record_id))
            
            result = cursor.fetchone()
            connection.close()
            
            if not result:
                return None
            
            token = result[0]
            return self.retrieve_by_token(token)
            
        except Exception as e:
            #print(f"Error retrieving by record: {e}")
            return None
    
    def is_record_processed(self, table_name, record_id):
        """Check if record is already processed."""
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT COUNT(*) FROM pii_vault 
                WHERE table_name = %s AND record_id = %s
            """, (table_name, record_id))
            
            count = cursor.fetchone()[0]
            connection.close()
            
            return count > 0
            
        except Exception as e:
            #print(f"Error checking record status: {e}")
            return False
    
    def store_field_data(self, field_token, table_name, record_id, field_name, original_value):
        """Store encrypted field data in vault with field-specific token."""
        try:
            # Encrypt the field value
            encrypted_value = self.fernet.encrypt(str(original_value).encode())
            encrypted_b64 = base64.b64encode(encrypted_value).decode()
            
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()
            
            # Insert new field entry (allow multiple fields per record)
            cursor.execute("""
                INSERT INTO pii_vault (token, table_name, record_id, field_name, field_mappings) 
                VALUES (%s, %s, %s, %s, %s)
            """, (field_token, table_name, record_id, field_name, json.dumps({field_name: encrypted_b64})))
            
            connection.commit()
            connection.close()
            
        except Exception as e:
            #print(f"Error storing field in vault: {e}")
            raise
    
    def store_field_data_in_main_table(self, field_token, table_name, record_id, field_name, original_value):
        """Store field token and encrypted original in main table JSON column."""
        try:
            encrypted_value = self.fernet.encrypt(str(original_value).encode())
            encrypted_b64 = base64.b64encode(encrypted_value).decode()
            
            if not self.connection:
                self.connection = mysql.connector.connect(autocommit=True, **DB_CONFIG)
            
            cursor = self.connection.cursor()
            
            cursor.execute(f"SELECT pii_data FROM {table_name} WHERE id = %s", (record_id,))
            result = cursor.fetchone()
            
            pii_data = json.loads(result[0]) if result and result[0] else {}
            pii_data[field_name] = {'token': field_token, 'encrypted_value': encrypted_b64}
            
            cursor.execute(f"UPDATE {table_name} SET pii_data = %s WHERE id = %s", 
                         (json.dumps(pii_data), record_id))
            
            cursor.close()
            
        except Exception as e:
            #print(f"JSON storage failed: {e}")
            raise
    
    def retrieve_field_from_main_table(self, table_name, record_id, field_name):
        """Retrieve original field data from main table JSON column.
        
        Args:
            table_name: Database table name
            record_id: Record ID
            field_name: Field name to retrieve
            
        Returns:
            Original field value
        """
        try:
            if not self.connection:
                self.connection = mysql.connector.connect(autocommit=True, **DB_CONFIG)
            
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT pii_data FROM {table_name} WHERE id = %s", (record_id,))
            result = cursor.fetchone()
            cursor.close()
            
            if not result or not result[0]:
                return None
            
            pii_data = json.loads(result[0])
            if field_name not in pii_data:
                return None
                
            encrypted_value = pii_data[field_name]['encrypted_value']
            return self.decrypt_value(encrypted_value)
                
        except Exception as e:
            #print(f"Error retrieving field: {e}")
            return None
    
    def get_field_token_from_json(self, table_name, record_id, field_name):
        """Check if field already processed by looking for token in JSON."""
        try:
            if not self.connection:
                self.connection = mysql.connector.connect(autocommit=True, **DB_CONFIG)
            
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT pii_data FROM {table_name} WHERE id = %s", (record_id,))
            result = cursor.fetchone()
            cursor.close()
            
            if not result or not result[0]:
                return None
            
            pii_data = json.loads(result[0])
            return pii_data.get(field_name, {}).get('token')
            
        except Exception:
            return None
    
    def get_pseudonymized_value(self, table_name, record_id, field_name):
        """Get current pseudonymized value from main table."""
        try:
            if not self.connection:
                self.connection = mysql.connector.connect(autocommit=True, **DB_CONFIG)
            
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT {field_name} FROM {table_name} WHERE id = %s", (record_id,))
            result = cursor.fetchone()
            cursor.close()
            
            return result[0] if result else None
            
        except Exception:
            return None
    
    def get_existing_token(self, table_name, record_id):
        """Get existing token for a record."""
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT token FROM pii_vault 
                WHERE table_name = %s AND record_id = %s
            """, (table_name, record_id))
            
            result = cursor.fetchone()
            connection.close()
            
            return result[0] if result else None
            
        except Exception as e:
            #print(f"Error getting existing token: {e}")
            return None
    
    def decrypt_value(self, encrypted_value):
        """Decrypt a base64 encoded encrypted value."""
        try:
            encrypted_data = base64.b64decode(encrypted_value.encode())
            original_value = self.fernet.decrypt(encrypted_data).decode()
            return original_value
        except Exception as e:
            raise Exception(f"decryption failed: {str(e)}")