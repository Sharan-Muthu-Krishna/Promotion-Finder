import zipfile
import os

def zip_project(output_filename, exclude_dirs):
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            if any(excl in root for excl in exclude_dirs):
                continue
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, '.')
                zipf.write(filepath, arcname)

zip_project('project_submission.zip', exclude_dirs=['venv', '__pycache__'])
