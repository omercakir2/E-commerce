import os
from pathlib import Path

# Paths
base_dir = Path(__file__).resolve().parent
screenshots_dir = base_dir / "sample_pngs"
readme_path = base_dir / "README.md"

# Prepare screenshot section
screenshot_section = "## 📸 Screenshots\n\n"

# Walk through each versioned folder
latest_version_folder = None
if screenshots_dir.exists():
    for version_folder in sorted(screenshots_dir.iterdir()):
        if version_folder.is_dir():
            latest_version_folder = version_folder # Keep track of the latest folder

if latest_version_folder:
    screenshot_section += f"### 📁 Version {latest_version_folder.name}\n\n"
    for image_file in sorted(latest_version_folder.glob("*")):
        if image_file.suffix.lower() in [".png", ".jpg", ".jpeg", ".gif"]:
            relative_path = image_file.relative_to(base_dir)
            screenshot_section += f"![{image_file.stem}]({relative_path})\n\n"
# Load existing README
readme_text = readme_path.read_text()

# Replace or append the screenshots section
if "## 📸 Screenshots" in readme_text:
    updated_readme = readme_text.split("## 📸 Screenshots")[0].strip() + "\n\n" + screenshot_section
else:
    updated_readme = readme_text.strip() + "\n\n" + screenshot_section

# Save it back
readme_path.write_text(updated_readme)
print("✅ README.md updated with screenshots.")
