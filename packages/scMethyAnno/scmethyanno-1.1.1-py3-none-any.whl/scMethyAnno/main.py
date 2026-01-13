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
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, cohen_kappa_score, f1_score, roc_auc_score

# --- 深度学习库 (PyTorch) ---
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torch.optim.lr_scheduler import ExponentialLR

# --- 脚本级别的设置 ---
warnings.filterwarnings("ignore")
gc.collect()

def setup_seed(seed = 123):
    """
    设置随机种子以保证实验可复现性

    Parameters
    ----------
    seed : int
        随机种子数值
    """
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

setup_seed(123)

# --- 自定义模块导入 ---
from .model import *
from .loss import *
from .train_test import *
from .data_preprocess import *
from .novel_discover import *
from .interpretation import *

def MethyAnno_train_test(
    adata_train: ad.AnnData,
    adata_test: ad.AnnData,
    target_colname: str,
    output_dir: str, 
    device: torch.device,
    is_calculate_metric: bool = False,  
    is_discover_novel_type: bool = False,
    is_interpret_model: bool = False, 

):
    """
    MethyAnno核心训练与测试主函数
    功能：完成scDNAm数据的细胞类型注释、新细胞类型发现、模型可解释性分析

    Parameters
    ----------
    adata_train : anndata.AnnData
        训练集AnnData对象（需包含target_colname列作为标签）
    adata_test : anndata.AnnData
        测试集AnnData对象
    target_colname : str
        细胞类型标签列名（如'cell_type'）
    output_dir : str
        输出文件保存目录
    device : torch.device
        训练设备
    is_calculate_metric : bool, optional
        是否计算分类指标（ACC/Kappa/F1），默认False
    is_discover_novel_type : bool, optional
        是否执行新细胞类型发现，默认False
    is_interpret_model : bool, optional
        是否进行模型可解释性分析（提取细胞类型特异性特征），默认False


    Returns
    -------
    None
        结果直接输出到指定路径，无返回值
    """

    # 【1. Data preprocess】
    # ============================================================================
    print("Step 1: Data Preprocessing...")
    
    adata_train, adata_test = data_preprocessing(adata_train, adata_test, target_colname)
    adata_concat = ad.concat([adata_train, adata_test], label='is_train', keys=['train', 'test'])
    train_index = np.where(adata_concat.obs['is_train'] == 'train')[0].tolist()
    test_index = np.where(adata_concat.obs['is_train'] == 'test')[0].tolist()

    # 【2. Feature selection】
    # ============================================================================
    print("Step 2: Feature Selection (F-test)...")
    feature1, feature1_idx, X1 = combined_f_test(adata_train, adata_concat, target_colname, 5000, None)
    feature2, feature2_idx, X2 = combined_f_test(adata_train, adata_concat, target_colname, 3000, '10X')
