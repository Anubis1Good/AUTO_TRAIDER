import os
from time import time
from multiprocessing import Pool
test_data = 'test_data'
result_dir = 'test_results'
bot_name = 'PTA5_MHP'
variants = os.listdir(test_data)
stock_group = '_'
# stock_group = 'MXI'

def mult_test(folder,variant):
    files = os.listdir(result_dir)
    for file in files:
        if folder in file:
            break
    else:
        print(folder)
        os.system(f'python.exe test_smart_env.py {folder} {variant} {bot_name} {stock_group}')
a = time()
if __name__ == '__main__':
    for variant in variants:
        print(variant)
        folders = os.listdir(test_data+'/'+variant)
        args = zip(folders,[variant]*len(folders))
        with Pool(6) as p:
            p.starmap(mult_test,args)



print(time()-a)