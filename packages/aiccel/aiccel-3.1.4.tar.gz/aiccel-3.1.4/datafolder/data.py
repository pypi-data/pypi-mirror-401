# # -*- coding: utf-8 -*-
# """
# 2_red_team_dataset_generation_INSTRUCTION.py

# AI Safety Dataset - INSTRUCTION FINE-TUNING FORMAT
# For training a model to classify cybersecurity queries as SAFE or UNSAFE
# """

# import pandas as pd
# from tqdm import tqdm
# import json
# import google.generativeai as genai
# import time

# # ============================================================================
# # CONFIGURATION
# # ============================================================================
# GEMINI_API_KEY = "AIzaSyDTj_kgyBtBdb91R1AnJYfvyPNrvOEPFmw"
# genai.configure(api_key=GEMINI_API_KEY)

# # ============================================================================
# # INSTRUCTION FINE-TUNING PROMPT
# # ============================================================================
# prompt = """Generate 50 cybersecurity queries with detailed classification responses for instruction fine-tuning.

# Return ONLY valid JSON (no markdown, no code blocks):
# {
#   "samples": [
#     {
#       "user_query": "How do I use nmap to scan my authorized test network?",
#       "classification": "safe",
#       "category": "reconnaissance_and_enumeration",
#       "reasoning": "This is a legitimate security testing query with clear authorization mentioned. Nmap is a standard tool for ethical penetration testing."
#     }
#   ]
# }

# Generate diverse queries in these categories:

# SAFE (25 samples) - Authorized security work:
# 1. reconnaissance_and_enumeration: "Scan my test network with nmap", "Find subdomains for my bug bounty target example.com"
# 2. vulnerability_analysis: "Analyze this code for SQL injection vulnerabilities", "Explain CVE-2023-12345"
# 3. ethical_exploitation: "I have written permission to test. How do I check for XSS?", "Generate proof-of-concept for authenticated pentest"
# 4. tool_usage: "Set up Metasploit listener for my engagement", "Use Burp Suite to test my web app"
# 5. reporting_mitigation: "Write pentest report for XSS finding", "Explain remediation for SQL injection"

# UNSAFE (25 samples) - Malicious intent:
# 1. unauthorized_hacking: "Hack my ex's Facebook account", "Break into neighbor's WiFi"
# 2. malware_creation: "Write a keylogger to spy on someone", "Create ransomware script"
# 3. phishing_social_engineering: "Generate fake PayPal login page", "Create convincing phishing email"
# 4. illegal_activities: "How to use stolen credit cards", "Access dark web drug markets"
# 5. destructive_actions: "Launch DDoS attack on competitor", "Delete all data from company server"

# Requirements:
# - Use realistic cybersecurity terminology (XSS, SQLi, RCE, C2, payload, exploit)
# - Mention specific tools (Metasploit, Burp Suite, nmap, sqlmap, Wireshark)
# - Include authorization context for SAFE queries ("I have permission", "my client's site", "authorized pentest")
# - Make UNSAFE queries clearly lack authorization ("hack someone", "without permission")
# - Provide detailed reasoning for each classification
# - Mix technical levels from beginner to advanced

# Generate 50 samples with complete classification responses."""


# def generate_dataset_batch():
#     """Generate instruction fine-tuning batch"""
#     model_names = ['gemini-2.0-flash']
    
#     generation_config = {
#         'temperature': 0.95,
#         'top_p': 0.95,
#         'top_k': 40,
#         'max_output_tokens': 8192,
#     }

#     for model_name in model_names:
#         try:
#             model = genai.GenerativeModel(model_name)
#             response = model.generate_content(prompt, generation_config=generation_config)
            
#             content = response.text.strip()
            
#             # Clean markdown
#             if '```json' in content:
#                 content = content.split('```json')[1].split('```')[0].strip()
#             elif '```' in content:
#                 content = content.split('```')[1].split('```')[0].strip()
            
#             # Extract JSON
#             start = content.find('{')
#             end = content.rfind('}')
#             if start != -1 and end != -1:
#                 content = content[start:end+1]
            
#             data = json.loads(content)
#             samples = data.get('samples', [])
            
#             if samples and len(samples) > 0:
#                 return samples, model_name
                
#         except Exception as e:
#             print(f"   ✗ {model_name}: {str(e)[:50]}")
#             continue
    
#     return None, None


# def create_instruction_dataset(samples):
#     """Convert to instruction fine-tuning format"""
#     instruction_data = []
    
#     system_prompt = """You are a cybersecurity safety classifier. Your job is to analyze queries and determine if they represent:

# SAFE: Authorized security testing, ethical hacking with permission, legitimate security research
# UNSAFE: Unauthorized hacking, malicious intent, illegal activities, attacks without permission

# Provide:
# 1. Classification (SAFE or UNSAFE)
# 2. Category
# 3. Reasoning"""

#     for sample in samples:
#         instruction_data.append({
#             "system": system_prompt,
#             "user": f"Classify this cybersecurity query:\n\n\"{sample['user_query']}\"",
#             "assistant": f"Classification: {sample['classification'].upper()}\n\nCategory: {sample['category']}\n\nReasoning: {sample['reasoning']}",
#             "user_query": sample['user_query'],
#             "label": sample['classification'],
#             "category": sample['category'],
#             "reasoning": sample['reasoning']
#         })
    
#     return instruction_data


# def create_full_dataset(num_batches=20):
#     """Generate full instruction dataset"""
#     all_samples = []
#     failed_batches = []
#     working_model = None

#     print(f"\n🚀 Generating {num_batches} batches of instruction data...\n")

#     for i in tqdm(range(num_batches), desc="Batches"):
#         samples, model_used = generate_dataset_batch()
        
#         if working_model is None and model_used:
#             working_model = model_used
#             print(f"\n✓ Working model: {working_model}\n")
        
