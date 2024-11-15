import os
test_data = 'test_data'
result_dir = 'test_results'
bot_name = 'PTA2_DDC_5'
variants = os.listdir(test_data)
# stock_group = '_'
stock_group = 'MXI'
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
            os.system(f'python.exe test_env.py {folder} {variant} {bot_name} {stock_group}')
            os.system(f'python.exe auto_analiz_test.py  {folder} {bot_name}')
