import anndata as ad
import numpy as np
import pandas as pd
import scanpy as sc
import scipy.stats

import torch
from torch.utils.data import Dataset, DataLoader, TensorDataset

import random
from sklearn.preprocessing import LabelEncoder

import scipy
import gc
import os


def setup_seed(seed):
    """
    Set random seed.

    Parameters
    ----------
    seed
        Number to be set as random seed for reproducibility.

    """
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

setup_seed(123)

def get_newwindow_matrix(adata, num_goal):
    """生成模拟的更大bins下划分的甲基化矩阵
    
    Args:
        adata(anndata): 待处理的anndata对象
        num_goal(int): 求均值的列数 
        
    Returns:
        wind_matrix(np.array): 模拟甲基化矩阵
        feature_names: 模拟数据的特征名
    """
    # 提取染色体信息
    chrom_df = adata.var.index.to_series().str.split('_', expand=True)
    chrom_df.columns = ['chr', 'start', 'end']
    
    # 初始化结果存储
    total_cells = adata.shape[0]
    all_windows = []
    feature_names = []
    
    # 对每个染色体进行处理
    for chr_name in chrom_df['chr'].unique():
        # 获取当前染色体的特征索引
        chr_indices = np.where(chrom_df['chr'] == chr_name)[0]
        chr_features = adata.var_names[chr_indices].tolist()
        chr_data = adata[:, chr_indices].X
        
        if scipy.sparse.issparse(chr_data):
            chr_data = chr_data.toarray()  # 确保数据为密集矩阵
            
        # 计算窗口数量
        num_features = len(chr_indices)
        full_windows = num_features // num_goal
        remaining = num_features % num_goal
        
        # 处理完整窗口
        if full_windows > 0:
            # 重塑数据以一次性计算所有完整窗口的均值
            reshaped_data = chr_data[:, :full_windows * num_goal].reshape(
                total_cells, full_windows, num_goal
            )
            window_means = np.nanmean(reshaped_data, axis=2)  # 形状：(cells, windows)
            
            # 添加到结果列表
            all_windows.append(window_means)
            
            # 生成特征名
            for i in range(full_windows):
                start_idx = i * num_goal
                feature_names.append(f"{chr_features[start_idx]}_win{i+1}")
        
        # 处理剩余特征
        if remaining > 0:
            remaining_data = chr_data[:, full_windows * num_goal:]
            remaining_mean = np.nanmean(remaining_data, axis=1, keepdims=True)
            all_windows.append(remaining_mean)
            feature_names.append(f"{chr_features[full_windows*num_goal]}_win_remaining")
    
    # 合并所有窗口矩阵
    if all_windows:
        wind_matrix = np.hstack(all_windows)
    else:
        wind_matrix = np.empty((total_cells, 0), dtype=np.float32)
    
    return wind_matrix, feature_names

def fill_nan_with_median(matrix):
    medians = np.nanmedian(matrix, axis=0)
    nan_mask = np.isnan(matrix)
    matrix = np.where(nan_mask, medians, matrix)
    return matrix


def data_preprocessing(adata1, adata2, target_colname, bin_fold = 10, fpeak = 0.01):

    if scipy.sparse.issparse(adata1.X):
        adata1.X = adata1.X.toarray()
    if scipy.sparse.issparse(adata2.X):
        adata2.X = adata2.X.toarray()  
      
    adata_concat = ad.concat([adata1, adata2], label = 'data_batch', keys = ['adata1', 'adata2'])
    
    # 过滤全为空的特征
    nan_ratio = np.isnan(adata_concat.X).mean(axis=0)
    adata_concat = adata_concat[:,nan_ratio!=1]


    # 先求均值再填补，保留新的特征名
    # 得到新矩阵
    tmp_mtx, feature_names = get_newwindow_matrix(adata_concat, bin_fold)
    # 填补
    tmp_mtx = fill_nan_with_median(tmp_mtx)
    # 质量控制
    filter_res = sc.pp.filter_genes(data = tmp_mtx, min_cells = np.ceil(fpeak * adata_concat.shape[0]))
    tmp_mtx = tmp_mtx[:, filter_res[0]]
    feature_names = [name for name, keep in zip(feature_names, filter_res[0]) if keep]

    adata_concat.obsm[str(bin_fold)+'X'] = tmp_mtx
    adata_concat.uns[f'{bin_fold}X_features'] = feature_names
            
            
    adata_concat.X = fill_nan_with_median(adata_concat.X)
       
    adata1 = adata_concat[adata_concat.obs['data_batch'] == 'adata1']
    adata1.uns = adata_concat.uns
    adata2 = adata_concat[adata_concat.obs['data_batch'] == 'adata2']
    adata2.uns = adata_concat.uns

    return adata1, adata2    



