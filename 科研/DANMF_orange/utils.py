"""Data reading utilities."""
'''数据读取实用程序'''

import pandas as pd
import networkx as nx
from texttable import Texttable

def read_graph(args):
    """
    Method to read graph and create a target matrix with matrix powers.
    :param args: Arguments object.
    读取图形并创建具有矩阵幂的目标矩阵的方法。:p aram args： Arguments 对象。
    """
    print("\nTarget matrix creation started.\n")
    graph = nx.from_edgelist(pd.read_csv(args.edge_path).values.tolist())
    return graph

def tab_printer(args):
    """
    Function to print the logs in a nice tabular format.
    :param args: Parameters used for the model.
    以漂亮的表格格式打印日志的函数。:param args：用于模型的参数。
    """
    args = vars(args)
    keys = sorted(args.keys())
    t = Texttable()
    t.add_rows([["Parameter", "Value"]])
    t.add_rows([[k.replace("_", " ").capitalize(), args[k]] for k in keys])
    print(t.draw())

def loss_printer(losses):
    """
    Printing the losses for each iteration.
    :param losses: List of losses in each iteration.
    打印每次迭代的损失。:param losses：每次迭代中的损失列表。
    """
    t = Texttable()
    t.add_rows([["Iteration",
                 "Reconstrcution Loss I.",
                 "Reconstruction Loss II.",
                 "Regularization Loss"]])
    t.add_rows(losses)
    print(t.draw())