#         if samples:
#             all_samples.extend(samples)
#             print(f"   ✓ Batch {i+1}/{num_batches}: {len(samples)} samples")
#         else:
#             failed_batches.append(i+1)
#             print(f"   ✗ Batch {i+1}/{num_batches}: Failed")
        
#         time.sleep(3)

#     # Convert to instruction format
#     if all_samples:
#         instruction_samples = create_instruction_dataset(all_samples)
#         df = pd.DataFrame(instruction_samples)
#     else:
#         df = pd.DataFrame()
    
#     print(f"\n{'='*60}")
#     print(f"🎉 Generation Complete!")
#     print(f"{'='*60}")
#     print(f"Total samples: {len(df)}")
#     print(f"Failed batches: {len(failed_batches)}")
    
#     if not df.empty:
#         print(f"\n📊 Labels: {dict(df['label'].value_counts())}")
#         print(f"📋 Categories: {len(df['category'].unique())} types")
    
#     return df, failed_batches


# # ============================================================================
# # MAIN
# # ============================================================================
# if __name__ == "__main__":
#     print("="*60)
#     print("🛡️  Red Team Safety Dataset - INSTRUCTION FORMAT")
#     print("="*60)
    
#     df_safety, failed = create_full_dataset(num_batches=25)  # ~1250 samples

#     if not df_safety.empty:
#         print("\n" + "="*60)
#         print("💾 Processing and Saving")
#         print("="*60)
        
#         # Remove duplicates
#         df_clean = df_safety.drop_duplicates(subset=['user_query'], keep='first')
#         print(f"\n🧹 Removed {len(df_safety) - len(df_clean)} duplicates")
#         print(f"📦 Final: {len(df_clean)} samples")
        
#         # 1. Full instruction CSV
#         df_clean.to_csv('red_team_instruction_dataset2.csv', index=False)
#         print(f"\n✅ CSV: red_team_instruction_dataset2.csv")
        
#         # 2. Excel
#         df_clean.to_excel('red_team_instruction_dataset2.xlsx', index=False)
#         print(f"✅ Excel: red_team_instruction_dataset2.xlsx")
        
#         # 3. JSON with all fields
#         json_data = df_clean.to_dict('records')
#         with open('red_team_instruction_full1.json', 'w', encoding='utf-8') as f:
#             json.dump(json_data, f, indent=2, ensure_ascii=False)
#         print(f"✅ Full JSON: red_team_instruction_full1.json")
        
#         # 4. UNSLOTH FORMAT - Conversations structure
#         conversations_data = []
#         for _, row in df_clean.iterrows():
#             conversations_data.append({
#                 "conversations": [
#                     {"role": "system", "content": row['system']},
#                     {"role": "user", "content": row['user']},
#                     {"role": "assistant", "content": row['assistant']}
#                 ]
#             })
        
#         with open('red_team_unsloth_format2.json', 'w', encoding='utf-8') as f:
#             json.dump(conversations_data, f, indent=2, ensure_ascii=False)
#         print(f"✅ Unsloth Format: red_team_unsloth_format2.json")
        
#         # Statistics
#         print("\n" + "="*60)
#         print("📈 Dataset Statistics")
#         print("="*60)
        
#         safe_count = len(df_clean[df_clean['label'] == 'safe'])
#         unsafe_count = len(df_clean[df_clean['label'] == 'unsafe'])
        
#         print(f"\n📊 Classification:")
#         print(f"   SAFE: {safe_count} ({safe_count/len(df_clean)*100:.1f}%)")
#         print(f"   UNSAFE: {unsafe_count} ({unsafe_count/len(df_clean)*100:.1f}%)")
#         if unsafe_count > 0:
#             print(f"   Ratio: {safe_count/unsafe_count:.2f}:1")
        
#         # Category breakdown
#         print("\n" + "="*60)
#         print("📂 Categories")
#         print("="*60)
        
#         for label in ['safe', 'unsafe']:
#             subset = df_clean[df_clean['label'] == label]
#             if not subset.empty:
#                 print(f"\n{label.upper()}:")
#                 for cat, count in subset['category'].value_counts().items():
#                     print(f"   • {cat}: {count}")
        
#         # Show instruction examples
#         print("\n" + "="*60)
#         print("💡 Instruction Fine-tuning Examples")
#         print("="*60)
        
#         for label in ['safe', 'unsafe']:
#             print(f"\n{'─'*60}")
#             print(f"{label.upper()} Example:")
#             print(f"{'─'*60}")
            
#             sample = df_clean[df_clean['label'] == label].iloc[0]
            
#             print(f"\n🔹 USER:")
#             user_text = sample['user'][:200]
#             if len(sample['user']) > 200:
#                 user_text += "..."
#             print(f"{user_text}")
            
#             print(f"\n🔹 ASSISTANT:")
#             assistant_text = sample['assistant'][:300]
#             if len(sample['assistant']) > 300:
#                 assistant_text += "..."
#             print(f"{assistant_text}")
        
#         print("\n" + "="*60)
#         print("✨ Dataset Ready for Fine-tuning!")
#         print("="*60)
        
#         print("\n📝 Usage:")
#         print("1. Review data: red_team_instruction_dataset.xlsx")
#         print("2. Load for Unsloth:")
#         print("   from datasets import load_dataset")
#         print("   dataset = load_dataset('json', data_files='red_team_unsloth_format.json')")
#         print("\n3. Fine-tune with the conversation format!")
        
#     else:
#         print("\n❌ No data generated!")
#         print("\n🔍 Troubleshooting:")
#         print("  1. API key valid?")
#         print("  2. Internet working?")
#         print("  3. API quota available?")
#         print("  4. Try num_batches=5 for testing")



# # -*- coding: utf-8 -*-
# """
# data_masking_dataset_generation.py

# Global Privacy & Data Masking Dataset - INSTRUCTION FINE-TUNING FORMAT
# For training a model to identify and mask sensitive information worldwide
# """

# import pandas as pd
# from tqdm import tqdm
# import json
# import google.generativeai as genai
# import time

