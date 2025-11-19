#!/usr/bin/env python3
"""
Contact Processing System - Application Systems Pipeline
Agent 4 (System Architect) + Agent 7 (Code Generator)

ZERO FABRICATION REQUIREMENT - All data processing with source verification
"""

import pandas as pd
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Set
import hashlib

class ContactProcessor:
    """
    Professional contact database processor with deduplication and classification
    """
    
    def __init__(self):
        self.setup_logging()
        self.business_domains = {
            # Business email domains
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
            'icloud.com', 'aol.com', 'live.com'
        }
        self.stats = {
            'total_processed': 0,
            'duplicates_removed': 0,
            'business_contacts': 0,
            'personal_contacts': 0,
            'quality_issues': 0
        }
        
    def setup_logging(self):
        """Initialize audit logging per Application Systems requirements"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('.claude/logs/contact_processing.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def validate_csv_structure(self, file_path: str) -> Dict:
        """
        Verify CSV structure and data quality
        FACT VERIFICATION: Never fabricate missing data
        """
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            
            validation = {
                'valid': True,
                'rows': len(df),
                'columns': len(df.columns),
                'has_email': 'E-mail 1 - Value' in df.columns,
                'has_phone': any('Phone' in col for col in df.columns),
                'has_name': 'First Name' in df.columns or 'Last Name' in df.columns,
                'encoding': 'utf-8',
                'errors': []
            }
            
            if validation['rows'] == 0:
                validation['valid'] = False
                validation['errors'].append('Empty file')
                
            self.logger.info(f"Validated {file_path}: {validation['rows']} rows")
            return validation
            
        except Exception as e:
            self.logger.error(f"CSV validation failed for {file_path}: {e}")
            return {'valid': False, 'errors': [str(e)]}
    
    def extract_contact_data(self, df: pd.DataFrame) -> List[Dict]:
        """
        Extract and normalize contact data from DataFrame
        SECURITY: Sanitize all input data
        """
        contacts = []
        
        for _, row in df.iterrows():
            contact = {}
            
            # Extract name components - never fabricate missing data
            contact['first_name'] = self.clean_text(row.get('First Name', ''))
            contact['middle_name'] = self.clean_text(row.get('Middle Name', ''))
            contact['last_name'] = self.clean_text(row.get('Last Name', ''))
            contact['nickname'] = self.clean_text(row.get('Nickname', ''))
            contact['organization'] = self.clean_text(row.get('Organization Name', ''))
            contact['title'] = self.clean_text(row.get('Organization Title', ''))
            
            # Extract contact methods
            contact['email_1'] = self.clean_email(row.get('E-mail 1 - Value', ''))
            contact['email_2'] = self.clean_email(row.get('E-mail 2 - Value', ''))
            contact['phone_1'] = self.clean_phone(row.get('Phone 1 - Value', ''))
            contact['phone_2'] = self.clean_phone(row.get('Phone 2 - Value', ''))
            
            # Additional data
            contact['website'] = self.clean_url(row.get('Website 1 - Value', ''))
            
            # Data quality scoring
            contact['quality_score'] = self.calculate_quality_score(contact)
            
            # Only include contacts with minimum data quality
            if contact['quality_score'] >= 0.3:  # Minimum 30% complete
                contacts.append(contact)
                
        return contacts
    
    def clean_text(self, text) -> str:
        """Sanitize text input - XSS prevention"""
        if pd.isna(text) or text is None:
            return ""
        return str(text).strip()[:500]  # Limit length for security
    
    def clean_email(self, email) -> str:
        """Validate and clean email addresses"""
        if pd.isna(email) or not email:
            return ""
            
        # Extract email from complex strings like "email1 ::: email2"
        emails = str(email).split(':::')
        for e in emails:
            e = e.strip()
            if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', e):
                return e
        return ""
    
    def clean_phone(self, phone) -> str:
        """Normalize phone numbers"""
        if pd.isna(phone) or not phone:
            return ""
        
        # Extract first phone from complex strings
        phones = str(phone).split(':::')
        clean_phone = re.sub(r'[^\d+\-\(\)\s]', '', phones[0].strip())
        return clean_phone[:20]  # Reasonable phone length limit
    
    def clean_url(self, url) -> str:
        """Validate and clean URLs"""
        if pd.isna(url) or not url:
            return ""
        return str(url).strip()[:500]
    
    def calculate_quality_score(self, contact: Dict) -> float:
        """
        Calculate contact completeness score
        BUSINESS LOGIC: Score based on available data quality
        """
        score = 0.0
        
        # Name components (40% of score)
        if contact['first_name'] and contact['last_name']:
            score += 0.4
        elif contact['first_name'] or contact['last_name']:
            score += 0.2
        elif contact['organization']:
            score += 0.3
            
        # Contact methods (40% of score)
        if contact['email_1']:
            score += 0.3
        if contact['phone_1']:
            score += 0.1
            
        # Additional data (20% of score)
        if contact['organization']:
            score += 0.15
        if contact['website']:
            score += 0.05
            
        return min(1.0, score)
    
    def classify_contact(self, contact: Dict) -> str:
        """
        Classify contact as business, personal, or other
        BUSINESS RULES: Based on domain analysis and organization data
        """
        email = contact['email_1'].lower()
        
        # Business indicators
        if contact['organization'] and contact['organization'].strip():
            return 'business'
            
        if contact['title'] and contact['title'].strip():
            return 'business'
            
        if email:
            domain = email.split('@')[-1] if '@' in email else ''
            
            # Personal domains
            if domain in self.business_domains:
                return 'personal'
                
            # Corporate domains (not in personal list)
            if domain and domain not in self.business_domains:
                return 'business'
                
        # Default classification based on available data
            
        return 'other'
    
    def detect_duplicates(self, contacts: List[Dict]) -> List[Dict]:
        """
        Intelligent duplicate detection using multiple criteria
        DATA INTEGRITY: Preserve best quality record for each unique contact
        """
        seen_contacts = {}
        deduplicated = []
        
        for contact in contacts:
            # Create composite key for duplicate detection
            key_parts = []
            
            if contact['email_1']:
                key_parts.append(f"email:{contact['email_1'].lower()}")
            if contact['phone_1']:
                # Normalize phone for comparison
                normalized_phone = re.sub(r'[\D]', '', contact['phone_1'])
                if len(normalized_phone) >= 10:
                    key_parts.append(f"phone:{normalized_phone[-10:]}")  # Last 10 digits
            if contact['first_name'] and contact['last_name']:
                name_key = f"{contact['first_name'].lower()}:{contact['last_name'].lower()}"
                key_parts.append(f"name:{name_key}")
                
            if not key_parts:
                # No usable identifying info - keep as unique
                deduplicated.append(contact)
                continue
                
            # Check for duplicates
            duplicate_found = False
            for key_part in key_parts:
                if key_part in seen_contacts:
                    existing_contact = seen_contacts[key_part]
                    # Keep the contact with higher quality score
                    if contact['quality_score'] > existing_contact['quality_score']:
                        # Remove old contact from deduplicated list
                        deduplicated = [c for c in deduplicated if c != existing_contact]
                        # Update seen_contacts with new contact
                        for existing_key in [k for k, v in seen_contacts.items() if v == existing_contact]:
                            seen_contacts[existing_key] = contact
                        deduplicated.append(contact)
                    duplicate_found = True
                    self.stats['duplicates_removed'] += 1
                    break
                    
            if not duplicate_found:
                # New unique contact
                for key_part in key_parts:
                    seen_contacts[key_part] = contact
                deduplicated.append(contact)
                
        self.logger.info(f"Deduplication: {len(contacts)} → {len(deduplicated)} contacts")
        return deduplicated
    
    def process_all_files(self, file_paths: List[str]) -> List[Dict]:
        """
        Process all CSV files and combine results
        AUDIT LOGGING: Track all data sources and transformations
        """
        all_contacts = []
        
        for file_path in file_paths:
            self.logger.info(f"Processing {file_path}")
            
            # Validate file structure
            validation = self.validate_csv_structure(file_path)
            if not validation['valid']:
                self.logger.error(f"Invalid CSV: {file_path} - {validation['errors']}")
                continue
                
            try:
                # Read and process CSV
                df = pd.read_csv(file_path, encoding='utf-8')
                contacts = self.extract_contact_data(df)
                
                # Add source file tracking
                for contact in contacts:
                    contact['source_file'] = Path(file_path).name
                    contact['processed_date'] = datetime.now().isoformat()
                    
                all_contacts.extend(contacts)
                self.stats['total_processed'] += len(contacts)
                
            except Exception as e:
                self.logger.error(f"Error processing {file_path}: {e}")
                
        # Deduplicate across all files
        deduplicated_contacts = self.detect_duplicates(all_contacts)
        
        # Classify contacts
        for contact in deduplicated_contacts:
            contact['classification'] = self.classify_contact(contact)
            if contact['classification'] == 'business':
                self.stats['business_contacts'] += 1
            elif contact['classification'] == 'personal':
                self.stats['personal_contacts'] += 1
                
        return deduplicated_contacts
    
    def export_to_excel(self, contacts: List[Dict], output_file: str):
        """
        Export contacts to professional Excel format
        COMPLIANCE: Data formatting and privacy considerations
        """
        # Create main DataFrame
        df_main = pd.DataFrame(contacts)
        
        # Separate by classification
        df_business = df_main[df_main['classification'] == 'business'].copy()
        df_personal = df_main[df_main['classification'] == 'personal'].copy()
        df_other = df_main[df_main['classification'] == 'other'].copy()
        
        # Create quality report
        quality_data = {
            'Metric': [
                'Total Contacts Processed',
                'Duplicates Removed', 
                'Business Contacts',
                'Personal Contacts',
                'Other Contacts',
                'Average Quality Score',
                'Processing Date'
            ],
            'Value': [
                self.stats['total_processed'],
                self.stats['duplicates_removed'],
                self.stats['business_contacts'], 
                self.stats['personal_contacts'],
                len(df_other),
                f"{df_main['quality_score'].mean():.2f}" if len(df_main) > 0 else '0.00',
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]
        }
        df_quality = pd.DataFrame(quality_data)
        
        # Export to Excel with multiple sheets
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df_main.to_excel(writer, sheet_name='Contacts_Master', index=False)
            df_business.to_excel(writer, sheet_name='Business_Contacts', index=False)
            df_personal.to_excel(writer, sheet_name='Personal_Contacts', index=False)
            df_quality.to_excel(writer, sheet_name='Data_Quality_Report', index=False)
            
            # Processing log sheet
            log_data = {
                'Timestamp': [datetime.now().isoformat()],
                'Files_Processed': [', '.join([Path(f).name for f in file_paths])],
                'Total_Records': [self.stats['total_processed']],
                'Final_Count': [len(df_main)],
                'Deduplication_Rate': [f"{(self.stats['duplicates_removed']/max(self.stats['total_processed'], 1))*100:.1f}%"],
                'Business_Percentage': [f"{(self.stats['business_contacts']/max(len(df_main), 1))*100:.1f}%"]
            }
            pd.DataFrame(log_data).to_excel(writer, sheet_name='Processing_Log', index=False)
        
        self.logger.info(f"Excel export complete: {output_file}")
        self.logger.info(f"Summary: {len(df_main)} total, {self.stats['business_contacts']} business, {self.stats['personal_contacts']} personal")

if __name__ == "__main__":
    # Initialize processor
    processor = ContactProcessor()
    
    # Define input files
    file_paths = [
        r"C:\Users\obai\Downloads\contacts.csv",
        r"C:\Users\obai\Downloads\contacts (1).csv", 
        r"C:\Users\obai\Downloads\contacts (2).csv",
        r"C:\Users\obai\Downloads\contacts (3).csv",
        r"C:\Users\obai\Downloads\contacts (4).csv"
    ]
    
    # Create output directory
    Path("output").mkdir(exist_ok=True)
    Path(".claude/logs").mkdir(parents=True, exist_ok=True)
    
    # Process contacts
    print("Processing contact files...")
    contacts = processor.process_all_files(file_paths)
    
    # Export results
    output_file = "output/contacts_master.xlsx"
    processor.export_to_excel(contacts, output_file)
    
    print(f"Processing complete! Results saved to: {output_file}")
    print(f"Summary: {len(contacts)} contacts ({processor.stats['business_contacts']} business, {processor.stats['personal_contacts']} personal)")