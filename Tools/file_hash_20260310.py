import os
import hashlib
import sys

#檢查檔案、資料夾路徑、演算法、檔案模式
def validate_directory(path):
    if not os.path.isdir(path):
        print(f"Error: '{path}' is not a valid directory")
        sys.exit(1)
def validate_file(path):
    if not os.path.isfile(path):
        print(f"Error: '{path}' is not a valid file")
        sys.exit(1)
def validate_algorithm(algorithm):
    if algorithm not in hashlib.algorithms_available:
        print(f"Error: '{algorithm}' is not supported.")
        sys.exit(1)

#選擇模式
answer=input("Choose mode: \nsave file hash[s] | verify file hash[v] | save & verify[sv] \n")

#選擇演算法模式
print("Available algorithm: ",hashlib.algorithms_available)
algorithm=input("Choose algorithm: \n")
validate_algorithm(algorithm)

#計算hash值
def calculate_hash(file_path,algorithm):
    hash_func=hashlib.new(algorithm)
    with open(file_path,"rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)

    return hash_func.hexdigest()

#存取hash值至txt檔
def save_hash(file_path,hash_value,hash_file):
    file_name=os.path.basename(file_path)
    print(f"✅ Saved hash for: '{file_name}'")
    with open(hash_file, "a") as f:
        f.write(f"{file_name},{hash_value}\n")

#對比hash值
def verify_hash(file_path,hash_file):
    validate_file(hash_file)
    
    current_hash=calculate_hash(file_path,algorithm)
    file_name=os.path.basename(file_path)
    with open(hash_file,"r") as f:
        for line in f:
            stored_file,stored_hash=line.strip().split(",")
            if(stored_file==file_name):
                if(stored_hash==current_hash):
                    print(f"✅ Integrity check passed: '{file_name}'")
                    return True
                else:
                    print(f"⚠️ File has been modified: '{file_name}'")
                    return False
                
    print(f"❌ No record found for: {file_path}")
    return False

#統計次數
save_summary=0
check_summary=0

#要求存取hash值
if "s" in answer:
    target_dir=input("Target_dir: \n").strip("'").strip('"').strip(" ")
    validate_directory(target_dir)

    SUPPORTED_FILE_MODE=["w","a"]
    print("Support file mode: \n",SUPPORTED_FILE_MODE)
    file_mode=input("Choose file mode: \n")

    if(file_mode=="w"):
        operation=input("Choose operation: \nmake file[m] | cover file[c]: \n")
        if(operation=="m"):
            hash_dir=input("Hash dir: \n").strip("'").strip('"').strip(" ")
            validate_directory(hash_dir)
            hash_file=os.path.join(hash_dir,"hash_file.txt")
        if(operation=="c"):
            hash_file=input("Hash file: \n").strip("'").strip('"').strip(" ")
            validate_file(hash_file)
    
    if(file_mode=="a"):
        hash_file=input("Hash file: \n").strip("'").strip('"').strip(" ")
        validate_file(hash_file)

    open(hash_file,file_mode).close()

    #逐一生成並存取hash值
    for entry in os.scandir(target_dir):
        if(entry.is_file()):
            file_path=entry.path
            hash_value=calculate_hash(file_path,algorithm)
            save_hash(file_path,hash_value,hash_file)
            save_summary+=1

    print(f"✅ Hash file saved successfully!*{save_summary}")

#要求對比hash值
if "v" in answer:
    check_dir=input("Check dir: \n").strip("'").strip('"').strip(" ")
    validate_directory(check_dir)

    #讀取已有的hash值存取txt檔
    if "s" not in answer:
        hash_file=input("Hash file: \n").strip("'").strip('"').strip(" ")
        validate_file(hash_file)

    #逐一對比hash值
    for entry in os.scandir(check_dir):
        if(entry.is_file()):
            file_path=entry.path
            verify_hash(file_path,hash_file)
            check_summary+=1

    print(f"✅ File checked successfully!*{check_summary}")
