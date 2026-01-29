"""
Root Cause Extractor - Trích xuất nguyên nhân lỗi từ log
Phân tích log để tìm thông tin cụ thể cho gợi ý sửa lỗi
"""
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class RootCause:
    """Thông tin root cause được trích xuất từ log"""
    category: str
    error_message: str = ""
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    package_name: Optional[str] = None
    package_version: Optional[str] = None
    required_version: Optional[str] = None
    command_failed: Optional[str] = None
    exit_code: Optional[int] = None
    timeout_seconds: Optional[int] = None
    missing_env_var: Optional[str] = None
    permission_path: Optional[str] = None
    network_host: Optional[str] = None
    memory_limit: Optional[str] = None
    test_name: Optional[str] = None
    assertion_expected: Optional[str] = None
    assertion_actual: Optional[str] = None
    suggestions: List[str] = field(default_factory=list)
    raw_errors: List[str] = field(default_factory=list)
    confidence: float = 0.0


class RootCauseExtractor:
    """Trích xuất root cause từ log dựa trên patterns"""
    
    def __init__(self):
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns cho các loại lỗi"""
        
        # ===== DEPENDENCY ERRORS =====
        self.dep_patterns = {
            # NPM errors
            'npm_not_found': re.compile(
                r"npm ERR!.*(?:Cannot find module|Module not found)[:\s]*['\"]?([^'\"]+)['\"]?",
                re.IGNORECASE
            ),
            'npm_peer_dep': re.compile(
                r"npm ERR!.*peer (?:dep(?:endency)?)[:\s]*['\"]?([^'\"@\s]+)@?['\"]?([^\s]*)?.*from[:\s]*['\"]?([^'\"@\s]+)",
                re.IGNORECASE
            ),
            'npm_version_conflict': re.compile(
                r"npm ERR!.*Found:\s*([^@]+)@(\S+).*Could not resolve.*(?:requires?|peer)[:\s]*([^@]+)@([^\s]+)",
                re.IGNORECASE | re.DOTALL
            ),
            'npm_eresolve': re.compile(
                r"npm ERR! ERESOLVE.*unable to resolve.*tree",
                re.IGNORECASE
            ),
            
            # Python/pip errors
            'pip_not_found': re.compile(
                r"(?:ModuleNotFoundError|ImportError)[:\s]*No module named ['\"]?([^'\"]+)['\"]?",
                re.IGNORECASE
            ),
            'pip_version': re.compile(
                r"(?:pip|requires)[:\s]*([^>=<!\s]+)\s*([><=!]+)\s*(\S+)",
                re.IGNORECASE
            ),
            'pip_conflict': re.compile(
                r"(?:incompatible|conflict).*([^>=<\s]+)\s*([><=]+)\s*(\S+)",
                re.IGNORECASE
            ),
            
            # Generic package errors
            'package_missing': re.compile(
                r"(?:package|module|library)[:\s]*['\"]?([^'\"]+)['\"]?\s*(?:not found|missing|does not exist)",
                re.IGNORECASE
            ),
        }
        
        # ===== SYNTAX ERRORS =====
        self.syntax_patterns = {
            'python_syntax': re.compile(
                r"(?:SyntaxError|IndentationError)[:\s]*(.+?)(?:\n|$).*?File ['\"]([^'\"]+)['\"],\s*line (\d+)",
                re.IGNORECASE | re.DOTALL
            ),
            'js_syntax': re.compile(
                r"(?:SyntaxError|Unexpected token)[:\s]*(.+?)(?:\n|$).*?(?:at\s+)?([^\s:]+):(\d+)",
                re.IGNORECASE | re.DOTALL
            ),
            'ts_error': re.compile(
                r"(?:error TS\d+)[:\s]*(.+?)(?:\n|$).*?([^\s:]+)\((\d+),(\d+)\)",
                re.IGNORECASE | re.DOTALL
            ),
            'generic_syntax': re.compile(
                r"(?:syntax error|parse error)[:\s]*(.+?)(?:\n|$)",
                re.IGNORECASE
            ),
            'file_line': re.compile(
                r"(?:File|at)\s+['\"]?([^'\":\s]+)['\"]?[:\s]*(?:line\s*)?(\d+)",
                re.IGNORECASE
            ),
        }
        
        # ===== TEST FAILURES =====
        self.test_patterns = {
            'jest_fail': re.compile(
                r"(?:FAIL|✕)\s+(.+?\.(?:test|spec)\.[jt]sx?)",
                re.IGNORECASE
            ),
            'pytest_fail': re.compile(
                r"(?:FAILED|ERROR)\s+([^\s:]+)::([^\s:]+)",
                re.IGNORECASE
            ),
            'assertion': re.compile(
                r"(?:AssertionError|assert|expect)[:\s]*(.+?)(?:\n|$)",
                re.IGNORECASE
            ),
            'expected_actual': re.compile(
                r"(?:expected|received)[:\s]*['\"]?(.+?)['\"]?\s*(?:but got|to (?:be|equal)|received)[:\s]*['\"]?(.+?)['\"]?(?:\n|$)",
                re.IGNORECASE
            ),
            'test_name': re.compile(
                r"(?:test|it|describe)\s*\(['\"](.+?)['\"]",
                re.IGNORECASE
            ),
        }
        
        # ===== TIMEOUT =====
        self.timeout_patterns = {
            'timeout_seconds': re.compile(
                r"(?:timeout|timed? out)[:\s]*(\d+)\s*(?:s(?:ec(?:ond)?s?)?|m(?:in(?:ute)?s?)?)?",
                re.IGNORECASE
            ),
            'connection_timeout': re.compile(
                r"(?:connection|connect|request)\s*(?:timeout|timed? out)",
                re.IGNORECASE
            ),
            'operation_timeout': re.compile(
                r"(?:operation|task|job|build)\s*(?:exceeded|timeout|timed? out)",
                re.IGNORECASE
            ),
        }
        
        # ===== NETWORK ERRORS =====
        self.network_patterns = {
            'host_unreachable': re.compile(
                r"(?:ENOTFOUND|ENETUNREACH|ECONNREFUSED|getaddrinfo)[:\s]*.*?(?:host|address)[:\s]*['\"]?([^\s'\"]+)['\"]?",
                re.IGNORECASE
            ),
            'dns_error': re.compile(
                r"(?:DNS|getaddrinfo).*?(?:failed|error|ENOTFOUND).*?['\"]?([^\s'\"]+)['\"]?",
                re.IGNORECASE
            ),
            'connection_refused': re.compile(
                r"(?:ECONNREFUSED|connection refused).*?(?:to\s+)?['\"]?([^\s'\":]+)['\"]?(?::(\d+))?",
                re.IGNORECASE
            ),
            'ssl_error': re.compile(
                r"(?:SSL|TLS|certificate).*?(?:error|failed|invalid)",
                re.IGNORECASE
            ),
        }
        
        # ===== PERMISSION ERRORS =====
        self.permission_patterns = {
            'permission_denied': re.compile(
                r"(?:permission denied|EACCES|EPERM)[:\s]*['\"]?([^'\"]+)['\"]?",
                re.IGNORECASE
            ),
            'access_denied': re.compile(
                r"(?:access denied|forbidden|unauthorized).*?['\"]?([^'\"]+)['\"]?",
                re.IGNORECASE
            ),
            'sudo_required': re.compile(
                r"(?:requires? (?:root|sudo|admin)|run as (?:root|administrator))",
                re.IGNORECASE
            ),
        }
        
        # ===== RESOURCE ERRORS =====
        self.resource_patterns = {
            'oom': re.compile(
                r"(?:out of memory|OOMKilled|ENOMEM|heap out of memory|JavaScript heap)",
                re.IGNORECASE
            ),
            'disk_space': re.compile(
                r"(?:no space left|ENOSPC|disk full|out of disk)",
                re.IGNORECASE
            ),
            'memory_limit': re.compile(
                r"(?:memory limit|max.?old.?space)[:\s]*(\d+)\s*(?:MB|GB|bytes)?",
                re.IGNORECASE
            ),
        }
        
        # ===== ENVIRONMENT ERRORS =====
        self.env_patterns = {
            'env_var_missing': re.compile(
                r"(?:environment variable|env|process\.env)\s*['\"]?([A-Z_][A-Z0-9_]*)['\"]?\s*(?:is not set|undefined|missing|not found)",
                re.IGNORECASE
            ),
            'command_not_found': re.compile(
                r"(?:command not found|not recognized)[:\s]*['\"]?([^'\"]+)['\"]?",
                re.IGNORECASE
            ),
            'version_mismatch': re.compile(
                r"(?:requires?|expected)\s*(?:node|python|java|npm)\s*(?:version\s*)?([><=!]*\s*[\d.]+)",
                re.IGNORECASE
            ),
        }
        
        # ===== BUILD ERRORS =====
        self.build_patterns = {
            'compilation_error': re.compile(
                r"(?:compilation|compile|build)\s*(?:failed|error).*?([^\n]+)",
                re.IGNORECASE
            ),
            'exit_code': re.compile(
                r"(?:exit(?:ed)?\s*(?:with|code)|return(?:ed)?\s*(?:code)?)[:\s]*(\d+)",
                re.IGNORECASE
            ),
            'command_failed': re.compile(
                r"(?:command|script)\s*['\"]?([^'\"]+)['\"]?\s*(?:failed|error|exit)",
                re.IGNORECASE
            ),
        }
    
    def _detect_actual_category(self, log_content: str, ml_category: str) -> str:
        """
        Auto-detect category từ log content để cross-validate với GRU model.
        Nếu log content rõ ràng cho thấy loại lỗi khác, ưu tiên loại đó.
        """
        log_lower = log_content.lower()
        
        # Strong indicators for each category
        indicators = {
            'test_failure': [
                r'\bFAILED\s+\S+::\S+',  # pytest format
                r'\b(?:FAIL|✕)\s+\S+\.(?:test|spec)\.',  # jest format
                r'AssertionError',
                r'test.*(?:failed|failure)',
                r'expected.*(?:but\s+(?:got|received)|to\s+(?:be|equal))',
            ],
            'dependency_error': [
                r'npm ERR!.*(?:Cannot find module|peer dep)',
                r'ModuleNotFoundError',
                r'ImportError.*No module',
                r'Could not resolve dependency',
                r'package.*not found',
            ],
            'syntax_error': [
                r'SyntaxError',
                r'IndentationError',
                r'Unexpected token',
                r'error TS\d+:',
                r'Parse error',
            ],
            'network_error': [
                r'ENOTFOUND|ENETUNREACH|ECONNREFUSED',
                r'getaddrinfo.*fail',
                r'connection refused',
                r'DNS.*(?:error|fail)',
            ],
            'permission_error': [
                r'EACCES|EPERM',
                r'permission denied',
                r'access denied',
            ],
            'resource_error': [
                r'out of memory|OOMKilled',
                r'ENOMEM',
                r'heap out of memory',
                r'no space left|ENOSPC',
            ],
            'environment_error': [
                r'command not found',
                r'env.*(?:not set|undefined|missing)',
                r'version.*(?:mismatch|required)',
            ],
            'timeout': [
                r'timeout|timed?\s*out',
                r'exceeded.*time.*limit',
            ],
        }
        
        # Count matches for each category
        scores = {}
        for category, patterns in indicators.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, log_content, re.IGNORECASE):
                    score += 1
            scores[category] = score
        
        # Find best matching category
        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]
        
        # Only override if we have strong evidence (score >= 2) and ML category has no matches
        if best_score >= 2 and scores.get(ml_category.lower(), 0) == 0:
            return best_category
        elif best_score >= 1 and ml_category.lower() == 'build_error':
            # build_error is often a catch-all, be more lenient to override
            return best_category
        
        return ml_category
    
    def extract(self, log_content: str, category: str) -> RootCause:
        """
        Trích xuất root cause từ log dựa trên category
        
        Args:
            log_content: Nội dung log
            category: Loại lỗi từ GRU model
            
        Returns:
            RootCause object với thông tin chi tiết
        """
        # Cross-validate category with log content
        actual_category = self._detect_actual_category(log_content, category)
        
        root_cause = RootCause(category=actual_category)
        
        # Store original ML category if different
        if actual_category != category:
            root_cause.error_message = f"[Auto-corrected: {category} → {actual_category}] "
        
        # Extract raw error lines
        root_cause.raw_errors = self._extract_error_lines(log_content)
        if root_cause.raw_errors:
            if root_cause.error_message:
                root_cause.error_message += root_cause.raw_errors[0]
            else:
                root_cause.error_message = root_cause.raw_errors[0]
        
        # Category-specific extraction
        extractors = {
            'dependency_error': self._extract_dependency,
            'syntax_error': self._extract_syntax,
            'test_failure': self._extract_test,
            'timeout': self._extract_timeout,
            'network_error': self._extract_network,
            'permission_error': self._extract_permission,
            'resource_error': self._extract_resource,
            'environment_error': self._extract_environment,
            'build_error': self._extract_build,
        }
        
        extractor = extractors.get(actual_category.lower(), self._extract_generic)
        extractor(log_content, root_cause)
        
        # Generate suggestions based on extracted info
        root_cause.suggestions = self._generate_suggestions(root_cause)
        
        # Calculate confidence based on how much info was extracted
        root_cause.confidence = self._calculate_confidence(root_cause)
        
        return root_cause
    
    def _extract_error_lines(self, log_content: str) -> List[str]:
        """Trích xuất các dòng có chứa error"""
        error_pattern = re.compile(
            r"^.*(?:error|fail(?:ed|ure)?|exception|fatal|critical).*$",
            re.IGNORECASE | re.MULTILINE
        )
        matches = error_pattern.findall(log_content)
        # Lọc bỏ các dòng trùng lặp và giữ top 5
        seen = set()
        unique = []
        for m in matches:
            m_clean = m.strip()
            if m_clean and m_clean not in seen:
                seen.add(m_clean)
                unique.append(m_clean)
        return unique[:5]
    
    def _extract_dependency(self, log_content: str, rc: RootCause):
        """Trích xuất thông tin dependency error"""
        # NPM not found
        match = self.dep_patterns['npm_not_found'].search(log_content)
        if match:
            rc.package_name = match.group(1)
        
        # NPM peer dependency
        match = self.dep_patterns['npm_peer_dep'].search(log_content)
        if match:
            rc.package_name = match.group(1)
            rc.package_version = match.group(2) if match.group(2) else None
        
        # NPM version conflict
        match = self.dep_patterns['npm_version_conflict'].search(log_content)
        if match:
            rc.package_name = match.group(1)
            rc.package_version = match.group(2)
            rc.required_version = match.group(4) if len(match.groups()) >= 4 else None
        
        # Python module not found
        match = self.dep_patterns['pip_not_found'].search(log_content)
        if match:
            rc.package_name = match.group(1)
        
        # Generic package missing
        if not rc.package_name:
            match = self.dep_patterns['package_missing'].search(log_content)
            if match:
                rc.package_name = match.group(1)
    
    def _extract_syntax(self, log_content: str, rc: RootCause):
        """Trích xuất thông tin syntax error"""
        # Python syntax error
        match = self.syntax_patterns['python_syntax'].search(log_content)
        if match:
            rc.error_message = match.group(1).strip()
            rc.file_path = match.group(2)
            rc.line_number = int(match.group(3))
            return
        
        # TypeScript error
        match = self.syntax_patterns['ts_error'].search(log_content)
        if match:
            rc.error_message = match.group(1).strip()
            rc.file_path = match.group(2)
            rc.line_number = int(match.group(3))
            return
        
        # JavaScript syntax error
        match = self.syntax_patterns['js_syntax'].search(log_content)
        if match:
            rc.error_message = match.group(1).strip()
            rc.file_path = match.group(2)
            rc.line_number = int(match.group(3))
            return
        
        # Generic file:line
        match = self.syntax_patterns['file_line'].search(log_content)
        if match:
            rc.file_path = match.group(1)
            rc.line_number = int(match.group(2))
    
    def _extract_test(self, log_content: str, rc: RootCause):
        """Trích xuất thông tin test failure"""
        # Jest test file
        match = self.test_patterns['jest_fail'].search(log_content)
        if match:
            rc.file_path = match.group(1)
        
        # Pytest test
        match = self.test_patterns['pytest_fail'].search(log_content)
        if match:
            rc.file_path = match.group(1)
            rc.test_name = match.group(2)
        
        # Test name
        match = self.test_patterns['test_name'].search(log_content)
        if match and not rc.test_name:
            rc.test_name = match.group(1)
        
        # Assertion
        match = self.test_patterns['assertion'].search(log_content)
        if match:
            rc.error_message = match.group(1).strip()
        
        # Expected vs actual
        match = self.test_patterns['expected_actual'].search(log_content)
        if match:
            rc.assertion_expected = match.group(1).strip()
            rc.assertion_actual = match.group(2).strip()
    
    def _extract_timeout(self, log_content: str, rc: RootCause):
        """Trích xuất thông tin timeout"""
        match = self.timeout_patterns['timeout_seconds'].search(log_content)
        if match:
            value = int(match.group(1))
            unit = match.group(2) if len(match.groups()) > 1 else 's'
            if unit and unit.startswith('m'):
                value *= 60
            rc.timeout_seconds = value
        
        # Connection timeout host
        match = self.network_patterns['host_unreachable'].search(log_content)
        if match:
            rc.network_host = match.group(1)
    
    def _extract_network(self, log_content: str, rc: RootCause):
        """Trích xuất thông tin network error"""
        match = self.network_patterns['host_unreachable'].search(log_content)
        if match:
            rc.network_host = match.group(1)
            return
        
        match = self.network_patterns['dns_error'].search(log_content)
        if match:
            rc.network_host = match.group(1)
            return
        
        match = self.network_patterns['connection_refused'].search(log_content)
        if match:
            rc.network_host = match.group(1)
    
    def _extract_permission(self, log_content: str, rc: RootCause):
        """Trích xuất thông tin permission error"""
        match = self.permission_patterns['permission_denied'].search(log_content)
        if match:
            rc.permission_path = match.group(1)
            return
        
        match = self.permission_patterns['access_denied'].search(log_content)
        if match:
            rc.permission_path = match.group(1)
    
    def _extract_resource(self, log_content: str, rc: RootCause):
        """Trích xuất thông tin resource error"""
        match = self.resource_patterns['memory_limit'].search(log_content)
        if match:
            rc.memory_limit = match.group(1)
        
        if self.resource_patterns['oom'].search(log_content):
            rc.error_message = "Out of memory"
        elif self.resource_patterns['disk_space'].search(log_content):
            rc.error_message = "Out of disk space"
    
    def _extract_environment(self, log_content: str, rc: RootCause):
        """Trích xuất thông tin environment error"""
        match = self.env_patterns['env_var_missing'].search(log_content)
        if match:
            rc.missing_env_var = match.group(1)
            return
        
        match = self.env_patterns['command_not_found'].search(log_content)
        if match:
            rc.command_failed = match.group(1)
    
    def _extract_build(self, log_content: str, rc: RootCause):
        """Trích xuất thông tin build error"""
        match = self.build_patterns['exit_code'].search(log_content)
        if match:
            rc.exit_code = int(match.group(1))
        
        match = self.build_patterns['command_failed'].search(log_content)
        if match:
            rc.command_failed = match.group(1)
        
        # Also try syntax patterns for file/line info
        self._extract_syntax(log_content, rc)
    
    def _extract_generic(self, log_content: str, rc: RootCause):
        """Fallback extraction for unknown categories"""
        # Try to extract any file:line info
        match = self.syntax_patterns['file_line'].search(log_content)
        if match:
            rc.file_path = match.group(1)
            rc.line_number = int(match.group(2))
        
        # Exit code
        match = self.build_patterns['exit_code'].search(log_content)
        if match:
            rc.exit_code = int(match.group(1))
    
    def _generate_suggestions(self, rc: RootCause) -> List[str]:
        """Tạo gợi ý sửa lỗi dựa trên thông tin đã extract"""
        suggestions = []
        
        if rc.category == 'dependency_error':
            if rc.package_name:
                suggestions.append(f"Install package: `npm install {rc.package_name}` hoặc `pip install {rc.package_name}`")
                if rc.required_version:
                    suggestions.append(f"Cài đặt version cụ thể: `npm install {rc.package_name}@{rc.required_version}`")
                suggestions.append(f"Kiểm tra package.json/requirements.txt có chứa `{rc.package_name}`")
            suggestions.append("Clean install: `rm -rf node_modules && npm ci`")
            if rc.package_version and rc.required_version:
                suggestions.append(f"Resolve conflict: package yêu cầu {rc.required_version} nhưng found {rc.package_version}")
        
        elif rc.category == 'syntax_error':
            if rc.file_path and rc.line_number:
                suggestions.append(f"Kiểm tra file `{rc.file_path}` tại dòng {rc.line_number}")
                suggestions.append(f"Mở file: `code {rc.file_path}:{rc.line_number}`")
            if rc.error_message:
                suggestions.append(f"Lỗi: {rc.error_message}")
            suggestions.append("Chạy linter: `npx eslint . --fix` hoặc `pylint`")
        
        elif rc.category == 'test_failure':
            if rc.test_name:
                suggestions.append(f"Test thất bại: `{rc.test_name}`")
            if rc.file_path:
                suggestions.append(f"Chạy lại test cụ thể: `npm test -- --testPathPattern=\"{rc.file_path}\"`")
            if rc.assertion_expected and rc.assertion_actual:
                suggestions.append(f"Expected: `{rc.assertion_expected}` nhưng received: `{rc.assertion_actual}`")
            suggestions.append("Chạy tests với verbose: `npm test -- --verbose`")
        
        elif rc.category == 'timeout':
            if rc.timeout_seconds:
                new_timeout = rc.timeout_seconds * 2
                suggestions.append(f"Tăng timeout lên {new_timeout}s (hiện tại: {rc.timeout_seconds}s)")
            if rc.network_host:
                suggestions.append(f"Kiểm tra kết nối đến: `ping {rc.network_host}`")
            suggestions.append("Thêm retry logic cho network calls")
            suggestions.append("Sử dụng caching để giảm network requests")
        
        elif rc.category == 'network_error':
            if rc.network_host:
                suggestions.append(f"Kiểm tra host: `ping {rc.network_host}` hoặc `curl -I https://{rc.network_host}`")
                suggestions.append(f"Kiểm tra DNS: `nslookup {rc.network_host}`")
            suggestions.append("Thử dùng mirror/proxy khác")
            suggestions.append("Kiểm tra firewall/VPN settings")
        
        elif rc.category == 'permission_error':
            if rc.permission_path:
                suggestions.append(f"Fix permission: `chmod +x {rc.permission_path}` hoặc `sudo chown -R $USER {rc.permission_path}`")
            suggestions.append("Kiểm tra CI runner có quyền truy cập secrets")
            suggestions.append("Verify deployment keys configured correctly")
        
        elif rc.category == 'resource_error':
            if rc.memory_limit:
                new_limit = int(rc.memory_limit) * 2
                suggestions.append(f"Tăng memory limit: `export NODE_OPTIONS=\"--max-old-space-size={new_limit}\"`")
            suggestions.append("Dọn dẹp: `docker system prune -a && npm cache clean --force`")
            suggestions.append("Upgrade CI runner instance size")
        
        elif rc.category == 'environment_error':
            if rc.missing_env_var:
                suggestions.append(f"Set environment variable: `export {rc.missing_env_var}=value`")
                suggestions.append(f"Thêm `{rc.missing_env_var}` vào CI secrets")
            if rc.command_failed:
                suggestions.append(f"Install command: `npm install -g {rc.command_failed}` hoặc `brew install {rc.command_failed}`")
            suggestions.append("Kiểm tra .env file và CI environment variables")
        
        elif rc.category == 'build_error':
            if rc.exit_code:
                suggestions.append(f"Build failed với exit code: {rc.exit_code}")
            if rc.command_failed:
                suggestions.append(f"Command thất bại: `{rc.command_failed}`")
            if rc.file_path and rc.line_number:
                suggestions.append(f"Kiểm tra: `{rc.file_path}:{rc.line_number}`")
            suggestions.append("Clean build: `rm -rf dist node_modules && npm ci && npm run build`")
        
        # Fallback
        if not suggestions:
            suggestions.append("Xem chi tiết error message bên trên")
            suggestions.append("Chạy lại build với debug mode")
        
        return suggestions
    
    def _calculate_confidence(self, rc: RootCause) -> float:
        """Tính confidence dựa trên số lượng thông tin đã extract"""
        score = 0.3  # Base score
        
        if rc.package_name:
            score += 0.15
        if rc.file_path:
            score += 0.15
        if rc.line_number:
            score += 0.1
        if rc.error_message:
            score += 0.1
        if rc.suggestions:
            score += min(0.2, len(rc.suggestions) * 0.05)
        
        return min(1.0, score)


# Singleton instance
extractor = RootCauseExtractor()


def extract_root_cause(log_content: str, category: str) -> RootCause:
    """
    Hàm tiện ích để trích xuất root cause
    
    Args:
        log_content: Nội dung log
        category: Loại lỗi từ GRU model
        
    Returns:
        RootCause object
    """
    return extractor.extract(log_content, category)