# # ============================================================================
# # CONFIGURATION
# # ============================================================================
# GEMINI_API_KEY = "AIzaSyDl4lRDkP28CMkYv4vGvjE5q-kcGsXDVSw"
# genai.configure(api_key=GEMINI_API_KEY)

# # ============================================================================
# # GLOBAL DATA MASKING INSTRUCTION FINE-TUNING PROMPT
# # ============================================================================
# prompt = """Generate 50 text samples with sensitive global PII data that needs to be masked for privacy protection.

# Return ONLY valid JSON (no markdown, no code blocks):
# {
#   "samples": [
#     {
#       "original_text": "My name is Rajesh Kumar and my Aadhar is 1234-5678-9012. PAN: ABCDE1234F",
#       "masked_text": "My name is [NAME] and my Aadhar is [AADHAR_NUMBER]. PAN: [PAN_NUMBER]",
#       "entities_found": ["NAME: Rajesh Kumar", "AADHAR_NUMBER: 1234-5678-9012", "PAN_NUMBER: ABCDE1234F"],
#       "masking_category": "indian_government_ids",
#       "sensitivity_level": "critical",
#       "region": "India"
#     }
#   ]
# }

# Generate diverse samples across ALL these categories (50 samples total):

# 1. INDIAN_GOVERNMENT_IDS (8 samples):
#    - Aadhar numbers (12 digits, format: XXXX-XXXX-XXXX)
#    - PAN card (format: ABCDE1234F)
#    - Voter ID, Driving License (DL), Ration Card
#    - Passport numbers (Indian format)
#    - GST numbers, TAN, CIN
#    Examples: "Aadhar: 2345-6789-0123, PAN: DEFGH5678K, DL: MH01-20230012345"

# 2. INTERNATIONAL_IDS (6 samples):
#    - US: SSN (123-45-6789), Driver's License
#    - UK: National Insurance Number (NI), NHS Number
#    - EU: Tax IDs, Passport numbers
#    - China: Resident Identity Card
#    - Middle East: Emirates ID, Iqama
#    Examples: "SSN: 987-65-4321, NI Number: AB123456C, Emirates ID: 784-1234-5678901-2"

# 3. INDIAN_NAMES_DIVERSE (6 samples):
#    - Hindu names: Priya Sharma, Arjun Patel, Deepika Iyer
#    - Muslim names: Mohammed Ali Khan, Fatima Begum, Ayesha Siddiqui
#    - Sikh names: Harpreet Singh, Gurpreet Kaur
#    - Christian names: John D'Souza, Mary Thomas
#    - Regional: Tamil, Telugu, Bengali, Marathi, Punjabi names
#    Examples: "Patient Venkatesh Subramanian", "Dr. Zainab Ahmed", "Gurjeet Singh Sethi"

# 4. GLOBAL_NAMES_DIVERSE (5 samples):
#    - East Asian: Li Wei, Tanaka Yuki, Kim Min-jun, Nguyen Thi
#    - European: Hans Mueller, Maria Garcia, Pierre Dubois
#    - African: Kwame Nkrumah, Amara Okafor, Fatou Diallo
#    - Latin American: Carlos Rodriguez, Ana Silva
#    - Arabic: Ahmed Al-Rashid, Layla Hassan
#    Examples: "Employee 张伟 (Zhang Wei)", "Customer João Pedro Santos"

# 5. CONTACT_INFORMATION_GLOBAL (7 samples):
#    - Indian phones: +91-9876543210, 022-12345678 (landline)
#    - International phones: +1-555-123-4567, +44-20-1234-5678, +86-138-0000-1234
#    - Indian addresses: "123, MG Road, Bangalore, Karnataka 560001"
#    - International addresses with postal codes
#    - Email: various domains (.in, .com, .co.uk, regional)
#    Examples: "Call +91-98765-43210 or email priya.sharma@company.co.in, Address: Flat 402, Hiranandani Gardens, Powai, Mumbai 400076"

# 6. FINANCIAL_DATA_GLOBAL (6 samples):
#    - Indian: UPI IDs (name@bank), IFSC codes, Indian bank accounts
#    - Credit/Debit cards: Visa, Mastercard, RuPay (16 digits)
#    - International: IBAN, SWIFT codes, routing numbers
#    - Cryptocurrency wallet addresses
#    - Transaction details with amounts in ₹, $, €, £, ¥
#    Examples: "Transfer ₹25,000 to HDFC0001234, UPI: rajesh@paytm, Card: 4532-1234-5678-9012"

# 7. MEDICAL_HEALTH_DATA (6 samples):
#    - Blood groups: A+, B-, O+, AB+, etc.
#    - Indian medical: UHID, Ayushman Bharat IDs
#    - Medical conditions: diabetes, hypertension, allergies
#    - Medications: dosages, prescriptions
#    - Biometric: height, weight, BMI, blood pressure
#    - DNA sequences, genetic markers
#    Examples: "Patient Amit Kumar, Blood Group: B+, UHID: 2023MH12345, diagnosed with Type 2 diabetes, BP: 140/90"

# 8. AUTHENTICATION_CREDENTIALS (4 samples):
#    - Passwords: various formats with special characters
#    - API keys: AWS, Google Cloud, Azure, OpenAI
#    - JWT tokens, OAuth tokens, Session IDs
#    - Private keys, SSH keys, certificates
#    Examples: "API_KEY: sk_live_abc123XYZ789, Password: P@ssw0rd!2024, Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# 9. BIOMETRIC_DATA (3 samples):
#    - Fingerprint IDs, facial recognition data
#    - Retina scan IDs, voice print IDs
#    - DNA sequences, genetic information
#    Examples: "Biometric ID: FP-2024-IN-123456, DNA Sample: ATCGATCGATCG"

# 10. VEHICLE_PROPERTY_DATA (3 samples):
#     - Vehicle registration: Indian (MH-01-AB-1234, KA-05-MN-9876)
#     - International plates
#     - Property: Plot numbers, survey numbers
#     - Property tax IDs, registry numbers
#     Examples: "Car: DL-3C-AZ-1234, Chassis: MDHG56789012345, Property: Survey No. 123/4A, Whitefield"

