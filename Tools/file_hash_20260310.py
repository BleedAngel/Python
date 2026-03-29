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
def validate_response(response,options):
    if response not in options:
        print(f"Error: '{response}' is not supported.")
        sys.exit(1)

#選擇模式
EXECUTE_MODE=["s","v","sv"]
execute_mode=input(
    f"Supported execute_mode: \n"
    f"Save hash[{EXECUTE_MODE[0]}] | "
    f"Verify hash[{EXECUTE_MODE[1]}] | "
    f"Save & Verify[{EXECUTE_MODE[2]}] \n"
    f"Choose execute_mode: \n"
)
validate_response(execute_mode,EXECUTE_MODE)

#選擇演算法模式
print("Supported algorithm: \n",hashlib.algorithms_available)
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
if "s" in execute_mode:
    target_dir=input("Target_dir: \n").strip("'").strip('"').strip(" ")
    validate_directory(target_dir)

    FILE_MODE=["w","a"]
    file_mode=input(
        f"Supported file_mode: \n"
        f"Write file[{FILE_MODE[0]}]"
        f"Append file[{FILE_MODE[1]}]"
        f"Choose file mode: \n"
    )
    validate_response(file_mode,FILE_MODE)

    if file_mode not in FILE_MODE:
        print(f"Error: '{file_mode}' is not supported")
        sys.exit(1)

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
if "v" in execute_mode:
    check_dir=input("Check dir: \n").strip("'").strip('"').strip(" ")
    validate_directory(check_dir)

    #讀取已有的hash值存取txt檔
    if "s" not in execute_mode:
        hash_file=input("Hash file: \n").strip("'").strip('"').strip(" ")
        validate_file(hash_file)

    #逐一對比hash值
    for entry in os.scandir(check_dir):
        if(entry.is_file()):
            file_path=entry.path
            verify_hash(file_path,hash_file)
            check_summary+=1

    print(f"✅ File checked successfully!*{check_summary}")
