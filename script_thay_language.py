import re
import os

def transform_msgid(msgid: str) -> str:
    # Thay _ và - bằng khoảng trắng
    msgid = msgid.replace("_", " ").replace("-", " ")

    # Viết hoa chữ cái đầu tiên
    msgid = msgid.capitalize()

    # Viết hoa các từ viết tắt quen thuộc
    known_acronyms = ['AI', 'PC', 'VIP', 'GPU', 'RAM', 'API', 'SDK']
    for acronym in known_acronyms:
        pattern = r'\b' + acronym.lower() + r'\b'
        msgid = re.sub(pattern, acronym, msgid, flags=re.IGNORECASE)

    # Làm gọn dấu cách thừa
    msgid = re.sub(r'\s+', ' ', msgid).strip()

    return msgid

def update_po_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    msgid_pattern = re.compile(r'^msgid\s+"(.*)"\s*$')
    in_msgid = False
    current_msgid = ""
    for line in lines:
        match = msgid_pattern.match(line)
        if match:
            current_msgid = match.group(1)
            in_msgid = True
            new_lines.append(line)
            continue

        if in_msgid and line.startswith('msgstr'):
            if current_msgid == "":
                new_lines.append(line)
            else:
                new_msgstr = transform_msgid(current_msgid)
                new_lines.append(f'msgstr "{new_msgstr}"\n')
            in_msgid = False
        else:
            new_lines.append(line)

    # Ghi đè lại file
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

# 🟢 Quét tất cả file .po trong thư mục hiện tại
def update_all_po_files():
    for file in os.listdir("."):
        if file.endswith(".po"):
            print(f"🔧 Đang xử lý: {file}")
            update_po_file(file)
    print("✅ Hoàn tất.")

# 🟢 Gọi hàm
update_all_po_files()
