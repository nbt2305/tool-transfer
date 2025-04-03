import pandas as pd

# Đường dẫn tới file CSV của bạn
file_path = "AWS-Certified-DevOps-Engineer-Professional-DOP-C02.csv"  # đổi tên file nếu cần

# Đọc dữ liệu từ file
df = pd.read_csv(file_path)

# Chọn các cột cần thiết
df_trimmed = df[['Title', 'Question', 'Answers', 'Answer_Correct']]

# Gom nhóm theo Title
df_grouped = df_trimmed.groupby('Title', as_index=False).agg({
    'Question': 'first',  # Lấy dòng đầu tiên
    'Answers': 'first',   # Lấy dòng đầu tiên
    'Answer_Correct': lambda x: ' || '.join(x.dropna().astype(str).unique())  # Nối chuỗi
})

# Tách số thứ tự để sắp xếp
df_grouped['Question_Number'] = df_grouped['Title'].str.extract(r'(\d+)').astype(int)

# Sắp xếp theo số thứ tự Question
df_sorted = df_grouped.sort_values('Question_Number').drop(columns='Question_Number')

# Xuất ra file mới
output_file = "cleaned_questions.csv"
df_sorted.to_csv(output_file, index=False)

print(f"✅ Đã xử lý xong! File mới được lưu tại: {output_file}")