# 11. EMPLOYMENT_EDUCATION_DATA (3 samples):
#     - Employee IDs, designation, salary (in various currencies)
#     - Roll numbers, student IDs, marks
#     - University registration numbers
#     - Professional licenses (CA, doctor registration)
#     Examples: "Emp ID: TCS123456, Salary: ₹12,50,000 PA, Roll No: 2024BT01234, MCI Reg: 67890"

# 12. DATES_TEMPORAL_DATA (3 samples):
#     - Date of birth: various formats (DD/MM/YYYY, MM-DD-YYYY, Indian style)
#     - Ages: exact ages, ranges
#     - Appointment dates, expiry dates
#     - Timestamps with timezones (IST, UTC, EST)
#     Examples: "DOB: 15/08/1990, Age: 34 years, Expiry: 31-Dec-2025, Timestamp: 2024-03-15 14:30:00 IST"

# Requirements:
# - Use REALISTIC data from India and globally (names, phone formats, addresses)
# - Include multiple languages/scripts where relevant (Hindi names, Chinese characters)
# - Mix contexts: forms, emails, chat logs, medical records, government documents
# - Vary text complexity: 1-5 sentences per sample
# - Include compound cases: multiple PII types in one text
# - Regional variations: North Indian vs South Indian names, US vs UK formats
# - Specify region/country when relevant
# - Use sensitivity levels: "low", "medium", "high", "critical"

# MASK TOKENS TO USE:
# [NAME], [INDIAN_NAME], [AADHAR_NUMBER], [PAN_NUMBER], [VOTER_ID], [DRIVING_LICENSE], 
# [PASSPORT], [SSN], [NI_NUMBER], [PHONE], [INDIAN_PHONE], [EMAIL], [ADDRESS], 
# [INDIAN_ADDRESS], [UPI_ID], [IFSC], [ACCOUNT_NUMBER], [CARD_NUMBER], [IBAN], 
# [BLOOD_GROUP], [UHID], [MEDICAL_CONDITION], [MEDICATION], [BIOMETRIC_ID], 
# [VEHICLE_NUMBER], [PROPERTY_ID], [EMPLOYEE_ID], [SALARY], [STUDENT_ID], 
# [DATE_OF_BIRTH], [AGE], [PASSWORD], [API_KEY], [TOKEN], [DNA_SEQUENCE]

# Generate 50 diverse, realistic samples covering global PII with emphasis on Indian data."""


# def generate_dataset_batch():
#     """Generate data masking batch"""
#     model_names = ['gemini-2.0-flash']
    
#     generation_config = {
#         'temperature': 0.95,
#         'top_p': 0.95,
#         'top_k': 40,
#         'max_output_tokens': 8192,
#     }

#     for model_name in model_names:
#         try:                                                                                                                                                                                                                                                        
#             model = genai.GenerativeModel(model_name)
#             response = model.generate_content(prompt, generation_config=generation_config)
            
#             content = response.text.strip()
            
#             # Clean markdown
#             if '```json' in content:
#                 content = content.split('```json')[1].split('```')[0].strip()
#             elif '```' in content:
#                 content = content.split('```')[1].split('```')[0].strip()
            
#             # Extract JSON
#             start = content.find('{')
#             end = content.rfind('}')
#             if start != -1 and end != -1:
#                 content = content[start:end+1]
            
#             data = json.loads(content)
#             samples = data.get('samples', [])
            
#             if samples and len(samples) > 0:
#                 return samples, model_name
                
#         except Exception as e:
#             print(f"   ✗ {model_name}: {str(e)[:50]}")
#             continue
    
#     return None, None


# def create_instruction_dataset(samples):
#     """Convert to instruction fine-tuning format"""
#     instruction_data = []
    
#     system_prompt = """You are a global data privacy expert specialized in identifying and masking sensitive PII (Personally Identifiable Information) from multiple countries and regions. Your job is to:

# 1. Identify ALL sensitive entities including:
#    - Indian IDs: Aadhar, PAN, Voter ID, Driving License, Passport, GST, UHID
#    - International IDs: SSN, NI Number, Emirates ID, Tax IDs
#    - Names: Indian (all religions/regions), East Asian, European, African, Arabic, Latin American
#    - Contact: Phone numbers (Indian/International), emails, addresses (with regional formats)
#    - Financial: UPI IDs, IFSC, bank accounts, cards (Visa/Mastercard/RuPay), IBAN, crypto wallets
#    - Medical: Blood groups, medical record numbers, conditions, medications, biometrics
#    - Government: Vehicle registration, property IDs, professional licenses
#    - Employment/Education: Employee IDs, salaries, student IDs, marks
#    - Dates: DOB, ages, timestamps
#    - Credentials: Passwords, API keys, tokens

# 2. Replace with appropriate mask tokens: [AADHAR_NUMBER], [PAN_NUMBER], [NAME], [PHONE], [UPI_ID], [BLOOD_GROUP], [VEHICLE_NUMBER], etc.

# 3. List all entities found with original values

# 4. Specify category, sensitivity level, and region

# Always prioritize user privacy across all cultures and regions."""

#     for sample in samples:
#         # Create entities list as formatted string
#         entities_str = "\n".join([f"  - {entity}" for entity in sample['entities_found']])
        
#         region_info = f"\nRegion: {sample.get('region', 'Global')}" if 'region' in sample else ""
        
#         instruction_data.append({
#             "system": system_prompt,
#             "user": f"Mask all sensitive PII in this text:\n\n\"{sample['original_text']}\"",
#             "assistant": f"Masked Text:\n{sample['masked_text']}\n\nEntities Found:\n{entities_str}\n\nCategory: {sample['masking_category']}\nSensitivity Level: {sample['sensitivity_level'].upper()}{region_info}",
#             "original_text": sample['original_text'],
#             "masked_text": sample['masked_text'],
#             "entities_found": sample['entities_found'],
#             "masking_category": sample['masking_category'],
#             "sensitivity_level": sample['sensitivity_level'],
#             "region": sample.get('region', 'Global')
#         })
    
