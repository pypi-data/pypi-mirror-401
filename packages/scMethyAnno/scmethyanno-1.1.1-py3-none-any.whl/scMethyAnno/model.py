# --- Python 标准库 ---
import os
import gc
import random
import warnings

# --- 第三方核心科学计算库 ---
import numpy as np
import pandas as pd
import scipy.stats  # 只导入需要的子模块

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



class CrossAttention(nn.Module):
    def __init__(self, query_dim, context_dim, dropout_rate, embedding_dim = 64, head_dim=64, num_heads=1):
        """
        改进的交叉注意力模块，将特征维度视为序列元素。

        Args:
            query_feature_dim (int): 查询输入张量的原始特征维度 (例如，feat1的维度)
            context_feature_dim (int): 上下文输入张量的原始特征维度 (例如，feat2的维度)
            embedding_dim (int): 每个特征元素将被映射到的嵌入维度
            dropout_rate (float): Dropout比率
            head_dim (int): 每个注意力头的维度
            num_heads (int): 注意力头的数量
        """
        super().__init__()

        self.query_feature_dim = query_dim
        self.context_feature_dim = context_dim
        self.embedding_dim = embedding_dim
        self.num_heads = num_heads
        self.head_dim = head_dim
        self.scale = head_dim ** -0.5
        
        inner_dim = num_heads * head_dim # 每个头的维度 * 头数量

        # 线性层用于将 (batch_size, feature_dim) -> (batch_size, feature_dim, embedding_dim)
        # 注意：这里 query 和 context 可能来自不同维度，所以需要两个独立的映射层
        self.query_to_embedding = nn.Linear(1, embedding_dim) # 每个独立的特征值映射到embedding
        self.context_to_embedding = nn.Linear(1, embedding_dim)

        # 用于生成Q, K, V的线性层
        # 现在 Q, K, V 的输入维度是 embedding_dim
        self.to_q = nn.Linear(embedding_dim, inner_dim, bias=False)
        self.to_k = nn.Linear(embedding_dim, inner_dim, bias=False)
        self.to_v = nn.Linear(embedding_dim, inner_dim, bias=False)

        # 最终输出的线性层
        # 输出应匹配原 query_feature_dim，但这里是融合后的embedding_dim，
        # 如果需要保持原始query_feature_dim，则需要额外映射。
        # 这里假设输出的每个特征元素是embedding_dim
        self.to_out = nn.Sequential(
            nn.Linear(inner_dim, embedding_dim), # 从合并的头维度映射回embedding_dim
            nn.Dropout(dropout_rate)
        )
        
        # 后面还需要一个将 (batch_size, feature_dim, embedding_dim) 变回 (batch_size, feature_dim) 的层
        self.output_to_original_dim = nn.Linear(embedding_dim, 1)

        # 位置编码 (针对 feature_dim 维度)
        # query 和 context 可能有不同的 feature_dim，所以需要两个独立的 Positional Encoding
        # 注意：这里是可学习的位置编码，形状为 (feature_dim, embedding_dim)
        self.pos_enc_query = nn.Parameter(torch.randn(query_dim, embedding_dim))
        self.pos_enc_context = nn.Parameter(torch.randn(context_dim, embedding_dim))
        
        # FFN 和 LayerNorm 应该作用在 embedding_dim 上
        self.norm_query = nn.LayerNorm(embedding_dim)
        self.norm_context = nn.LayerNorm(embedding_dim)
        self.ffn = nn.Sequential(
            nn.LayerNorm(embedding_dim),
            nn.Linear(embedding_dim, embedding_dim * 4),
            nn.GELU(),
            nn.Dropout(dropout_rate),
            nn.Linear(embedding_dim * 4, embedding_dim)
        )

    def forward(self, query, context):
        """
        Args:
            query (torch.Tensor): 查询张量，形状为 [B, query_feature_dim]
            context (torch.Tensor): 上下文张量，形状为 [B, context_feature_dim]
            
        Returns:
            torch.Tensor: 更新后的查询张量，形状为 [B, query_feature_dim] (融合后，维度与原始query一致)
        """
        # --- 1. 将输入特征转换为序列形式并应用位置编码 ---
        
        # query: [B, query_feature_dim] -> [B, query_feature_dim, 1]
        query_expanded = query.unsqueeze(-1) 
        # [B, query_feature_dim, 1] -> [B, query_feature_dim, embedding_dim]
        query_seq = self.query_to_embedding(query_expanded) + self.pos_enc_query
        
        # context: [B, context_feature_dim] -> [B, context_feature_dim, 1]
        context_expanded = context.unsqueeze(-1)
        # [B, context_feature_dim, 1] -> [B, context_feature_dim, embedding_dim]
        context_seq = self.context_to_embedding(context_expanded) + self.pos_enc_context

        # 记录原始的 query_seq 用于残差连接，以及原始的 query 用于最终输出维度匹配
        residual_query_seq = query_seq
        
        # --- 2. 归一化输入序列 ---
        query_seq = self.norm_query(query_seq)
        context_seq = self.norm_context(context_seq)

        # --- 3. 计算 Q, K, V ---
        # Q: [B, query_feature_dim, embedding_dim] -> [B, query_feature_dim, inner_dim]
        # K, V: [B, context_feature_dim, embedding_dim] -> [B, context_feature_dim, inner_dim]
        q = self.to_q(query_seq)
        k = self.to_k(context_seq)
        v = self.to_v(context_seq)

        # 拆分成多个头
        # [B, seq_len, inner_dim] -> [B, num_heads, seq_len, head_dim]
        q = q.view(q.shape[0], q.shape[1], self.num_heads, self.head_dim).transpose(1, 2)
        k = k.view(k.shape[0], k.shape[1], self.num_heads, self.head_dim).transpose(1, 2)
        v = v.view(v.shape[0], v.shape[1], self.num_heads, self.head_dim).transpose(1, 2)
        
        # --- 4. 计算注意力分数 ---
        # attention_scores: [B, num_heads, query_seq_len, context_seq_len]
        attention_scores = torch.matmul(q, k.transpose(-1, -2)) * self.scale
        attention_probs = attention_scores.softmax(dim=-1)       
        
        # attention_output: [B, num_heads, query_seq_len, head_dim]
        attention_output = torch.matmul(attention_probs, v)
        
        # --- 5. 合并多头的结果 ---
        # [B, num_heads, query_seq_len, head_dim] -> [B, query_seq_len, num_heads, head_dim]
        attention_output = attention_output.transpose(1, 2).contiguous() 
        # [B, query_seq_len, num_heads, head_dim] -> [B, query_seq_len, inner_dim]
        attention_output = attention_output.view(attention_output.shape[0], attention_output.shape[1], -1)

        # [B, query_seq_len, inner_dim] -> [B, query_seq_len, embedding_dim]
        attention_output = self.to_out(attention_output) 
        
        # --- 6. 残差连接和FFN ---
        x = residual_query_seq + attention_output # [B, query_feature_dim, embedding_dim]
        x = x + self.ffn(x) # [B, query_feature_dim, embedding_dim]

        # --- 7. 将融合后的嵌入序列转换回原始特征维度 ---
        # [B, query_feature_dim, embedding_dim] -> [B, query_feature_dim, 1]
        final_output = self.output_to_original_dim(x)
        # [B, query_feature_dim, 1] -> [B, query_feature_dim]
        final_output = final_output.squeeze(-1)

        return final_output

    
