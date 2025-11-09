"""
技术性能评估指标

包括：
- BERT Score: 语义相似度评估
- ROUGE: 文本重叠度评估
- BLEU: 机器翻译质量评估（适用于对话）
- Perplexity: 语言模型困惑度
- Response Length: 回复长度统计
"""

import numpy as np
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

try:
    from bert_score import score as bert_score_func
    BERT_SCORE_AVAILABLE = True
except ImportError:
    BERT_SCORE_AVAILABLE = False
    logger.warning("bert-score not installed. Install with: pip install bert-score")

try:
    from rouge_score import rouge_scorer
    ROUGE_AVAILABLE = True
except ImportError:
    ROUGE_AVAILABLE = False
    logger.warning("rouge-score not installed. Install with: pip install rouge-score")

try:
    from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
    import nltk
    BLEU_AVAILABLE = True
except ImportError:
    BLEU_AVAILABLE = False
    logger.warning("nltk not installed. Install with: pip install nltk")


class TechnicalMetrics:
    """技术性能指标计算器"""
    
    def __init__(self, device: str = "cpu"):
        """
        初始化
        
        Args:
            device: 计算设备 ("cpu" 或 "cuda")
        """
        self.device = device
        
        if ROUGE_AVAILABLE:
            self.rouge_scorer = rouge_scorer.RougeScorer(
                ['rouge1', 'rouge2', 'rougeL'], 
                use_stemmer=True
            )
        
        if BLEU_AVAILABLE:
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                logger.info("Downloading NLTK punkt tokenizer...")
                nltk.download('punkt', quiet=True)
    
    def compute_bert_score(
        self, 
        predictions: List[str], 
        references: List[str],
        lang: str = "zh",
        verbose: bool = False
    ) -> Dict[str, float]:
        """
        计算BERT Score
        
        Args:
            predictions: 预测文本列表
            references: 参考文本列表
            lang: 语言 ("zh" 或 "en")
            verbose: 是否显示详细信息
            
        Returns:
            包含 precision, recall, f1 的字典
        """
        if not BERT_SCORE_AVAILABLE:
            logger.error("BERT Score not available. Please install bert-score.")
            return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
        
        if len(predictions) != len(references):
            raise ValueError("predictions and references must have same length")
        
        try:
            P, R, F1 = bert_score_func(
                predictions, 
                references, 
                lang=lang,
                device=self.device,
                verbose=verbose
            )
            
            return {
                "precision": float(P.mean().item()),
                "recall": float(R.mean().item()),
                "f1": float(F1.mean().item())
            }
        except Exception as e:
            logger.error(f"Error computing BERT Score: {e}")
            return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    
    def compute_rouge(
        self, 
        prediction: str, 
        reference: str
    ) -> Dict[str, Dict[str, float]]:
        """
        计算ROUGE分数（单个样本）
        
        Args:
            prediction: 预测文本
            reference: 参考文本
            
        Returns:
            包含rouge1, rouge2, rougeL的字典
        """
        if not ROUGE_AVAILABLE:
            logger.error("ROUGE not available. Please install rouge-score.")
            return {}
        
        try:
            scores = self.rouge_scorer.score(reference, prediction)
            return {
                "rouge1": {
                    "precision": scores['rouge1'].precision,
                    "recall": scores['rouge1'].recall,
                    "f1": scores['rouge1'].fmeasure
                },
                "rouge2": {
                    "precision": scores['rouge2'].precision,
                    "recall": scores['rouge2'].recall,
                    "f1": scores['rouge2'].fmeasure
                },
                "rougeL": {
                    "precision": scores['rougeL'].precision,
                    "recall": scores['rougeL'].recall,
                    "f1": scores['rougeL'].fmeasure
                }
            }
        except Exception as e:
            logger.error(f"Error computing ROUGE: {e}")
            return {}
    
    def compute_rouge_batch(
        self, 
        predictions: List[str], 
        references: List[str]
    ) -> Dict[str, float]:
        """
        批量计算ROUGE分数（平均值）
        
        Args:
            predictions: 预测文本列表
            references: 参考文本列表
            
        Returns:
            平均ROUGE分数字典
        """
        if len(predictions) != len(references):
            raise ValueError("predictions and references must have same length")
        
        rouge1_f1_list = []
        rouge2_f1_list = []
        rougeL_f1_list = []
        
        for pred, ref in zip(predictions, references):
            scores = self.compute_rouge(pred, ref)
            if scores:
                rouge1_f1_list.append(scores['rouge1']['f1'])
                rouge2_f1_list.append(scores['rouge2']['f1'])
                rougeL_f1_list.append(scores['rougeL']['f1'])
        
        return {
            "rouge1_f1": np.mean(rouge1_f1_list) if rouge1_f1_list else 0.0,
            "rouge2_f1": np.mean(rouge2_f1_list) if rouge2_f1_list else 0.0,
            "rougeL_f1": np.mean(rougeL_f1_list) if rougeL_f1_list else 0.0
        }
    
    def compute_bleu(
        self, 
        prediction: str, 
        reference: str
    ) -> float:
        """
        计算BLEU分数（单个样本）
        
        Args:
            prediction: 预测文本
            reference: 参考文本
            
        Returns:
            BLEU分数
        """
        if not BLEU_AVAILABLE:
            logger.error("BLEU not available. Please install nltk.")
            return 0.0
        
        try:
            # 简单分词（可以根据需要改进）
            pred_tokens = list(prediction)
            ref_tokens = list(reference)
            
            # 使用平滑函数避免0分
            smoothing = SmoothingFunction()
            score = sentence_bleu(
                [ref_tokens], 
                pred_tokens,
                smoothing_function=smoothing.method1
            )
            return score
        except Exception as e:
            logger.error(f"Error computing BLEU: {e}")
            return 0.0
    
    def compute_bleu_batch(
        self, 
        predictions: List[str], 
        references: List[str]
    ) -> float:
        """
        批量计算BLEU分数（平均值）
        
        Args:
            predictions: 预测文本列表
            references: 参考文本列表
            
        Returns:
            平均BLEU分数
        """
        if len(predictions) != len(references):
            raise ValueError("predictions and references must have same length")
        
        scores = []
        for pred, ref in zip(predictions, references):
            score = self.compute_bleu(pred, ref)
            scores.append(score)
        
        return np.mean(scores) if scores else 0.0
    
    def compute_response_stats(
        self, 
        responses: List[str]
    ) -> Dict[str, float]:
        """
        计算回复统计信息
        
        Args:
            responses: 回复文本列表
            
        Returns:
            统计信息字典
        """
        lengths = [len(r) for r in responses]
     
        return {
            "avg_length": float(np.mean(lengths)) if lengths else 0.0,
            "min_length": float(np.min(lengths)) if lengths else 0.0,
            "max_length": float(np.max(lengths)) if lengths else 0.0,
            "std_length": float(np.std(lengths)) if lengths else 0.0
        }
    
    def compute_all_metrics(
        self, 
        predictions: List[str], 
        references: List[str],
        lang: str = "zh"
    ) -> Dict[str, float]:
        """
        计算所有技术指标
        
        Args:
            predictions: 预测文本列表
            references: 参考文本列表
            lang: 语言
            
        Returns:
            所有指标的字典
        """
        results = {}
        
        # BERT Score
        if BERT_SCORE_AVAILABLE:
            logger.info("Computing BERT Score...")
            bert_scores = self.compute_bert_score(predictions, references, lang)
            results.update({
                "bert_precision": bert_scores["precision"],
                "bert_recall": bert_scores["recall"],
                "bert_f1": bert_scores["f1"]
            })
        
        # ROUGE
        if ROUGE_AVAILABLE:
            logger.info("Computing ROUGE...")
            rouge_scores = self.compute_rouge_batch(predictions, references)
            results.update(rouge_scores)
        
        # BLEU
        if BLEU_AVAILABLE:
            logger.info("Computing BLEU...")
            bleu_score = self.compute_bleu_batch(predictions, references)
            results["bleu"] = bleu_score
        
        # Response Statistics
        logger.info("Computing response statistics...")
        stats = self.compute_response_stats(predictions)
        results.update(stats)
        
        return results


def evaluate_technical_metrics(
    predictions: List[str],
    references: List[str],
    lang: str = "zh",
    device: str = "cpu"
) -> Dict[str, float]:
    """
    便捷函数：计算所有技术指标
    
    Args:
        predictions: 预测文本列表
        references: 参考文本列表
        lang: 语言
        device: 计算设备
        
    Returns:
        所有指标的字典
    """
    metrics = TechnicalMetrics(device=device)
    return metrics.compute_all_metrics(predictions, references, lang)
