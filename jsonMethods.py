import json


def write_to_json(key, value, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            data[key] = value
            f.close()
        except FileNotFoundError:
            newFile = open(file_path, 'x')
            newFile.close()
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.close()

def read_from_json(key, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            value = data[key]
            f.close()
            return value
        except FileNotFoundError:
            print(f'No JSON file found in {file_path}.')
