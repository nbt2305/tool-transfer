import pandas as pd
import sys

if len(sys.argv) != 3:
    print("⚠️  Cách dùng: python process_csv.py <đầu_vào.csv> <đầu_ra.csv>")
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]

# Đọc file
df = pd.read_csv(input_path)

# Chọn các cột cần thiết
df_trimmed = df[['Title', 'Question', 'Answers', 'Answer_Correct']]

# Gom nhóm theo Title
df_grouped = df_trimmed.groupby('Title', as_index=False).agg({
    'Question': 'first',
    'Answers': 'first',
    'Answer_Correct': lambda x: ' || '.join(x.dropna().astype(str).unique())
})

# Tách số thứ tự để sắp xếp
df_grouped['Question_Number'] = df_grouped['Title'].str.extract(r'(\d+)').astype(int)

# Sắp xếp và lưu
df_sorted = df_grouped.sort_values('Question_Number').drop(columns='Question_Number')
df_sorted.to_csv(output_path, index=False)

print(f"✅ Xử lý xong! File được lưu tại: {output_path}")
