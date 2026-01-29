"""
Hybrid Log Classifier for AI-LogGuard

Giải quyết vấn đề Domain Gap bằng cách kết hợp:
1. Rule-based detection cho các patterns rõ ràng
2. GRU model cho các trường hợp phức tạp
3. Confidence adjustment dựa trên context

Vấn đề gốc: GRU model trained trên synthetic data không nhận diện được
real logs vì:
- Synthetic data có format khác (thiếu Jenkins/GitLab pipeline output)
- Các từ như "timeout=10" trong git commands bị nhầm với timeout errors
- TypeScript/build errors không được recognize đúng
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ErrorCategory(str, Enum):
    """Error categories matching GRU model"""
    BUILD_ERROR = "build_error"
    DEPENDENCY_ERROR = "dependency_error"
    SYNTAX_ERROR = "syntax_error"
    TEST_FAILURE = "test_failure"
    TIMEOUT = "timeout"
    PERMISSION_ERROR = "permission_error"
    NETWORK_ERROR = "network_error"
    RESOURCE_ERROR = "resource_error"
    ENVIRONMENT_ERROR = "environment_error"
    SUCCESS = "success"


@dataclass
class RuleMatch:
    """Result of a rule-based match"""
    category: str
    confidence: float
    matched_pattern: str
    evidence: List[str]


class HybridLogClassifier:
    """
    Hybrid classifier combining rules and GRU model.
    
    Strategy:
    1. Apply rule-based detection first (high precision patterns)
    2. If rules match with high confidence, use that result
    3. Otherwise, use GRU model prediction
    4. Apply confidence adjustment based on context
    
    This solves the domain gap problem by:
    - Handling real CI/CD log formats (Jenkins, GitLab, GitHub Actions)
    - Filtering noise (e.g., "timeout=10" in git commands is NOT a timeout error)
    - Boosting confidence for clear error patterns
    """
    
    # ============================================================
    # RULE DEFINITIONS
    # Each rule has: pattern, category, confidence, and exclusions
    # ============================================================
    
    BUILD_ERROR_PATTERNS = [
        # TypeScript/JavaScript
        (r'error TS\d+:', 'TypeScript compilation error'),
        (r'Failed to compile', 'Compilation failed'),
        (r'Build failed|build failed', 'Build process failed'),
        (r'npm run build.*failed', 'NPM build failed'),
        (r'webpack.*error', 'Webpack bundling error'),
        (r'Module build failed', 'Module build error'),
        (r'SyntaxError.*Unexpected token', 'JavaScript syntax error in build'),
        (r'Cannot find module', 'Missing module during build'),
        
        # Java/Gradle/Maven
        (r'BUILD FAILED', 'Gradle/Maven build failed'),
        (r'Compilation failure', 'Java compilation failure'),
        (r'javac.*error', 'Java compiler error'),
        (r'\[ERROR\].*Compilation failure', 'Maven compilation failure'),
        
        # C/C++/Go
        (r'make\[\d+\]: \*\*\*.*Error', 'Make build error'),
        (r'gcc.*error:', 'GCC compilation error'),
        (r'go build.*cannot', 'Go build error'),
        
        # Docker
        (r'docker build.*failed', 'Docker build failed'),
        (r'ERROR.*building.*image', 'Docker image build error'),
        (r'failed to build.*Dockerfile', 'Dockerfile error'),
        
        # Next.js specific
        (r'next build.*failed', 'Next.js build failed'),
        (r'Type error:.*Object literal', 'TypeScript type error'),
    ]
    
    DEPENDENCY_ERROR_PATTERNS = [
        # NPM/Node
        (r'npm ERR!.*ERESOLVE', 'NPM dependency resolution error'),
        (r'npm ERR!.*peer dep', 'NPM peer dependency conflict'),
        (r'npm ERR!.*not found', 'NPM package not found'),
        (r'npm ERR!.*ENOENT', 'NPM file not found'),
        (r'yarn.*error.*Couldn\'t find package', 'Yarn package not found'),
        (r'Module not found.*Can\'t resolve', 'Module resolution failed'),
        
        # Python
        (r'pip.*No matching distribution', 'pip package not found'),
        (r'ModuleNotFoundError', 'Python module not found'),
        (r'ImportError:.*No module named', 'Python import error'),
        (r'pkg_resources\.DistributionNotFound', 'Python package missing'),
        
        # Java
        (r'Could not resolve dependencies', 'Maven/Gradle dependency error'),
        (r'Failed to collect dependencies', 'Dependency collection failed'),
        
        # General
        (r'dependency.*not found', 'Dependency not found'),
        (r'unable to resolve dependency', 'Dependency resolution failed'),
    ]
    
    SYNTAX_ERROR_PATTERNS = [
        # General
        (r'SyntaxError:', 'Syntax error'),
        (r'ParseError:', 'Parse error'),
        (r'Unexpected token', 'Unexpected token'),
        (r'expected.*got', 'Syntax expectation mismatch'),
        
        # Python
        (r'IndentationError:', 'Python indentation error'),
        (r'TabError:', 'Python tab/space error'),
        
        # YAML/JSON
        (r'YAMLException:', 'YAML syntax error'),
        (r'JSON\.parse.*error', 'JSON parse error'),
        (r'invalid yaml', 'Invalid YAML syntax'),
    ]
    
    TEST_FAILURE_PATTERNS = [
        (r'FAILED.*tests?', 'Test(s) failed'),
        (r'\d+ failing', 'Tests failing'),
        (r'AssertionError', 'Assertion failed'),
        (r'test.*failed', 'Test failed'),
        (r'pytest.*FAILED', 'Pytest test failed'),
        (r'FAIL:.*test_', 'Unit test failed'),
        (r'Expected.*but got', 'Test expectation failed'),
        (r'jest.*FAIL', 'Jest test failed'),
        (r'mocha.*failing', 'Mocha test failed'),
        (r'✖.*tests? failed', 'Test(s) failed'),
    ]
    
    TIMEOUT_PATTERNS = [
        # Real timeout errors (NOT git timeout=10)
        (r'operation timed? out', 'Operation timeout'),
        (r'timeout exceeded', 'Timeout exceeded'),
        (r'Job timed out', 'Job timeout'),
        (r'exceeded.*timeout', 'Exceeded timeout limit'),
        (r'TimeoutError:', 'Timeout error'),
        (r'ETIMEDOUT', 'Connection timeout'),
        (r'took too long', 'Process took too long'),
        (r'deadline exceeded', 'Deadline exceeded'),
    ]
    
    PERMISSION_ERROR_PATTERNS = [
        (r'Permission denied', 'Permission denied'),
        (r'EACCES:', 'Access error'),
        (r'Access denied', 'Access denied'),
        (r'EPERM:', 'Permission error'),
        (r'not authorized', 'Not authorized'),
        (r'401 Unauthorized', 'Unauthorized'),
        (r'403 Forbidden', 'Forbidden'),
        (r'publickey.*Permission denied', 'SSH key permission error'),
    ]
    
    NETWORK_ERROR_PATTERNS = [
        (r'ECONNREFUSED', 'Connection refused'),
        (r'ENOTFOUND', 'Host not found'),
        (r'getaddrinfo.*ENOTFOUND', 'DNS lookup failed'),
        (r'network.*unreachable', 'Network unreachable'),
        (r'Connection refused', 'Connection refused'),
        (r'Could not connect', 'Connection failed'),
        (r'SSL.*error', 'SSL/TLS error'),
        (r'certificate.*verify failed', 'Certificate verification failed'),
    ]
    
    RESOURCE_ERROR_PATTERNS = [
        (r'out of memory', 'Out of memory'),
        (r'OOMKilled', 'OOM killed'),
        (r'MemoryError', 'Memory error'),
        (r'ENOMEM', 'No memory'),
        (r'no space left on device', 'Disk full'),
        (r'ENOSPC', 'No space'),
        (r'disk quota exceeded', 'Disk quota exceeded'),
        (r'heap.*exceeded', 'Heap size exceeded'),
    ]
    
    ENVIRONMENT_ERROR_PATTERNS = [
        (r'command not found', 'Command not found'),
        (r'is not recognized', 'Command not recognized'),
        (r'not installed', 'Tool not installed'),
        (r'missing.*environment', 'Missing environment variable'),
        (r'JAVA_HOME.*not set', 'JAVA_HOME not set'),
        (r'node.*not found', 'Node.js not found'),
        (r'python.*not found', 'Python not found'),
    ]
    
    # Patterns to IGNORE (false positives)
    IGNORE_PATTERNS = [
        r'timeout=\d+',  # git timeout parameter, NOT an error
        r'# timeout=',   # comment
        r'--timeout',    # CLI flag
        r'-t \d+',       # timeout flag
    ]
    
    # Category descriptions
    CATEGORY_DESCRIPTIONS = {
        'build_error': 'Build Error - Compilation or build process failed',
        'dependency_error': 'Dependency/Package Error - Missing or incompatible dependencies',
        'syntax_error': 'Syntax Error - Code syntax issues',
        'test_failure': 'Test Failure - Unit/Integration tests failed',
        'timeout': 'Timeout - Operation exceeded time limit',
        'permission_error': 'Permission Error - Access denied or insufficient permissions',
        'network_error': 'Network Error - Connection issues or DNS failures',
        'resource_error': 'Resource Error - Out of memory or disk space',
        'environment_error': 'Environment Error - Missing tools or misconfiguration',
        'success': 'Success - Build/Job completed successfully',
    }
    
    def __init__(self, use_gru_fallback: bool = True):
        """
        Initialize hybrid classifier.
        
        Args:
            use_gru_fallback: Whether to use GRU model for unclear cases
        """
        self.use_gru_fallback = use_gru_fallback
        self._gru_classifier = None
        
        # Compile patterns
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for efficiency"""
        self.compiled_rules = {
            'build_error': [(re.compile(p, re.IGNORECASE), d) for p, d in self.BUILD_ERROR_PATTERNS],
            'dependency_error': [(re.compile(p, re.IGNORECASE), d) for p, d in self.DEPENDENCY_ERROR_PATTERNS],
            'syntax_error': [(re.compile(p, re.IGNORECASE), d) for p, d in self.SYNTAX_ERROR_PATTERNS],
            'test_failure': [(re.compile(p, re.IGNORECASE), d) for p, d in self.TEST_FAILURE_PATTERNS],
            'timeout': [(re.compile(p, re.IGNORECASE), d) for p, d in self.TIMEOUT_PATTERNS],
            'permission_error': [(re.compile(p, re.IGNORECASE), d) for p, d in self.PERMISSION_ERROR_PATTERNS],
            'network_error': [(re.compile(p, re.IGNORECASE), d) for p, d in self.NETWORK_ERROR_PATTERNS],
            'resource_error': [(re.compile(p, re.IGNORECASE), d) for p, d in self.RESOURCE_ERROR_PATTERNS],
            'environment_error': [(re.compile(p, re.IGNORECASE), d) for p, d in self.ENVIRONMENT_ERROR_PATTERNS],
        }
        
        self.ignore_patterns = [re.compile(p, re.IGNORECASE) for p in self.IGNORE_PATTERNS]
    
    def _get_gru_classifier(self):
        """Lazy load GRU classifier"""
        if self._gru_classifier is None and self.use_gru_fallback:
            try:
                from .gru_classifier import GRULogClassifier
                self._gru_classifier = GRULogClassifier()
            except Exception as e:
                print(f"Warning: Could not load GRU classifier: {e}")
        return self._gru_classifier
    
    def _preprocess_log(self, log_content: str) -> str:
        """
        Preprocess log to remove noise that causes false positives.
        
        This is key to solving the domain gap - we filter out patterns
        that confuse the model (e.g., "timeout=10" in git commands).
        """
        processed = log_content
        
        # Remove lines that are just noise
        noise_patterns = [
            r'^\s*\[Pipeline\].*$',  # Jenkins pipeline markers
            r'^>\s*git.*timeout=\d+.*$',  # git commands with timeout param
            r'^\s*MallocStackLogging.*$',  # macOS debug noise
        ]
        
        lines = processed.split('\n')
        filtered_lines = []
        
        for line in lines:
            # Keep the line if it doesn't match noise patterns
            is_noise = False
            for pattern in noise_patterns:
                if re.match(pattern, line, re.IGNORECASE):
                    is_noise = True
                    break
            
            # But always keep error lines
            if 'error' in line.lower() or 'failed' in line.lower():
                is_noise = False
            
            if not is_noise:
                filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)
    
    def _detect_success(self, log_content: str) -> bool:
        """Check if log indicates success"""
        content_lower = log_content.lower()
        
        # Final status indicators
        final_success = [
            'finished: success',
            'job succeeded',
            'build succeeded',
            'pipeline succeeded',
            'build successful',
        ]
        
        final_failure = [
            'finished: failure',
            'job failed',
            'build failed', 
            'pipeline failed',
            'error: script returned exit code',
        ]
        
        # Check final status (usually at end of log)
        last_200_chars = content_lower[-200:]
        
        has_success = any(p in content_lower for p in final_success)
        has_failure = any(p in content_lower for p in final_failure)
        
        # Final verdict based on last lines
        for pattern in final_failure:
            if pattern in last_200_chars:
                return False
        
        for pattern in final_success:
            if pattern in last_200_chars:
                return True
        
        return has_success and not has_failure
    
    def _apply_rules(self, log_content: str) -> Optional[RuleMatch]:
        """
        Apply rule-based detection.
        
        Returns the highest confidence match, or None if no match.
        """
        matches: List[RuleMatch] = []
        
        for category, patterns in self.compiled_rules.items():
            category_matches = []
            
            for pattern, description in patterns:
                found = pattern.findall(log_content)
                if found:
                    # Extract evidence (actual matched text)
                    evidence = []
                    for match in pattern.finditer(log_content):
                        # Get line containing match
                        start = log_content.rfind('\n', 0, match.start()) + 1
                        end = log_content.find('\n', match.end())
                        if end == -1:
                            end = len(log_content)
                        evidence.append(log_content[start:end].strip()[:200])
                    
                    # Check if this is a false positive
                    is_false_positive = False
                    for ignore_pattern in self.ignore_patterns:
                        if any(ignore_pattern.search(e) for e in evidence):
                            is_false_positive = True
                            break
                    
                    if not is_false_positive:
                        category_matches.append({
                            'description': description,
                            'count': len(found),
                            'evidence': evidence[:3]  # Top 3 examples
                        })
            
            if category_matches:
                # Calculate confidence based on number of matches
                total_matches = sum(m['count'] for m in category_matches)
                confidence = min(0.95, 0.7 + (total_matches * 0.05))
                
                matches.append(RuleMatch(
                    category=category,
                    confidence=confidence,
                    matched_pattern=category_matches[0]['description'],
                    evidence=[e for m in category_matches for e in m['evidence']][:5]
                ))
        
        if not matches:
            return None
        
        # Return highest confidence match
        matches.sort(key=lambda x: x.confidence, reverse=True)
        return matches[0]
    
    def predict(self, log_content: str) -> Dict:
        """
        Predict error category using hybrid approach.
        
        Strategy:
        1. Check for success first
        2. Apply rule-based detection
        3. If rules match with high confidence, use that
        4. Otherwise, fall back to GRU model
        
        Args:
            log_content: Raw log text
            
        Returns:
            Dict with category, confidence, description, evidence, etc.
        """
        # Step 1: Check for success
        if self._detect_success(log_content):
            return {
                'category': 'success',
                'confidence': 1.0,
                'description': 'Build/Job completed successfully - No errors detected',
                'all_probabilities': {'success': 1.0},
                'is_success': True,
                'method': 'rule-based',
                'evidence': []
            }
        
        # Step 2: Preprocess to remove noise
        processed_log = self._preprocess_log(log_content)
        
        # Step 3: Apply rule-based detection
        rule_match = self._apply_rules(processed_log)
        
        if rule_match and rule_match.confidence >= 0.75:
            # High confidence rule match - use it
            return {
                'category': rule_match.category,
                'confidence': rule_match.confidence,
                'description': self.CATEGORY_DESCRIPTIONS.get(rule_match.category, ''),
                'all_probabilities': {rule_match.category: rule_match.confidence},
                'is_success': False,
                'method': 'rule-based',
                'matched_pattern': rule_match.matched_pattern,
                'evidence': rule_match.evidence
            }
        
        # Step 4: Fall back to GRU model
        gru = self._get_gru_classifier()
        if gru:
            try:
                # Use preprocessed log for GRU too
                gru_result = gru.predict(processed_log)
                
                # If rules had a low-confidence match, consider combining
                if rule_match and rule_match.category == gru_result['category']:
                    # Both agree - boost confidence
                    combined_confidence = min(0.95, gru_result['confidence'] + 0.1)
                    return {
                        'category': gru_result['category'],
                        'confidence': combined_confidence,
                        'description': self.CATEGORY_DESCRIPTIONS.get(gru_result['category'], gru_result['description']),
                        'all_probabilities': gru_result['all_probabilities'],
                        'is_success': False,
                        'method': 'hybrid (rules + GRU agree)',
                        'matched_pattern': rule_match.matched_pattern if rule_match else None,
                        'evidence': rule_match.evidence if rule_match else []
                    }
                elif rule_match and rule_match.confidence > gru_result['confidence']:
                    # Rules more confident than GRU
                    return {
                        'category': rule_match.category,
                        'confidence': rule_match.confidence,
                        'description': self.CATEGORY_DESCRIPTIONS.get(rule_match.category, ''),
                        'all_probabilities': {rule_match.category: rule_match.confidence},
                        'is_success': False,
                        'method': 'rule-based (override GRU)',
                        'matched_pattern': rule_match.matched_pattern,
                        'evidence': rule_match.evidence
                    }
                else:
                    # Use GRU result
                    return {
                        'category': gru_result['category'],
                        'confidence': gru_result['confidence'],
                        'description': self.CATEGORY_DESCRIPTIONS.get(gru_result['category'], gru_result['description']),
                        'all_probabilities': gru_result['all_probabilities'],
                        'is_success': gru_result.get('is_success', False),
                        'method': 'GRU model',
                        'evidence': []
                    }
            except Exception as e:
                print(f"GRU prediction error: {e}")
        
        # Step 5: If all else fails, use rule match or unknown
        if rule_match:
            return {
                'category': rule_match.category,
                'confidence': rule_match.confidence,
                'description': self.CATEGORY_DESCRIPTIONS.get(rule_match.category, ''),
                'all_probabilities': {rule_match.category: rule_match.confidence},
                'is_success': False,
                'method': 'rule-based (fallback)',
                'matched_pattern': rule_match.matched_pattern,
                'evidence': rule_match.evidence
            }
        
        return {
            'category': 'build_error',  # Default assumption for failed builds
            'confidence': 0.5,
            'description': 'Unknown error - Could not determine specific category',
            'all_probabilities': {'build_error': 0.5},
            'is_success': False,
            'method': 'default',
            'evidence': []
        }


