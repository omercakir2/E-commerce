import os
from pathlib import Path
import re

# 📁 Yol tanımları
base_dir = Path(__file__).resolve().parent
screenshots_dir = base_dir / "sample_pngs"
readme_path = base_dir / "README.md"

# 🔍 En son versiyon klasörünü bul
latest_version_folder = None
if screenshots_dir.exists():
    for version_folder in sorted(screenshots_dir.iterdir()):
        if version_folder.is_dir():
            latest_version_folder = version_folder  # sadece en son klasör

# 📸 Görselleri topla
screenshot_section = "## 📸 Screenshots\n\n"
if latest_version_folder:
    screenshot_section += f"### 📁 Version {latest_version_folder.name}\n\n"
    image_files = sorted(
        latest_version_folder.glob("*"),
        key=lambda x: int(re.search(r'\d+', x.stem).group()) if re.search(r'\d+', x.stem) else float('inf')
    )

    for i, image_file in enumerate(image_files):
        if image_file.suffix.lower() in [".png", ".jpg", ".jpeg", ".gif"]:
            relative_path = image_file.relative_to(base_dir)
            simplified_name = f"Photo {i + 1}"
            screenshot_section += f"![{simplified_name}]({relative_path})\n\n"

# 📝 README dosyasını oku
readme_text = readme_path.read_text()

# 📌 Eğer en başta zaten eski screenshot varsa, onu sil
readme_text = re.sub(r"(?s)^## 📸 Screenshots.*?\n(?=\S)", "", readme_text).strip()

# 🚀 Yeni screenshot bölümünü en üste ekle
updated_readme = screenshot_section.strip() + "\n\n" + readme_text.strip()

# 💾 README'yi güncelle
readme_path.write_text(updated_readme)

print("✅ README.md updated successfully with screenshots at the top, rest untouched.")