import networkx as nx
import pandas as pd
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import normalized_mutual_info_score

from karateclub.node_embedding.attributed import AE
from karateclub.community_detection.overlapping import DANMF
from karateclub.node_embedding.attributed import ASNE
from karateclub.node_embedding.attributed import BANE
from karateclub.node_embedding.attributed import FeatherNode
from karateclub.node_embedding.attributed import FSCNMF
from karateclub.node_embedding.attributed import MUSAE
from karateclub.node_embedding.attributed import SINE
from karateclub.node_embedding.attributed import TADW
from karateclub.node_embedding.attributed import TENE
from karateclub.community_detection.overlapping import BigClam
from karateclub.community_detection.non_overlapping import EdMot
from karateclub.community_detection.overlapping import EgoNetSplitter
from karateclub.community_detection.non_overlapping import GEMSEC
from karateclub.community_detection.non_overlapping import LabelPropagation
from karateclub.community_detection.overlapping import MNMF
from karateclub.community_detection.overlapping import NNSED
from karateclub.community_detection.non_overlapping import SCD
from karateclub.community_detection.overlapping import SymmNMF
from karateclub.node_embedding.neighbourhood import GraRep
from karateclub.node_embedding.neighbourhood import HOPE
from karateclub.node_embedding.neighbourhood import LaplacianEigenmaps
from karateclub.node_embedding.neighbourhood import NetMF
from karateclub.node_embedding.neighbourhood import NMFADMM
from karateclub.node_embedding.neighbourhood import Node2Vec
from karateclub.node_embedding.neighbourhood import NodeSketch
from karateclub.node_embedding.neighbourhood import RandNE
from karateclub.node_embedding.neighbourhood import Walklets
from karateclub.node_embedding.structural import GraphWave
from karateclub.node_embedding.structural import Role2Vec
from karateclub.graph_embedding import FeatherGraph
from karateclub.graph_embedding import IGE
from karateclub.graph_embedding import GL2Vec
from karateclub.graph_embedding import GeoScattering
from karateclub.graph_embedding import FGSD
from karateclub.graph_embedding import NetLSD
from karateclub.graph_embedding import SF
from karateclub.graph_embedding import Graph2Vec
from karateclub.graph_embedding import LDP

def main():
    """
    Parsing command lines, creating target matrix, fitting DANMF and saving the embedding.
    """
    #读取数据
    #取得结果
    #

    # 读取csv文件
    df = pd.read_csv('Email/email-Eu-core.csv')
    g = nx.from_pandas_edgelist(df, 'from', 'to')
    models = [DANMF(),BigClam(),EdMot(),LabelPropagation(),MNMF(),NNSED(),SCD()]
    #需要参数X
    #,AE(),ASNE(),BANE(),FeatherNode(),FSCNMF(),MUSAE(),SINE(),TADW(),TENE()
    #暂时运行不了的，和运行长时间没有结果的
    #EgoNetSplitter()GEMSEC(),,SymmNMF(),GraRep(),HOPE(),LaplacianEigenmaps(),NetMF(),NMFADMM(),Node2Vec(),NodeSketch(),RandNE()，Walklets(),GraphWave(),Role2Vec(),
    # FeatherGraph(),IGE(),GL2Vec(),GeoScattering(),FGSD(),NetLSD(),SF(),Graph2Vec(),LDP()
    for model in models:
        model = model
        model.fit(g)
        abel = model.get_memberships()
        result_dict = {'node_id': list(abel.keys()), 'community_id': list(abel.values())}
        df = pd.DataFrame.from_dict(result_dict)

        labels_true = pd.read_csv('Email/email-Eu-core-department-labels.csv', header=None)
        labels_pred = df
        labels_true = list(labels_true[1])
        labels_pred = list(labels_pred["community_id"])
        ARI = adjusted_rand_score(labels_true, labels_pred)
        ACC = accuracy_score(labels_true, labels_pred)
        NMI=normalized_mutual_info_score(labels_true, labels_pred)
        print(f"Model: {type(model).__name__}")
        # NMI = Normalized_Mutual_Information(labels_true, labels_pred)
        print("ARI: %f" % (ARI))
        print("ACC: %f" % (ACC))
        print("NMI: %f" % (NMI))

if __name__ == "__main__":
    main()