import os
import json

start_json = {

}

test_data = 'test_data'
folders_type = os.listdir(test_data)

last_ticker = None
last_price = None

for folder_type in folders_type:
    path_folder_type = os.path.join(test_data,folder_type)
    folder_files = os.listdir(path_folder_type)
    for folder in folder_files:
        path_folder_files = os.path.join(test_data,folder_type,folder)
        folder_files = os.listdir(path_folder_files)
        start_json[folder] = {}
        for file in folder_files:
            ticker,_,price = file.replace('.png','').split('_')
            if last_ticker != ticker:
                start_json[folder][last_ticker]=last_price
            last_ticker = ticker
            last_price = price
        start_json[folder][last_ticker]=last_price
        del start_json[folder][None]
        last_ticker = None
        last_price = None

with open('test_files/last_price.json',mode='x+') as f:
    json.dump(start_json,f)
# print(start_json)