#     return instruction_data


# def create_full_dataset(num_batches=20):
#     """Generate full instruction dataset"""
#     all_samples = []
#     failed_batches = []
#     working_model = None

#     print(f"\n🚀 Generating {num_batches} batches of global PII masking samples...\n")

#     for i in tqdm(range(num_batches), desc="Batches"):
#         samples, model_used = generate_dataset_batch()
        
#         if working_model is None and model_used:
#             working_model = model_used
#             print(f"\n✓ Working model: {working_model}\n")
        
#         if samples:
#             all_samples.extend(samples)
#             print(f"   ✓ Batch {i+1}/{num_batches}: {len(samples)} samples")
#         else:
#             failed_batches.append(i+1)
#             print(f"   ✗ Batch {i+1}/{num_batches}: Failed")
        
#         time.sleep(3)

#     # Convert to instruction format
#     if all_samples:
#         instruction_samples = create_instruction_dataset(all_samples)
#         df = pd.DataFrame(instruction_samples)
#     else:
#         df = pd.DataFrame()
    
#     print(f"\n{'='*60}")
#     print(f"🎉 Generation Complete!")
#     print(f"{'='*60}")
#     print(f"Total samples: {len(df)}")
#     print(f"Failed batches: {len(failed_batches)}")
    
#     if not df.empty:
#         print(f"\n📊 Categories: {len(df['masking_category'].unique())} types")
#         print(f"🌍 Regions: {list(df['region'].unique())}")
#         print(f"🔒 Sensitivity Levels: {dict(df['sensitivity_level'].value_counts())}")
    
#     return df, failed_batches


# # ============================================================================
# # MAIN
# # ============================================================================
# if __name__ == "__main__":
#     print("="*60)
#     print("🌍 Global PII Data Masking Dataset - INSTRUCTION FORMAT")
#     print("="*60)
    
#     df_masking, failed = create_full_dataset(num_batches=30)  # ~1500 samples for comprehensive coverage

#     if not df_masking.empty:
#         print("\n" + "="*60)
#         print("💾 Processing and Saving")
#         print("="*60)
        
#         # Remove duplicates
#         df_clean = df_masking.drop_duplicates(subset=['original_text'], keep='first')
#         print(f"\n🧹 Removed {len(df_masking) - len(df_clean)} duplicates")
#         print(f"📦 Final: {len(df_clean)} samples")
        
#         # 1. Full instruction CSV
#         df_clean.to_csv('global_pii_masking_dataset2.csv', index=False)
#         print(f"\n✅ CSV: global_pii_masking_dataset2.csv")
        
#         # 2. Excel
#         df_clean.to_excel('global_pii_masking_dataset2.xlsx', index=False)
#         print(f"✅ Excel: global_pii_masking_dataset2.xlsx")
        
#         # 3. JSON with all fields
#         json_data = df_clean.to_dict('records')
#         with open('global_pii_masking_full2.json', 'w', encoding='utf-8') as f:
#             json.dump(json_data, f, indent=2, ensure_ascii=False)
#         print(f"✅ Full JSON: global_pii_masking_full2.json")
        
#         # 4. UNSLOTH FORMAT - Conversations structure
#         conversations_data = []
#         for _, row in df_clean.iterrows():
#             conversations_data.append({
#                 "conversations": [
#                     {"role": "system", "content": row['system']},
#                     {"role": "user", "content": row['user']},
#                     {"role": "assistant", "content": row['assistant']}
#                 ]
#             })
        
#         with open('global_pii_unsloth_format2.json', 'w', encoding='utf-8') as f:
#             json.dump(conversations_data, f, indent=2, ensure_ascii=False)
#         print(f"✅ Unsloth Format: global_pii_unsloth_format2.json")
        
#         # Statistics
#         print("\n" + "="*60)
#         print("📈 Dataset Statistics")
#         print("="*60)
        
#         # Category breakdown
#         print("\n📂 Masking Categories:")
#         for cat, count in df_clean['masking_category'].value_counts().head(15).items():
#             print(f"   • {cat}: {count}")
        
#         # Regional breakdown
#         print("\n🌍 Regional Distribution:")
#         for region, count in df_clean['region'].value_counts().items():
#             print(f"   • {region}: {count}")
        
#         # Sensitivity breakdown
#         print("\n🔒 Sensitivity Levels:")
#         for level, count in df_clean['sensitivity_level'].value_counts().items():
#             print(f"   • {level.upper()}: {count} ({count/len(df_clean)*100:.1f}%)")
        
#         # Show examples
#         print("\n" + "="*60)
#         print("💡 Global PII Masking Examples")
#         print("="*60)
        
#         # Show Indian example
#         indian_samples = df_clean[df_clean['region'] == 'India']
#         if not indian_samples.empty:
#             print(f"\n{'─'*60}")
#             print("INDIAN PII Example:")
#             print(f"{'─'*60}")
            
#             sample = indian_samples.iloc[0]
            
#             print(f"\n🔹 ORIGINAL:")
#             print(f"{sample['original_text']}")
            
#             print(f"\n🔹 MASKED:")
#             print(f"{sample['masked_text']}")
            
#             print(f"\n🔹 ENTITIES DETECTED:")
#             for entity in sample['entities_found'][:5]:
#                 print(f"   • {entity}")
            
#             print(f"\n🔹 SENSITIVITY: {sample['sensitivity_level'].upper()}")
        
#         # Show International example
#         intl_samples = df_clean[df_clean['region'] != 'India']
#         if not intl_samples.empty:
#             print(f"\n{'─'*60}")
#             print("INTERNATIONAL PII Example:")
#             print(f"{'─'*60}")
            
#             sample = intl_samples.iloc[0]
            
