# Завдання 3: Фільтрація IP-адрес з файлу

def filter_ips(input_file_path, output_file_path, allowed_ips):
    ip_counts = {}

    try:
        with open(input_file_path, "r", encoding="utf-8") as infile:
            for line in infile:
                parts = line.split()
                
                if parts:
                    ip = parts[0]
                    
                    if ip in allowed_ips:
                        ip_counts[ip] = ip_counts.get(ip, 0) + 1
        
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for ip, count in ip_counts.items():
                outfile.write(f"{ip} - {count}\n")
        
        print("Succesful, results in: {output_file_path}")

    except FileNotFoundError:
        print("Error, '{input_file_path}' not found.")
    except IOError:
        print("Error was found. (IOError).")

allowed_ips = [
    "83.149.9.216",
    "93.114.45.13",
    "50.16.19.13"
]

input_log = "apache_logs.txt"
output_log = "filtered_ips.txt"

filter_ips(input_log, output_log, allowed_ips)
