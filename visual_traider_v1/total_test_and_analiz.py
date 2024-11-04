import os

folders = os.listdir('test_data')

for folder in folders:
    print(folder)
    os.system(f'python.exe test_env.py {folder}')
    os.system(f'python.exe auto_analiz_test.py  {folder}')