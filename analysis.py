import pandas as pd

# Load cleaned attendance data
attendance = pd.read_csv(
    "cleaned_data/attendance_cleaned.csv"
)

print("Attendance data loaded:")
print(attendance.shape)
print(attendance.head())