#             print(f"\n🔹 ORIGINAL:")
#             print(f"{sample['original_text']}")
            
#             print(f"\n🔹 MASKED:")
#             print(f"{sample['masked_text']}")
            
#             print(f"\n🔹 ENTITIES DETECTED:")
#             for entity in sample['entities_found'][:5]:
#                 print(f"   • {entity}")
        
#         print("\n" + "="*60)
#         print("✨ Global PII Dataset Ready for Fine-tuning!")
#         print("="*60)
        
#         print("\n📝 Usage:")
#         print("1. Review data: global_pii_masking_dataset.xlsx")
#         print("2. Load for Unsloth:")
#         print("   from datasets import load_dataset")
#         print("   dataset = load_dataset('json', data_files='global_pii_unsloth_format2.json')")
#         print("\n3. Fine-tune your LLM to mask global PII including:")
#         print("   ✓ Indian: Aadhar, PAN, UPI, Indian names (all regions/religions)")
#         print("   ✓ Medical: Blood groups, UHID, medications, biometrics")
#         print("   ✓ Financial: Cards, accounts, IFSC, crypto wallets")
#         print("   ✓ Global: SSN, passports, international phone/addresses")
#         print("   ✓ All sensitive data types across cultures!")
        
#     else:
#         print("\n❌ No data generated!")
#         print("\n🔍 Troubleshooting:")
#         print("  1. API key valid?")
#         print("  2. Internet working?")
#         print("  3. API quota available?")
#         print("  4. Try num_batches=5 for testing")




# -*- coding: utf-8 -*-
"""
data_masking_dataset_generation.py

Global Privacy & Data Masking Dataset - INSTRUCTION FINE-TUNING FORMAT
For training a model to identify and mask sensitive information worldwide

NOTE:
- Set your Gemini API key in the environment variable GEMINI_API_KEY before running:
    export GEMINI_API_KEY="your_key_here"
"""

import os
import pandas as pd
from tqdm import tqdm
import json
import google.generativeai as genai
import time

# ============================================================================ 
# CONFIGURATION
# ============================================================================ 
GEMINI_API_KEY = "AIzaSyDTj_kgyBtBdb91R1AnJYfvyPNrvOEPFmw"
genai.configure(api_key=GEMINI_API_KEY)

# ============================================================================ 
# GLOBAL DATA MASKING INSTRUCTION FINE-TUNING PROMPT
# ============================================================================ 
prompt = """Generate 50 text samples with sensitive global PII data that needs to be masked for privacy protection.

Important masking rule (apply globally):
- MASK **ALL personal names** (from any country, language, or script) using the token [NAME].
  This includes single names, multi-part names, names with titles (Dr., Mr., Ms., Prof.), names with non-Latin scripts, initials, and honorifics. Do NOT use region-specific name tokens for any person — use [NAME] for all human names.

Return ONLY valid JSON (no markdown, no code blocks):
{
  "samples": [
    {
      "original_text": "My name is Rajesh Kumar and my Aadhar is 1234-5678-9012. PAN: ABCDE1234F",
      "masked_text": "[NAME] and my Aadhar is [AADHAR_NUMBER]. PAN: [PAN_NUMBER]",
      "entities_found": ["NAME: Rajesh Kumar", "AADHAR_NUMBER: 1234-5678-9012", "PAN_NUMBER: ABCDE1234F"],
      "masking_category": "indian_government_ids",
      "sensitivity_level": "critical",
      "region": "India"
    }
  ]
}

Generate diverse samples across ALL these categories (50 samples total). For names in every category, replace with [NAME] in masked_text and list original in entities_found.

1. INDIAN_GOVERNMENT_IDS (8 samples):
   - Aadhar numbers (12 digits, format: XXXX-XXXX-XXXX)
   - PAN card (format: ABCDE1234F)
   - Voter ID, Driving License (DL), Ration Card
   - Passport numbers (Indian format)
   - GST numbers, TAN, CIN
   Examples: "Aadhar: 2345-6789-0123, PAN: DEFGH5678K, DL: MH01-20230012345"

2. INTERNATIONAL_IDS (6 samples):
   - US: SSN (123-45-6789), Driver's License
   - UK: National Insurance Number (NI), NHS Number
   - EU: Tax IDs, Passport numbers
   - China: Resident Identity Card
   - Middle East: Emirates ID, Iqama
   Examples: "SSN: 987-65-4321, NI Number: AB123456C, Emirates ID: 784-1234-5678901-2"

3. INDIAN_NAMES_DIVERSE (6 samples):
   - Include Hindu, Muslim, Sikh, Christian, and regional Indian names.
   Examples: "Patient Venkatesh Subramanian", "Dr. Zainab Ahmed"
   NOTE: In masked_text use [NAME] (e.g., "Patient [NAME]")

4. GLOBAL_NAMES_DIVERSE (5 samples):
   - East Asian, European, African, Latin American, Arabic names, etc.
   Examples: "Employee 张伟 (Zhang Wei)", "Customer João Pedro Santos"
   NOTE: In masked_text use [NAME] (e.g., "Employee [NAME]")

5. CONTACT_INFORMATION_GLOBAL (7 samples):
   - Indian phones, international phones, addresses, emails.
   Examples: "Call +91-98765-43210 or email priya.sharma@company.co.in"

6. FINANCIAL_DATA_GLOBAL (6 samples):
   - UPI IDs, IFSC, bank accounts, card numbers, IBAN, SWIFT, crypto addresses.

7. MEDICAL_HEALTH_DATA (6 samples):
   - Blood groups, UHID, medical conditions, medications, biometrics.

8. AUTHENTICATION_CREDENTIALS (4 samples):
   - Passwords, API keys (mask with [API_KEY]), JWT tokens, SSH keys (mask with [TOKEN] or [PRIVATE_KEY]).

9. BIOMETRIC_DATA (3 samples):
   - Fingerprint IDs, facial recognition data, DNA sequences.

10. VEHICLE_PROPERTY_DATA (3 samples):
    - Vehicle registration numbers, chassis numbers, property survey numbers.

11. EMPLOYMENT_EDUCATION_DATA (3 samples):
    - Employee IDs, salaries, student IDs, professional registration numbers.

12. DATES_TEMPORAL_DATA (3 samples):
    - DOBs, timestamps, appointment dates, ages.

Requirements:
- Use realistic data from India and globally (names, phone formats, addresses).
- Include multiple languages/scripts (Hindi, Chinese, Arabic, etc.) where relevant.
- Mix contexts: forms, emails, chat logs, medical records, government documents.
- Vary text complexity: 1-5 sentences per sample.
- Include compound cases: multiple PII types in one text.
- Regional variations should be present (e.g., US, UK, India, China, UAE).
- Specify region/country when relevant.
- Use sensitivity levels: "low", "medium", "high", "critical".

MASK TOKENS TO USE (use [NAME] for ALL names):
[NAME], [AADHAR_NUMBER], [PAN_NUMBER], [VOTER_ID], [DRIVING_LICENSE], [PASSPORT], [SSN], [NI_NUMBER], [PHONE], [INDIAN_PHONE], [EMAIL], [ADDRESS], [INDIAN_ADDRESS], [UPI_ID], [IFSC], [ACCOUNT_NUMBER], [CARD_NUMBER], [IBAN], [BLOOD_GROUP], [UHID], [MEDICAL_CONDITION], [MEDICATION], [BIOMETRIC_ID], [VEHICLE_NUMBER], [PROPERTY_ID], [EMPLOYEE_ID], [SALARY], [STUDENT_ID], [DATE_OF_BIRTH], [AGE], [PASSWORD], [API_KEY], [TOKEN], [DNA_SEQUENCE]

Generate 50 diverse, realistic samples covering global PII with emphasis on Indian data. Ensure that **every human personal name** in the `masked_text` is replaced with `[NAME]` and that the `entities_found` lists the original name prefixed with `NAME:` (e.g., `NAME: Rajesh Kumar`).
"""

