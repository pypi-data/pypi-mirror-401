"""
Log Analyzer - Multi-stage CI/CD Log Analysis Engine
Phân tích log theo từng stage, xác định root cause và tạo gợi ý sửa lỗi cụ thể

Architecture:
    Log Input → Stage Parser → Error Detector → Root Cause Analyzer 
    → Layer Classifier → Fix Priority Ranker → Contextual Fix Generator
"""
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class ErrorLayer(Enum):
    """Tầng lỗi trong hệ thống"""
    CI = "CI/Runner"           # GitLab Runner, Jenkins Agent
    BUILD = "Build/Dependency" # Docker build, npm install, pip
    CODE = "Code/TypeScript"   # TypeScript, ESLint, type errors
    ENV = "Environment"        # Environment variables, config
    APP = "Application Logic"  # Code logic, exceptions
    INFRA = "Infrastructure"   # Docker, K8s, Network
    PLATFORM = "Platform"      # 1C, ERP specific
    DATA = "Database/Schema"   # DB migrations, schema
    SECURITY = "Security"      # Vulnerabilities, CVEs
    UNKNOWN = "Unknown"


@dataclass
class DetectedError:
    """Một lỗi được phát hiện trong log"""
    stage: str
    stage_number: int
    error_type: str
    message: str
    raw_lines: List[str]
    line_numbers: List[int]
    layer: ErrorLayer
    is_root_cause: bool = False
    caused_by: Optional[str] = None  # ID của error gây ra lỗi này
    
    @property
    def id(self) -> str:
        return f"{self.stage_number}_{self.error_type}"


@dataclass
class StageAnalysis:
    """Kết quả phân tích một stage"""
    stage_name: str
    stage_number: int
    status: str  # SUCCESS, FAILED, WARNING
    errors: List[DetectedError]
    warnings: List[str]
    duration: Optional[str] = None


@dataclass
class PipelineAnalysis:
    """Kết quả phân tích toàn bộ pipeline"""
    stages: List[StageAnalysis]
    root_causes: List[DetectedError]
    all_errors: List[DetectedError]
    summary: Dict[str, Any]


