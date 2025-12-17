#  Завдання 1: Аналізатор лог-файлів
log_file_path = "apache_logs.txt"
def analyze_log_file(log_file_path):
    stats = {}
    try:
        with open(log_file_path, "r") as file:
            for line in file:
                parts = line.split('"')
                if len(parts) > 2:
                    code = parts[2].strip().split()[0]
                    
                    if code.isdigit():
                        stats[code] = stats.get(code, 0) + 1
                        
    except (FileNotFoundError, IOError):
        print(f"Помилка: Файл '{log_file_path}' не знайдено")
    return stats
  

results = analyze_log_file(file_path)

print("Результати аналізу (Код: Кількість):")
    for code, count in sorted(results.items()):
        print(f"{code}: {count}")