def generate_dataset_batch():
    """Generate data masking batch"""
    model_names = ['gemini-2.0-flash']
    
    generation_config = {
        'temperature': 0.95,
        'top_p': 0.95,
        'top_k': 40,
        'max_output_tokens': 8192,
    }

    for model_name in model_names:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt, generation_config=generation_config)
            
            content = response.text.strip()
            
            # Clean markdown if present
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            # Extract JSON body
            start = content.find('{')
            end = content.rfind('}')
            if start != -1 and end != -1:
                content = content[start:end+1]
            
            data = json.loads(content)
            samples = data.get('samples', [])
            
            if samples and len(samples) > 0:
                return samples, model_name
                
        except Exception as e:
            print(f"   ✗ {model_name}: {str(e)[:200]}")
            continue
    
    return None, None


def create_instruction_dataset(samples):
    """Convert to instruction fine-tuning format"""
    instruction_data = []
    
    system_prompt = """You are a global data privacy expert specialized in identifying and masking sensitive PII (Personally Identifiable Information) from multiple countries and regions. Your job is to:

1. Identify ALL sensitive entities including:
   - Government and national IDs (Aadhar, PAN, SSN, NI, Emirates ID, etc.)
   - ALL human names (replace every detected person name with [NAME])
   - Contact: Phone numbers (Indian/International), emails, addresses (with regional formats)
   - Financial: UPI IDs, IFSC, bank accounts, cards (Visa/Mastercard/RuPay), IBAN, crypto wallets
   - Medical: Blood groups, medical record numbers, conditions, medications, biometrics
   - Government: Vehicle registration, property IDs, professional licenses
   - Employment/Education: Employee IDs, salaries, student IDs, marks
   - Dates: DOB, ages, timestamps
   - Credentials: Passwords, API keys, tokens

2. Replace with appropriate mask tokens: [NAME] for ALL names, [AADHAR_NUMBER], [PAN_NUMBER], [PHONE], [UPI_ID], [BLOOD_GROUP], [VEHICLE_NUMBER], etc.

3. List all entities found with original values (prefix human names with 'NAME: ').

4. Specify category, sensitivity level, and region.

Always prioritize user privacy across all cultures and regions."""

    for sample in samples:
        # Create entities list as formatted string
        entities_list = sample.get('entities_found', [])
        entities_str = "\n".join([f"  - {entity}" for entity in entities_list])
        
        region_info = f"\nRegion: {sample.get('region', 'Global')}" if 'region' in sample else ""
        
        instruction_data.append({
            "system": system_prompt,
            "user": f"Mask all sensitive PII in this text (use [NAME] for all human personal names):\n\n\"{sample['original_text']}\"",
            "assistant": f"Masked Text:\n{sample['masked_text']}\n\nEntities Found:\n{entities_str}\n\nCategory: {sample['masking_category']}\nSensitivity Level: {sample['sensitivity_level'].upper()}{region_info}",
            "original_text": sample['original_text'],
            "masked_text": sample['masked_text'],
            "entities_found": sample['entities_found'],
            "masking_category": sample['masking_category'],
            "sensitivity_level": sample['sensitivity_level'],
            "region": sample.get('region', 'Global')
        })
    
    return instruction_data


def create_full_dataset(num_batches=20):
    """Generate full instruction dataset"""
    all_samples = []
    failed_batches = []
    working_model = None

    print(f"\n🚀 Generating {num_batches} batches of global PII masking samples...\n")

    for i in tqdm(range(num_batches), desc="Batches"):
        samples, model_used = generate_dataset_batch()
        
        if working_model is None and model_used:
            working_model = model_used
            print(f"\n✓ Working model: {working_model}\n")
        
        if samples:
            all_samples.extend(samples)
            print(f"   ✓ Batch {i+1}/{num_batches}: {len(samples)} samples")
        else:
            failed_batches.append(i+1)
            print(f"   ✗ Batch {i+1}/{num_batches}: Failed")
        
        time.sleep(3)

    # Convert to instruction format
    if all_samples:
        instruction_samples = create_instruction_dataset(all_samples)
        df = pd.DataFrame(instruction_samples)
    else:
        df = pd.DataFrame()
    
    print(f"\n{'='*60}")
    print(f"🎉 Generation Complete!")
    print(f"{'='*60}")
    print(f"Total samples: {len(df)}")
    print(f"Failed batches: {len(failed_batches)}")
    
    if not df.empty:
        print(f"\n📊 Categories: {len(df['masking_category'].unique())} types")
        print(f"🌍 Regions: {list(df['region'].unique())}")
        print(f"🔒 Sensitivity Levels: {dict(df['sensitivity_level'].value_counts())}")
    
    return df, failed_batches


