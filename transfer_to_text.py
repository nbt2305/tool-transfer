import pandas as pd
import re
import sys

# Kiểm tra tham số dòng lệnh
if len(sys.argv) != 3:
    print("⚠️ Cách dùng: python convert_csv_to_txt.py <đầu_vào.csv> <đầu_ra.txt>")
    sys.exit(1)

input_csv_path = sys.argv[1]
output_txt_path = sys.argv[2]

# ✅ Đọc file CSV
df = pd.read_csv(input_csv_path)

# ✅ Hàm tách đáp án từ chuỗi answers theo đúng thứ tự A → Z
def extract_answers_by_letter_sequence(answer_str):
    pattern = r"([A-Z])\.\s?"
    matches = list(re.finditer(pattern, answer_str))
    results = []
    expected_ord = ord('A')
    for i in range(len(matches)):
        current_letter = matches[i].group(1)
        current_ord = ord(current_letter)
        if current_ord == expected_ord:
            start = matches[i].start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(answer_str)
            content = answer_str[start:end].strip()
            results.append(content)
            expected_ord += 1
            if expected_ord > ord('Z'):
                break
    return results

# ✅ Hàm tách đáp án đúng từ answer_correct
def extract_correct_letters_safely(answer_correct_str, valid_answers):
    pattern = r"([A-Z])\.\s?"
    matches = re.findall(pattern, answer_correct_str)
    valid_letters = [ans[0] for ans in valid_answers]
    if '||' in answer_correct_str and len(matches) >= 2:
        return [m for m in matches if m in valid_letters]
    for m in matches:
        if m in valid_letters:
            return [m]
    return []

# ✅ Xử lý dữ liệu
output_lines = []
for idx, row in df.iterrows():
    title = f"Q{idx + 1}"
    question = row['Question'].strip()
    answer_str = row['Answers']
    correct_str = row['Answer_Correct']

    answers = extract_answers_by_letter_sequence(answer_str)
    correct_letters = extract_correct_letters_safely(correct_str, answers)

    output_lines.append(title)
    output_lines.append(question)
    output_lines.extend(answers)
    output_lines.append(f"ANSWER: {','.join(correct_letters)}")
    output_lines.append("")

# ✅ Ghi ra file TXT
with open(output_txt_path, "w", encoding="utf-8") as f:
    for line in output_lines:
        f.write(line + "\n")

print(f"✅ File đã được xuất ra: {output_txt_path}")