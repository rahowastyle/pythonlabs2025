# Завдання 2: Генератор хешів файлів

from hashlib import sha256 
# "missing_file.txt" - для перевірки помилки.
file_paths = ["apache_logs.txt", "missing_file.txt"]

def generate_file_hashes(*file_paths):
    dic_hashes = {}
    for path in file_paths:
        try:
            with open(path, "rb") as f:
                file_data = f.read()
                dic_hashes[path] = sha256(file_data).hexdigest()
                
        except FileNotFoundError:
            print(f"File Not Found Error: '{path}'")
        except IOError:
            print(f"IO Error: '{path}'")
        except Exception as e:
            print(f"An undefined error has occurred: '{path}' -> {e}")
            
    return dic_hashes

if __name__ == "__main__":
    hashes = generate_file_hashes(*file_paths)
    print("results: (path: hash):")
    print(hashes)
