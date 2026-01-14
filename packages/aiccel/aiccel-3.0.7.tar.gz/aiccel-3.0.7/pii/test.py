"""
pii_token_classification_dataset.py

GLOBALLY DIVERSE Privacy & Data Masking Dataset - TOKEN CLASSIFICATION FORMAT
For training transformer models to identify PII from ALL countries and cultures

NOTE:
- Set your Gemini API key before running:
    export GEMINI_API_KEY="your_key_here"
"""

import os
import pandas as pd
from tqdm import tqdm
import json
import google.generativeai as genai
import time
import re

# ============================================================================ 
# CONFIGURATION
# ============================================================================ 
GEMINI_API_KEY = "AIzaSyDTj_kgyBtBdb91R1AnJYfvyPNrvOEPFmw"
genai.configure(api_key=GEMINI_API_KEY)

# ============================================================================ 
# TOKEN CLASSIFICATION LABELS (BIO FORMAT)
# ============================================================================ 
LABELS = [
    "O",  # Outside (no PII)
    "B-PERSON", "I-PERSON",
    "B-AADHAR", "I-AADHAR",
    "B-PAN", "I-PAN",
    "B-VOTER_ID", "I-VOTER_ID",
    "B-DRIVING_LICENSE", "I-DRIVING_LICENSE",
    "B-PASSPORT", "I-PASSPORT",
    "B-SSN", "I-SSN",
    "B-NI_NUMBER", "I-NI_NUMBER",
    "B-NHS_NUMBER", "I-NHS_NUMBER",
    "B-SIN", "I-SIN",  # Canada
    "B-TFN", "I-TFN",  # Australia Tax File Number
    "B-CPF", "I-CPF",  # Brazil CPF
    "B-CURP", "I-CURP",  # Mexico
    "B-RFC", "I-RFC",  # Mexico Tax ID
    "B-CHINESE_ID", "I-CHINESE_ID",
    "B-EMIRATES_ID", "I-EMIRATES_ID",
    "B-IQAMA", "I-IQAMA",  # Saudi Arabia
    "B-NRIC", "I-NRIC",  # Singapore
    "B-JUMIN_NUMBER", "I-JUMIN_NUMBER",  # South Korea
    "B-PHONE", "I-PHONE",
    "B-EMAIL", "I-EMAIL",
    "B-ADDRESS", "I-ADDRESS",
    "B-UPI_ID", "I-UPI_ID",
    "B-IFSC", "I-IFSC",
    "B-ACCOUNT_NUMBER", "I-ACCOUNT_NUMBER",
    "B-CARD_NUMBER", "I-CARD_NUMBER",
    "B-IBAN", "I-IBAN",
    "B-SWIFT", "I-SWIFT",
    "B-SORT_CODE", "I-SORT_CODE",  # UK
    "B-ROUTING_NUMBER", "I-ROUTING_NUMBER",  # US
    "B-BLOOD_GROUP", "I-BLOOD_GROUP",
    "B-UHID", "I-UHID",
    "B-MEDICAL_CONDITION", "I-MEDICAL_CONDITION",
    "B-MEDICATION", "I-MEDICATION",
    "B-BIOMETRIC_ID", "I-BIOMETRIC_ID",
    "B-VEHICLE_NUMBER", "I-VEHICLE_NUMBER",
    "B-PROPERTY_ID", "I-PROPERTY_ID",
    "B-EMPLOYEE_ID", "I-EMPLOYEE_ID",
    "B-SALARY", "I-SALARY",
    "B-STUDENT_ID", "I-STUDENT_ID",
    "B-DATE_OF_BIRTH", "I-DATE_OF_BIRTH",
    "B-AGE", "I-AGE",
    "B-PASSWORD", "I-PASSWORD",
    "B-API_KEY", "I-API_KEY",
    "B-TOKEN", "I-TOKEN",
    "B-DNA_SEQUENCE", "I-DNA_SEQUENCE",
    "B-GST", "I-GST",
    "B-VAT", "I-VAT",  # European VAT
    "B-TAX_ID", "I-TAX_ID",
]

