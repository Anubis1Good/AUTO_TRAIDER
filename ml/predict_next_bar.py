import torch
from torch import nn
import pandas as pd 


df = pd.read_csv('./Data/SPBFUT.MMU4_T1.txt',sep='\t')
df.drop_duplicates(inplace=True)

df.info()


model = nn.Sequential(
    nn.Linear(),
    nn.ReLU(),
    nn.Linear()
)