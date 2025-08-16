"""Parsing the model parameters."""

import argparse


def parameter_parser():
    """
    A method to parse up command line parameters.
    By default it gives an embedding of the Twitch Brasilians dataset.
    The default hyperparameters give a good quality representation without grid search.
    Representations are sorted by node identifiers.

    一种解析命令行参数的方法。默认情况下，它提供 Twitch Brasilians 数据集的嵌入。
    默认超参数在没有网格搜索的情况下提供高质量的表示。表示按节点标识符排序。
    """

    # 创建 ArgumentParser 实例
    # 为这个程序添加了描述 "Run DANMF."，用于在 --help 选项时显示
    parser = argparse.ArgumentParser(description="Run DANMF.")

    # 数据路径参数
    # --edge-path：输入数据的路径；nargs="?" 表示该参数可选‘help 用于 --help 选项时的提示信息。
    parser.add_argument("--edge-path",
                        nargs="?",
                        default="./input/ptbr_edges.csv",
                        help="Edge list csv.")

    # --output-path：指定嵌入后的数据存储路径
    parser.add_argument("--output-path",
                        nargs="?",
                        default="./output/ptbr_danmf.csv",
                        help="Target embedding csv.")

    # --membership-path：指定聚类成员关系的 JSON 文件路径
    parser.add_argument("--membership-path",
                        nargs="?",
                        default="./output/ptbr_membership.json",
                        help="Cluster membership json.")

    # 模型训练参数
    # --iterations：DANMF 训练的总迭代次数
    parser.add_argument("--iterations",
                        type=int,
                        default=100,
                        help="Number of training iterations. Default is 100.")

    # --pre-iterations：逐层预训练
    parser.add_argument("--pre-iterations",
                        type=int,
                        default=100,
                        help="Number of layerwsie pre-training iterations. Default is 100.")

    # --seed：用于 sklearn 预训练的随机种子
    parser.add_argument("--seed",
                        type=int,
                        default=42,
                        help="Random seed for sklearn pre-training. Default is 42.")

    # --lamb：正则化参数（lambda）
    parser.add_argument("--lamb",
                        type=float,
                        default=0.01,
                        help="Regularization parameter. Default is 0.01.")

    # --layers：指定神经网络的隐藏层维度
    # nargs="+" 表示这个参数可以传入 多个数值，用空格分隔
    parser.add_argument("--layers",
                        nargs="+",
                        type=int,
                        help="Layer dimensions separated by space. E.g. 128 64 32.")

    # 损失计算选项
    # 这两个参数是互斥的，只有一个生效，默认情况是 False（不计算损失
    # --calculate-loss：如果在命令行中添加这个参数
    parser.add_argument("--calculate-loss",
                        dest="calculate_loss",
                        action="store_true")

    # --not-calculate-loss：如果添加这个参数
    parser.add_argument("--not-calculate-loss",
                        dest="calculate_loss",
                        action="store_false")

    # 设定默认值 calculate_loss=False，即如果用户没有显式传递 --calculate-loss
    parser.set_defaults(calculate_loss=True)

    parser.set_defaults(layers=[32, 8])

    # 解析参数
    return parser.parse_args()
