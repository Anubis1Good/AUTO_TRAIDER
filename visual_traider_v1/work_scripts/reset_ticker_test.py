import os

old_ticker = 'ST1'
new_ticker = 'ST1a'
path_result = 'test_results'
files = os.listdir(path_result)

for file in files:
    old_path = os.path.join(path_result,file)
    new_path = os.path.join(path_result,file.replace(old_ticker,new_ticker))
    os.rename(old_path,new_path)