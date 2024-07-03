# Work in prgress 


#import modules 
import pandas as pd 
import glob 
import os

# path of the folder 
path = r'C:\Users\khale\Desktop\temp_out]'

# reading all the CSV files 
filenames = glob.glob(r"C:\Users\khale\Desktop\temp_out]" + "/*.csv") 
print('File names:', filenames) 

all_dfs = pd.DataFrame() #combining all dataframes into 1
for file in filenames: 
    # Check if the file is empty
    if os.path.getsize(file) <= 3:
        print(f"Skipping empty file: {file}")
        continue
    
    # reading CSV files 
    df = pd.read_csv(file)
    
    # Check if the dataframe is empty
    if df.empty:
        print(f"Skipping empty file: {file}")
        continue

    # appending CSV files one by one 
    all_dfs = pd.concat([all_dfs, df], ignore_index=True) 

all_dfs = all_dfs[all_dfs.filter(regex='^(?!Unnamed)').columns]
out_path = r'C:\Users\khale\Desktop\temp_out]\Combined.csv'
all_dfs.to_csv(out_path, index=False)
                                                                                                                                                                                                                                                                                        