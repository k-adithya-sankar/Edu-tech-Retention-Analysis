import pandas as pd
df=pd.read_csv("schoolinfo.csv")
df['date']=pd.to_datetime(df['date'], format='mixed',errors='coerce')
# print(df['has_electricity'].value_counts())
# print(df['has_drinking_water'].value_counts())
# print(df['has_boundary_wall'].value_counts())
# print(df['has_functional_toilet'].value_counts())
# print(df['has_playground'].value_counts())
true_values = [
    'true', 'yes', 'y', '1', 'hai', 'haan', 'working', 'available', 'functional', 'h'
]

false_values = [
    'false', 'no', 'n', '0', 'nahi', 'nahi hai', 'kharab', 'na'
]

bool_cols = [
    'has_electricity',
    'has_drinking_water',
    'has_functional_toilet',
    'has_boundary_wall',
    'has_playground'
]


def normalize_bool_col(s):
    
    s = s.astype('string').str.lower().str.strip()
    
    
    s = s.replace(true_values, 1)
    s = s.replace(false_values, 0)
    
    
    s = pd.to_numeric(s, errors='coerce')
    
   
    s = s.astype('Int64')
    return s


for col in bool_cols:
    df[col] = normalize_bool_col(df[col])
df['inspector_name'] = df['inspector_name'].str.upper()

# print(df.info())
# print(df['remarks'].unique())
df['remarks'] = df['remarks'].fillna('no remarks')
df['remarks'] = df['remarks'].str.upper()
# print(df['remarks'].value_counts())
# print(df['school_id'].value_counts())
# print(df['school_id'].head(30))
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
print(df.info())
# print(df['school_id'].head(30))
# df.to_csv("cleaned_data/infrastructure_cleaned.csv", index=False)
# print("Infrastructure cleaned data saved successfully!")