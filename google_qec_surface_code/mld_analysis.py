import stim
import MLD

import logging
# 设置 logging 配置
# logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
from typing import List, Union, Optional, Tuple, Set, Dict

def add_neightboring_nodes(currently_calculated_nodes: List[str], current_distribution_related_nodes: Set[str], detector_connectivity:Dict[str:List[int]]) -> Set[str]:
    
    for node in currently_calculated_nodes:
        for i in detector_connectivity[node]:
            current_distribution_related_nodes.add(f"D{i}")
    return current_distribution_related_nodes

def get_current_neightboring_nodes_new_nodes_lenth(current_neighboring_nodes: List[str], current_distribution_related_nodes: Set[str], detector_connectivity:Dict[str:List[int]]) -> Dict[str:int]:
    current_neightboring_nodes_new_nodes_lenth = {}
    # print("current_neighboring_nodes:",current_neighboring_nodes)
    for neighbor in current_neighboring_nodes:
        ## 当前相邻节点的相邻节点数
        current_neighboring_neighboring_nodes = detector_connectivity[neighbor]
        ## 新增的节点
        new_nodes = [f"D{i}" for i in current_neighboring_neighboring_nodes if f"D{i}" not in current_distribution_related_nodes]
        # print(neighbor, new_nodes)
        current_neightboring_nodes_new_nodes_lenth[neighbor] = len(new_nodes)
    return current_neightboring_nodes_new_nodes_lenth

def Greedy_MLD_max_dimensions(detector_error_model: stim.DetectorErrorModel):
    """基于贪心的思路, 利用MLD来解码, 我们希望找到过程中所涉及的最大规模计算

    Args:
        detector_error_model (stim.DetectorErrorModel): 含噪surface code电路对应的错误检测模型。
    
    Returns:
        int: 计算过程的最大概率分布规模
    """
    max_distribution_dimensions = 0
    max_distribution_dimensions_number = 0
    ml_decoder = MLD.MaxLikelihoodDecoder(detector_error_model=detector_error_model)
    detector_connectivity = ml_decoder.compute_detector_connectivity(have_logical_observable=False)
    detector_connectivity_length = {k:len(v) for k,v in detector_connectivity.items()}
    ## 当前计算得到的维度
    current_distribution_dimensions = 0
    currently_calculated_nodes = []
    current_neighboring_nodes = []
    current_distribution_related_nodes = set()

    for step in range(ml_decoder.detector_number):
        logger.debug(f"step: {step}")
        if step == 0:
            detector = min(detector_connectivity_length, key=detector_connectivity_length.get)
        else:
            current_neightboring_nodes_new_nodes_lenth = get_current_neightboring_nodes_new_nodes_lenth(current_neighboring_nodes, current_distribution_related_nodes, detector_connectivity)
            detector = min(current_neightboring_nodes_new_nodes_lenth, key=current_neightboring_nodes_new_nodes_lenth.get)
            
        logger.debug(f"detector is:{detector}")
        
        currently_calculated_nodes.append(detector)
        current_distribution_related_nodes.add(detector)
        current_distribution_related_nodes = add_neightboring_nodes(currently_calculated_nodes, current_distribution_related_nodes, detector_connectivity)
        current_neighboring_nodes = [i for i in current_distribution_related_nodes if i not in currently_calculated_nodes]
        
        current_distribution_dimensions = (len(current_distribution_related_nodes) - len(currently_calculated_nodes))
        if current_distribution_dimensions> max_distribution_dimensions:
            max_distribution_dimensions = current_distribution_dimensions
            max_distribution_dimensions_number= 1
        elif current_distribution_dimensions == max_distribution_dimensions:
            max_distribution_dimensions_number += 1

        logger.debug(f"current_distribution_dimensions: {current_distribution_dimensions}, size is: {2**current_distribution_dimensions}")
        logger.debug(f"currently_calculated_nodes: {currently_calculated_nodes}")
        logger.debug(f"current_distribution_related_nodes: {current_distribution_related_nodes}")
        logger.debug(f"current_neighboring_nodes: {current_neighboring_nodes}")

    logger.debug(f"max_distribution_dimensions:{max_distribution_dimensions}")
    return max_distribution_dimensions

def MLD_max_dimensions(detector_error_model: stim.DetectorErrorModel) ->int:
    """基于序列顺序的思路, 利用MLD来解码, 我们希望找到过程中所涉及的最大规模计算

    Args:
        detector_error_model (stim.DetectorErrorModel): 含噪surface code电路对应的错误检测模型。

    Returns:
        int: 计算过程的最大概率分布规模
    """
    max_distribution_dimensions = 0
    max_distribution_dimensions_number = 0
    ml_decoder = MLD.MaxLikelihoodDecoder(detector_error_model=detector_error_model)
    detector_connectivity = ml_decoder.compute_detector_connectivity(have_logical_observable=False)
    detector_connectivity_length = {k:len(v) for k,v in detector_connectivity.items()}
    ## 当前计算得到的维度
    current_distribution_dimensions = 0
    currently_calculated_nodes = []
    current_neighboring_nodes = []
    current_distribution_related_nodes = set()
    for step in range(ml_decoder.detector_number):
        logger.debug(f"step: {step}")
        ## 当前执行的节点，就是当前步骤索引对应的检测器
        detector = f"D{step}"
        logger.debug(f"detector is:{detector}")
        currently_calculated_nodes.append(detector)
        current_distribution_related_nodes.add(detector)
        current_distribution_related_nodes = add_neightboring_nodes(currently_calculated_nodes, current_distribution_related_nodes, detector_connectivity)
        current_neighboring_nodes = [i for i in current_distribution_related_nodes if i not in currently_calculated_nodes]
        
        current_distribution_dimensions = (len(current_distribution_related_nodes) - len(currently_calculated_nodes))
        if current_distribution_dimensions> max_distribution_dimensions:
            max_distribution_dimensions = current_distribution_dimensions
            max_distribution_dimensions_number= 1
        elif current_distribution_dimensions == max_distribution_dimensions:
            max_distribution_dimensions_number += 1

        logger.debug(f"current_distribution_dimensions: {current_distribution_dimensions}, size is: {2**current_distribution_dimensions}")
        logger.debug(f"currently_calculated_nodes: {currently_calculated_nodes}")
        logger.debug(f"current_distribution_related_nodes: {current_distribution_related_nodes}")
        logger.debug(f"current_neighboring_nodes: {current_neighboring_nodes}")
        
    logger.debug(f"max_distribution_dimensions:{max_distribution_dimensions}")
    return max_distribution_dimensions