# ============================================================================ 
# GLOBALLY DIVERSE DATASET GENERATION PROMPT
# ============================================================================ 
prompt = """Generate 30 GLOBALLY DIVERSE text samples with PII data from multiple countries for token classification training.

CRITICAL INSTRUCTIONS:
1. Return ONLY valid, parseable JSON
2. NO trailing commas in arrays or objects
3. Properly escape all special characters in strings
4. Close all brackets and braces correctly

Return in this EXACT format:
{
  "samples": [
    {
      "text": "My name is Rajesh Kumar and my Aadhar is 1234-5678-9012.",
      "tokens": ["My", "name", "is", "Rajesh", "Kumar", "and", "my", "Aadhar", "is", "1234-5678-9012", "."],
      "labels": ["O", "O", "O", "B-PERSON", "I-PERSON", "O", "O", "O", "O", "B-AADHAR", "O"],
      "entities": [
        {"text": "Rajesh Kumar", "label": "PERSON", "start_idx": 3, "end_idx": 4},
        {"text": "1234-5678-9012", "label": "AADHAR", "start_idx": 9, "end_idx": 9}
      ],
      "category": "indian_government_ids",
      "sensitivity": "critical",
      "region": "India",
      "language": "English"
    }
  ]
}

BIO TAGGING RULES:
- B-LABEL: Beginning of entity
- I-LABEL: Inside/continuation of entity
- O: Outside (not PII)

ENTITY LABELS:
PERSON, AADHAR, PAN, SSN, NI_NUMBER, CHINESE_ID, EMIRATES_ID, CPF, CURP, SIN, TFN, NRIC, JUMIN_NUMBER, PHONE, EMAIL, ADDRESS, UPI_ID, IFSC, ACCOUNT_NUMBER, CARD_NUMBER, IBAN, PASSPORT, DRIVING_LICENSE, VOTER_ID, BLOOD_GROUP, UHID, MEDICAL_CONDITION, MEDICATION, VEHICLE_NUMBER, EMPLOYEE_ID, SALARY, STUDENT_ID, DATE_OF_BIRTH, AGE, GST, VAT, TAX_ID

Generate 30 samples with MAXIMUM DIVERSITY:

REGIONS TO COVER (distribute samples):
- India (5 samples): Diverse Indian names, Aadhar, PAN, UPI, GST
- USA (4 samples): American names, SSN, US addresses, +1 phones
- UK (3 samples): British names, NI Number, NHS Number, UK postcodes
- China (3 samples): Chinese names, 18-digit ID, +86 phones
- Brazil (2 samples): Portuguese names, CPF format, Brazilian addresses
- Mexico (2 samples): Spanish names, CURP, RFC
- UAE/Saudi (2 samples): Arabic names, Emirates ID, Iqama
- Canada (2 samples): Canadian names, SIN
- Australia (2 samples): Australian names, TFN
- Europe (3 samples): German/French/Spanish names, IBAN, VAT
- Others (2 samples): Singapore NRIC, Korean Jumin, African IDs

DIVERSITY REQUIREMENTS:
✓ Mix Hindu, Muslim, Christian, Sikh names for India
✓ Include non-English names (Chinese, Arabic, Spanish, Portuguese)
✓ Use correct phone formats: +91, +1, +44, +86, +971, +55, +52, +61
✓ Realistic address formats for each country
✓ Authentic ID number formats
✓ 1-3 sentences per sample
✓ Mix contexts: forms, emails, medical, business

CRITICAL: Ensure valid JSON syntax with no trailing commas!
"""

def fix_json(json_str):
    """Attempt to fix common JSON issues"""
    # Remove trailing commas before closing brackets/braces
    json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
    
    # Fix common escape issues
    json_str = json_str.replace('\n', ' ').replace('\r', ' ')
    
    # Remove any text before first { and after last }
    start = json_str.find('{')
    end = json_str.rfind('}')
    if start != -1 and end != -1:
        json_str = json_str[start:end+1]
    
    return json_str