# Global instance
_hybrid_classifier: Optional[HybridLogClassifier] = None


def get_hybrid_classifier() -> HybridLogClassifier:
    """Get or create global hybrid classifier instance"""
    global _hybrid_classifier
    if _hybrid_classifier is None:
        _hybrid_classifier = HybridLogClassifier()
    return _hybrid_classifier


def classify_log_hybrid(log_content: str) -> Dict:
    """
    Classify a log using hybrid approach.
    
    This is the recommended function to use for production.
    """
    classifier = get_hybrid_classifier()
    return classifier.predict(log_content)


if __name__ == '__main__':
    # Test with sample logs
    test_logs = [
        # TypeScript build error (was misclassified as timeout)
        """
        [2025-10-14T19:20:24.478Z] Failed to compile.
        [2025-10-14T19:20:24.478Z] Type error: Object literal may only specify known properties, but 'MONGODB_URL' does not exist in type 'EnvironmentConfig'.
        > git fetch --tags --force --progress -- https://github.com/example # timeout=10
        ERROR: script returned exit code 1
        """,
        
        # NPM dependency error
        """
        npm ERR! code ERESOLVE
        npm ERR! ERESOLVE unable to resolve dependency tree
        npm ERR! peer react@"^17.0.0" from react-scripts@4.0.3
        """,
        
        # Test failure
        """
        FAIL src/tests/auth.test.ts
        ✕ should authenticate user (45 ms)
        Expected: true
        Received: false
        3 tests failed
        """,
    ]
    
    classifier = HybridLogClassifier()
    
    for i, log in enumerate(test_logs, 1):
        print(f"\n{'='*60}")
        print(f"Test #{i}")
        print(f"{'='*60}")
        result = classifier.predict(log)
        print(f"Category: {result['category']}")
        print(f"Confidence: {result['confidence']:.1%}")
        print(f"Method: {result['method']}")
        if result.get('evidence'):
            print(f"Evidence: {result['evidence'][0][:100]}...")
