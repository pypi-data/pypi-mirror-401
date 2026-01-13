# --- Python 标准库 ---
import gc
import warnings

# --- 第三方核心科学计算库 ---
import numpy as np
import pandas as pd

# --- 生物信息学与数据分析库 ---
import anndata as ad
import scanpy as sc
import seaborn as sns
import matplotlib.pyplot as plt

# --- 深度学习库 (PyTorch) ---
import torch
import torch.nn.functional as F

# --- 脚本级别的设置 ---
warnings.filterwarnings("ignore")
gc.collect()

from sklearn.mixture import GaussianMixture
from scipy.stats import norm
from sklearn.cluster import dbscan
from sklearn.neighbors import NearestNeighbors


def get_embedding(data_loader, model, device, is_train = True):
    model.eval()
    model.to(device)

    all_labels = []
    all_embeddings = []
    all_preds = []
    
    with torch.no_grad():
        if is_train:
            for x1_batch, x2_batch, labels_batch in data_loader:
                x1_batch, x2_batch = x1_batch.to(device), x2_batch.to(device)

                _, _, logits, embedding = model(x1_batch, x2_batch)

                probs = F.softmax(logits, dim=-1)
                preds = torch.argmax(probs, dim=1)

                all_labels.append(labels_batch)
                all_embeddings.append(embedding.cpu().numpy())
        else:
            for x1_batch, x2_batch in data_loader:
                x1_batch, x2_batch = x1_batch.to(device), x2_batch.to(device)

                _, _, logits, embedding = model(x1_batch, x2_batch)

                probs = F.softmax(logits, dim=-1)
                preds = torch.argmax(probs, dim=1)

                all_embeddings.append(embedding.cpu().numpy())
                all_preds.extend(preds.cpu().numpy())
    
    embeddings = np.concatenate(all_embeddings)
    
    if is_train:
        true_labels = torch.cat(all_labels).cpu()
        return embeddings, true_labels
    else:
        return embeddings, all_preds


def calculate_distance_score(test_embeddings, train_embeddings, k = 10):
   
    # 平均到训练集距离
    knn = NearestNeighbors(n_neighbors=k, metric='euclidean')
    knn.fit(train_embeddings)
    distances, _ = knn.kneighbors(test_embeddings)
    score = np.mean(distances, axis=1)
    
    return score

def calculate_gaussian_intersection(w1, mu1, sigma1, w2, mu2, sigma2):
    """
    计算两个带权重高斯分布的交点（解方程 f1(x) = f2(x)）
    
    参数：
        w1, mu1, sigma1: 第一个高斯分量的权重、均值、标准差
        w2, mu2, sigma2: 第二个高斯分量的权重、均值、标准差
    
    返回：
        intersections: 交点x值列表（sorted，从小到大），空列表表示无交点
    """
    # 计算二次方程系数 A*x² + B*x + C = 0
    A = (1 / (2 * sigma2**2)) - (1 / (2 * sigma1**2))
    B = (mu1 / sigma1**2) - (mu2 / sigma2**2)
    C = (mu2**2 / (2 * sigma2**2)) - (mu1**2 / (2 * sigma1**2)) + np.log((w1 * sigma2) / (w2 * sigma1))
    
    # 计算判别式
    delta = B**2 - 4 * A * C
    intersections = []
    
    if delta > 0:
        # 两个不同实根
        x1 = (-B - np.sqrt(delta)) / (2 * A)
        x2 = (-B + np.sqrt(delta)) / (2 * A)
        intersections = sorted([x1, x2])  # 按从小到大排序
    elif delta == 0:
        # 一个实根（相切）
        x = -B / (2 * A)
        intersections = [x]
    else:
        # 无实根（两个分布几乎不重叠）
        print("警告：两个高斯分布无交点，建议用均值中间值作为阈值")
        # 可选：返回两个均值的中间值作为替代阈值
        intersections = [(mu1 + mu2) / 2]
    
    return intersections

