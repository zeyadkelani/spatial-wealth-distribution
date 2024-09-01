import os
import json
import pandas as pd

def convert_json_to_excel(file_path, output_dir):
    # Load JSON file
    with open(file_path, 'r', encoding='utf-8-sig') as json_file:
        data = json.load(json_file)
    
    # Extract "places" data from JSON
    places_data = data["places"]
    
    # Convert "places" data to DataFrame
    df = pd.json_normalize(places_data)
    
    # Extract file and directory names
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    dir_name = os.path.basename(os.path.dirname(file_path))
    
    # Generate new file name
    new_file_name = f'{file_name}_{dir_name}.csv'
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert DataFrame to Excel
    excel_path = os.path.join(output_dir, new_file_name)
    df.to_csv(excel_path, index=False)
    
    print(f'Converted "{file_path}" to "{excel_path}"')

def traverse_directory(directory, output_dir):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('sortedPlaces.json'):
                convert_json_to_excel(file_path, output_dir)


directory_path = r'C:\Users\khale\Desktop\Temp_out2'  
output_directory = r"C:\Users\khale\Desktop\Temp_out"   

traverse_directory(directory_path, output_directory)