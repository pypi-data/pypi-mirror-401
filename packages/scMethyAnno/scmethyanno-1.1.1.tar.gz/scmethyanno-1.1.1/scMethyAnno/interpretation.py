# --- Python 标准库 ---
import os
import gc
import warnings

# --- 第三方核心科学计算库 ---
import numpy as np
import pandas as pd
import anndata as ad

# --- 机器学习库 (Scikit-learn) ---
from sklearn.preprocessing import LabelEncoder

# --- 深度学习库 (PyTorch) ---
import torch
from torch.utils.data import DataLoader, TensorDataset
from captum.attr import IntegratedGradients

# --- 脚本级别的设置 ---
warnings.filterwarnings("ignore")
gc.collect()


def get_type_feature_score_one_rest(adata, typename, label_encoder, feature1, feature2, model, device):
    adata_use = adata[adata.obs['MajorType'] == typename].copy()
    
    x1 = adata_use.X[:, feature1]
#     feature_names2 = adata_use.uns.get("10X_features")
#     feature_index2 = pd.Index(feature_names2)
#     selected_indices2 = feature_index2.get_indexer(feature2_names)
#     selected_indices2 = selected_indices2[selected_indices2 != -1]
    x2 = adata_use.obsm['10X'][:, feature2]

    labels_encoded = label_encoder.transform(adata_use.obs['MajorType'].tolist()) 

    # 得到模型的输入
    x1_tensor = torch.tensor(x1, dtype=torch.float32)
    x2_tensor = torch.tensor(x2, dtype=torch.float32)
    label_tensor = torch.tensor(labels_encoded, dtype=torch.long)
    
    dataset = TensorDataset(x1_tensor, x2_tensor, label_tensor)
    dataloader = DataLoader(dataset, batch_size = 64)
    
    
    def create_one_vs_rest_wrapper(model, target_class_idx):
        """
        This outer function "manufactures" and returns the actual wrapper.
        It captures the model and target_class_idx in a closure.
        """
        # The actual wrapper function that Captum will call
        def one_vs_rest_forward_wrapper(input1, input2):
            """
            This wrapper has the exact signature Captum expects: (input1, input2).
            `model` and `target_class_idx` are available from the outer scope.
            """
            # Get the original logits from the model
            # Assuming model.forward returns (z1, z2, logits, fused_intermediate)
            _, _, all_logits, _ = model(input1, input2)
            
            # Create a mask to select all "rest" classes
            mask = torch.ones_like(all_logits, dtype=torch.bool)
            mask[:, target_class_idx] = False
            
            target_logits = all_logits[:, target_class_idx]
            
            # Calculate the mean of the "rest" logits
            rest_logits = all_logits[mask].view(all_logits.shape[0], -1)
            mean_rest_logits = rest_logits.mean(dim=1)
            
            # The final score to be explained is the contrast
            contrastive_score = target_logits - mean_rest_logits
            return contrastive_score
            
        return one_vs_rest_forward_wrapper
    
    # 初始化Captum
    ig = IntegratedGradients(model) 
    all_attributions_1 = []
    all_attributions_2 = []
    
    for batch in dataloader:
        batch_input1, batch_input2, batch_labels = [item.to(device) for item in batch]
        target_class_for_batch = batch_labels[0].item()
        
        from functools import partial
        wrapped_model_func = create_one_vs_rest_wrapper(model, target_class_for_batch)
        
        # 再次初始化IG，这次使用临时的wrapper
        # Captum的新版本可以直接将forward_func传入attribute方法
        ig_temp = IntegratedGradients(forward_func=wrapped_model_func)

        attributions_tuple = ig_temp.attribute(
            inputs=(batch_input1, batch_input2)
            # 注意：现在不需要target参数了，因为目标已经在wrapper中定义了
        )

        attr1, attr2 = attributions_tuple
        all_attributions_1.append(attr1.cpu())
        all_attributions_2.append(attr2.cpu())
        
    final_attributions_1 = torch.cat(all_attributions_1, dim=0)
    
    return final_attributions_1


def get_all_type_peak(adata, label_encoder, feature1,feature2, model, device, top_n=1000):
    
    score_1_dict = {}
    peak_1_dict = {}
    print(feature1[0:10])
    all_peak_1_name = adata.var.index[np.array(feature1)].tolist() 
    
    for typename in adata.obs.MajorType.unique():
        final_attributions_1 = get_type_feature_score_one_rest(adata, 
                                                               typename, 
                                                                label_encoder, 
                                                                feature1, 
                                                               feature2,
                                                                model, 
                                                                device)
        
        # 特征1计算重要性(返回排序后数据)
        abs_attributions_1 = final_attributions_1.abs()
        avg_importance_scores_1 = abs_attributions_1.mean(dim=0)
        sorted_indices_1 = torch.argsort(avg_importance_scores_1, descending=True)
        results_df_1 = pd.DataFrame({
            'feature_index': sorted_indices_1.cpu().numpy(),
            'avg_importance_score': avg_importance_scores_1[sorted_indices_1].cpu().numpy()
        })
        top_peak_1 = results_df_1['feature_index'].head(top_n).values
        top_peak_1 = [all_peak_1_name[i] for i in top_peak_1]
        
        score_1_dict[typename] = results_df_1
        peak_1_dict[typename] = top_peak_1
    
    
    return peak_1_dict


def peaks_to_bed(peak_list, output_file, split_char = '_'):
    """
    将peak列表转换为BED文件
    
    参数:
        peak_list: 包含peak信息的列表，每个元素格式如"chr1_12345-67890"
        output_file: 输出的BED文件名
    """
    with open(output_file, 'w') as f:
        for peak in peak_list:
            # 分割染色体部分和位置部分
            try:
                chrom_part, start, end = peak.split(split_char)
            except:
                print(f'Error! {peak}')
            
            # BED文件要求起始位置是0-based（半开区间）
            # 如果你的数据是1-based，可能需要调整：start = str(int(start) - 1)
            
            # 写入BED行（染色体、起始、终止，用制表符分隔）
            f.write(f"{chrom_part}\t{start}\t{end}\n")
            
def cell_peak_to_bed(output_dir, peak_dict):
    
    os.makedirs(output_dir, exist_ok=True)
    print(f'输出目标文件夹:{output_dir}')
    
    for typename in sorted(list(peak_dict.keys())):
        
        safe_typename = typename.replace("/", "-").replace("\\", "-").replace(":", "-")
        
        
        feature_list = peak_dict[typename]
        output_file = os.path.join(output_dir, f'{safe_typename}.bed')
        peaks_to_bed(feature_list, output_file)
        
        del feature_list
        gc.collect()
    
def background_peak_to_bed(output_dir, adata, pick_dict, unsname = None):
    
    if unsname is not None:
        all_peak_name = adata.uns[unsname].tolist()
        all_peak_name = [peak.split('_win')[0] for peak in all_peak_name]
    else:
        all_peak_name = adata.var.index.to_list()
    
    # 取特异peak的并集

    union_set = set()
    for value_list in pick_dict.values():
        union_set.update(value_list)
    
    back_peak_list = list(set(all_peak_name) - union_set)
    output_file = os.path.join(output_dir, 'background.bed')
    peaks_to_bed(back_peak_list, output_file)
    