import os
import random
from PIL import Image, ImageDraw, ImageFont

# ========== 配置 ==========
NUM_IMAGES = 10                     # 生成图片数量
PLATES_PER_IMAGE = 50              # 每张图车牌数量
HIGHLIGHT_RATIO = 0.06             # 高亮比例（约3个/50）
SPECIAL_NUMBER_PROB = 0.30         # 使用热门梗的概率（15%）

# ========== 车牌数据 ==========
PROVINCES = [
    '京', '沪', '津', '渝', '冀', '晋', '蒙', '辽', '吉', '黑',
    '苏', '浙', '皖', '闽', '赣', '鲁', '豫', '鄂', '湘', '粤',
    '桂', '琼', '川', '贵', '云', '藏', '陕', '甘', '青', '宁', '新'
]

LETTERS = 'ABCDEFGHJKLMNPQRSTUVWXYZ'  # 排除 I, O
DIGITS = '0123456789'
ALPHANUM = LETTERS + DIGITS

# 热门梗数字（长度需兼容传统/新能源格式）
SPECIAL_NUMBERS_OLD = ['110', '119', '120', '521', '666', '888', '9527', '12345']  # 3~5位
SPECIAL_NUMBERS_NEW = ['11000', '11999', '12000', '52100', '66666', '88888', '95270', '123456']  # 6位

# ========== 工具函数 ==========
def find_chinese_font():
    """尝试寻找系统中可用的中文字体"""
    candidates = [
        # Windows
        "simhei.ttf",
        "msyh.ttc",
        "simsun.ttc",
        # macOS
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        # Linux (Debian/Ubuntu)
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    ]
    for font_path in candidates:
        try:
            font = ImageFont.truetype(font_path, 24)
            # 测试能否渲染中文
            img = Image.new('RGB', (10, 10))
            draw = ImageDraw.Draw(img)
            draw.text((0, 0), "京", font=font, fill=(0, 0, 0))
            return font_path
        except:
            continue
    return None

CHINESE_FONT_PATH = find_chinese_font()

def get_font(size=24):
    if CHINESE_FONT_PATH:
        return ImageFont.truetype(CHINESE_FONT_PATH, size)
    else:
        print("⚠️ 未找到中文字体，部分车牌可能显示为方框。建议安装中文字体。")
        return ImageFont.load_default()

# ========== 车牌生成 ==========
def generate_old_plate():
    """生成传统燃油车车牌（7位：京A12345）"""
    province = random.choice(PROVINCES)
    letter = random.choice(LETTERS)
    
    if random.random() < SPECIAL_NUMBER_PROB:
        # 使用热门梗，但需补足到5位（右对齐或左补随机数字）
        base = random.choice(SPECIAL_NUMBERS_OLD)
        if len(base) < 5:
            pad = ''.join(random.choices(DIGITS, k=5 - len(base)))
            # 可选：base + pad 或 pad + base，这里用 base + pad 更自然
            suffix = (base + pad)[:5]
        else:
            suffix = base[:5]
    else:
        suffix = ''.join(random.choices(ALPHANUM, k=5))
    
    return province + letter + suffix

def generate_new_energy_plate():
    """生成新能源车牌（8位：京AD12345）"""
    province = random.choice(PROVINCES)
    # 新能源第二位固定为 A（实际规则复杂，此处简化）
    second = 'A'
    third = random.choice(['D', 'F'])  # 纯电/混动
    
    if random.random() < SPECIAL_NUMBER_PROB:
        suffix = random.choice(SPECIAL_NUMBERS_NEW)
    else:
        suffix = ''.join(random.choices(DIGITS, k=6))
    
    return province + second + third + suffix[:6]

def generate_plate():
    """随机生成传统或新能源车牌"""
    # if random.random() < 0.3:  # 30% 概率生成新能源车牌
    #     return generate_new_energy_plate()
    # else:
    return generate_old_plate()

# ========== 单个车牌图像 ==========
def create_plate_image(plate_text, selected=False):
    width, height = 140, 70
    bg_color = (210, 255, 210) if selected else (245, 245, 245)
    border_color = (80, 180, 80) if selected else (180, 180, 180)
    
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width - 1, height - 1], outline=border_color, width=2)
    
    font = get_font(26 if len(plate_text) <= 7 else 22)  # 新能源车牌字小一点
    
    # 居中文本
    bbox = draw.textbbox((0, 0), plate_text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (width - text_w) // 2
    y = (height - text_h) // 2 - 2  # 微调垂直位置
    draw.text((x, y), plate_text, fill=(0, 0, 0), font=font)
    
    return img

# ========== 生成整张选号界面 ==========
def generate_selection_screen(output_path, image_index):
    plates = [generate_plate() for _ in range(PLATES_PER_IMAGE)]
    
    # 随机选择 1~3 个高亮
    num_highlight = random.randint(1, 3)
    highlight_indices = set(random.sample(range(PLATES_PER_IMAGE), num_highlight))
    
    cols, rows = 10, 5
    block_w, block_h = 140, 70
    margin = 12
    top_margin = 60
    
    img_w = cols * (block_w + margin) + margin
    img_h = top_margin + rows * (block_h + margin) + margin
    
    bg = Image.new('RGB', (img_w, img_h), (253, 253, 253))
    draw = ImageDraw.Draw(bg)
    
    title_font = get_font(28)
    draw.text((20, 15), f"车管所随机选号界面 - 图片 {image_index}", fill=(30, 30, 30), font=title_font)
    
    for i, plate in enumerate(plates):
        row = i // cols
        col = i % cols
        x = margin + col * (block_w + margin)
        y = top_margin + row * (block_h + margin)
        
        selected = i in highlight_indices
        plate_img = create_plate_image(plate, selected=selected)
        bg.paste(plate_img, (x, y))
    
    bg.save(output_path)

# ========== 主程序 ==========
def main():
    output_dir = "test_license_plates"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🔍 检测到中文字体路径: {CHINESE_FONT_PATH or '未找到'}")
    print(f"🖼️  正在生成 {NUM_IMAGES} 张测试图片，每张包含 {PLATES_PER_IMAGE} 个车牌...")
    
    for i in range(1, NUM_IMAGES + 1):
        filename = f"plate_selection_{i:03d}.png"
        filepath = os.path.join(output_dir, filename)
        generate_selection_screen(filepath, i)
        print(f"✅ 已生成: {filename}")
    
    print(f"\n🎉 全部完成！图片已保存至文件夹：'{os.path.abspath(output_dir)}'")

if __name__ == "__main__":
    main()