def gmm_calculate_plot(score, plt_gmm = True):
    score_reshaped = score.reshape(-1, 1)

    # Fit the Gaussian Mixture Model
    gmm = GaussianMixture(n_components=2, random_state = 123)
    gmm.fit(score_reshaped)

    # Extract parameters
    weights = gmm.weights_
    means = gmm.means_.flatten()
    covariances = gmm.covariances_.flatten()
    stds = np.sqrt(covariances)
    
    # 提取交点
    if means[0] < means[1]:
        w_low, mu_low, stds_low = weights[0], means[0], stds[0]
        w_high, mu_high, stds_high = weights[1], means[1], stds[1]
    else:
        w_low, mu_low, stds_low = weights[1], means[1], stds[1]
        w_high, mu_high, stds_high = weights[0], means[0], stds[0]
    
    print(f"低置信高斯分量：权重={w_low:.3f}, 均值={mu_low:.3f}, 标准差={stds_low:.3f}")
    print(f"高置信高斯分量：权重={w_high:.3f}, 均值={mu_high:.3f}, 标准差={stds_high:.3f}")
    
    # 4. 计算两个高斯分布的交点
    intersections = calculate_gaussian_intersection(
        w1=w_low, mu1=mu_low, sigma1=stds_low,
        w2=w_high, mu2=mu_high, sigma2=stds_high
    )
    if len(intersections) >= 1:
        threshold = [i for i in intersections if i<mu_high and i> mu_low] # 两均值中间的
        print(f"两个高斯分布的交点：{intersections}，处于两均值中间的交点：{threshold}")
    else:
        # 极端情况：无交点，用两个均值的中间值
        threshold = (mu_low + mu_high) / 2
        print(f"无交点，用均值中间值作为阈值：{threshold:.4f}")
        
    if plt_gmm:
        # --- Visualization ---
        plt.figure(figsize=(6, 4))

        # Plot the data histogram
        sns.histplot(
            score,
            bins=50,
            stat='density',
            kde=True,
            edgecolor='black',
            color = 'lightgrey',
            label='Raw Data Distribution',
            line_kws={
                'color': 'g',
                'linewidth': 2,
                'label': 'Raw Data KDE'}
        )

        x = np.linspace(score.min()-0.1, score.max()+0.1, 500).reshape(-1, 1)

        # Plot individual Gaussian components
        order = np.argsort(means)
        sorted_means = means[order]
        sorted_stds = stds[order]
        sorted_weights = weights[order]

        for i in range(2):
            gaussian_pdf = sorted_weights[i] * norm.pdf(x.flatten(), loc=sorted_means[i], scale=sorted_stds[i])
            plt.plot(
                x.flatten(),
                gaussian_pdf,
                linewidth=2.5,
                linestyle='--',
                label=f'Gaussian {i+1} (μ={sorted_means[i]:.1f}, σ={sorted_stds[i]:.1f}, w={sorted_weights[i]:.2f})'
            )

        # Plot the combined mixed Gaussian PDF
        mixed_pdf = np.exp(gmm.score_samples(x))
        plt.plot(
            x.flatten(),
            mixed_pdf,
            linewidth=3,
            color='red',
            label='Total Mixed Gaussian Model',
            alpha=0.8
        )

        # Add labels, title, and legend
        plt.title('Gaussian Mixture Model Fit to Score Data')
        plt.xlabel('Score')
        plt.ylabel('Density')
        plt.legend(fontsize=10, loc='upper left')
        plt.grid(True)

        plt.show()
    
    return {'weights': [w_high, w_low],
           'means': [mu_high, mu_low],
           'covariances': covariances,
           'stds': [stds_high, stds_low],
           'intersection': intersections,
           'threshold':threshold}




def find_novel_type(adata_test, target_colname, threshold, test_embeddings, train_embeddings, scores, fig_path, min_samples = 10):
    adata_test_use = adata_test.copy()
    adata_test_use.obsm['prototype_embedding'] = test_embeddings
    
    adata_test_use.obs['distance_score'] = scores
    adata_test_use.obs.loc[adata_test_use.obs['distance_score'] > threshold, 'likely_novel'] = 'True'
    
    # 筛选低置信度样本
    adata_unconfident = adata_test_use[adata_test_use.obs['likely_novel'] == 'True'].copy()
    embeddings_uncocnfident = adata_unconfident.obsm['prototype_embedding'].copy()
    
    # DBSCAN聚类
    core_samples, labels = dbscan(embeddings_uncocnfident, eps=threshold, min_samples = min_samples) # eps使用与划分低置信都样本相同阈值
    processed_labels = ['False' if x == -1 else f'novel_{x}' for x in labels]
    final_novel_clusters = [label for label in processed_labels if label != 'False']
    
    # 显示聚类结果
    adata_test_use.obs['predict_novel'] = 'False'
    adata_unconfident.obs['predict_novel'] = processed_labels 
    adata_test_use.obs.loc[adata_unconfident.obs.index, 'predict_novel'] = processed_labels 
    
    # 得到非新类型带标签的结果
    adata_test_use.obs['is_novel_with_label'] = adata_test_use.obs[target_colname].astype(str)
    final_mask = adata_test_use.obs['predict_novel'].isin(final_novel_clusters)
    adata_test_use.obs.loc[final_mask, 'is_novel_with_label'] = adata_test_use.obs.loc[final_mask, 'predict_novel']
    
    sc.pp.neighbors(adata_test_use, use_rep = 'prototype_embedding')
    sc.tl.umap(adata_test_use)
    sc.pl.umap(adata_test_use, color=['is_novel_with_label', 'distance_score','predict_novel'], title = 'test data Embedding umap', wspace=0.4, show = False)
    
    if fig_path is not None:
        plt.savefig(fig_path)
        
        
    return adata_test_use.obs['is_novel_with_label'], adata_test_use.obs['predict_novel']
