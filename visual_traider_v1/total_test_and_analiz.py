import os

# data_variant = 'old_data'
# data_variant = 'new_data1'
data_variant = 'new_data2'
folders = os.listdir('test_data/'+data_variant)

for folder in folders:
    print(folder)
    os.system(f'python.exe test_env.py {folder}')
    os.system(f'python.exe auto_analiz_test.py  {folder}')