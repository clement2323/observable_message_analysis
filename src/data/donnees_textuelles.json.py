import pandas as pd

# Minimal example DataFrame
data = {
    'sender': ['example1@example.com', 'example2@example.com'],
    'subject': ['Subject 1', 'Subject 2'],
    'date': ['2023-10-01-12-00-00', '2023-10-02-13-00-00'],
    'full_name': ['Example One', 'Example Two']
}

# Create DataFrame
df = pd.DataFrame(data)

# Export to JSON
json_output = df.to_json(orient='records', lines=True)
print(json_output)
