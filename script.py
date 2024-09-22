import json
import os
import shutil
from datetime import datetime
from memory_profiler import profile
    
def load_sample(path: str):
    """Generator to yield lines from the file one at a time."""
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
           yield line
    
def generate_json(data) -> dict:
    total_sent = {}
    for line in data:
        parts = line.strip().split()
        if len(parts) < 3:
               continue
    
        name = parts[0]
        amount_str = parts[2].replace('€', '').replace('â‚¬', '').strip()
    
        try:
            amount = float(amount_str)
        except ValueError:
            continue
    
        if name in total_sent:
            total_sent[name] += amount
        else:
            total_sent[name] = amount
    result = ({"name": name, "total_sent": total} for name, total in total_sent.items())
    return list(result)
    
def save_result(path: str, result: dict) -> None:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"result_sample_{timestamp}.json"
    output_path = os.path.join(path, filename)
    with open(output_path, 'w') as json_file:
        json.dump(result, json_file, indent=4)
    
def process_files(source_dir: str = "source", result_dir: str = "result", archived_dir: str = "archived") -> None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
        source_dir = os.path.join(script_dir, source_dir)
        result_dir = os.path.join(script_dir, result_dir)
        archived_dir = os.path.join(script_dir, archived_dir)
    
        os.makedirs(result_dir, exist_ok=True)
        os.makedirs(archived_dir, exist_ok=True)
    
        for filename in os.listdir(source_dir):
            if filename.endswith('.txt'):
                data_path = os.path.join(source_dir, filename)
                data = load_sample(data_path)
                result = generate_json(data)
                save_result(result_dir, result)
                shutil.move(data_path, os.path.join(archived_dir, filename))
    
@profile
def main():
    process_files()
    
if __name__ == "__main__":
        main()