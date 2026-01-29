"""
GRU-based Log Error Classifier for AI-LogGuard
Best performing model with F1: 0.9763
"""

import re
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn


class GRUClassifier(nn.Module):
    """GRU model architecture (same as training)"""
    
    def __init__(self, vocab_size, embed_dim=128, hidden_dim=128, num_classes=9, num_layers=2, dropout=0.3):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.gru = nn.GRU(
            embed_dim, hidden_dim, 
            num_layers=num_layers,
            batch_first=True, 
            bidirectional=True,
            dropout=dropout if num_layers > 1 else 0
        )
        self.attention = nn.Linear(hidden_dim * 2, 1)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * 2, num_classes)
        
    def forward(self, x, lengths=None):
        embedded = self.embedding(x)
        gru_out, _ = self.gru(embedded)
        
        # Attention mechanism
        attn_weights = torch.softmax(self.attention(gru_out), dim=1)
        context = torch.sum(attn_weights * gru_out, dim=1)
        
        out = self.dropout(context)
        out = self.fc(out)
        return out


class GRULogClassifier:
    """
    Production GRU classifier for CI/CD log error classification.
    
    This is the best performing model with:
    - F1-Score: 0.9763
    - Accuracy: 0.9763
    - Latency: ~2.7ms per sample
    
    Usage:
        classifier = GRULogClassifier()
        result = classifier.predict(log_text)
        print(result['category'])  # e.g., 'dependency_error'
        print(result['confidence'])  # e.g., 0.95
    """
    
    # Category descriptions for user-friendly output
    CATEGORY_DESCRIPTIONS = {
        'dependency_error': 'Dependency/Package Error - Missing or incompatible dependencies',
        'syntax_error': 'Syntax Error - Code syntax issues',
        'test_failure': 'Test Failure - Unit/Integration tests failed',
        'build_error': 'Build Error - Compilation or build process failed',
        'timeout': 'Timeout - Operation exceeded time limit',
        'permission_error': 'Permission Error - Access denied or insufficient permissions',
        'network_error': 'Network Error - Connection issues or DNS failures',
        'resource_error': 'Resource Error - Out of memory or disk space',
        'environment_error': 'Environment Error - Missing tools or misconfiguration',
    }
    
    def __init__(self, model_dir: Optional[Path] = None):
        """
        Initialize the GRU classifier.
        
        Args:
            model_dir: Path to models directory. Defaults to project's models/deep_learning/
        """
        if model_dir is None:
            model_dir = Path(__file__).parent.parent.parent / 'models' / 'deep_learning'
        
        self.model_dir = Path(model_dir)
        self.device = torch.device('cpu')  # Use CPU for production inference
        
        # Load vocabulary and label encoder
        self._load_tokenizer()
        self._load_model()
        
        self._is_loaded = True
    
    def _load_tokenizer(self):
        """Load vocabulary and label encoder"""
        with open(self.model_dir / 'vocab.pkl', 'rb') as f:
            self.vocab = pickle.load(f)
        
        with open(self.model_dir / 'label_encoder.pkl', 'rb') as f:
            self.label_encoder = pickle.load(f)
        
        self.num_classes = len(self.label_encoder.classes_)
        self.vocab_size = len(self.vocab)
    
    def _load_model(self):
        """Load the trained GRU model"""
        self.model = GRUClassifier(
            vocab_size=self.vocab_size,
            embed_dim=128,
            hidden_dim=128,  # Same as training
            num_classes=self.num_classes,
            num_layers=2,
            dropout=0.0  # No dropout during inference
        )
        
        # Load weights
        model_path = self.model_dir / 'gru.pt'
        state_dict = torch.load(model_path, map_location=self.device, weights_only=True)
        self.model.load_state_dict(state_dict)
        self.model.to(self.device)
        self.model.eval()
    
    def _tokenize(self, text: str) -> List[int]:
        """Tokenize text using the same method as training"""
        text = text.lower()
        tokens = re.findall(r'\b[a-z]+\b|\d+|[^\s\w]', text)
        
        # Convert to indices (max 256 tokens)
        indices = [self.vocab.get(t, 1) for t in tokens[:256]]  # 1 = <UNK>
        
        if len(indices) == 0:
            indices = [1]
        
        return indices
    
    def _detect_success(self, log_content: str) -> bool:
        """
        Detect if log indicates a successful build/job (no errors).
        Returns True if log appears to be successful.
        """
        content_lower = log_content.lower()
        
        # Success indicators
        success_patterns = [
            'job succeeded',
            'build succeeded',
            'build successful',
            'pipeline succeeded',
            'passed',
            'deployment complete',
            'deployment successful',
            'all tests passed',
            'build finished successfully',
            'succeeded in',
            '✓ done',
            'success',
        ]
        
        # Error indicators (if any exist, not a clean success)
        error_patterns = [
            'error',
            'failed',
            'failure',
            'exception',
            'fatal',
            'critical',
            'aborted',
            'terminated',
            'killed',
            'timeout',
            'timed out',
        ]
        
        has_success = any(pattern in content_lower for pattern in success_patterns)
        has_error = any(pattern in content_lower for pattern in error_patterns)
        
        # Consider success if has success indicators AND no error indicators
        return has_success and not has_error
    
    def predict(self, log_content: str) -> Dict:
        """
        Predict error category for a log.
        
        Args:
            log_content: Raw log text content
            
        Returns:
            Dict with keys:
                - category: Predicted error category
                - confidence: Prediction confidence (0-1)
                - description: Human-readable description
                - all_probabilities: Dict of all categories with their probabilities
                - is_success: Boolean indicating if log appears successful
        """
        # First check if this is a success log
        if self._detect_success(log_content):
            return {
                'category': 'success',
                'confidence': 1.0,
                'description': 'Build/Job completed successfully - No errors detected',
                'all_probabilities': {'success': 1.0},
                'is_success': True
            }
        
        # Tokenize
        indices = self._tokenize(log_content)
        input_tensor = torch.tensor([indices], dtype=torch.long).to(self.device)
        
        # Predict
        with torch.no_grad():
            outputs = self.model(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)[0]
            
            confidence, predicted_idx = torch.max(probabilities, dim=0)
            predicted_label = self.label_encoder.inverse_transform([predicted_idx.item()])[0]
        
        # Build result
        all_probs = {
            self.label_encoder.inverse_transform([i])[0]: float(probabilities[i])
            for i in range(len(probabilities))
        }
        
        return {
            'category': predicted_label,
            'confidence': float(confidence),
            'description': self.CATEGORY_DESCRIPTIONS.get(predicted_label, 'Unknown error category'),
            'all_probabilities': dict(sorted(all_probs.items(), key=lambda x: -x[1])),
            'is_success': False
        }
    
    def predict_batch(self, logs: List[str]) -> List[Dict]:
        """
        Predict error categories for multiple logs.
        
        Args:
            logs: List of log text contents
            
        Returns:
            List of prediction results
        """
        return [self.predict(log) for log in logs]
    
    def get_top_predictions(self, log_content: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Get top-k predictions with probabilities.
        
        Args:
            log_content: Raw log text
            top_k: Number of top predictions to return
            
        Returns:
            List of (category, probability) tuples
        """
        result = self.predict(log_content)
        probs = result['all_probabilities']
        return list(probs.items())[:top_k]


# Global instance for CLI usage
_classifier_instance: Optional[GRULogClassifier] = None


def get_classifier() -> GRULogClassifier:
    """Get or create the global classifier instance (singleton pattern)"""
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = GRULogClassifier()
    return _classifier_instance


def classify_log(log_content: str) -> Dict:
    """
    Convenience function to classify a log.
    
    Args:
        log_content: Raw log text
        
    Returns:
        Classification result dict
    """
    classifier = get_classifier()
    return classifier.predict(log_content)


if __name__ == '__main__':
    # Quick test
    sample_log = """
    [ERROR] npm ERR! code ERESOLVE
    npm ERR! ERESOLVE unable to resolve dependency tree
    npm ERR! peer react@"^17.0.0" from react-scripts@4.0.3
    """
    
    classifier = GRULogClassifier()
    result = classifier.predict(sample_log)
    
    print(f"Category: {result['category']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"Description: {result['description']}")
    print("\nTop predictions:")
    for cat, prob in list(result['all_probabilities'].items())[:5]:
        print(f"  {cat}: {prob:.2%}")
