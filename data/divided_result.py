import json

def process_text_to_json(file_path):
    data = {}
    current_prompt = None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('Prompt'):
                    current_prompt = line
                    data[current_prompt] = {}
                elif line.startswith('Stage') and current_prompt:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        stage_name = parts[0].strip()
                        stage_content = parts[1].strip()
                        data[current_prompt][stage_name] = stage_content
                        
        return data
        
    except FileNotFoundError:
        print(f"Hata: Dosya bulunamadı: {file_path}")
        return None
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
        return None

file_path = r'C:\Users\bitir\OneDrive\Desktop\RetentionDB\prompt_chaining_numeric_based.txt'

json_data = process_text_to_json(file_path)

if json_data:
   
    output_file_path = 'prompt_chainig_numeric_based.json'
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
        
    print(f"Veriler başarıyla {output_file_path} dosyasına kaydedildi.")