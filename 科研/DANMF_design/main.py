"""Fitting a DANMF model."""

from danmf import HDANMF
from parser1 import parameter_parser
from utils import read_graph, tab_printer, loss_printer

def main():
    """
    Parsing command lines, creating target matrix, fitting DANMF and saving the embedding.
    解析命令行，创建目标矩阵，拟合 DANMF 并保存嵌入。
    """
    args = parameter_parser('cora/cora')
    tab_printer(args)
    graph = read_graph(args)
    model = HDANMF(graph, args)
    model.pre_training()
    model.training()
    if args.calculate_loss:
        loss_printer(model.loss)

    model.evaluate_clustering()
    model.visualize_embedding(method='tsne')
    # model.visualize_embedding(method='umap')
    model.plot_loss()

# __name__ 是一个特殊的内置变量，当一个 Python 脚本被直接执行时，__name__ 的值会被设置为 "__main__"。
# 当脚本作为模块被导入到其他脚本时，__name__ 的值将会是模块的名字，而不是 "__main__"。

if __name__ == "__main__":
    main()
