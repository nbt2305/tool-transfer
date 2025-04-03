import pandas as pd
import re

# ✅ Đường dẫn đến file CSV đầu vào (bạn thay đổi cho phù hợp)
input_csv_path = "check.csv"
# input_csv_path = "cleaned_questions.csv"
output_txt_path = "formatted_questions_final_cleanedd.txt"

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
        else:
            continue
    return results

# ✅ Hàm tách đáp án đúng từ answer_correct nhưng chỉ giữ lại nếu có trong danh sách đáp án đã tách
def extract_correct_letters_safely(answer_correct_str, valid_answers):
    pattern = r"([A-Z])\.\s?"
    matches = re.findall(pattern, answer_correct_str)
    valid_letters = [ans[0] for ans in valid_answers]

    # Nếu thỏa mãn đồng thời có '||' và có từ 2 đáp án trở lên
    if '||' in answer_correct_str and len(matches) >= 2:
        return [m for m in matches if m in valid_letters]
    
    # Ngược lại: chỉ lấy 1 đáp án đúng đầu tiên phù hợp
    for m in matches:
        if m in valid_letters:
            return [m]
    
    return []
    # pattern = r"([A-Z])\.\s?"
    # matches = re.findall(pattern, answer_correct_str)
    # valid_letters = [ans[0] for ans in valid_answers]
    # return [m for m in matches if m in valid_letters]

# ✅ Tạo danh sách dòng kết quả
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
    output_lines.append("")  # Dòng trống giữa các câu hỏi

# ✅ Ghi ra file TXT
with open(output_txt_path, "w", encoding="utf-8") as f:
    for line in output_lines:
        f.write(line + "\n")

print(f"✅ File đã được xuất ra: {output_txt_path}")
