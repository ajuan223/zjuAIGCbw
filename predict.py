from ultralytics import YOLO
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, roc_curve, auc, roc_auc_score
from sklearn.preprocessing import label_binarize
from typing import List, Tuple, Dict, Union


def cmetrics(true_labels: np.ndarray, pred_probs: np.ndarray) -> Dict[str, Union[float, np.ndarray]]:
    accuracy = accuracy_score(true_labels, pred_labels)
    precision = precision_score(true_labels, pred_labels, average='macro', zero_division=0)
    recall = recall_score(true_labels, pred_labels, average='macro', zero_division=0)
    f1 = f1_score(true_labels, pred_labels, average='macro', zero_division=0)
    cm = confusion_matrix(true_labels, pred_labels)
    
    n_classes = 20
    y_true_bin = label_binarize(true_labels, classes=list(range(n_classes)))
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    
    for i in range(n_classes):
        if np.sum(y_true_bin[:, i]) == 0:
            fpr[i] = np.array([0, 1])
            tpr[i] = np.array([0, 0])
            roc_auc[i] = 0.0
        else:
            fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], pred_probs[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])
    
    fpr["micro"], tpr["micro"], _ = roc_curve(y_true_bin.ravel(), pred_probs.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'confusion_matrix': cm,
        'fpr': fpr,
        'tpr': tpr,
        'roc_auc': roc_auc
    }

def proc(metrics: Dict[str, Union[float, np.ndarray]], n_classes: int) -> None:
    plt.figure(figsize=(10, 8))
    plt.plot(metrics['fpr']['micro'], metrics['tpr']['micro'],
             label=f"微平均 ROC 曲线 (面积 = {metrics['roc_auc']['micro']:.2f})",
             color='deeppink', linestyle=':', linewidth=4)
    
    for i in range(n_classes):
        plt.plot(metrics['fpr'][i], metrics['tpr'][i],
                 lw=2, label=f"类别 {i} ROC 曲线 (面积 = {metrics['roc_auc'][i]:.2f})")
    
    plt.plot([0, 1], [0, 1], 'k--', lw=2)  
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('假阳性率')
    plt.ylabel('真阳性率')
    plt.title('多类别 ROC 曲线')
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.savefig('roc_curves.png')
    plt.show()

def psummary(metrics: Dict[str, Union[float, np.ndarray]]) -> None:
    print("\n===== 模型性能评估 =====")
    print(f"准确率: {metrics['accuracy']:.4f}")
    print(f"精确率: {metrics['precision']:.4f}")
    print(f"召回率: {metrics['recall']:.4f}")
    print(f"F1 分数: {metrics['f1']:.4f}")

true_labels = []
pred_probs_list = []
pred_labels = []
pred_probs=[]
model = YOLO("best.pt")

dirname = os.path.join(os.path.dirname(os.path.abspath('best.pt')), 'drug', 'test_img')

for i in range(20):
    data_path = os.path.join(dirname, str(i))
    results = model(data_path,verbose=False)
    for result in results:
        pred_probs_list = []
        true_labels.append(i)
        pred_label = result.probs.top1
        pred_labels.append(pred_label)
        
        for j in range(20):
            pred_probs_list.append(result.probs.data[j].item())
        pred_probs.append(pred_probs_list)
true_labels = np.array(true_labels, dtype=int)
pred_labels = np.array(pred_labels, dtype=int)
pred_probs=np.array(pred_probs)
metrics = cmetrics(true_labels, pred_probs)
psummary(metrics)
proc(metrics, 20)