import re
import os

def contains_chinese(text):
    return re.search(r'[\u4e00-\u9fff]', text) is not None

def split_po_blocks(lines):
    blocks = []
    block = []
    in_block = False

    for line in lines:
        if line.startswith('msgid '):
            if block:
                blocks.append(block)
            block = [line]
            in_block = True
        elif in_block:
            block.append(line)
        else:
            blocks.append([line])  # dòng ngoài khối msgid
    if block:
        blocks.append(block)

    return blocks

def block_has_chinese_literal(block):
    for line in block:
        if re.match(r'^".*"$', line.strip()) and contains_chinese(line):
            return True
    return False

def reorder_po_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    blocks = split_po_blocks(lines)

    normal_blocks = []
    chinese_blocks = []

    for block in blocks:
        if block_has_chinese_literal(block):
            chinese_blocks.append(block)
        else:
            normal_blocks.append(block)

    with open(filename, 'w', encoding='utf-8') as f:
        for block in normal_blocks + chinese_blocks:
            f.writelines(block)

    print(f"✅ Đã sắp xếp lại file: {filename}")

def reorder_all_po_files():
    for file in os.listdir("."):
        if file.endswith(".po"):
            reorder_po_file(file)

reorder_all_po_files()
