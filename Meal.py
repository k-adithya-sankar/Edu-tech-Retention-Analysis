import pandas as pd
df=pd.read_excel("middaymeal.xlsx")
df['date']=pd.to_datetime(df['date'], format='mixed',errors='coerce')
# df['quantity']=pd.to_numeric(df['quantity'], errors='coerce')
# df['total_cost']=pd.to_numeric(df['total_cost'], errors='coerce')
# print(df[['quantity','total_cost']].isna().sum())
# print(df[['quantity','total_cost']].head(10))
unit_map = {
    "KG": "kilogram",
    "kg": "kilogram",
    "Kgs": "kilogram",
    "KGS": "kilogram",
    "Grams": "gram",
    "grams": "gram",
    "g": "gram",
    "Sacks": "BAGS",
    "bags": "BAGS",
    "Bags": "BAGS",
    "Bori": "BAGS",
    # "50kg Bags" is intentionally NOT included → will stay as is
}
df['unit']=df['unit'].replace(unit_map)
quantity_text=df['quantity'].astype('string').str.strip()
quantity_with_unit=df[quantity_text.str.contains(r'[A-Za-z]',na=False)][['quantity','unit']]
#print(quantity_with_unit['quantity'].value_counts().to_string())
df['quantity_orginal']=df["quantity"]
df['quantity']=(df['quantity'].astype('string').str.replace(',','',regex=False).str.extract(r'([-+]?\d*\.?\d+)',expand=False))
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
mask_text=df['quantity_orginal'].astype('string').str.contains(r'[A-Za-z]',na=False)
#print(df.loc[mask_text, ['quantity_orginal', 'unit']].value_counts().head(30))
qty_str=df['quantity_orginal'].astype('string')
mask_kg = qty_str.str.contains(r'kg', case=False, na=False)
mask_g = qty_str.str.contains(r'\bg\b', case=False, na=False)
missing_unit = df['unit'].isna()
df.loc[missing_unit & mask_kg, 'unit'] = 'kilogram'
df.loc[missing_unit & mask_g & ~mask_kg, 'unit'] = 'gram'
#print(df[['quantity_orginal', 'quantity', 'unit']].head(50).to_string())
#print(df.info())
df['payment_status'] = df['payment_status'].str.upper()
df['vendor_name'] = df['vendor_name'].str.upper()
df['grain_type'] = df['grain_type'].str.upper()
df['total_cost'] = df['total_cost'].astype('string')
df['total_cost'] = df['total_cost'].str.replace('Rs.', '', regex=False)
df['total_cost'] = df['total_cost'].str.replace('₹', '', regex=False)
df['total_cost'] = df['total_cost'].str.replace(',', '', regex=False)
df['total_cost']=df['total_cost'].str.replace('/-', '', regex=False)
df['total_cost'] = pd.to_numeric(df['total_cost'], errors='coerce')
df['payment_status'] = df['payment_status'].fillna('Unknown')
#print(df['grain_type'].value_counts())
# Define grain mapping
grain_map = {
    "RICE": "Rice",
    "CHAWAL": "Rice",
    "DAL": "Pulses",
    "DAAL": "Pulses",
    "PULSES": "Pulses",
    "LENTILS": "Pulses",
    "WHEAT": "Wheat",
    "GEHUN": "Wheat",
    "ATTA": "Atta",
    "SARSON TEL": "Mustard Oil",
    "OIL": "Mustard Oil",
    "COOKING OIL": "Mustard Oil",
    "MUSTARD OIL": "Mustard Oil",
}
df['grain_type'] = df['grain_type'].replace(grain_map)
#print(df['grain_type'].value_counts())

df['quantity_kg'] = df['quantity'].copy()

mask_gram = df['unit'] == 'gram'
df.loc[mask_gram, 'quantity_kg'] = df.loc[mask_gram, 'quantity'] / 1000

mask_bag = df['unit'].isin(['BAGS', '50kg Bags'])
df.loc[mask_bag, 'quantity_kg'] = df.loc[mask_bag, 'quantity'] * 50

# print("Sample quantity conversions to kg:")
# print(df[['quantity', 'unit', 'quantity_kg']].head(20))

# print("\nquantity_kg stats:")
# print(df['quantity_kg'].describe())
def normalize_school_id(s):
    s = s.astype('string').str.upper().str.strip()

    # Remove separators
    s = s.str.replace('-', '', regex=False)
    s = s.str.replace('_', '', regex=False)

    # Remove SCH / S prefix
    s = s.str.replace(r'^SCH', '', regex=True)
    s = s.str.replace(r'^S', '', regex=True)

    # Keep only the numeric part
    s = s.str.extract(r'(\d+)', expand=False)

    # Convert to standard 4-digit ID
    s = s.str.zfill(4)

    # Add standard prefix
    s = 'SCH' + s

    return s

df['school_id'] = normalize_school_id(df['school_id'])
mask = df['unit'].astype('string').str.lower().str.strip() == '50kg bags'

df.loc[mask, 'quantity_kg'] = df.loc[mask, 'quantity'] * 50
df.loc[mask, 'unit'] = 'kg'
df['unit'] = df['unit'].replace('kg', 'kilogram')
df['unit']=df['unit'].str.upper()
df.to_csv("cleaned_data/mdm_cleaned.csv", index=False)
print("MDM cleaned data saved successfully!")