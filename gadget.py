import re
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

cnt = dict()

def init_tags(filepath: str):
    tags = []
    with open(filepath, "r") as f:
        for line in f.readlines():
            match = re.match(r"^\[tag\.(.+?)\]$", line.strip())
            if match:
                tags.append(match.group(1))
    for tag in tags:
        cnt[tag] = 0

def count_rust_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    pattern_multiline = r'#\[safety\s*\{\s*((?:\w+\([^)]*\)\s*,\s*)*\w+\([^)]*\))\s*(?::\s*"[^"]*")?\s*\}\s*\]'
    matches = re.findall(pattern_multiline, content, re.DOTALL)
    if matches:
        for match in matches:
            tags = re.findall(r'(\w+)\([^)]*\)', match)
            for tag in tags:
                if tag not in cnt:
                    print(f"Error! Invalid tag: {tag}.")
                else:
                    cnt[tag] += 1

def count_rust_files(directory: str):
    rust_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.rs'):
                full_path = os.path.join(root, file)
                rust_files.append(full_path)
    for file in rust_files:
        count_rust_file(file)

def draw_graph(cnt: dict):
    fig, ax = plt.subplots(figsize=(15, 12))
    
    # 定义大类分组
    categories = {
        "Execution Sequence": ["PostToFunc", "NotPostToFunc", "NotPriorToFunc", "CallOnce", "Context", "OriginateFrom"],
        "Value": ["Eq", "Ne", "Ge"],
        "Valid": ["Valid", "ValidAccessAddr", "ValidBaseAddr", "ValidInstanceAddr"],
        "Reference": ["RefHeld", "RefUnheld", "OwnedResource"],
        "Memory": ["UserSpace", "KernelMemorySafe", "Section"],
        "MISC": ["Forgotten", "MutAccess", "NonModifying", "Unaccessed", "Bounded", "LockHeld", "ReferTo", "Sync", "Memo"]
    }
    
    # 为每个大类定义不同的基础色系
    base_colors = {
        "Execution Sequence": '#1f77b4',  # 蓝色系
        "Value": '#ff7f0e',  # 橙色系
        "Valid": '#2ca02c',  # 绿色系
        "Reference": '#d62728',  # 红色系
        "Memory": '#9467bd',  # 紫色系
        "MISC": '#8c564b'   # 棕色系
    }
    
    # 生成颜色列表
    colors = []
    labels_ordered = list(cnt.keys())
    
    for label in labels_ordered:
        # 找到当前标签所属的大类
        category = None
        for cat_name, subcats in categories.items():
            if label in subcats:
                category = cat_name
                break
        
        if category:
            base_color = base_colors[category]
            # 在大类中找到当前标签的索引
            idx = categories[category].index(label)
            total = len(categories[category])
            
            # 生成同一色系的不同深浅
            if total == 1:
                colors.append(base_color)
            else:
                # 创建从浅到深的颜色变化
                cmap = LinearSegmentedColormap.from_list(
                    f'cmap_{category}', 
                    ['white', base_color], 
                    N=total+2
                )
                # 跳过最浅的颜色，使用中间的颜色
                color = cmap(idx + 1)
                colors.append(color)
        else:
            # 如果没有找到对应大类，使用灰色
            colors.append('#7f7f7f')
    
    def my_autopct(pct):
        return ('%1.1f%%' % pct) if pct > 2 else ''

    ax.pie(cnt.values(), 
           labels=labels_ordered, 
           autopct=my_autopct,
           colors=colors,
           startangle=90)
    
    plt.tight_layout()
    plt.savefig("statistic.jpg", dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    init_tags(r"ostd/safety-tags.toml")
    count_rust_files(r"ostd/src")
    print(cnt)
    draw_graph(cnt)
    