def generate_dataset_batch():
    """Generate globally diverse token classification batch"""
    model_names = ['gemini-2.0-flash', 'gemini-2.0-flash']
    
    generation_config = {
        'temperature': 0.7,  
        'top_p': 0.9,
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
            
            # Fix common JSON issues
            content = fix_json(content)
            
            # Try to parse
            try:
                data = json.loads(content)
            except json.JSONDecodeError as e:
                # Try more aggressive fixing
                print(f"      JSON parse error at position {e.pos}, attempting fix...")
                
                # Try to find and extract just the samples array
                samples_match = re.search(r'"samples"\s*:\s*\[(.*)\]', content, re.DOTALL)
                if samples_match:
                    samples_str = samples_match.group(1)
                    # Try to parse individual samples
                    samples = []
                    # This is a fallback - skip this batch
                    raise e
                else:
                    raise e
            
            samples = data.get('samples', [])
            
            # Validate samples
            valid_samples = []
            for sample in samples:
                if validate_sample(sample):
                    valid_samples.append(sample)
            
            if valid_samples and len(valid_samples) >= 10:  # Accept if at least 10 valid samples
                print(f"   ✓ {model_name}: {len(valid_samples)} valid samples")
                return valid_samples, model_name
            elif valid_samples:
                print(f"   ⚠ {model_name}: Only {len(valid_samples)} valid samples (need 10+), retrying...")
                
        except json.JSONDecodeError as e:
            print(f"   ✗ {model_name}: JSON error at position {e.pos}")
            continue
        except Exception as e:
            print(f"   ✗ {model_name}: {str(e)[:100]}")
            continue
    
    return None, None


def validate_sample(sample):
    """Validate that sample has correct format"""
    try:
        # Check required fields
        required_fields = ['text', 'tokens', 'labels', 'entities', 'category', 'sensitivity', 'region']
        for field in required_fields:
            if field not in sample:
                return False
        
        tokens = sample.get('tokens', [])
        labels = sample.get('labels', [])
        
        if not tokens or not labels:
            return False
        
        if len(tokens) != len(labels):
            return False
        
        # Check all labels are valid
        valid_entities = [
            "PERSON", "AADHAR", "PAN", "VOTER_ID", "DRIVING_LICENSE", "PASSPORT", 
            "SSN", "NI_NUMBER", "NHS_NUMBER", "SIN", "TFN", "CPF", "CURP", "RFC",
            "CHINESE_ID", "EMIRATES_ID", "IQAMA", "NRIC", "JUMIN_NUMBER",
            "PHONE", "EMAIL", "ADDRESS", "UPI_ID", "IFSC", "ACCOUNT_NUMBER", 
            "CARD_NUMBER", "IBAN", "SWIFT", "SORT_CODE", "ROUTING_NUMBER",
            "BLOOD_GROUP", "UHID", "MEDICAL_CONDITION", "MEDICATION",
            "BIOMETRIC_ID", "VEHICLE_NUMBER", "PROPERTY_ID", "EMPLOYEE_ID",
            "SALARY", "STUDENT_ID", "DATE_OF_BIRTH", "AGE", "PASSWORD",
            "API_KEY", "TOKEN", "DNA_SEQUENCE", "GST", "VAT", "TAX_ID"
        ]
        
        for label in labels:
            if label != "O":
                is_valid = False
                for entity in valid_entities:
                    if label == f"B-{entity}" or label == f"I-{entity}":
                        is_valid = True
                        break
                if not is_valid:
                    return False
        
        return True
    except Exception as e:
        return False


def create_full_dataset(num_batches=50):
    """Generate full globally diverse token classification dataset"""
    all_samples = []
    failed_batches = []
    working_model = None

    print(f"\n🌍 Generating {num_batches} batches of GLOBALLY DIVERSE PII data...\n")
    print("Note: Each batch generates 30 samples, aiming for 1500+ total samples\n")

    for i in tqdm(range(num_batches), desc="Batches"):
        max_retries = 3
        success = False
        
        for retry in range(max_retries):
            samples, model_used = generate_dataset_batch()
            
            if working_model is None and model_used:
                working_model = model_used
                print(f"\n✓ Working model: {working_model}\n")
            
            if samples:
                all_samples.extend(samples)
                print(f"   ✓ Batch {i+1}/{num_batches}: {len(samples)} samples (Total: {len(all_samples)})")
                success = True
                break
            else:
                if retry < max_retries - 1:
                    print(f"   ⟳ Retry {retry + 1}/{max_retries} for batch {i+1}")
                    time.sleep(2)
        
        if not success:
            failed_batches.append(i+1)
            print(f"   ✗ Batch {i+1}/{num_batches}: Failed after {max_retries} retries")
        
        time.sleep(2)  # Shorter delay between batches

    # Create DataFrame
    if all_samples:
        df = pd.DataFrame(all_samples)
    else:
        df = pd.DataFrame()
    
    print(f"\n{'='*60}")
    print(f"🎉 Generation Complete!")
    print(f"{'='*60}")
    print(f"Total samples generated: {len(all_samples)}")
    print(f"Failed batches: {len(failed_batches)}")
    
    if not df.empty:
        print(f"\n📊 Unique categories: {len(df['category'].unique())}")
        print(f"🌍 Regions covered: {len(df['region'].unique())}")
        print(f"   Regions: {', '.join(df['region'].unique()[:10])}")
        if 'language' in df.columns:
            print(f"🗣️  Languages: {', '.join(df['language'].unique()[:10])}")
    
    return df, failed_batches


def save_in_multiple_formats(df):
    """Save dataset in various formats for training"""
    
    print("\n" + "="*60)
    print("💾 Saving in Multiple Formats")
    print("="*60)
    
    # 1. Full CSV with all fields
    df.to_csv('pii_global_token_classification_full.csv', index=False)
    print(f"\n✅ Full CSV: pii_global_token_classification_full.csv")
    
    # 2. Excel
    df.to_excel('pii_global_token_classification_full.xlsx', index=False)
    print(f"✅ Excel: pii_global_token_classification_full.xlsx")
    
    # 3. JSON format (standard)
    json_data = df.to_dict('records')
    with open('pii_global_token_classification_full.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Full JSON: pii_global_token_classification_full.json")
    
    # 4. Simple training format (tokens + labels only)
    simple_format = []
    for _, row in df.iterrows():
        simple_format.append({
            "tokens": row['tokens'],
            "labels": row['labels']
        })
    
    with open('pii_global_simple.json', 'w', encoding='utf-8') as f:
        json.dump(simple_format, f, indent=2, ensure_ascii=False)
    print(f"✅ Simple Format: pii_global_simple.json")
    
    # 5. CoNLL format (standard NER format)
    with open('pii_global.conll', 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            for token, label in zip(row['tokens'], row['labels']):
                f.write(f"{token}\t{label}\n")
            f.write("\n")  # Empty line between samples
    print(f"✅ CoNLL Format: pii_global.conll")
    
    # 6. HuggingFace Datasets compatible format
    hf_format = []
    for _, row in df.iterrows():
        hf_format.append({
            "id": str(len(hf_format)),
            "tokens": row['tokens'],
            "ner_tags": row['labels'],
            "metadata": {
                "text": row['text'],
                "category": row['category'],
                "sensitivity": row['sensitivity'],
                "region": row['region'],
                "language": row.get('language', 'English')
            }
        })
    
    with open('pii_global_hf.json', 'w', encoding='utf-8') as f:
        json.dump(hf_format, f, indent=2, ensure_ascii=False)
    print(f"✅ HuggingFace Format: pii_global_hf.json")
    
    # 7. Split into train/val/test (80/10/10)
    train_size = int(0.8 * len(simple_format))
    val_size = int(0.1 * len(simple_format))
    
    train_data = simple_format[:train_size]
    val_data = simple_format[train_size:train_size + val_size]
    test_data = simple_format[train_size + val_size:]
    
    with open('pii_global_train.json', 'w', encoding='utf-8') as f:
        json.dump(train_data, f, indent=2, ensure_ascii=False)
    
    with open('pii_global_val.json', 'w', encoding='utf-8') as f:
        json.dump(val_data, f, indent=2, ensure_ascii=False)
    
    with open('pii_global_test.json', 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Train/Val/Test Split:")
    print(f"   • pii_global_train.json: {len(train_data)} samples")
    print(f"   • pii_global_val.json: {len(val_data)} samples")
    print(f"   • pii_global_test.json: {len(test_data)} samples")


def analyze_diversity(df):
    """Analyze and display diversity metrics"""
    print("\n" + "="*60)
    print("🌍 GLOBAL DIVERSITY ANALYSIS")
    print("="*60)
    
    # Regional distribution
    print("\n🗺️  Regional Distribution:")
    region_counts = df['region'].value_counts()
    for region, count in region_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   • {region:20s}: {count:4d} samples ({percentage:.1f}%)")
    
    # Language distribution
    if 'language' in df.columns:
        print("\n🗣️  Language Distribution:")
        lang_counts = df['language'].value_counts()
        for lang, count in lang_counts.head(10).items():
            percentage = (count / len(df)) * 100
            print(f"   • {lang:20s}: {count:4d} samples ({percentage:.1f}%)")
    
    # Entity type distribution
    print("\n🏷️  Top 20 Entity Types:")
    all_entities = []
    for entities_list in df['entities']:
        for entity in entities_list:
            all_entities.append(entity['label'])
    
    entity_counts = pd.Series(all_entities).value_counts()
    for entity, count in entity_counts.head(20).items():
        print(f"   • {entity:25s}: {count:4d}")
    
    # Category distribution
    print("\n📂 Category Distribution:")
    cat_counts = df['category'].value_counts()
    for cat, count in cat_counts.head(15).items():
        print(f"   • {cat:40s}: {count:4d}")
    
    # Sensitivity distribution
    print("\n🔒 Sensitivity Distribution:")
    sens_counts = df['sensitivity'].value_counts()
    for sens, count in sens_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   • {sens.upper():15s}: {count:4d} ({percentage:.1f}%)")


# ============================================================================ 
# MAIN
# ============================================================================ 
if __name__ == "__main__":
    print("="*60)
    print("🌍 GLOBALLY DIVERSE PII Token Classification Dataset")
    print("="*60)
    
    # Generate dataset with more batches to ensure good coverage
    df_pii, failed = create_full_dataset(num_batches=50)

    if not df_pii.empty:
        # Remove duplicates
        df_clean = df_pii.drop_duplicates(subset=['text'], keep='first')
        print(f"\n🧹 Removed {len(df_pii) - len(df_clean)} duplicates")
        print(f"📦 Final dataset size: {len(df_clean)} samples")
        
        # Analyze diversity
        analyze_diversity(df_clean)
        
        # Save in multiple formats
        save_in_multiple_formats(df_clean)
        
        # Show diverse examples
        print("\n" + "="*60)
        print("💡 SAMPLE EXAMPLES FROM DIFFERENT REGIONS")
        print("="*60)
        
        # Show examples from different regions
        regions_shown = set()
        for _, row in df_clean.iterrows():
            if row['region'] not in regions_shown and len(regions_shown) < 6:
                regions_shown.add(row['region'])
                print(f"\n{'─'*60}")
                print(f"📍 {row['region']} - {row['category']}")
                print(f"{'─'*60}")
                print(f"📝 Text: {row['text']}")
                print(f"🏷️  Entities: {', '.join([e['label'] + ': ' + e['text'] for e in row['entities'][:3]])}")
        
        print("\n" + "="*60)
        print("✨ Dataset Generation Complete!")
        print("="*60)
        
        print("\n🎯 What You Got:")
        print(f"   • {len(df_clean)} diverse PII samples")
        print(f"   • {len(df_clean['region'].unique())} countries/regions")
        print(f"   • {len(df_clean['category'].unique())} PII categories")
        
        print("\n📂 Files Created:")
        print("   • pii_global_train.json ← Use this for training")
        print("   • pii_global_val.json ← Use this for validation")
        print("   • pii_global_test.json ← Use this for testing")
        print("   • pii_global_token_classification_full.json ← Full dataset")
        print("   • pii_global.conll ← CoNLL format")
        
        print("\n🚀 Quick Start:")
        print("   import json")
        print("   with open('pii_global_train.json', 'r', encoding='utf-8') as f:")
        print("       train_data = json.load(f)")
        print("   # Use with your PIIDataset class!")
        
    else:
        print("\n❌ No data generated!")
        print("Check your API key and internet connection.")