class LogAnalyzer:
    """
    Multi-stage CI/CD Log Analyzer
    
    Phân tích log theo kiến trúc:
    1. Stage Parser - Tách log theo stage
    2. Error Detector - Phát hiện lỗi trong mỗi stage
    3. Root Cause Analyzer - Xác định nguyên nhân gốc
    4. Layer Classifier - Xác định tầng lỗi
    5. Fix Priority Ranker - Xếp hạng thứ tự sửa
    6. Contextual Fix Generator - Tạo gợi ý cụ thể
    """
    
    def __init__(self):
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns cho phân tích log"""
        
        # Stage detection patterns
        self.stage_patterns = [
            re.compile(r'^\[\d+:\d+:\d+\]\s*STAGE\s*(\d+)[:\s]*(.+?)\s*$', re.MULTILINE | re.IGNORECASE),
            re.compile(r'^[=]{3,}\s*STAGE\s*(\d+)[:\s]*(.+?)\s*[=]{3,}$', re.MULTILINE | re.IGNORECASE),
            re.compile(r'^Stage:\s*(.+)$', re.MULTILINE | re.IGNORECASE),
            re.compile(r'^\[Stage:\s*(.+?)\]', re.MULTILINE),
        ]
        
        # Error patterns by layer
        self.error_patterns = {
            # CI/Runner layer
            ErrorLayer.CI: [
                (r'Cannot connect to the Docker daemon', 'docker_daemon_unavailable'),
                (r'gitlab-runner.*error', 'runner_error'),
                (r'jenkins.*agent.*(?:offline|unavailable)', 'agent_unavailable'),
                (r'executor.*(?:failed|error)', 'executor_error'),
            ],
            
            # Build/Dependency layer
            ErrorLayer.BUILD: [
                (r'Could not find a version that satisfies the requirement\s+(\S+)', 'pip_version_not_found'),
                (r'No matching distribution found for\s+(\S+)', 'pip_no_distribution'),
                (r'Failed building wheel for\s+(\S+)', 'pip_wheel_failed'),
                (r'npm ERR!.*ERESOLVE', 'npm_eresolve'),
                (r'npm ERR!.*Cannot find module', 'npm_module_not_found'),
                (r'Docker build failed', 'docker_build_failed'),
                (r'ERROR:.*pip install', 'pip_install_error'),
                (r'error Command failed with exit code', 'command_failed'),
            ],
            
            # Code/TypeScript layer
            ErrorLayer.CODE: [
                # TypeScript errors
                (r'error TS\d+:\s*(.+)', 'typescript_error'),
                (r"'\w+' is possibly 'null'", 'ts_null_check'),
                (r"Type '.*' is not assignable to type '.*'", 'ts_type_mismatch'),
                (r"Argument of type '.*' is not assignable to parameter", 'ts_argument_error'),
                (r'Found \d+ errors? in \d+ files?', 'typescript_errors_summary'),
                (r'tsc.*--noEmit.*failed', 'typecheck_failed'),
                # ESLint errors
                (r'\d+:\d+\s+error\s+.+', 'eslint_error'),
                (r'ESLint:\s*error', 'eslint_error'),
                # General code errors
                (r'SyntaxError:', 'syntax_error'),
                (r'ReferenceError:', 'reference_error'),
            ],
            
            # Environment layer
            ErrorLayer.ENV: [
                (r'Missing env var[:\s]+(\S+)', 'env_var_missing'),
                (r'Environment variable (\S+) is not set', 'env_var_not_set'),
                (r'\[check-env\]\s*ERROR', 'env_check_error'),
                (r'NEXTAUTH_SECRET.*missing', 'nextauth_secret_missing'),
                (r'process\.env\.(\S+).*undefined', 'env_undefined'),
                (r'Required environment variable', 'env_required'),
                (r'env check failed', 'env_check_failed'),
            ],
            
            # Application layer
            ErrorLayer.APP: [
                (r'AssertionError:\s*(.+)', 'assertion_error'),
                (r'KeyError:\s*[\'"]?(\w+)[\'"]?', 'key_error'),
                (r'TypeError:\s*(.+)', 'type_error'),
                (r'ValueError:\s*(.+)', 'value_error'),
                (r'Expected\s+(\d+)\s+but got\s+(\d+)', 'status_code_mismatch'),
                (r'FAILED\s+(\S+)::(\S+)', 'test_failed'),
            ],
            
            # Infrastructure layer
            ErrorLayer.INFRA: [
                (r'configmap\s+[\'"]?([^\s\'"]+)[\'"]?\s+not found', 'configmap_not_found'),
                (r'FailedMount.*volume\s+[\'"]?([^\s\'"]+)[\'"]?', 'volume_mount_failed'),
                (r'exceeded its progress deadline', 'deployment_timeout'),
                (r'Back-off restarting failed container', 'container_crash_loop'),
                (r'kubectl.*error', 'kubectl_error'),
                (r'ImagePullBackOff', 'image_pull_failed'),
                # Shell command not found errors
                (r'(\w+):\s*(?:command\s+)?not found', 'command_not_found'),
                (r'/bin/(?:sh|bash):\s*(?:eval:\s*)?(?:line\s+\d+:\s*)?(\w+):\s*not found', 'command_not_found'),
                (r'bash:\s*(\w+):\s*command not found', 'command_not_found'),
                (r'zsh:\s*command not found:\s*(\w+)', 'command_not_found'),
                (r'which:\s*no\s+(\w+)\s+in', 'command_not_in_path'),
                # Missing tools/binaries
                (r'(?:docker|git|npm|node|python|java|mvn|gradle|kubectl):\s*not found', 'tool_not_installed'),
                (r'unable to locate package\s+(\S+)', 'package_not_found'),
            ],
            
            # Platform (1C) layer
            ErrorLayer.PLATFORM: [
                (r'Extension.*repository mismatch', '1c_repo_mismatch'),
                (r'Repository UUID does not match', '1c_uuid_mismatch'),
                (r'Access denied for repository user\s+(\S+)', '1c_access_denied'),
                (r'Failed to unbind extension\s+(\S+)', '1c_unbind_failed'),
                (r'ConfigurationRepositoryUnbindCfg returned code\s+(\d+)', '1c_unbind_error'),
                (r'Object\s+["\']([^"\']+)["\']\s+is locked by user\s+(\S+)', '1c_object_locked'),
                (r'ConfigurationRepositoryUpdateCfg failed', '1c_update_failed'),
                (r'Update aborted due to locked metadata', '1c_update_aborted'),
            ],
            
            # Database layer
            ErrorLayer.DATA: [
                (r"Field\s+['\"]?([^\s'\"]+)['\"]?\s+type mismatch.*expected\s+(\w+).*found\s+(\w+)", 'field_type_mismatch'),
                (r'Table\s+([^\s]+)\s+has incompatible structure', 'table_incompatible'),
                (r'UpdateDBCfg failed with code\s+(\d+)', 'db_update_failed'),
                (r'migration.*(?:failed|error)', 'migration_error'),                (r'UpdateDBCfg failed', 'db_update_cfg_failed'),
                (r'Cannot add index\s+(\S+)', 'db_index_add_failed'),
                (r'Index already exists', 'db_index_exists'),
                (r'Index\s+(\S+)\s+already exists', 'db_index_duplicate'),            ],
            
            # Security layer
            ErrorLayer.SECURITY: [
                (r'(CRITICAL|HIGH)\s+(CVE-\d+-\d+)\s+(\S+)', 'cve_found'),
                (r'Vulnerabilities found above threshold', 'vuln_threshold_exceeded'),
                (r'trivy.*(?:CRITICAL|HIGH)', 'security_scan_failed'),
            ],
        }
        
        # Context extraction patterns
        self.context_patterns = {
            'docker_image': re.compile(r'(?:FROM|image[:\s]+)(\S+:\S+)', re.IGNORECASE),
            'python_version': re.compile(r'python[:\s]*(\d+\.\d+(?:\.\d+)?)', re.IGNORECASE),
            'package_version': re.compile(r'(\S+)==(\S+)'),
            'k8s_namespace': re.compile(r'-n\s+(\S+)|namespace[:\s]+(\S+)', re.IGNORECASE),
            'k8s_deployment': re.compile(r'deployment[/\s]+(\S+)', re.IGNORECASE),
            'configmap_name': re.compile(r'configmap\s+[\'"]?(\S+)[\'"]?', re.IGNORECASE),
            'git_branch': re.compile(r'CI_COMMIT_BRANCH=(\S+)'),
            'environment': re.compile(r'DEPLOY_ENV=(\S+)'),
            '1c_extension': re.compile(r'Extension\s+(\S+)'),
            '1c_infobase': re.compile(r'/S[\'"]?(\S+)[\'"]?'),
            'table_name': re.compile(r'Table\s+(\S+\.\S+)'),
            'field_name': re.compile(r"Field\s+['\"]?(\S+)['\"]?"),
        }
        
        # =============================================
        # GENERIC ERROR DETECTION PATTERNS
        # =============================================
        # Patterns để detect BẤT KỲ lỗi nào, kể cả chưa biết trước
        self.generic_error_patterns = [
            # Explicit error keywords
            re.compile(r'^.*\bERROR[:\s]+(.+)$', re.MULTILINE | re.IGNORECASE),
            re.compile(r'^.*\bFAILED[:\s]+(.+)$', re.MULTILINE | re.IGNORECASE),
            re.compile(r'^.*\bFATAL[:\s]+(.+)$', re.MULTILINE | re.IGNORECASE),
            re.compile(r'^.*\bException[:\s]+(.+)$', re.MULTILINE | re.IGNORECASE),
            re.compile(r'^.*\bTraceback\s+\(most recent call last\)', re.MULTILINE | re.IGNORECASE),
            re.compile(r'^.*\bpanic[:\s]+(.+)$', re.MULTILINE | re.IGNORECASE),
            re.compile(r'^.*\bCRITICAL[:\s]+(.+)$', re.MULTILINE | re.IGNORECASE),
            # Exit codes
            re.compile(r'(?:exit|return|error)\s*(?:code|status)[:\s]*([1-9]\d*)', re.IGNORECASE),
            re.compile(r'(?:failed|error).*(?:code|status)[:\s]*([1-9]\d*)', re.IGNORECASE),
            # Command failures
            re.compile(r'command\s+(?:failed|not found|error)', re.IGNORECASE),
            re.compile(r'(?:cannot|could not|unable to)\s+(.+)', re.IGNORECASE),
            # Process failures
            re.compile(r'process\s+(?:failed|killed|crashed|terminated)', re.IGNORECASE),
            re.compile(r'(?:timeout|timed out)\s+(?:waiting|connecting|executing)', re.IGNORECASE),
        ]
        
        # Keywords để xác định layer của unknown errors
        self.layer_keywords = {
            ErrorLayer.CI: [
                'runner', 'agent', 'executor', 'gitlab-runner', 'jenkins-agent',
                'github actions', 'workflow', 'circleci'
            ],
            ErrorLayer.BUILD: [
                'build', 'compile', 'npm', 'pip', 'yarn', 'maven', 'gradle', 'cargo',
                'package', 'dependency', 'module', 'install', 'webpack', 'vite',
                'dockerfile', 'docker build', 'requirements', 'package.json'
            ],
            ErrorLayer.CODE: [
                'typescript', 'tsc', 'eslint', 'ts18047', 'ts2322', 'ts2345',
                'type error', 'type mismatch', 'not assignable', 'possibly null',
                'syntaxerror', 'referenceerror', 'tsconfig', 'noEmit'
            ],
            ErrorLayer.ENV: [
                'env', 'environment', 'env var', 'config', 'secret',
                'nextauth', 'sentry_dsn', 'api_key', 'process.env',
                'missing variable', 'not set', 'undefined variable'
            ],
            ErrorLayer.APP: [
                'test', 'assert', 'expect', 'pytest', 'jest', 'unittest', 'spec',
                'exception', 'traceback', 'stacktrace',
                'keyerror', 'typeerror', 'valueerror', 'attributeerror', 'api', 'request'
            ],
            ErrorLayer.INFRA: [
                'kubernetes', 'k8s', 'kubectl', 'helm', 'docker', 'container', 'pod',
                'deployment', 'service', 'ingress', 'configmap', 'secret', 'volume',
                'network', 'dns', 'load balancer', 'nginx', 'aws', 'gcp', 'azure',
                'not found', 'command not found', 'not installed', 'which', '/bin/sh',
                '/bin/bash', 'bash:', 'zsh:', 'unable to locate'
            ],
            ErrorLayer.PLATFORM: [
                '1c', '1с', 'designer', 'configurator', 'infobase', 'repository',
                'extension', 'configuration', 'erp', 'accounting', 'metadata',
                'platform', 'enterprise', 'sap', 'oracle erp'
            ],
            ErrorLayer.DATA: [
                'database', 'db', 'sql', 'postgres', 'mysql', 'mongodb', 'redis',
                'migration', 'schema', 'table', 'column', 'index', 'constraint',
                'query', 'transaction', 'connection', 'pool', 'deadlock'
            ],
            ErrorLayer.SECURITY: [
                'security', 'vulnerability', 'vulnerabilities', 'cve', 'trivy', 'snyk', 'sonar',
                'permission', 'access denied', 'unauthorized', 'forbidden',
                'certificate', 'ssl', 'tls', 'auth', 'token', 'credential', 'scan'
            ],
        }
        
        # High-priority keywords that strongly indicate a layer (score = 3)
        self.high_priority_keywords = {
            ErrorLayer.SECURITY: ['vulnerability', 'vulnerabilities', 'cve', 'trivy', 'snyk', 'security scan'],
            ErrorLayer.DATA: ['database', 'migration', 'schema', 'sql', 'updatedbcfg'],
            ErrorLayer.PLATFORM: ['1c', '1cv8', 'designer', 'infobase', 'repository'],
            ErrorLayer.INFRA: ['kubernetes', 'k8s', 'kubectl', 'docker'],
            ErrorLayer.BUILD: ['pip install', 'npm install', 'build failed'],
            ErrorLayer.CODE: ['error ts', 'typescript', 'eslint', 'tsc', 'type mismatch', 'not assignable'],
            ErrorLayer.ENV: ['missing env', 'env var', 'environment variable', 'nextauth_secret', 'process.env'],
            ErrorLayer.APP: ['test failed', 'assertion', 'exception'],
            ErrorLayer.CI: ['gitlab-runner', 'jenkins-agent', 'executor'],
        }
    
    def analyze(self, log_content: str) -> PipelineAnalysis:
        """
        Phân tích toàn bộ log và trả về kết quả chi tiết
        
        Args:
            log_content: Nội dung log đầy đủ
            
        Returns:
            PipelineAnalysis với đầy đủ thông tin
        """
        # Step 1: Parse stages
        stages = self._parse_stages(log_content)
        
        # Step 2: Detect errors in each stage
        all_errors = []
        for stage in stages:
            errors = self._detect_errors(stage, log_content)
            stage.errors = errors
            all_errors.extend(errors)
            
            # Determine stage status
            if errors:
                stage.status = "FAILED"
            else:
                stage.status = "SUCCESS"
        
        # Step 3: Identify root causes (causal analysis)
        root_causes = self._identify_root_causes(all_errors, stages)
        
        # Step 4: Generate summary
        summary = self._generate_summary(stages, root_causes)
        
        return PipelineAnalysis(
            stages=stages,
            root_causes=root_causes,
            all_errors=all_errors,
            summary=summary
        )
    
    def _parse_stages(self, log_content: str) -> List[StageAnalysis]:
        """Tách log thành các stage"""
        stages = []
        
        # Find all stage markers
        stage_matches = []
        for pattern in self.stage_patterns:
            for match in pattern.finditer(log_content):
                if len(match.groups()) >= 2:
                    stage_num = int(match.group(1)) if match.group(1).isdigit() else len(stage_matches) + 1
                    stage_name = match.group(2).strip()
                else:
                    stage_num = len(stage_matches) + 1
                    stage_name = match.group(1).strip()
                
                stage_matches.append({
                    'number': stage_num,
                    'name': stage_name,
                    'start': match.start(),
                    'end': match.end()
                })
        
        # Sort by position
        stage_matches.sort(key=lambda x: x['start'])
        
        # Create StageAnalysis for each stage
        for i, stage_match in enumerate(stage_matches):
            # Get content until next stage or end
            start = stage_match['end']
            end = stage_matches[i + 1]['start'] if i + 1 < len(stage_matches) else len(log_content)
            
            stages.append(StageAnalysis(
                stage_name=stage_match['name'],
                stage_number=stage_match['number'],
                status="UNKNOWN",
                errors=[],
                warnings=[]
            ))
        
        # If no stages found, treat entire log as single stage
        if not stages:
            stages.append(StageAnalysis(
                stage_name="Main",
                stage_number=1,
                status="UNKNOWN",
                errors=[],
                warnings=[]
            ))
        
        return stages
    
    def _detect_errors(self, stage: StageAnalysis, log_content: str) -> List[DetectedError]:
        """
        Phát hiện lỗi trong một stage
        
        Sử dụng 2 phương pháp:
        1. Known Patterns - Match với patterns đã định nghĩa → gợi ý cụ thể
        2. Generic Detection - Detect lỗi chưa biết → gợi ý thông minh dựa trên context
        """
        errors = []
        lines = log_content.split('\n')
        
        # Get stage content
        stage_content = self._get_stage_content(stage, log_content)
        
        # Track detected error messages to avoid duplicates
        detected_messages = set()
        
        # =============================================
        # PHASE 1: KNOWN PATTERN MATCHING
        # =============================================
        for layer, patterns in self.error_patterns.items():
            for pattern_str, error_type in patterns:
                pattern = re.compile(pattern_str, re.IGNORECASE | re.MULTILINE)
                
                for match in pattern.finditer(stage_content):
                    # Find line numbers
                    line_start = stage_content[:match.start()].count('\n')
                    matched_lines = match.group(0).split('\n')
                    
                    # Get surrounding context (3 lines before and after)
                    context_start = max(0, line_start - 3)
                    context_end = min(len(lines), line_start + len(matched_lines) + 3)
                    raw_lines = lines[context_start:context_end] if context_start < len(lines) else [match.group(0)]
                    
                    # Extract specific info from match
                    message = self._build_error_message(error_type, match)
                    
                    # Track this message
                    msg_key = f"{error_type}:{message[:50]}"
                    if msg_key in detected_messages:
                        continue
                    detected_messages.add(msg_key)
                    
                    error = DetectedError(
                        stage=stage.stage_name,
                        stage_number=stage.stage_number,
                        error_type=error_type,
                        message=message,
                        raw_lines=raw_lines,
                        line_numbers=list(range(context_start, context_end)),
                        layer=layer
                    )
                    
                    # Avoid duplicates
                    if not any(e.error_type == error.error_type and e.stage == error.stage for e in errors):
                        errors.append(error)
        
        # =============================================
        # PHASE 2: GENERIC ERROR DETECTION
        # Detect lỗi chưa biết dựa trên keywords chung
        # =============================================
        for pattern in self.generic_error_patterns:
            for match in pattern.finditer(stage_content):
                error_line = match.group(0).strip()
                error_detail = match.group(1) if match.lastindex and match.lastindex >= 1 else error_line
                
                # Skip if already detected by known patterns
                skip = False
                for known_error in errors:
                    if any(line in error_line for line in known_error.raw_lines):
                        skip = True
                        break
                if skip:
                    continue
                
                # Skip common false positives
                false_positive_keywords = [
                    'no error', 'error: 0', 'error count: 0', 'errors: 0',
                    'successfully', 'passed', 'success', 'completed',
                    'info:', 'debug:', 'warn:', 'notice:',
                    'no critical', 'no high', 'threshold not exceeded',
                    'scan passed', 'test passed', 'check passed',
                    'vulnerability detected',  # This is informational, not error
                    'medium vulnerability',    # Informational
                ]
                if any(fp in error_line.lower() for fp in false_positive_keywords):
                    continue
                
                # Also check if the whole stage passed (from stage content)
                if 'passed' in stage_content.lower() and 'failed' not in stage_content.lower():
                    # Stage passed, skip this generic error
                    continue
                
                # Track to avoid duplicates
                msg_key = f"generic:{error_line[:80]}"
                if msg_key in detected_messages:
                    continue
                detected_messages.add(msg_key)
                
                # Detect layer based on keywords in error and surrounding context
                line_start = stage_content[:match.start()].count('\n')
                context_start = max(0, line_start - 5)
                context_end = min(len(lines), line_start + 5)
                context_text = '\n'.join(lines[context_start:context_end]).lower()
                
                detected_layer = self._detect_layer_from_context(error_line + ' ' + context_text)
                
                # Build generic error message
                generic_message = self._build_generic_message(error_detail, context_text)
                
                error = DetectedError(
                    stage=stage.stage_name,
                    stage_number=stage.stage_number,
                    error_type='generic_error',
                    message=generic_message,
                    raw_lines=[error_line] + lines[context_start:context_end],
                    line_numbers=list(range(context_start, context_end)),
                    layer=detected_layer
                )
                
                errors.append(error)
        
        return errors
    
    def _detect_layer_from_context(self, text: str) -> ErrorLayer:
        """
        Xác định error layer dựa trên keywords trong context
        
        Sử dụng 2-tier scoring:
        1. High-priority keywords (score = 3) - Xác định chắc chắn layer
        2. Normal keywords (score = 1) - Gợi ý layer
        """
        text_lower = text.lower()
        
        layer_scores = {layer: 0 for layer in ErrorLayer}
        
        # First pass: High-priority keywords (score = 3)
        for layer, keywords in self.high_priority_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    layer_scores[layer] += 3
        
        # Second pass: Normal keywords (score = 1)
        for layer, keywords in self.layer_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    layer_scores[layer] += 1
        
        # Return layer with highest score, default to UNKNOWN
        max_score = max(layer_scores.values())
        if max_score > 0:
            for layer, score in layer_scores.items():
                if score == max_score:
                    return layer
        
        return ErrorLayer.UNKNOWN
    
    def _build_generic_message(self, error_detail: str, context: str) -> str:
        """Xây dựng message cho generic error"""
        # Clean up error detail
        message = error_detail.strip()
        if len(message) > 200:
            message = message[:200] + "..."
        return message
    
    def _get_stage_content(self, stage: StageAnalysis, log_content: str) -> str:
        """
        Lấy nội dung của một stage từ log
        
        Sử dụng nhiều patterns để tìm đúng stage content:
        1. [HH:MM:SS] STAGE N: NAME format
        2. === STAGE N: NAME === format
        3. Fallback to full log if no stage markers found
        """
        lines = log_content.split('\n')
        
        # Pattern 1: [00:00:01] STAGE N: NAME format
        stage_start_patterns = [
            rf'\[\d+:\d+:\d+\]\s*STAGE\s*{stage.stage_number}[:\s]*',  # [00:00:01] STAGE 1: 
            rf'^[=]{{3,}}\s*STAGE\s*{stage.stage_number}[:\s]*',      # === STAGE 1: ===
            rf'^\[Stage:\s*{re.escape(stage.stage_name)}\]',          # [Stage: NAME]
        ]
        
        # Find start of this stage
        stage_start = -1
        for i, line in enumerate(lines):
            for pattern in stage_start_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    stage_start = i
                    break
            if stage_start >= 0:
                break
        
        if stage_start < 0:
            # No stage marker found - if this is the only stage ("Main"), use full log
            if stage.stage_name == "Main" and stage.stage_number == 1:
                return log_content
            return ""
        
        # Find end of this stage (start of next stage or end of log)
        stage_end = len(lines)
        next_stage_patterns = [
            rf'\[\d+:\d+:\d+\]\s*STAGE\s*{stage.stage_number + 1}[:\s]*',
            rf'^[=]{{3,}}\s*STAGE\s*{stage.stage_number + 1}[:\s]*',
            r'\[\d+:\d+:\d+\]\s*STAGE\s*\d+[:\s]*',  # Any next stage
            r'^[=]{3,}\s*STAGE\s*\d+[:\s]*',         # Any next stage
            r'^[=]{10,}\s*$',                         # Separator line
            r'^PIPELINE\s+SUMMARY',                   # Summary section
        ]
        
        for i in range(stage_start + 1, len(lines)):
            for pattern in next_stage_patterns:
                if re.search(pattern, lines[i], re.IGNORECASE):
                    # Check if this is actually the next stage (not current)
                    next_stage_match = re.search(r'STAGE\s*(\d+)', lines[i], re.IGNORECASE)
                    if next_stage_match:
                        next_num = int(next_stage_match.group(1))
                        if next_num > stage.stage_number:
                            stage_end = i
                            break
                    else:
                        stage_end = i
                        break
            if stage_end < len(lines) and stage_end > stage_start:
                break
        
        return '\n'.join(lines[stage_start:stage_end])
    
    def _build_error_message(self, error_type: str, match: re.Match) -> str:
        """Xây dựng error message từ match groups"""
        groups = match.groups()
        
        messages = {
            'pip_version_not_found': f"Package `{groups[0] if groups else 'unknown'}` version không tồn tại",
            'pip_no_distribution': f"Không tìm thấy distribution cho `{groups[0] if groups else 'unknown'}`",
            'pip_wheel_failed': f"Failed to build wheel cho `{groups[0] if groups else 'unknown'}`",
            'docker_daemon_unavailable': "Docker daemon không thể kết nối",
            'configmap_not_found': f"ConfigMap `{groups[0] if groups else 'unknown'}` không tồn tại",
            'volume_mount_failed': f"Mount volume `{groups[0] if groups else 'unknown'}` thất bại",
            'deployment_timeout': "Deployment vượt quá thời gian chờ",
            'test_failed': f"Test `{groups[1] if len(groups) > 1 else 'unknown'}` trong `{groups[0] if groups else 'unknown'}` thất bại",
            'assertion_error': f"Assertion failed: {groups[0] if groups else 'unknown'}",
            'key_error': f"Missing key: `{groups[0] if groups else 'unknown'}`",
            'status_code_mismatch': f"Expected status {groups[0] if groups else '?'} but got {groups[1] if len(groups) > 1 else '?'}",
            'cve_found': f"{groups[0] if groups else 'CRITICAL'} {groups[1] if len(groups) > 1 else 'CVE'} trong {groups[2] if len(groups) > 2 else 'package'}",
            '1c_repo_mismatch': "Extension repository không khớp với bound repository",
            '1c_uuid_mismatch': "Repository UUID không khớp",
            '1c_access_denied': f"Truy cập bị từ chối cho user `{groups[0] if groups else 'unknown'}`",
            '1c_object_locked': f"Object `{groups[0] if groups else 'unknown'}` đang bị lock bởi user `{groups[1] if len(groups) > 1 else 'unknown'}`",
            '1c_update_failed': "ConfigurationRepositoryUpdateCfg thất bại",
            '1c_update_aborted': "Update bị hủy do metadata object bị lock",
            'field_type_mismatch': f"Field `{groups[0] if groups else '?'}`: expected {groups[1] if len(groups) > 1 else '?'}, found {groups[2] if len(groups) > 2 else '?'}",
            'table_incompatible': f"Table `{groups[0] if groups else 'unknown'}` có cấu trúc không tương thích",
            'db_update_cfg_failed': "UpdateDBCfg thất bại",
            'db_index_exists': "Index đã tồn tại trong database",
            'db_index_duplicate': f"Index `{groups[0] if groups else 'unknown'}` đã tồn tại",
            'db_index_add_failed': f"Không thể thêm index `{groups[0] if groups else 'unknown'}`",
        }
        
        return messages.get(error_type, match.group(0)[:200])
    
    def _identify_root_causes(self, all_errors: List[DetectedError], stages: List[StageAnalysis]) -> List[DetectedError]:
        """
        Xác định root causes từ tất cả errors
        
        Quy tắc:
        1. Lỗi ở stage sớm hơn có thể gây ra lỗi ở stage sau
        2. Lỗi CI/Build thường là root cause của lỗi Deploy/Test
        3. Lỗi Infra có thể cascade sang nhiều stage
        4. Trong cùng một stage, chỉ lấy error đầu tiên của mỗi layer làm root cause
        5. Lỗi liên quan được group lại, chỉ giữ error gốc
        6. Loại bỏ các lỗi hậu quả (exit code, job failed, etc.)
        """
        if not all_errors:
            return []
        
        # =============================================
        # STEP 0: Filter out consequence errors (not root causes)
        # =============================================
        consequence_patterns = [
            'exit code',
            'exit_code',
            'job failed',
            'job_failed',
            'command failed with exit',
            'cleaning up',
            'uploading artifacts',
            'no files to upload',
        ]
        
        # Error types that are consequences, not root causes
        consequence_error_types = [
            'command_failed',  # "error Command failed with exit code 2" is a consequence
        ]
        
        def is_consequence_error(error: DetectedError) -> bool:
            """Check if this error is a consequence, not a root cause"""
            msg_lower = error.message.lower()
            
            # Check message patterns
            for pattern in consequence_patterns:
                if pattern in msg_lower:
                    return True
            
            # Check error type
            if error.error_type in consequence_error_types:
                return True
            
            # "generic_error" with exit code message or just exit code number
            if error.error_type == 'generic_error':
                if 'exit code' in msg_lower or 'job failed' in msg_lower:
                    return True
                # If message is just a number (exit code), it's a consequence
                if error.message.strip().isdigit():
                    return True
            
            return False
        
        # Filter out consequence errors
        filtered_errors = [e for e in all_errors if not is_consequence_error(e)]
        
        # =============================================
        # STEP 1: Deduplicate similar errors
        # =============================================
        # TypeScript errors: typescript_error, ts_type_mismatch, ts_null_check, ts_argument_error
        # are often the same underlying issue
        typescript_error_types = [
            'typescript_error', 
            'ts_type_mismatch', 
            'ts_null_check', 
            'ts_argument_error',
            'typescript_errors_summary',
        ]
        
        def get_error_signature(error: DetectedError) -> str:
            """Get unique signature for deduplication"""
            # For TypeScript errors, use the core message
            if error.error_type in typescript_error_types:
                # Extract TS error code if present (e.g., TS2322, TS18047)
                import re
                ts_code_match = re.search(r'TS\d+', error.message)
                if ts_code_match:
                    return f"ts_{ts_code_match.group()}"
                # Fallback to normalized message
                return f"ts_{error.message[:50].lower()}"
            
            return f"{error.error_type}_{error.message[:30].lower()}"
        
        # Deduplicate
        seen_signatures = set()
        deduplicated_errors = []
        
        for error in filtered_errors:
            sig = get_error_signature(error)
            if sig not in seen_signatures:
                seen_signatures.add(sig)
                deduplicated_errors.append(error)
        
        if not deduplicated_errors:
            return []
        
        root_causes = []
        
        # Sort errors by stage number, then by layer
        sorted_errors = sorted(deduplicated_errors, key=lambda e: (e.stage_number, e.layer.value))
        
        # Causal relationships - lỗi này có thể gây ra lỗi kia
        causal_map = {
            # Error type -> có thể gây ra những error types nào
            'docker_daemon_unavailable': ['docker_build_failed', 'deployment_timeout', 'test_failed'],
            'docker_build_failed': ['deployment_timeout', 'container_crash_loop', 'test_failed'],
            'pip_version_not_found': ['docker_build_failed', 'pip_no_distribution', 'pip_wheel_failed'],
            'pip_no_distribution': ['docker_build_failed', 'pip_wheel_failed'],
            'pip_wheel_failed': ['docker_build_failed'],
            'npm_eresolve': ['docker_build_failed', 'test_failed'],
            'configmap_not_found': ['volume_mount_failed', 'container_crash_loop', 'deployment_timeout'],
            'volume_mount_failed': ['container_crash_loop', 'deployment_timeout'],
            '1c_repo_mismatch': ['1c_unbind_failed', '1c_access_denied', '1c_uuid_mismatch', '1c_unbind_error'],
            '1c_uuid_mismatch': ['1c_unbind_failed', '1c_access_denied'],
            '1c_object_locked': ['1c_update_failed', '1c_update_aborted'],  # Object lock gây ra update fail
            '1c_update_failed': ['1c_update_aborted'],
            'field_type_mismatch': ['table_incompatible', 'db_update_failed', 'db_update_cfg_failed'],
            'table_incompatible': ['db_update_failed', 'db_update_cfg_failed'],
            'db_index_exists': ['db_index_add_failed', 'db_update_cfg_failed'],  # Index exists gây ra add fail
            'db_index_duplicate': ['db_index_add_failed', 'db_update_cfg_failed'],
            'cve_found': ['vuln_threshold_exceeded'],
            'assertion_error': ['test_failed'],
            'key_error': ['test_failed', 'status_code_mismatch'],
        }
        
        # Related errors - những error này thực chất là cùng một vấn đề
        related_groups = [
            ['pip_version_not_found', 'pip_no_distribution', 'pip_wheel_failed'],  # Tất cả là dependency issue
            ['typescript_error', 'ts_type_mismatch', 'ts_null_check', 'ts_argument_error', 'typescript_errors_summary'],  # TypeScript errors
            ['env_var_missing', 'env_check_error', 'env_required', 'env_check_failed'],  # Environment errors
            ['1c_repo_mismatch', '1c_uuid_mismatch', '1c_unbind_failed', '1c_unbind_error'],  # Tất cả là 1C repo issue
            ['1c_object_locked', '1c_update_failed', '1c_update_aborted'],  # Tất cả là 1C lock issue
            ['field_type_mismatch', 'table_incompatible', 'db_update_failed', 'db_update_cfg_failed'],  # Tất cả là schema issue
            ['db_index_exists', 'db_index_duplicate', 'db_index_add_failed'],  # Tất cả là index issue
            ['cve_found', 'vuln_threshold_exceeded'],  # Tất cả là security issue
            ['assertion_error', 'status_code_mismatch'],  # Tất cả là test assertion
            ['configmap_not_found', 'volume_mount_failed'],  # K8s config issue
            ['command_not_found', 'command_not_in_path', 'tool_not_installed', 'package_not_found'],  # Missing command/tool
        ]
        
        # Find primary error in each related group
        def get_primary_error_type(error_type: str) -> str:
            for group in related_groups:
                if error_type in group:
                    return group[0]  # First in group is primary
            return error_type
        
        # Track which primary errors we've already added as root cause
        seen_primary_types = {}  # stage_number -> set of primary error types
        
        # Mark root causes
        for i, error in enumerate(sorted_errors):
            is_root = True
            
            # Get primary type for this error
            primary_type = get_primary_error_type(error.error_type)
            
            # Check if we already have this primary type in this stage
            stage_key = error.stage_number
            if stage_key not in seen_primary_types:
                seen_primary_types[stage_key] = set()
            
            if primary_type in seen_primary_types[stage_key]:
                # Already have root cause for this issue, mark as caused
                error.is_root_cause = False
                error.caused_by = f"{stage_key}_{primary_type}"
                continue
            
            # Check if this error is caused by an earlier error
            for prev_error in sorted_errors[:i]:
                # Must be in earlier stage
                if prev_error.stage_number >= error.stage_number:
                    continue
                
                if not prev_error.is_root_cause:
                    continue
                
                caused_types = causal_map.get(prev_error.error_type, [])
                if error.error_type in caused_types or primary_type in caused_types:
                    is_root = False
                    error.caused_by = prev_error.id
                    error.is_root_cause = False
                    break
            
            # Check if caused by same-stage earlier error in causal chain
            if is_root:
                for prev_error in sorted_errors[:i]:
                    if prev_error.stage_number != error.stage_number:
                        continue
                    
                    caused_types = causal_map.get(prev_error.error_type, [])
                    if error.error_type in caused_types:
                        is_root = False
                        error.caused_by = prev_error.id
                        error.is_root_cause = False
                        break
            
            if is_root:
                error.is_root_cause = True
                root_causes.append(error)
                seen_primary_types[stage_key].add(primary_type)
        
        return root_causes
    
    def _generate_summary(self, stages: List[StageAnalysis], root_causes: List[DetectedError]) -> Dict[str, Any]:
        """Tạo summary của toàn bộ analysis"""
        
        failed_stages = [s for s in stages if s.status == "FAILED"]
        
        layers_affected = list(set(e.layer for e in root_causes))
        
        return {
            'total_stages': len(stages),
            'failed_stages': len(failed_stages),
            'failed_stage_names': [s.stage_name for s in failed_stages],
            'total_errors': sum(len(s.errors) for s in stages),
            'root_cause_count': len(root_causes),
            'layers_affected': [l.value for l in layers_affected],
            'first_failure_stage': failed_stages[0].stage_name if failed_stages else None,
        }


# Singleton instance
analyzer = LogAnalyzer()


def analyze_pipeline_log(log_content: str) -> PipelineAnalysis:
    """
    Phân tích CI/CD pipeline log
    
    Args:
        log_content: Nội dung log đầy đủ
        
    Returns:
        PipelineAnalysis với stages, errors và root causes
    """
    return analyzer.analyze(log_content)
