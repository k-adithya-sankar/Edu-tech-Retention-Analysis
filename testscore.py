import pandas as pd
df=pd.read_json("testscore.json")
# print(df.loc[df['grading_scale'] == 'CGPA', 'avg_score'].value_counts().sort_index())
# print(df.loc[df['grading_scale'] == 'Raw Marks', ['avg_score', 'max_marks']].head(30).to_string(index=False))
df['score_100'] = pd.NA

percentage_scales = ['%', 'pct', 'Percentage']

mask = df['grading_scale'].isin(percentage_scales)

df.loc[mask, 'score_100'] = (
    df.loc[mask, 'avg_score']
    .astype('string')
    .str.replace('%', '', regex=False)
    .astype(float)
)

#print(df[['grading_scale', 'avg_score', 'score_100']].head(15).to_string(index=False))
mask = df['grading_scale'] == 'Raw Marks'

raw = df.loc[mask, 'avg_score'].astype('string')

obtained = raw.str.split('/').str[0].astype(float)
maximum = raw.str.split('/').str[1].astype(float)

df.loc[mask, 'score_100'] = (obtained / maximum) * 100

# print(
#     df.loc[mask, ['grading_scale', 'avg_score', 'max_marks', 'score_100']]
#     .head(15)
#     .to_string(index=False)
# )

mask = df['grading_scale'] == 'CGPA'

df.loc[mask, 'score_100'] = (
    pd.to_numeric(df.loc[mask, 'avg_score'], errors='coerce') * 10
)

# print(
#     df.loc[mask, ['grading_scale', 'avg_score', 'score_100']]
#     .head(15)
#     .to_string(index=False)
# )

grade_mapping = {
    'A+': 95,
    'A': 90,
    'B': 80,
    'C': 70,
    'D': 60,
    'E': 50
}

mask = df['grading_scale'] == 'Letter Grade'

df.loc[mask, 'score_100'] = (
    df.loc[mask, 'avg_score'].map(grade_mapping)
)

# print(
#     df.loc[mask, ['grading_scale', 'avg_score', 'score_100']]
#     .head(15)
#     .to_string(index=False)
# )
# print("Missing scores:", df['score_100'].isna().sum())
# print("Scores below 0:", (df['score_100'] < 0).sum())
# print("Scores above 100:", (df['score_100'] > 100).sum())

# print("\nScore statistics:")
# print(df['score_100'].describe())

# print("\nScore count by grading scale:")
# print(
#     df.groupby('grading_scale')['score_100']
#       .count()
# )
# print(df['subject'].value_counts())
subject_mapping = {
    'Ganit': 'Mathematics',
    'Math': 'Mathematics',
    'Mathematics': 'Mathematics'
}

df['subject'] = df['subject'].replace(subject_mapping)

#print(df['subject'].value_counts())
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
# print("Unique test-score schools:", df['school_id'].nunique())

# print("Missing school IDs:", df['school_id'].isna().sum())

# print("\nSample school IDs:")
# print(df['school_id'].head(10).to_string(index=False))
df['score_100'] = pd.to_numeric(df['score_100'], errors='coerce')

master_df = pd.read_csv("schoolmaster.csv")

unmatched = set(df['school_id']) - set(master_df['school_id'])

print("Unmatched test-score schools:", len(unmatched))

if len(unmatched) > 0:
    print(unmatched)
else:
    print("All test-score school IDs exist in school master.")
    
df.to_csv("cleaned_data/testscore_cleaned.csv", index=False)
print("Test score cleaned data saved successfully!")