def combined_f_test(adata_train, adata_concat, target_colname, num_features, obsm_name=None):
    # 转为稠密，得到特征名
    if obsm_name is None:
        if scipy.sparse.issparse(adata_train.X) or isinstance(adata_train.X, pd.DataFrame):
            tmp_data = adata_train.X.toarray()
        else:
            tmp_data = adata_train.X
        var_names = adata_train.var_names
    else:
        
        tmp_data = adata_train.obsm[obsm_name].copy()
        var_names = np.array(range(tmp_data.shape[1]))

    # 准备每个类别下的数据
    cell_annots = adata_train.obs[target_colname].tolist()
    uniq_celltypes = set(cell_annots)
    array_list = []
    for celltype in uniq_celltypes:
        idx = np.where(np.array(cell_annots) == celltype)[0].tolist()
        array_list.append(tmp_data[idx, :])

    # 进行F-test
    F, p = scipy.stats.f_oneway(*array_list)
    F_updated = np.nan_to_num(F)
    sorted_idx = np.argsort(F_updated)[-num_features:]
    features = var_names[sorted_idx].tolist()

    features.sort()

     # 得到筛选后的矩阵
    if obsm_name is None:
        result = adata_concat[:, features].X.copy()
        if scipy.sparse.issparse(result):
            result = result.toarray()
    else:
        tmp_adata = adata_concat.obsm[obsm_name]
        if scipy.sparse.issparse(tmp_adata):
            tmp_adata = tmp_adata.toarray()
        result = tmp_adata[:, features].copy()

    return features, sorted_idx, result


class MultiBranchDataset_2branch(Dataset):
    def __init__(self, data_x1, data_x2, labels=None):
        """
        初始化双分支数据集（兼容有/无标签模式）
        :param data_x1: 输入 x1 数据 (N, D1)
        :param data_x2: 输入 x2 数据 (N, D2)
        :param labels: 标签 (N,)，训练集传值，测试集默认None（无标签）
        """
        self.data_x1 = data_x1
        self.data_x2 = data_x2
        self.labels = labels  

    def __len__(self):
        return len(self.data_x1)

    def __getitem__(self, idx):
        """
        根据索引获取样本（适配有/无标签）
        :param idx: 索引
        :return: 训练集返回 (x1, x2, label)；测试集返回 (x1, x2)
        """
        # 处理NaN/Inf值，避免tensor报错
        x1 = torch.tensor(self.data_x1[idx], dtype=torch.float32)
        x2 = torch.tensor(self.data_x2[idx], dtype=torch.float32)
        
        # 有标签则返回label，无标签仅返回x1/x2
        if self.labels is not None:
            label = torch.tensor(self.labels[idx], dtype=torch.long)
            return x1, x2, label
        else:
            return x1, x2
        

def preprocess_data_2branch(X1, X2, y_train, train_index, test_index, batch_size, return_label_encoder = False):
    '''
    数据预处理函数，返回训练和测试 DataLoader、模型输入维度和类别数
    '''
    setup_seed(123)
    
    num_classes = len(set(y_train))

    # 划分训练测试集
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)

    X1_train = X1[train_index,:].copy()
    X1_test = X1[test_index,:].copy()
    X2_train = X2[train_index,:].copy()
    X2_test = X2[test_index,:].copy()

    # 创建 DataLoader
    train_dataset = MultiBranchDataset_2branch(X1_train, X2_train, y_train_encoded)
    test_dataset = MultiBranchDataset_2branch(X1_test, X2_test)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, drop_last=False)


    return train_loader, test_loader, num_classes, label_encoder
    