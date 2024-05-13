import pandas as pd

# Replace 'example.xlsx' with the path to your Excel file
file_path = '/home/nagipragalathan/Test/mayan-edms-4.6.3/Backup/file_example_XLS_50.xls'

# Read the Excel file into a Pandas DataFrame
df = pd.read_excel(file_path)

# Display the DataFrame (optional)
print(str(df))
