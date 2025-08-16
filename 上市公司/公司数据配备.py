import pandas as pd
import numpy as np
import matplotlib as plt

Data = pd.read_excel("数据.xlsx",sheet_name = "Sheet1")
data = Data["Year"]
print(data)