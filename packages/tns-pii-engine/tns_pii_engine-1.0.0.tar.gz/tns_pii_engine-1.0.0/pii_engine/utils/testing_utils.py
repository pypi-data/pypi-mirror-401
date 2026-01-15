#!/usr/bin/env python3
"""
Testing and Development Utilities for PII Engine
"""

import mysql.connector
from dotenv import load_dotenv
import os
from ..core.clean_processor import PIIProcessor

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def reset_demo_records():
    """Reset test records to original state for demo."""
    
    #print("DEMO RESET - Restoring Test Records to Original State")
    #print("=" * 55)
    
    # CONFIGURE: Update these to match your test records
    test_records = [31, 32, 33, 34]  # Same as in main.py
    table_name = "MASKING_users_test"  # Same as in main.py
    
    # Original data for demo records
    original_data = {
        31: {
            "email": "dchakras@gmail.com",
            "mobile_number": None,
            "password": "2133f910Aa1@"
        },
        32: {
            "email": "dchakras1@gmail.com", 
            "mobile_number": None,
            "password": "2133f910Aa1@"
        },
        33: {
            "email": "sonjoy.c@tnsservices.com",
            "mobile_number": "8477956894",
            "password": "2133f910Aa1@"
        },
        34: {
            "email": "naveenkumar.k@tnsservices.com",
            "mobile_number": "9874563210", 
            "password": "2133f910Aa1@"
        }
    }
    
    processor = PIIProcessor()
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    
    #print(f"Resetting records: {test_records}")
    #print(f"Table: {table_name}")
    #print("-" * 30)
    
    # Step 1: Restore original data to main table
    for record_id, data in original_data.items():
        #print(f"\nRestoring Record {record_id}:")
        #print(f"  Email: {data['email']}")
        #print(f"  Mobile: {data['mobile_number']}")
        print()

        # Update main table with original data and clear pii_data
        cursor.execute(f"""
            UPDATE {table_name} 
            SET email = %s, mobile_number = %s, password = %s, pii_data = NULL, updated_at = NOW()
            WHERE id = %s
        """, (
            data['email'],
            data['mobile_number'],
            data['password'],
            record_id
        ))
        
        #print(f"  SUCCESS: Restored to original state")
    
    connection.commit()
    
    # Step 2: Clear vault entries for these records
    #print(f"\nClearing vault entries...")
    cursor.execute(f"""
        DELETE FROM pii_vault 
        WHERE table_name = %s 
        AND record_id IN ({','.join(['%s'] * len(test_records))})
    """, [table_name] + test_records)
    
    deleted_count = cursor.rowcount
    connection.commit()
    
    #print(f"SUCCESS: Deleted {deleted_count} vault entries")
    connection.close()
    
    #print(f"\nSUCCESS: Demo Reset Complete!")
    #print("=" * 35)
    #print("Records are now in original state")

def view_tokens_in_database():
    """View tokens stored in pii_vault table."""
    
    #print("PII TOKENS IN DATABASE")
    #print("=" * 30)
    
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    
    # View pii_vault table structure
    #print("\n1. PII_VAULT TABLE STRUCTURE:")
    #print("-" * 35)
    cursor.execute("DESCRIBE pii_vault")
    columns = cursor.fetchall()
    
    for column in columns:
        #print(f"  {column[0]} - {column[1]}")
        print()
    
    # View all tokens in vault
    #print(f"\n2. ALL TOKENS IN VAULT:")
    #print("-" * 25)
    cursor.execute("""
        SELECT token, table_name, record_id, created_at 
        FROM pii_vault 
        ORDER BY created_at DESC
    """)
    
    vault_records = cursor.fetchall()
    
    if vault_records:
        #print(f"Found {len(vault_records)} tokens:")
        print()
        for record in vault_records:
            #print(f"  Token: {record[0]} | Table: {record[1]} | Record: {record[2]} | Created: {record[3]}")
            print()
    else:
        #print("  No tokens found in vault")
        print()
    
    connection.close()

def get_processing_statistics(table_name):
    """Get processing statistics for a table."""
    
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    
    # Total records in table
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    total_records = cursor.fetchone()[0]
    
    # Processed records in vault
    cursor.execute("""
        SELECT COUNT(*) FROM pii_vault 
        WHERE table_name = %s
    """, (table_name,))
    processed_records = cursor.fetchone()[0]
    
    connection.close()
    
    percentage = (processed_records / total_records * 100) if total_records > 0 else 0
    
    return {
        'total': total_records,
        'processed': processed_records,
        'percentage': percentage
    }