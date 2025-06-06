import os


def read_files_in_folder(main_folder_path="../resources/data"):
    md_files_data = []

    for subfolder, _, files in os.walk(main_folder_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(subfolder, file)

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                md_files_data.append({
                    'subfolder': os.path.basename(subfolder),
                    'file_name': file,
                    'content': content
                })

    return md_files_data
