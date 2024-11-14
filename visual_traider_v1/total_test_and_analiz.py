import os
test_data = 'test_data'
result_dir = 'test_results'
variants = os.listdir(test_data)
for variant in variants:
    print(variant)
    folders = os.listdir(test_data+'/'+variant)
    for folder in folders:
        files = os.listdir(result_dir)
        for file in files:
            if folder in file:
                break
        else:
            print(folder)
            os.system(f'python.exe test_env.py {folder} {variant}')
            os.system(f'python.exe auto_analiz_test.py  {folder}')
