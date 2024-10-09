# google_qec_3_experiment
尝试复现google 2022年发表在Nature的Suppressing quantum errors by scaling a surface code logical qubit论文，其中使用到了stim模拟器。

## 1. 环境配置

创建新的python环境，使用anaconda创建虚拟环境，并安装相关依赖。

```bash
conda create -n google_qec python=3.8
conda activate google_qec 

python -m pip install jupyter
python -m pip install stim
python -m pip install numpy
python -m pip install scipy

python -m pip install stimcirq
python -m pip install cirq
```
详细依赖环境，参考可以参考requirments.txt文件，或者直接使用其进行环境配置：

```bash
conda activate google_qec 
python -m pip install -r requirements.txt
```