def projection_distance(x, subspace):
    # x: [B, H], subspace: [D, H]
    # 投影矩阵：P = U.T @ U
    # proj_x = x @ P.T
    P = subspace.T @ subspace  # [H, H]
    x_proj = x @ P  # [B, H]
    dist = F.mse_loss(x_proj, x, reduction='none').sum(dim=-1)  # 投影误差
    return dist

class PrototypeSubspace(nn.Module):
    def __init__(self, num_classes, subspace_dim, hidden_dim):
        super().__init__()
        self.num_classes = num_classes
        self.subspace_dim = subspace_dim
        self.hidden_dim = hidden_dim

        # 类别的子空间表示：[num_classes, subspace_dim, hidden_dim]
        self.subspaces = nn.Parameter(torch.randn(num_classes, subspace_dim, hidden_dim))
        nn.init.orthogonal_(self.subspaces.view(-1, hidden_dim))  # 初始化每个子空间为正交向量组
        
    def forward(self, x):
        """
        输入：
            x: [B, hidden_dim]  --- 样本嵌入表示
        输出：
            logits: [B, num_classes] --- 类别相似性得分
        """
        B = x.size(0)

        subspaces = self.subspaces  # [C, D, H]

        # 投影距离：计算 fused_feat 到每类原型子空间的投影误差
        logits = []
        for c in range(self.num_classes):
            dist = projection_distance(x, subspaces[c])  # [B]
            logits.append(-dist)  # 越小越相似
        logits = torch.stack(logits, dim=1)  # [B, C]
        
        return logits  # 可接 CrossEntropyLoss
class MultiScalePrototypeModel(nn.Module):
    def __init__(self, input_dims, num_classes, hidden_dim, dropout_rate, subspace_dim):
        super().__init__()

        self.encoder1 = nn.Sequential(
            nn.Linear(input_dims[0], hidden_dim*4),
            nn.BatchNorm1d(hidden_dim*4),
            nn.GELU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim*4, hidden_dim*2),
            nn.BatchNorm1d(hidden_dim*2),
            nn.GELU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim*2, hidden_dim),
            nn.GELU()
        )

        self.encoder2 = nn.Sequential(
            nn.Linear(input_dims[1], hidden_dim*2),
            nn.BatchNorm1d(hidden_dim*2),
            nn.GELU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim*2, hidden_dim),
            nn.GELU()
        )

        self.projection1 = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim//2),
            nn.GELU(),
            nn.Linear(hidden_dim//2, hidden_dim//2)
        )

        self.projection2 = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim//2),
            nn.GELU(),
            nn.Linear(hidden_dim//2, hidden_dim//2)
        )
        

        # 1. 定义两个交叉注意力模块
        # 一个用于 feat1 查询 feat2
        self.cross_attn_1_to_2 = CrossAttention(query_dim=hidden_dim, context_dim=hidden_dim, dropout_rate=dropout_rate)
        # 另一个用于 feat2 查询 feat1
        self.cross_attn_2_to_1 = CrossAttention(query_dim=hidden_dim, context_dim=hidden_dim, dropout_rate=dropout_rate)

        # 2. 定义最终的融合颈和分类器
        self.classifier = PrototypeSubspace(num_classes=num_classes,
                                              subspace_dim=subspace_dim, 
                                              hidden_dim=hidden_dim * 2)

    def forward(self, x1, x2):
        feat1 = self.encoder1(x1)
        feat2 = self.encoder2(x2)

        z1 = F.normalize(self.projection1(feat1), dim=-1)
        z2 = F.normalize(self.projection2(feat2), dim=-1)

        fused_feat1 = self.cross_attn_1_to_2(query=feat1, context=feat2)
        fused_feat2 = self.cross_attn_2_to_1(query=feat2, context=feat1)
        fused_intermediate = torch.cat([fused_feat1, fused_feat2], dim=-1)
        
        # 通过融合颈进行降维
        logits = self.classifier(fused_intermediate)
        
        return z1, z2, logits, fused_intermediate