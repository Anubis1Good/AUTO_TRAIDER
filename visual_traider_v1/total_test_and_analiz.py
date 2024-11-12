import os

test_data = 'test_data'
variants = os.listdir(test_data)
for variant in variants:
    folders = os.listdir(test_data+'/'+variant)
    for folder in folders:
        print(folder)
        os.system(f'python.exe test_env.py {folder} {variant}')
        os.system(f'python.exe auto_analiz_test.py  {folder}')