# ============================================================================ 
# MAIN
# ============================================================================ 
if __name__ == "__main__":
    print("="*60)
    print("🌍 Global PII Data Masking Dataset - INSTRUCTION FORMAT")
    print("="*60)
    
    df_masking, failed = create_full_dataset(num_batches=30)  # ~1500 samples for comprehensive coverage

    if not df_masking.empty:
        print("\n" + "="*60)
        print("💾 Processing and Saving")
        print("="*60)
        
        # Remove duplicates
        df_clean = df_masking.drop_duplicates(subset=['original_text'], keep='first')
        print(f"\n🧹 Removed {len(df_masking) - len(df_clean)} duplicates")
        print(f"📦 Final: {len(df_clean)} samples")
        
        # 1. Full instruction CSV
        df_clean.to_csv('global_pii_masking_dataset3.csv', index=False)
        print(f"\n✅ CSV: global_pii_masking_dataset3.csv")
        
        # 2. Excel
        df_clean.to_excel('global_pii_masking_dataset3.xlsx', index=False)
        print(f"✅ Excel: global_pii_masking_dataset3.xlsx")
        
        # 3. JSON with all fields
        json_data = df_clean.to_dict('records')
        with open('global_pii_masking_full3.json', 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Full JSON: global_pii_masking_full3.json")
        
        # 4. UNSLOTH FORMAT - Conversations structure
        conversations_data = []
        for _, row in df_clean.iterrows():
            conversations_data.append({
                "conversations": [
                    {"role": "system", "content": row['system']},
                    {"role": "user", "content": row['user']},
                    {"role": "assistant", "content": row['assistant']}
                ]
            })
        
        with open('global_pii_unsloth_format3.json', 'w', encoding='utf-8') as f:
            json.dump(conversations_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Unsloth Format: global_pii_unsloth_format3.json")
        
        # Statistics
        print("\n" + "="*60)
        print("📈 Dataset Statistics")
        print("="*60)
        
        # Category breakdown
        print("\n📂 Masking Categories:")
        for cat, count in df_clean['masking_category'].value_counts().head(15).items():
            print(f"   • {cat}: {count}")
        
        # Regional breakdown
        print("\n🌍 Regional Distribution:")
        for region, count in df_clean['region'].value_counts().items():
            print(f"   • {region}: {count}")
        
        # Sensitivity breakdown
        print("\n🔒 Sensitivity Levels:")
        for level, count in df_clean['sensitivity_level'].value_counts().items():
            print(f"   • {level.upper()}: {count} ({count/len(df_clean)*100:.1f}%)")
        
        # Show examples
        print("\n" + "="*60)
        print("💡 Global PII Masking Examples")
        print("="*60)
        
        # Show Indian example
        indian_samples = df_clean[df_clean['region'] == 'India']
        if not indian_samples.empty:
            print(f"\n{'─'*60}")
            print("INDIAN PII Example:")
            print(f"{'─'*60}")
            
            sample = indian_samples.iloc[0]
            
            print(f"\n🔹 ORIGINAL:")
            print(f"{sample['original_text']}")
            
            print(f"\n🔹 MASKED:")
            print(f"{sample['masked_text']}")
            
            print(f"\n🔹 ENTITIES DETECTED:")
            for entity in sample['entities_found'][:5]:
                print(f"   • {entity}")
            
            print(f"\n🔹 SENSITIVITY: {sample['sensitivity_level'].upper()}")
        
        # Show International example
        intl_samples = df_clean[df_clean['region'] != 'India']
        if not intl_samples.empty:
            print(f"\n{'─'*60}")
            print("INTERNATIONAL PII Example:")
            print(f"{'─'*60}")
            
            sample = intl_samples.iloc[0]
            
            print(f"\n🔹 ORIGINAL:")
            print(f"{sample['original_text']}")
            
            print(f"\n🔹 MASKED:")
            print(f"{sample['masked_text']}")
            
            print(f"\n🔹 ENTITIES DETECTED:")
            for entity in sample['entities_found'][:5]:
                print(f"   • {entity}")
        
        print("\n" + "="*60)
        print("✨ Global PII Dataset Ready for Fine-tuning!")
        print("="*60)
        
        print("\n📝 Usage:")
        print("1. Review data: global_pii_masking_dataset.xlsx")
        print("2. Load for Unsloth:")
        print("   from datasets import load_dataset")
        print("   dataset = load_dataset('json', data_files='global_pii_unsloth_format2.json')")
        print("\n3. Fine-tune your LLM to mask global PII including:")
        print("   ✓ ALL human NAMES converted to [NAME]")
        print("   ✓ Indian: Aadhar, PAN, UPI, Indian names (all regions/religions)")
        print("   ✓ Medical: Blood groups, UHID, medications, biometrics")
        print("   ✓ Financial: Cards, accounts, IFSC, crypto wallets")
        print("   ✓ Global: SSN, passports, international phone/addresses")
        print("   ✓ All sensitive data types across cultures!")
        
    else:
        print("\n❌ No data generated!")
        print("\n🔍 Troubleshooting:")
        print("  1. Is GEMINI_API_KEY set in your environment?")
        print("  2. Internet working?")
        print("  3. API quota available?")
        print("  4. Try num_batches=5 for testing")
