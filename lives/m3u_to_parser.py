import urllib.request
import re

def main():
    print("开始转换...")
    
    # 获取数据
    url = "https://bc.188766.xyz/?ip=&mishitong=true&mima=mianfeibuhuaqian&json=true"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        req.add_header('Referer', 'https://bc.188766.xyz/')
        
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
        print("数据获取成功")
    except Exception as e:
        print(f"获取数据失败: {e}")
        return
    
    # 解析并过滤内容
    lines = content.split('\n')
    result = []
    current_group = None
    skip_remaining = False
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # 检查是否遇到冰茶体育，如果是则停止处理后续内容
        if '冰茶体育' in line or skip_remaining:
            skip_remaining = True
            continue
        
        if line.startswith('#EXTINF:'):
            # 提取分组和频道名
            group_match = re.search(r'group-title="([^"]*)"', line)
            name_match = re.search(r',(.+)$', line)
            
            if group_match and name_match:
                group = group_match.group(1)
                name = name_match.group(1).replace(' ', '')  # 去除频道名称中的空格
                
                # 如果是新分组，添加分组标题
                if group != current_group:
                    if current_group is not None:
                        result.append("")
                    result.append(f"{group}\t\t,\t\t#genre#")
                    current_group = group
                
                # 获取下一行的URL
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line and not next_line.startswith('#'):
                        result.append(f"{name}\t,\t\t{next_line}")
    
    # 保存结果到lives目录
    output_content = '\n'.join(result)
    
    try:
        with open('playlist.txt', 'w', encoding='utf-8') as f:
            f.write(output_content)
        print("转换完成，已保存到 lives/playlist.txt")
    except Exception as e:
        print(f"保存失败: {e}")

if __name__ == "__main__":
    main()