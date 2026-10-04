import os

dataset_path = r"C:\Users\vemul\OneDrive\Desktop\DFU_Project\dataset"

for folder in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, folder)

    if os.path.isdir(folder_path):
        count = 0
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith((".jpg", ".jpeg", ".png")):
                    count += 1

        print(f"{folder}: {count} images")