import os
import hashlib

ANSWER=input("save file hash[s] | verify file hash[v]")

def validate_directory(path):
    if not os.path.isdir(path):
        print("Error")
        exit()
def validate_file(path):
    if not os.path.isfile(path):
        print("Error")
        exit()

def calculate_hash(file_path,algorithm="sha256"):
    hash_func=hashlib.new(algorithm)
    with open(file_path,"rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)

    return hash_func.hexdigest()

def save_hash(file_path,hash_value,hash_file):
    file_name=os.path.basename(file_path)
    print(f"Saved hash for {file_name}")
    with open(hash_file, "a") as f:
        f.write(f"{file_name},{hash_value}\n")

def verify_file(file_path,hash_file):
    validate_file(hash_file)
    
    current_hash=calculate_hash(file_path)
    file_name=os.path.basename(file_path)
    with open(hash_file,"r") as f:
        for line in f:
            stored_file,stored_hash=line.strip().split(",")
            if(stored_file==file_name):
                if(stored_hash==current_hash):
                    print(f"完整性檢查通過✅ {file_name}")
                    return True
                else:
                    print(f"已被修改❌ {file_name}")
                    return False
                
    print(f"沒有紀錄 {file_path}")
    return False

save_summary=0
check_summary=0

if "s" in ANSWER:
    TARGET_DIR=input("target_dir:\n").strip("'").strip('"').strip(" ")
    validate_directory(TARGET_DIR)

    HASH_DIR=input("hash dir:\n").strip("'").strip('"').strip(" ")
    validate_directory(HASH_DIR)
    hash_file=os.path.join(HASH_DIR,"hash_file.txt")
    open(hash_file,"w").close()

    for entry in os.scandir(TARGET_DIR):
        if(entry.is_file()):
            file_path=entry.path
            hash_value=calculate_hash(file_path)
            save_hash(file_path,hash_value,hash_file)
            save_summary+=1
    print(f"Hash file saved successfully!*{save_summary}")

if "v" in ANSWER:
    CHECK_DIR=input("check dir:\n").strip("'").strip('"').strip(" ")
    validate_directory(CHECK_DIR)

    if "s" not in ANSWER:
        hash_file=input("hash file:\n").strip("'").strip('"').strip(" ")
        validate_file(hash_file)

    for entry in os.scandir(CHECK_DIR):
        if(entry.is_file()):
            file_path=entry.path
            verify_file(file_path,hash_file)
            check_summary+=1
    print(f"file checked successfully!*{check_summary}")
