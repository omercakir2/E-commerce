import os
from pathlib import Path
import re

# Config
GITHUB_USER = "omercakir2"
GITHUB_REPO = "your-repo-name"  # <-- GITHUB REPO ADINI BURAYA YAZ
GITHUB_BRANCH = "main"          # ya da 'master'

# Paths
base_dir = Path(__file__).resolve().parent
screenshots_dir = base_dir / "sample_pngs"
readme_path = base_dir / "README.md"

# Clean filenames (boşluk ve ':' karakterlerini kaldır)
for version_folder in screenshots_dir.iterdir():
    if version_folder.is_dir():
        for file in version_folder.iterdir():
            if file.is_file():
                new_name = file.name.replace(" ", "_").replace(":", "-")
                if file.name != new_name:
                    file.rename(file.with_name(new_name))

# Prepare screenshot section
screenshot_section = "## 📸 Screenshots\n\n"

# Find latest version folder
latest_version_folder = None
if screenshots_dir.exists():
    for version_folder in sorted(screenshots_dir.iterdir()):
        if version_folder.is_dir():
            latest_version_folder = version_folder  # get the last one

# Build screenshot section
if latest_version_folder:
    screenshot_section += f"### 📁 Version `{latest_version_folder.name}`\n\n"

    # Sort images by number if available
    image_files = sorted(
        latest_version_folder.glob("*"),
        key=lambda x: int(re.search(r'\d+', x.stem).group()) if re.search(r'\d+', x.stem) else float('inf')
    )

    for i, image_file in enumerate(image_files):
        if image_file.suffix.lower() in [".png", ".jpg", ".jpeg", ".gif"]:
            relative_path = image_file.relative_to(base_dir)
            # Convert to GitHub raw URL
            url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{relative_path}".replace(" ", "%20")
            screenshot_section += f"![Photo {i+1}]({url})\n\n"

# Load existing README
readme_text = readme_path.read_text()

# Replace or append the screenshots section
if "## 📸 Screenshots" in readme_text:
    updated_readme = readme_text.split("## 📸 Screenshots")[0].strip() + "\n\n" + screenshot_section
else:
    updated_readme = readme_text.strip() + "\n\n" + screenshot_section

# Save back
readme_path.write_text(updated_readme)
print("✅ README.md updated with screenshots.")