# --- Python 标准库 ---
import os
import gc
import random
import warnings

# --- 第三方核心科学计算库 ---
import numpy as np
import pandas as pd
import scipy.stats 

# --- 生物信息学与数据分析库 ---
import anndata as ad
import scanpy as sc
import seaborn as sns
import matplotlib.pyplot as plt

# --- 机器学习库 (Scikit-learn) ---
from sklearn.model_selection import KFold, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, cohen_kappa_score, f1_score, roc_auc_score

# --- 深度学习库 (PyTorch) ---
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torch.optim.lr_scheduler import ExponentialLR

from .loss import *

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

def get_alpha(epoch, total_epochs, start=1.0, end=0.0):
    """线性调度 alpha，从 start 逐渐降低到 end"""
    return start - (start - end) * (epoch / total_epochs)


def train_model(model,
            train_loader,
            optimizer,
            scheduler,
            sup_temperature,
            prototype_temperature,
            alpha,
            lambda_sup_contra,
            lambda_proto_contra,
            lambda_ortho,
            epochs,
            device): 
    
    model.to(device)
    epoch_loss_list = []

    sup_cl_loss_fn = SupConLoss(temperature=sup_temperature)

    # 设置AMP（自动混合精度）开关
    device_type = device.type  # 'cuda' 或 'cpu'
    use_amp = (device_type == 'cuda') # 只有在CUDA可用时才开启AMP
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)
    
    print(f"训练设备: {device_type}, 自动混合精度(AMP)已{'启用' if use_amp else '禁用'}.")

    for epoch in range(epochs):
        model.train()
        total_train_loss = 0.0

        for batch in train_loader:
            x1, x2, labels = batch

            if x1.size(0) < 2:
                continue

            x1, x2, labels = x1.to(device), x2.to(device), labels.to(device)
            
            optimizer.zero_grad(set_to_none=True) 

            with torch.amp.autocast(device_type=device_type, dtype=torch.float16, enabled=use_amp):
                z1, z2, logits, _ = model(x1, x2)
                subspaces = model.classifier.subspaces

                # 分类损失
                loss_ce = F.cross_entropy(logits, labels)

                # 监督对比损失
                features = torch.cat([z1, z2], dim=0)
                labels_sup = labels.repeat(2)
                loss_sup = sup_cl_loss_fn(features, labels_sup)

                # 子空间约束
                loss_ortho = orthogonality_loss(subspaces)
                
                curr_alpha = get_alpha(epoch, epochs, start=alpha, end=0.0)
                loss_prototype = combined_subspace_loss(subspaces, alpha=curr_alpha, temperature=prototype_temperature)
                
                # 总损失
                loss = loss_ce + lambda_sup_contra * loss_sup + lambda_proto_contra * loss_prototype + lambda_ortho * loss_ortho


            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            total_train_loss += loss.item()
            
            del x1, x2, labels, z1, z2, logits, features, labels_sup, loss_ce, loss_sup, loss_prototype, loss
            
        gc.collect()
        if device_type == 'cuda':
            torch.cuda.empty_cache()

        scheduler.step()
        avg_train_loss = total_train_loss / len(train_loader)
        epoch_loss_list.append(avg_train_loss)
        
#         # 可以在这里打印每个epoch的损失
#         if (epoch + 1) % 10 == 0:
#             print(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_train_loss:.4f}")

    return model, epoch_loss_list


def test_model(model, test_loader, label_encoder, device='cuda', output_label_path=None):
    """
    评估模型，将预测结果（包括各类别概率）解码为真实标签，并选择性地保存到CSV文件。

    Args:
        model: 训练好的PyTorch模型。
        test_loader: 测试数据的DataLoader（不包含label）
        label_encoder: 从预处理中得到的、已经fit过的LabelEncoder对象。
        device (str): 计算设备 ('cuda' or 'cpu')。
        output_csv_path (str, optional): 保存预测结果的CSV文件路径。如果为None，则不保存。

    Returns:
        dict: 包含评估指标和结果的字典。
    """
    model.eval()
    model.to(device)

    all_preds_encoded = []

    with torch.no_grad():
        for batch in test_loader:
            x1, x2 = batch
            if x1.size(0) < 2:
                continue

            x1, x2 = x1.to(device), x2.to(device)

            _, _, logits, _ = model(x1, x2)
            probs = F.softmax(logits, dim=-1)
            preds = torch.argmax(probs, dim=1)

            all_preds_encoded.extend(preds.cpu().numpy())
            
            del logits, probs, preds, x1, x2
            torch.cuda.empty_cache()
            gc.collect()

    
    # 解码回真实标签
    encoded_preds = np.array(all_preds_encoded)
    
    try:
        decoded_preds = label_encoder.inverse_transform(encoded_preds)
    except Exception as e:
        print(f"标签解码失败: {e}")
        decoded_preds = encoded_preds

    results_df = pd.DataFrame({
        'Predicted_Label': decoded_preds
    })


    # 写入文件：包含标签、概率等   
    results_df.to_csv(output_label_path, index=True)
    print(f"包含概率的完整预测结果已保存至: {output_label_path}")
 
    
    return results_df


