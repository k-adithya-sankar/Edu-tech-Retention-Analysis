import pandas as pd
df=pd.read_csv("studentattenndance.csv")
df['date']=pd.to_datetime(df['date'], format='mixed',errors='coerce')
#print(df.info())

# print(df['school_id'].value_counts().head(30))
def normalize_school_id(s):
    s = s.astype('string').str.upper().str.strip()
    s = s.str.replace('-', '', regex=False)
    s = s.str.replace('_', '', regex=False)
    s = s.str.replace(r'^SCH', '', regex=True)
    s = s.str.replace(r'^S', '', regex=True)
    s = s.str.extract(r'(\d+)', expand=False)
    s = s.str.zfill(4)
    s = 'SCH' + s
    return s
df['school_id'] = normalize_school_id(df['school_id'])
# print(df['school_id'].head(30).to_string(index=False))
# print(df.info())
master=pd.read_csv("schoolmaster.csv")
master['school_id'] = normalize_school_id(master['school_id'])
attendance_schools = set(df['school_id'])
master_schools = set(master['school_id'])

unmatched = attendance_schools - master_schools

# print("Unique attendance schools:", len(attendance_schools))
# print("Master schools:", len(master_schools))
# print("Unmatched attendance schools:", len(unmatched))
# print(unmatched)
#print((df['present_students'] > df['total_students']).sum())
df['attendance_anomaly'] = (
    df['present_students'] > df['total_students']
)
true_values = [
    'true', 'yes', 'y', '1',
    'hai', 'haan', 'h',
    'available', 'working', 'functional'
]

false_values = [
    'false', 'no', 'n', '0',
    'nahi', 'nahi hai', 'na',
    'kharab', 'under repair',
    'broken', 'not available'
]

def normalize_teacher_present(s):
    s = s.astype('string').str.lower().str.strip()
    s = s.replace(true_values, 1)
    s = s.replace(false_values, 0)
    return s.astype('Int64')
df['teacher_present'] = normalize_teacher_present(
    df['teacher_present']
)
#print(df['teacher_present'].value_counts(dropna=False))
roman_to_grade = {
    'I': 1,
    'II': 2,
    'III': 3,
    'IV': 4,
    'V': 5
}

df['grade'] = (
    df['grade']
    .astype('string')
    .str.strip()
    .str.upper()
    .replace(roman_to_grade)
)

df['grade'] = pd.to_numeric(df['grade'], errors='coerce').astype('Int64')
df['marked_by']=df['marked_by'].str.upper()

df = df.drop_duplicates().reset_index(drop=True)

df['attendance_rate'] = (
    df['present_students'] / df['total_students'] * 100
)
#print("Attendance rates > 100%:", (df['attendance_rate'] > 100).sum())
# print(
#     df[
#         (df['present_students'] > df['total_students']) &
#         (df['attendance_rate'] <= 100)
#     ][
#         ['school_id', 'date', 'grade',
#          'total_students', 'present_students', 'attendance_rate']
#     ].head(30).to_string(index=False)
# )
# print("Attendance anomalies:", df['attendance_anomaly'].sum())
sunday_100 = df[
    (df['date'].dt.dayofweek == 6) &
    (df['attendance_rate'] == 100)
]

# print("Sunday records:", (df['date'].dt.dayofweek == 6).sum())
# print("Sunday 100% attendance:", len(sunday_100))

df['proxy_attendance_anomaly'] = (
    (df['date'].dt.dayofweek == 6) &
    (df['attendance_rate'] == 100)
)
logical_dupes = df.duplicated(
    subset=['school_id', 'date', 'grade'],
    keep=False
)

# print(
#     df[logical_dupes]
#     .sort_values(['school_id', 'date', 'grade'])
#     .head(30)
#     .to_string(index=False)
# )
duplicate_ids = df[df['record_id'].duplicated(keep=False)]

# print(
#     duplicate_ids
#     .sort_values('record_id')
#     .head(20)
#     .to_string(index=False)
# )
df.to_csv("cleaned_data/attendance_cleaned.csv", index=False)
print("Attendance cleaned data saved successfully!")