#     feature2_names = adata_train.uns.get("10X_features")[feature2]
    input_dims = [X1.shape[1], X2.shape[1]]
    y_train = adata_train.obs[target_colname].tolist()

    # 【3. Construct PyTorch DataLoader】
    # ============================================================================
    print("Step 3: Build DataLoader...")
    train_loader, test_loader, num_classes, label_encoder = preprocess_data_2branch(
        X1, X2, y_train, train_index, test_index, batch_size=64
    )

    # 【4. Model initialize】
    # ============================================================================
    print("Step 4: Initialize Model...")
    model = MultiScalePrototypeModel(input_dims = input_dims, 
                                     num_classes = num_classes, 
                                     hidden_dim = 256, 
                                     dropout_rate= 0.6, 
                                     subspace_dim = 8)

        
    # 优化器与学习率调度器
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=0.0001)
    scheduler = ExponentialLR(optimizer, gamma=0.95)

    # 【5. Model training】
    # ============================================================================
    print("Step 5: Model Training...")
    model, train_loss = train_model(
        model=model,
        train_loader=train_loader,
        optimizer=optimizer,
        scheduler=scheduler,
        alpha=1.0,
        prototype_temperature=0.5,
        lambda_ortho=0.1,
        sup_temperature=0.8,
        lambda_sup_contra=0.8,
        lambda_proto_contra=0.1,
        epochs=70,
        device=device
    )
    output_model_path = f'{output_dir}/model.pth'
    torch.save({
            'model_state_dict': model.state_dict(),
            'label_encoder': label_encoder, 
            'target_colname': target_colname, 
          
        }, output_model_path)
    print(f"Model saved to {output_model_path}")
        

    # 【6. Model testing】
    # ============================================================================
    print("Step 6: Model Testing & Save Predictions...")
    predicted_label = test_model(
        model=model,
        test_loader=test_loader,
        label_encoder=label_encoder,
        device=device,
        output_label_path=f'{output_dir}/pre_result.csv',
    )

    if is_calculate_metric:
        print("Calculate Classification Metrics...")
        y_test = adata_test.obs[target_colname].tolist()
        y_test_pred = predicted_label['Predicted_Label'].tolist()
        # caculate metric
        acc = accuracy_score(y_test, y_test_pred)
        kappa = cohen_kappa_score(y_test, y_test_pred)
        f1_macro = f1_score(y_test, y_test_pred, average='macro')
        
        metrics_dict = {
            'accuracy': [acc],
            'kappa': [kappa],
            'f1_macro': [f1_macro]
        }
        result_metric_df = pd.DataFrame(metrics_dict)

        # save metric
        result_metric_df.to_csv(f'{output_dir}/report.csv', mode='a', header=True, index=False)
        print(f"Metrics saved to: {output_dir}/report.csv")
         

    # 【8. Novel type discovery】
    # ============================================================================
    if is_discover_novel_type:
        print("Step 8: Novel Cell Type Discovery...")
        # get cell embedding
        test_embeddings, test_preds = get_embedding(test_loader, model, device, is_train=False)
        train_embeddings, train_labels = get_embedding(train_loader, model, device, is_train=True)

        # caculate score
        avg_distances = calculate_distance_score(test_embeddings, train_embeddings)  # 修正：caculate → calculate
        gmm_res = gmm_calculate_plot(avg_distances)
        threshold = gmm_res['threshold'][0]
        print(f"GMM threshold for novel discovery: {threshold:.4f}")

        # discover novel type
        novel_with_label, pred_is_novel = find_novel_type(
            adata_test,
            target_colname,
            threshold,
            test_embeddings,
            train_embeddings,
            avg_distances,
            fig_path=f'{output_dir}/novel_umap.pdf'
        )
        novel_res = pd.DataFrame({'novel_with_label':novel_with_label, 'pred_is_novel':pred_is_novel})
        novel_res.to_csv(f'{output_dir}/novel_res.csv', mode='a', header=True, index=False)
        print(f"Novel discovery res saved to: {output_dir}/novel_res.csv")

        
        

    # 【9. Model Interpretability】
    # ============================================================================
    if is_interpret_model:
        print("Step 9: Model Interpretability Analysis...")
        peak_dict = get_all_type_peak(
            adata_train,
            label_encoder,
            feature1_idx,
            feature2_idx,
            model,
            device,
            top_n=1000
        )

        # save feature
        output_feature_dir = f'{output_dir}/features/'
        os.makedirs(output_feature_dir, exist_ok=True)
        cell_peak_to_bed(output_feature_dir, peak_dict)
        background_peak_to_bed(output_feature_dir, adata_train, peak_dict)
        print(f"Cell-type specific features saved to: {output_feature_dir}")
        

    # ============================================================================
    # 【10. 资源释放】：清理显存/内存，避免泄漏
    # ============================================================================
    print("Step 10: Release Resources...")
    del model, adata_train, adata_test, adata_concat, train_loader, test_loader, optimizer, scheduler
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()
    print("MethyAnno pipeline completed!")