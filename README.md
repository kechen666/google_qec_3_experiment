# google_qec_3_experiment
尝试复现google 2022年发表在Nature的Suppressing quantum errors by scaling a surface code logical qubit论文，其中使用到了stim模拟器。

## 1. 环境配置

创建新的python环境，使用anaconda创建虚拟环境，并安装相关依赖。

```bash
conda create -n google_qec_decoder python=3.10
conda activate google_qec_decoder

python -m pip install jupyter
python -m pip install stim
python -m pip install numpy
python -m pip install scipy

python -m pip install stimcirq
python -m pip install cirq

python -m pip install networkx
python -m pip install hypernetx
```

详细依赖环境，参考可以参考requirments.txt文件，或者直接使用其进行环境配置：

```bash
conda activate google_qec_decoder
python -m pip install -r requirements.txt
```

其中rust版本为
```bash
rustc -V
rustc 1.81.0 (eeb90cda1 2024-09-04)
```

在python=3.8的情况下，存在依赖问题，考虑将上述环境转移到python=3.10中。
```bash
cirq-core 1.1.0 requires numpy<1.24,>=1.16, but you have numpy 1.24.4 which is incompatible.

ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
hypernetx 2.2.0 requires numpy<2.0,>=1.24.0, but you have numpy 1.23.5 which is incompatible.
```
