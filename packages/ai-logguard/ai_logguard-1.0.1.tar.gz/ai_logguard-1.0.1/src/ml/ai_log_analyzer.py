"""
AI-Powered Log Analyzer
Sử dụng LLM để phân tích log CI/CD và đưa ra gợi ý sửa lỗi

Không dùng regex patterns cố định - AI tự động:
1. Đọc và hiểu log
2. Xác định lỗi và nguyên nhân gốc
3. Đưa ra gợi ý sửa lỗi cụ thể

Hỗ trợ:
- Ollama (local, miễn phí)
- OpenAI API
- Fallback về basic analysis nếu không có AI
"""
import os
import json
import re
import subprocess
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class AIProvider(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    NONE = "none"


@dataclass
class AnalysisResult:
    """Kết quả phân tích từ AI"""
    success: bool
    error_summary: str
    root_cause: str
    root_cause_explanation: str
    layer: str  # CI, Build, App, Infra, Platform, Data, Security
    severity: str  # low, medium, high, critical
    fix_suggestions: List[Dict[str, Any]]
    raw_errors: List[str]
    confidence: float  # 0.0 - 1.0
    ai_provider: str
    

class AILogAnalyzer:
    """
    AI-Powered Log Analyzer
    
    Sử dụng LLM để phân tích log thay vì regex patterns
    """
    
    # System prompt cho AI - hướng dẫn cách phân tích log
    SYSTEM_PROMPT = """Bạn là chuyên gia phân tích CI/CD logs. Nhiệm vụ của bạn là:

1. ĐỌC LOG và xác định lỗi chính
2. PHÂN TÍCH nguyên nhân gốc (root cause) - không phải triệu chứng
3. ĐƯA RA gợi ý sửa lỗi cụ thể, có thể thực hiện được

QUAN TRỌNG:
- Tập trung vào LỖI CHÍNH, không liệt kê tất cả warnings
- Giải thích TẠI SAO lỗi xảy ra
- Đưa ra COMMANDS cụ thể để sửa
- Cảnh báo nếu action có rủi ro cao

Output JSON format:
{
    "error_found": true/false,
    "error_summary": "Tóm tắt ngắn gọn lỗi chính",
    "root_cause": "Nguyên nhân gốc của lỗi",
    "root_cause_explanation": "Giải thích chi tiết tại sao lỗi xảy ra",
    "layer": "CI|Build|App|Infra|Platform|Data|Security",
    "severity": "low|medium|high|critical",
    "raw_errors": ["dòng lỗi 1", "dòng lỗi 2"],
    "fix_suggestions": [
        {
            "title": "Tiêu đề gợi ý",
            "description": "Mô tả chi tiết",
            "commands": ["command 1", "command 2"],
            "risk_level": "safe|low|medium|high|critical",
            "conditions": ["điều kiện 1", "điều kiện 2"],
            "why": "Tại sao gợi ý này giải quyết được vấn đề"
        }
    ],
    "confidence": 0.95
}"""

    def __init__(self, provider: Optional[AIProvider] = None, model: Optional[str] = None):
        """
        Khởi tạo AI Analyzer
        
        Args:
            provider: AIProvider.OLLAMA hoặc AIProvider.OPENAI
            model: Tên model (e.g., "llama3.2", "gpt-4")
        """
        self.provider = provider or self._detect_provider()
        self.model = model or self._get_default_model()
        
    def _detect_provider(self) -> AIProvider:
        """Auto-detect available AI provider"""
        # Check Ollama first (local, free)
        if self._check_ollama():
            return AIProvider.OLLAMA
        
        # Check OpenAI
        if os.getenv("OPENAI_API_KEY"):
            return AIProvider.OPENAI
        
        return AIProvider.NONE
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is running"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _get_default_model(self) -> str:
        """Get default model for provider"""
        if self.provider == AIProvider.OLLAMA:
            # Check available models
            try:
                result = subprocess.run(
                    ["ollama", "list"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        # Get first model name
                        first_model = lines[1].split()[0]
                        return first_model
            except:
                pass
            return "llama3.2"  # Default
        elif self.provider == AIProvider.OPENAI:
            return "gpt-4o-mini"
        return ""
    
    def analyze(self, log_content: str) -> AnalysisResult:
        """
        Phân tích log sử dụng AI
        
        Args:
            log_content: Nội dung log
            
        Returns:
            AnalysisResult với đầy đủ thông tin
        """
        if self.provider == AIProvider.OLLAMA:
            return self._analyze_with_ollama(log_content)
        elif self.provider == AIProvider.OPENAI:
            return self._analyze_with_openai(log_content)
        else:
            return self._analyze_basic(log_content)
    
    def _analyze_with_ollama(self, log_content: str) -> AnalysisResult:
        """Phân tích sử dụng Ollama local"""
        try:
            # Truncate log if too long
            max_chars = 8000
            if len(log_content) > max_chars:
                # Keep first and last parts
                half = max_chars // 2
                log_content = log_content[:half] + "\n...[TRUNCATED]...\n" + log_content[-half:]
            
            prompt = f"""Phân tích CI/CD log sau và trả về JSON:

```
{log_content}
```

Trả về JSON theo format đã hướng dẫn. CHỈ trả về JSON, không có text khác."""

            # Call Ollama
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True,
                text=True,
                timeout=60,
                env={**os.environ, "OLLAMA_SYSTEM": self.SYSTEM_PROMPT}
            )
            
            if result.returncode != 0:
                return self._analyze_basic(log_content)
            
            # Parse JSON response
            response = result.stdout.strip()
            return self._parse_ai_response(response, "ollama")
            
        except Exception as e:
            print(f"Ollama error: {e}")
            return self._analyze_basic(log_content)
    
    def _analyze_with_openai(self, log_content: str) -> AnalysisResult:
        """Phân tích sử dụng OpenAI API"""
        try:
            import openai
            
            client = openai.OpenAI()
            
            # Truncate log if too long
            max_chars = 12000
            if len(log_content) > max_chars:
                half = max_chars // 2
                log_content = log_content[:half] + "\n...[TRUNCATED]...\n" + log_content[-half:]
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": f"Phân tích CI/CD log sau:\n\n```\n{log_content}\n```\n\nTrả về JSON theo format đã hướng dẫn."}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            return self._parse_ai_response(response.choices[0].message.content, "openai")
            
        except Exception as e:
            print(f"OpenAI error: {e}")
            return self._analyze_basic(log_content)
    
    def _parse_ai_response(self, response: str, provider: str) -> AnalysisResult:
        """Parse AI response thành AnalysisResult"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                data = json.loads(json_match.group())
            else:
                raise ValueError("No JSON found in response")
            
            return AnalysisResult(
                success=data.get("error_found", True),
                error_summary=data.get("error_summary", "Unknown error"),
                root_cause=data.get("root_cause", "Unknown"),
                root_cause_explanation=data.get("root_cause_explanation", ""),
                layer=data.get("layer", "Unknown"),
                severity=data.get("severity", "medium"),
                fix_suggestions=data.get("fix_suggestions", []),
                raw_errors=data.get("raw_errors", []),
                confidence=data.get("confidence", 0.8),
                ai_provider=provider
            )
        except Exception as e:
            print(f"Parse error: {e}")
            return self._create_fallback_result(response, provider)
    
    def _create_fallback_result(self, response: str, provider: str) -> AnalysisResult:
        """Tạo result khi không parse được JSON"""
        return AnalysisResult(
            success=True,
            error_summary="AI analysis completed but response parsing failed",
            root_cause="See raw response",
            root_cause_explanation=response[:500],
            layer="Unknown",
            severity="medium",
            fix_suggestions=[{
                "title": "Review AI Response",
                "description": response[:1000],
                "commands": [],
                "risk_level": "safe",
                "conditions": [],
                "why": "AI response cần được review thủ công"
            }],
            raw_errors=[],
            confidence=0.5,
            ai_provider=provider
        )
    
    def _analyze_basic(self, log_content: str) -> AnalysisResult:
        """
        Basic analysis khi không có AI
        Sử dụng simple heuristics thay vì regex patterns phức tạp
        """
        lines = log_content.split('\n')
        
        # Tìm dòng có keywords lỗi
        error_keywords = ['error', 'failed', 'fatal', 'exception', 'panic', 'denied', 'not found', 'cannot', 'unable']
        success_keywords = ['success', 'passed', 'completed', 'done']
        
        error_lines = []
        last_error_line = ""
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Skip success lines
            if any(kw in line_lower for kw in success_keywords):
                continue
            
            # Detect error lines
            if any(kw in line_lower for kw in error_keywords):
                error_lines.append(line.strip())
                last_error_line = line.strip()
        
        # Xác định lỗi cuối cùng (thường là root cause indicator)
        if error_lines:
            # Lấy context xung quanh error cuối
            root_cause = error_lines[-1] if error_lines else "Unknown error"
            
            # Detect layer từ keywords
            layer = self._detect_layer_basic(log_content)
            
            # Tạo gợi ý cơ bản
            fix_suggestions = self._generate_basic_suggestions(root_cause, layer, log_content)
            
            return AnalysisResult(
                success=True,
                error_summary=root_cause[:200],
                root_cause=root_cause,
                root_cause_explanation="Phân tích cơ bản dựa trên keywords. Cài đặt Ollama để có phân tích AI chi tiết hơn.",
                layer=layer,
                severity="medium",
                fix_suggestions=fix_suggestions,
                raw_errors=error_lines[:5],
                confidence=0.6,
                ai_provider="basic"
            )
        
        return AnalysisResult(
            success=False,
            error_summary="No errors detected",
            root_cause="",
            root_cause_explanation="",
            layer="Unknown",
            severity="low",
            fix_suggestions=[],
            raw_errors=[],
            confidence=0.9,
            ai_provider="basic"
        )
    
    def _detect_layer_basic(self, log_content: str) -> str:
        """Detect layer từ log content"""
        log_lower = log_content.lower()
        
        layer_keywords = {
            "CI": ["runner", "gitlab-runner", "jenkins", "github actions", "executor"],
            "Build": ["build", "compile", "npm", "pip", "docker build", "webpack"],
            "App": ["test", "assert", "exception", "traceback", "unittest", "pytest"],
            "Infra": ["kubernetes", "k8s", "kubectl", "docker", "container", "pod"],
            "Platform": ["1c", "designer", "infobase", "repository", "extension"],
            "Data": ["database", "migration", "sql", "schema", "table"],
            "Security": ["vulnerability", "cve", "security", "permission", "auth"],
        }
        
        scores = {layer: 0 for layer in layer_keywords}
        for layer, keywords in layer_keywords.items():
            for kw in keywords:
                if kw in log_lower:
                    scores[layer] += 1
        
        max_layer = max(scores, key=scores.get)
        return max_layer if scores[max_layer] > 0 else "Unknown"
    
    def _generate_basic_suggestions(self, error: str, layer: str, log_content: str) -> List[Dict]:
        """Tạo gợi ý cơ bản dựa trên error và layer"""
        suggestions = []
        
        error_lower = error.lower()
        
        # Common patterns
        if "not found" in error_lower or "cannot find" in error_lower:
            suggestions.append({
                "title": "🔍 Check Missing Resource",
                "description": f"Một resource không tìm thấy: {error[:100]}",
                "commands": [
                    "# Kiểm tra resource có tồn tại không",
                    "# Kiểm tra path/tên có đúng không",
                    "# Kiểm tra permissions",
                ],
                "risk_level": "safe",
                "conditions": ["Có thể reproduce lỗi locally"],
                "why": "Resource bị thiếu hoặc path không đúng"
            })
        
        if "permission" in error_lower or "denied" in error_lower or "access" in error_lower:
            suggestions.append({
                "title": "🔐 Check Permissions",
                "description": "Lỗi liên quan đến quyền truy cập",
                "commands": [
                    "# Kiểm tra user/role có quyền không",
                    "# Kiểm tra file permissions: ls -la <path>",
                    "# Kiểm tra credentials",
                ],
                "risk_level": "low",
                "conditions": ["Có quyền admin để kiểm tra"],
                "why": "User/process không có quyền thực hiện action"
            })
        
        if "exit code 1" in error_lower or "failed" in error_lower:
            suggestions.append({
                "title": "⚠️ Debug Command Failure",
                "description": "Command thực thi thất bại",
                "commands": [
                    "# Chạy lại command với verbose mode",
                    "# Kiểm tra dependencies",
                    "# Xem full error output",
                ],
                "risk_level": "safe",
                "conditions": ["Có thể chạy locally"],
                "why": "Command exit với error code"
            })
        
        if "is not a" in error_lower and "command" in error_lower:
            suggestions.append({
                "title": "🔧 Fix Invalid Command",
                "description": "Command không hợp lệ hoặc script syntax sai",
                "commands": [
                    "# Kiểm tra script syntax",
                    "# Đảm bảo dùng đúng shell (bash vs sh)",
                    "# Kiểm tra .gitlab-ci.yml hoặc Jenkinsfile",
                ],
                "risk_level": "safe",
                "conditions": ["Có access vào CI config"],
                "why": "Command được gọi sai hoặc script format không đúng"
            })
        
        # Layer-specific suggestions
        if layer == "CI":
            suggestions.append({
                "title": "🏃 Check CI Configuration",
                "description": "Kiểm tra CI/CD configuration",
                "commands": [
                    "# GitLab: Kiểm tra .gitlab-ci.yml",
                    "# Jenkins: Kiểm tra Jenkinsfile",
                    "# GitHub: Kiểm tra .github/workflows/",
                ],
                "risk_level": "safe",
                "conditions": [],
                "why": "Lỗi ở tầng CI thường do config sai"
            })
        elif layer == "Build":
            suggestions.append({
                "title": "📦 Fix Build Issues",
                "description": "Debug build problems",
                "commands": [
                    "# Build locally với verbose",
                    "# Clear cache và rebuild",
                    "# Kiểm tra dependencies versions",
                ],
                "risk_level": "low",
                "conditions": ["Có thể build locally"],
                "why": "Build errors thường do dependencies hoặc config"
            })
        
        if not suggestions:
            suggestions.append({
                "title": "🔍 General Debug Steps",
                "description": f"Lỗi: {error[:150]}",
                "commands": [
                    "# 1. Reproduce locally",
                    "# 2. Check full logs",
                    "# 3. Search error message online",
                    "# 4. Check recent changes (git diff)",
                ],
                "risk_level": "safe",
                "conditions": [],
                "why": "Cần debug thêm để xác định nguyên nhân cụ thể"
            })
        
        return suggestions


# Singleton instance
_analyzer_instance = None

def get_ai_analyzer(provider: Optional[AIProvider] = None, model: Optional[str] = None) -> AILogAnalyzer:
    """Get or create AI analyzer instance"""
    global _analyzer_instance
    if _analyzer_instance is None or provider is not None:
        _analyzer_instance = AILogAnalyzer(provider, model)
    return _analyzer_instance


def analyze_log_with_ai(log_content: str) -> AnalysisResult:
    """
    Phân tích log sử dụng AI
    
    Args:
        log_content: Nội dung log
        
    Returns:
        AnalysisResult
    """
    analyzer = get_ai_analyzer()
    return analyzer.analyze(log_content)
