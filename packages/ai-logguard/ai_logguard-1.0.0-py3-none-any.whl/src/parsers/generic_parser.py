"""
Generic parser - handles any log format that doesn't match specific parsers
"""
import re
from typing import List, Optional, Dict

from .base_parser import BaseParser
from ..models.schemas import (
    ParsedLog,
    Platform,
    BuildStatus,
    LogEntry,
    LogLevel,
    StageInfo,
)


class GenericParser(BaseParser):
    """
    Generic log parser that works with any CI/CD log format.
    Uses common patterns to detect errors, warnings, and build status.
    """
    
    def __init__(self):
        # Don't call super().__init__() as we override platform as property
        pass
    
    # Common error patterns across all CI/CD platforms
    ERROR_PATTERNS = [
        # General errors
        r'\[ERROR\]',
        r'\bERROR\b[:\s]',
        r'\bError\b[:\s]',
        r'\bFAILED\b',
        r'\bFAILURE\b',
        r'\bfailed\b',
        
        # Compilation/Build errors
        r'error\s+TS\d+:',  # TypeScript
        r'error\s+CS\d+:',  # C#
        r'error:\s+',       # GCC, Clang
        r'error\[E\d+\]:',  # Rust
        r'SyntaxError:',    # Python, JS
        r'TypeError:',      # Python, JS
        r'ReferenceError:', # JS
        r'ImportError:',    # Python
        r'ModuleNotFoundError:',  # Python
        r'NameError:',      # Python
        r'IndentationError:',  # Python
        r'AttributeError:', # Python
        
        # Build tools
        r'npm ERR!',
        r'yarn error',
        r'pip.*error',
        r'gradle.*FAILED',
        r'maven.*ERROR',
        r'\[ERROR\].*BUILD FAILURE',
        r'make\[\d+\]:.*Error',
        r'error Command failed',
        
        # Test failures
        r'FAIL\s+\w+',
        r'AssertionError:',
        r'assertion failed',
        r'Expected.*but got',
        r'test.*failed',
        r'Tests:\s+\d+\s+failed',
        
        # Docker/Container errors
        r'error during connect:',
        r'Cannot connect to the Docker daemon',
        r'Error response from daemon:',
        
        # General CI/CD
        r'exit code \d+',
        r'exited with code \d+',
        r'command not found',
        r'No such file or directory',
        r'Permission denied',
        r'fatal:',
    ]
    
    # Common warning patterns
    WARNING_PATTERNS = [
        r'\[WARNING\]',
        r'\bWARNING\b[:\s]',
        r'\bWarning\b[:\s]',
        r'\bWARN\b[:\s]',
        r'\bwarn\b[:\s]',
        r'deprecated',
        r'DEPRECATION',
        r'vulnerability|vulnerabilities',
        r'npm WARN',
        r'DeprecationWarning:',
    ]
    
    # Patterns to skip (false positives)
    SKIP_PATTERNS = [
        r'>\s*git\s+.*timeout=',  # Git commands with timeout
        r'echo\s+".*[Ee]rror',    # Echo commands mentioning error
        r'\$\s*echo',             # Shell echo commands
        r'print.*[Ee]rror',       # Print statements mentioning error
        r'log.*[Ee]rror',         # Log statements mentioning error
        r'#.*[Ee]rror',           # Comments mentioning error
    ]
    
    # Patterns indicating build status
    SUCCESS_PATTERNS = [
        r'Build succeeded',
        r'BUILD SUCCESS',
        r'Build passed',
        r'All tests passed',
        r'Job succeeded',
        r'\bSUCCESS\b',
        r'Finished: SUCCESS',
        r'Process completed with exit code 0',
    ]
    
    FAILURE_PATTERNS = [
        r'Build failed',
        r'BUILD FAILED',
        r'BUILD FAILURE',
        r'Job failed',
        r'Finished: FAILURE',
        r'Process completed with exit code [1-9]',
        r'exit code [1-9]\d*',
        r'exited with \d+',
        r'ERROR: Job failed',
    ]
    
    @property
    def platform(self) -> Platform:
        return Platform.UNKNOWN
    
    def can_parse(self, log_content: str) -> bool:
        """Generic parser can always parse - it's the fallback"""
        return True
    
    def parse(self, log_content: str, **kwargs) -> ParsedLog:
        """
        Parse any log using generic patterns
        
        Args:
            log_content: Raw log content
            **kwargs: job_name, build_number, etc.
            
        Returns:
            ParsedLog object
        """
        lines = log_content.splitlines()
        
        # Initialize parsed log
        parsed = ParsedLog(
            platform=Platform.UNKNOWN,
            job_name=kwargs.get('job_name'),
            build_number=kwargs.get('build_number'),
            build_url=kwargs.get('build_url'),
            raw_content=log_content,
            total_lines=len(lines),
        )
        
        # Detect platform from content
        detected_platform = self._detect_platform_from_content(log_content)
        if detected_platform != Platform.UNKNOWN:
            parsed.platform = detected_platform
        
        # Extract build status
        parsed.status = self._extract_build_status(log_content)
        
        # Parse errors and warnings
        errors: List[LogEntry] = []
        warnings: List[LogEntry] = []
        
        for line_num, line in enumerate(lines, start=1):
            # Skip empty lines
            if not line.strip():
                continue
            
            # Skip lines that are likely false positives
            if self._should_skip(line):
                continue
            
            # Check for errors
            if self._is_error_line(line):
                errors.append(LogEntry(
                    line_number=line_num,
                    message=line.strip(),
                    raw_line=line,
                    level=LogLevel.ERROR,
                ))
            # Check for warnings
            elif self._is_warning_line(line):
                warnings.append(LogEntry(
                    line_number=line_num,
                    message=line.strip(),
                    raw_line=line,
                    level=LogLevel.WARNING,
                ))
        
        parsed.errors = errors
        parsed.warnings = warnings
        parsed.error_count = len(errors)
        parsed.warning_count = len(warnings)
        
        # If we found errors but status is unknown, set to failed
        if errors and parsed.status == BuildStatus.UNKNOWN:
            parsed.status = BuildStatus.FAILED
        
        return parsed
    
    def _detect_platform_from_content(self, log_content: str) -> Platform:
        """Try to detect platform from log content"""
        content_lower = log_content.lower()
        
        # GitLab CI markers
        if any(marker in log_content for marker in [
            'gitlab-runner', 'section_start:', 'section_end:',
            'CI_PIPELINE_ID', 'CI_JOB_ID'
        ]):
            return Platform.GITLAB_CI
        
        # Jenkins markers
        if any(marker in log_content for marker in [
            '[Pipeline]', 'Started by', 'Building in workspace',
            'Finished: SUCCESS', 'Finished: FAILURE', 'Finished: UNSTABLE'
        ]):
            return Platform.JENKINS
        
        # GitHub Actions markers
        if any(marker in log_content for marker in [
            '##[group]', '##[endgroup]', '::error::', '::warning::',
            'GITHUB_ACTIONS', 'Run actions/'
        ]):
            return Platform.GITHUB_ACTIONS
        
        return Platform.UNKNOWN
    
    def _extract_build_status(self, log_content: str) -> BuildStatus:
        """Extract build status from log content"""
        # Check for explicit failure first
        for pattern in self.FAILURE_PATTERNS:
            if re.search(pattern, log_content, re.IGNORECASE):
                return BuildStatus.FAILED
        
        # Check for success
        for pattern in self.SUCCESS_PATTERNS:
            if re.search(pattern, log_content, re.IGNORECASE):
                return BuildStatus.SUCCESS
        
        return BuildStatus.UNKNOWN
    
    def _should_skip(self, line: str) -> bool:
        """Check if line should be skipped (likely false positive)"""
        for pattern in self.SKIP_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                return True
        return False
    
    def _is_error_line(self, line: str) -> bool:
        """Check if line contains an error"""
        for pattern in self.ERROR_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                return True
        return False
    
    def _is_warning_line(self, line: str) -> bool:
        """Check if line contains a warning"""
        for pattern in self.WARNING_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                return True
        return False
