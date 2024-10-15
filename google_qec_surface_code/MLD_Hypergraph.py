import stim

import networkx as nx
import hypernetx as hnx
import matplotlib.pyplot as plt

import logging
# 设置 logging 配置
# logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

from typing import List, Union, Optional, Tuple, Set, Dict

class MLD_Hypergraph:
    def __init__(self, detector_error_model: stim.DetectorErrorModel):
        self.detector_error_model = detector_error_model
        self.nodes: List[str]
        self.hyperedges: List[List[str]]
        self.weights: List[float]
        
        self.nodes, self.hyperedges, self.weights = self.detector_error_model_to_hypergraph(detector_error_model)

    def get_nodes(self) -> List[str]:
        return self.nodes

    def get_hyperedges(self) -> List[List[str]]:
        return self.hyperedges
    
    def get_weights(self) -> List[float]:
        return self.weights
    
    def get_nodes_number(self) -> int:
        return len(self.nodes)
    
    def get_hyperedges_number(self) -> int:
        return len(self.hyperedges)
    
    def detector_error_model_to_hypergraph(self, detector_error_model: stim.DetectorErrorModel)-> Tuple[List[str], List[List[str]], List[float]]:
        """将错误检测模型转换为超图。

        Args:
            detector_error_model (stim.DetectorErrorModel): 错误检测模型

        Returns:
            Tuple[List[str], List[List[str]], List[float]]: 节点集合和超边集合
        """
        self.detector_number = detector_error_model.num_detectors
        self.logical_observable_number = detector_error_model.num_observables
        
        nodes = self.detector_and_logical_observable_number_to_hypernodes(self.detector_number, self.logical_observable_number)
        hyperedges, weights = self.detector_error_model_to_hyperedge(detector_error_model)
        return nodes, hyperedges, weights

    def detector_and_logical_observable_number_to_hypernodes(self, detector_number: int, logical_observable_number: int, have_logical_observable: bool = False) -> List[str]:
        """获取超图节点集合。

        Args:
            detector_number (int): 错误检测模型中检测器的数量。
            logical_observable_number (int): 错误检测模型中逻辑可观测量的数量。
            have_logical_observable (bool, optional): 是否有逻辑可观测量。默认为False。
            
        Returns:
            List[str]: 超图节点集合。例如["D0","D1","D2","L0","L1"]
        """
        detector_nodes = [f"D{i}" for i in range(detector_number)]
        
        logical_observable_nodes = [f"L{i}" for i in range(logical_observable_number)]
        if have_logical_observable:
            nodes = detector_nodes + logical_observable_nodes
        else:
            nodes = detector_nodes
        
        return nodes

    def detector_error_model_to_hyperedge(self, detector_error_model: stim.DetectorErrorModel) -> Tuple[List[List[str]], List[float]]:
        """将detector_error_model中的error事件转换为超图边。

        Args:
            detector_error_model (stim.DetectorErrorModel): 错误检测模型, 通过stim进行生成。

        Returns:
            Tuple[List[List[str]], List[float]]: 超图边集合。例如[["D0","D1","D2"],["D3","D4","D5"]]
        """
        hyperedges = []
        weights = []
        for error in detector_error_model:
            if error.type == "error":
                error_even = error.targets_copy()
                weight = error.args_copy()[0]
                hyperedge = self.error_even_to_hyperedge(error_even)
                hyperedges.append(hyperedge)
                weights.append(weight)
        return hyperedges, weights

    def error_even_to_hyperedge(self, error_even: List[stim.DemTarget], have_logical_observable: bool = False) -> List[str]:
        """从一个error事件中,转换为一条超图边hyperedge。即错误事件翻转的detector和logical_observable的index。

        Args:
            error_even (List[stim.DemTarget]): 错误事件中的detector或logical_observable对象
            have_logical_observable (bool, optional): 是否有logical_observable作为超图节点. Defaults to False.
            
        Returns:
            List[str]: 超图对应的边. 例如["D0","D1","D2"]
        """
        hyperedge = []
        for flip_object in error_even:
            if flip_object.is_relative_detector_id():
                hyperedge.append(f"D{flip_object.val}")
            elif have_logical_observable and flip_object.is_logical_observable_id():
                hyperedge.append(f"L{flip_object.val}")
        return hyperedge
    
    def to_hypernetx_hypergraph(self) -> hnx.Hypergraph:
        """将超图转换为hypernetx.Hypergraph对象。

        Returns:
            hypernetx.Hypergraph: 超图对象
        """
        hyperedges_number = len(self.hyperedges)
        hypernetx_hyperedges =  [(self.hyperedges[i], {'weight': self.weights[i]}) for i in range(len(hyperedges_number))]
        
        return hnx.Hypergraph(hypernetx_hyperedges)
    
    def draw_bipartite_graph(self, nodes: Union[int, None] = None, hyperedges: Union[int, None] = None) -> None:
        """绘制二部图。

        Args:
            nodes (Union[int, None], optional): 超图的节点. Defaults to None.
            hyperedges (Union[int, None], optional): 超图的边. Defaults to None.
        """
        if nodes is None or hyperedges is None:
            nodes = self.nodes
            hyperedges = self.hyperedges
            
        # 创建一个空的二部图
        B = nx.Graph()

        # 添加节点
        for node in nodes:
            B.add_node(node, bipartite=0)  # 将节点分类为一类

        # 添加超边作为新的节点类型
        for idx, hyperedge in enumerate(hyperedges):
            hyperedge_name = f'edge_{idx}'
            B.add_node(hyperedge_name, bipartite=1)  # 超边作为另一类节点
            for node in hyperedge:
                B.add_edge(hyperedge_name, node)  # 连接超边与它包含的节点

        # 调整布局参数，使节点更加分散
        pos = nx.spring_layout(B, k=0.6, scale=2, iterations=100)

        # 进行绘制
        nx.draw(B, pos, with_labels=True, node_color=['lightblue' if B.nodes[node]['bipartite'] == 0 else 'lightgreen' for node in B], 
                font_size=8, node_size=600, edge_color='gray')

        # 显示图像
        plt.show()