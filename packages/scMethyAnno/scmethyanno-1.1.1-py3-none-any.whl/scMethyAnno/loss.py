# --- Python 标准库 ---
import gc
import random
import warnings

# --- 第三方核心科学计算库 ---
import numpy as np
import pandas as pd

# --- 生物信息学与数据分析库 ---
import anndata as ad

# --- 深度学习库 (PyTorch) ---
import torch
import torch.nn as nn
import torch.nn.functional as F


# --- 脚本级别的设置 ---
warnings.filterwarnings("ignore")
gc.collect()

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


class SupConLoss(nn.Module):
    def __init__(self, temperature):
        super().__init__()
        self.temperature = temperature

    def forward(self, features, labels):
        """
        features: tensor [2B, D] (z1 and z2 concatenated)
        labels:   tensor [2B]
        returns:  scalar loss
        """
        B2 = features.shape[0]
        labels = labels.view(-1,1) # -1表示该维度取决于其它维度大小，即转换为列数=1的tensor(从1维变成2维，利于进行标签的比较)
        mask = torch.eq(labels, labels.T).float().to(features.device) # torch.eq, 对两个tensor进行逐元素的比较

        features = F.normalize(features, dim=1)
        sim = torch.matmul(features, features.T) / self.temperature # 计算相似性

        # 数值稳定性处理
        logits_max, _ = torch.max(sim, dim=1, keepdim=True)
        logits = sim - logits_max.detach()

        # 掩码自身匹配
        logits_mask = (torch.ones_like(mask) - torch.eye(B2, device=features.device))
        exp_logits = torch.exp(logits) * logits_mask

        log_prob = logits - torch.log(exp_logits.sum(1, keepdim=True) + 1e-9)
        mean_log_prob_pos = (mask * log_prob).sum(1) / mask.sum(1) # 只取同类的
        loss = - mean_log_prob_pos.mean()
        return loss 
    
    
def subspace_contrastive_loss(subspaces, temperature):
    C, D, H = subspaces.shape
    all_vectors = subspaces.reshape(C * D, H)
    labels = torch.arange(C).repeat_interleave(D).to(subspaces.device)

    # Normalize
    all_vectors = F.normalize(all_vectors, dim=1)
    similarity = torch.matmul(all_vectors, all_vectors.T) / temperature
    loss = F.cross_entropy(similarity, labels)
    return loss


# def subspace_center_contrastive_loss(subspaces, temperature):
#     """
#     对不同类别的子空间中心进行对比，推远不同类别的子空间。
#     subspaces: [C, D, H]，C个类，每类D个基向量，H维。
#     """
#     C, D, H = subspaces.shape
#     centers = subspaces.mean(dim=1)  # [C, H]
#     centers = F.normalize(centers, dim=1)

#     # 计算 pairwise 相似度
#     sim = torch.matmul(centers, centers.T) / temperature  # [C, C]
    
#     # 构造标签
#     labels = torch.arange(C).to(subspaces.device)
    
#     # 计算交叉熵对比损失（排除自身）
#     logits_mask = ~torch.eye(C, dtype=torch.bool, device=subspaces.device)
#     sim = sim[logits_mask].reshape(C, C - 1)
    
#     # 使用 logsumexp 拉开不同类之间距离
#     contrastive_loss = -torch.log(torch.exp(sim).sum(dim=1)).mean()
#     return contrastive_loss
def subspace_center_contrastive_loss(subspaces, temperature):
    """
    使用标准的 InfoNCE (CrossEntropyLoss) 来推远不同类别的中心。
    这会最大化每个类别与自身的相似度，同时最小化与其它类别的相似度。
    
    subspaces: [C, D, H]，C个类，每类D个基向量，H维。
    """
    C, D, H = subspaces.shape
    centers = subspaces.mean(dim=1)  # [C, H]
    centers = F.normalize(centers, dim=1)

    # 计算 pairwise 相似度 (包含自身)
    # sim 矩阵的对角线是“正样本” (sim[i, i])
    # sim 矩阵的非对角线是“负样本” (sim[i, j])
    sim = torch.matmul(centers, centers.T) / temperature  # [C, C]
    
    # 构造标签，[0, 1, 2, ..., C-1]
    # 对于第 i 行的 logits (sim[i, :])，它的正确标签是 i
    labels = torch.arange(C).to(subspaces.device)
    
    # F.cross_entropy 会计算：
    # -log( exp(sim[i, i]) / sum(exp(sim[i, j])) )
    # 这会推动 sim[i, i] 变大，并推动 sim[i, j] (j != i) 变小。
    # 这正是您想要的！
    contrastive_loss = F.cross_entropy(sim, labels)
    
    return contrastive_loss

def combined_subspace_loss(subspaces, alpha, temperature=0.07):
    loss_all = subspace_contrastive_loss(subspaces, temperature)
    loss_center = subspace_center_contrastive_loss(subspaces, temperature)
    return alpha * loss_all + (1 - alpha) * loss_center


def orthogonality_loss(subspaces):
    # subspaces: [C, D, H]
    # 保持正交
    V = F.normalize(subspaces, dim=-1) # [C, D, H]
    gram = torch.matmul(V, V.transpose(-1, -2)) # [C, D, D]
    I = torch.eye(gram.shape[-1], device=subspaces.device).unsqueeze(0)
    loss = F.mse_loss(gram, I.expand_as(gram)) # [C, D, D]
    return loss
    