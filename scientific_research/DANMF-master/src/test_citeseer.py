"""Fitting a DANMF model."""

from danmf import DANMF
from nanmf_parser import parameter_parser
from nanmf_utils import read_graph, tab_printer, loss_printer

import pandas as pd
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import accuracy_score
from nmi import Normalized_Mutual_Information
from sklearn import metrics

def main():
    """
    Parsing command lines, creating target matrix, fitting DANMF and saving the embedding.
    """
    file = "Citeseer/citeseer_cites"
    kind = "csv"
    layers = [256,64,6] #[3312,256,64,6]
    args = parameter_parser(file,kind,layers)
    tab_printer(args)
    graph = read_graph(args)
    model = DANMF(graph, args)
    model.pre_training()
    model.training()
    if args.calculate_loss:
        loss_printer(model.loss)

    labels_true = pd.read_csv("../input/Citeseer/citeseer_content.csv", header=None)
    labels_pred = pd.read_csv("../output/" + file + "membership." + kind, header=None)
    labels_true = list(labels_true[3705])
    labels_pred = list(labels_pred[1])
    labels_pred = labels_pred[0:3312]
    ARI = adjusted_rand_score(labels_true, labels_pred)
    ACC = accuracy_score(labels_true, labels_pred)
    NMI=metrics.normalized_mutual_info_score(labels_true, labels_pred)

    # NMI = Normalized_Mutual_Information(labels_true, labels_pred)
    print("ARI: %f" % (ARI))
    print("ACC: %f" % (ACC))
    print("NMI: %f" % (NMI))

if __name__ == "__main__":
    main()