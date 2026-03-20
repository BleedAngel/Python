line = "example.txt,abcdef123456 \n"
stored_file, stored_hash = line.strip().split(",")

print(stored_file)  # 輸出: example.txt
print(stored_hash)  # 輸出: abcdef123456