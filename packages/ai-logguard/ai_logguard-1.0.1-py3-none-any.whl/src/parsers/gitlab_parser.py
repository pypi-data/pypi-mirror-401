"""
GitLab CI log parser
Parses GitLab CI job output into unified ParsedLog structure
"""
import re
from typing import Optional, Dict, List
from collections import defaultdict

from .base_parser import BaseParser
from ..models.schemas import (
    ParsedLog,
    LogEntry,
    StageInfo,
    LogLevel,
    BuildStatus,
    Platform,
)


class GitLabParser(BaseParser):
    """Parser for GitLab CI logs"""
    
    # GitLab-specific patterns
    SECTION_START = re.compile(r'section_start:\d+:(\w+)')
    SECTION_END = re.compile(r'section_end:\d+:(\w+)')
    JOB_SUCCEEDED = re.compile(r'Job succeeded', re.IGNORECASE)
    JOB_FAILED = re.compile(r'Job failed', re.IGNORECASE)
    RUNNING_WITH = re.compile(r'Running with gitlab-runner')
    GITLAB_STEP = re.compile(r'\$ (.+)')  # Commands prefixed with $
    
    def __init__(self):
        super().__init__()
        self.platform = Platform.GITLAB_CI
    
    def can_parse(self, log_content: str) -> bool:
        """Check if this is a GitLab CI log"""
        gitlab_markers = [
            'Running with gitlab-runner',
            'section_start:',
            'section_end:',
            'Fetching changes with git depth',
            'Getting source from Git repository',
            'gitlab-ci',
            'CI_JOB_ID',
            'CI_PIPELINE_ID',
        ]
        return any(marker in log_content for marker in gitlab_markers)
    
    def parse(self, log_content: str, **kwargs) -> ParsedLog:
        """
        Parse GitLab CI job log
        
        Args:
            log_content: Raw GitLab CI output
            **kwargs: job_name, pipeline_id, job_url
            
        Returns:
            ParsedLog object
        """
        lines = log_content.splitlines()
        
        # Initialize parsed log
        parsed = ParsedLog(
            platform=Platform.GITLAB_CI,
            job_name=kwargs.get('job_name'),
            build_number=kwargs.get('pipeline_id'),
            build_url=kwargs.get('job_url'),
            raw_content=log_content,
            total_lines=len(lines),
        )
        
        # Extract metadata
        parsed.status = self.extract_build_status(log_content)
        parsed.duration_seconds = self._extract_duration(log_content)
        
        # Parse stages/sections and content
        stage_data = self._parse_sections(lines)
        parsed.stages = list(stage_data['stages'].values())
        
        # Parse errors and warnings
        errors: List[LogEntry] = []
        warnings: List[LogEntry] = []
        retry_count = 0
        
        current_section: Optional[str] = None
        
        for line_num, line in enumerate(lines, start=1):
            # Track current section
            section_match = self.SECTION_START.search(line)
            if section_match:
                current_section = section_match.group(1)
            
            # Detect retries
            if self.is_retry_line(line):
                retry_count += 1
                if current_section and current_section in stage_data['stages']:
                    stage_data['stages'][current_section].retry_count += 1
            
            # Collect errors
            if self.is_error_line(line):
                error_entry = LogEntry(
                    line_number=line_num,
                    message=line.strip(),
                    raw_line=line,
                    level=LogLevel.ERROR,
                )
                errors.append(error_entry)
                
                # Mark stage as failed
                if current_section and current_section in stage_data['stages']:
                    stage_data['stages'][current_section].status = BuildStatus.FAILED
            
            # Collect warnings
            elif self.is_warning_line(line):
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
        parsed.retry_count = retry_count
        
        return parsed
    
    def extract_build_status(self, log_content: str) -> BuildStatus:
        """Extract build status from GitLab log"""
        if self.JOB_SUCCEEDED.search(log_content):
            return BuildStatus.SUCCESS
        if self.JOB_FAILED.search(log_content):
            return BuildStatus.FAILED
        
        # Check for error indicators
        if re.search(r'(ERROR|error:|fatal:)', log_content, re.IGNORECASE):
            return BuildStatus.FAILED
            
        return BuildStatus.UNKNOWN
    
    def _parse_sections(self, lines: List[str]) -> Dict:
        """Parse GitLab CI sections/stages"""
        stages: Dict[str, StageInfo] = {}
        current_section = None
        section_start_line = None
        
        for line_num, line in enumerate(lines, start=1):
            # Section start
            start_match = self.SECTION_START.search(line)
            if start_match:
                section_name = start_match.group(1)
                current_section = section_name
                section_start_line = line_num
                stages[section_name] = StageInfo(
                    name=section_name,
                    status=BuildStatus.SUCCESS,
                    start_line=line_num,
                )
            
            # Section end
            end_match = self.SECTION_END.search(line)
            if end_match:
                section_name = end_match.group(1)
                if section_name in stages:
                    stages[section_name].end_line = line_num
                current_section = None
        
        return {'stages': stages}
    
    def _extract_duration(self, log_content: str) -> Optional[int]:
        """Extract job duration"""
        # GitLab format: Job succeeded in 1m 30s
        duration_match = re.search(r'Job (?:succeeded|failed) in (\d+)m\s*(\d+)?s?', log_content)
        if duration_match:
            minutes = int(duration_match.group(1))
            seconds = int(duration_match.group(2) or 0)
            return minutes * 60 + seconds
        
        # Alternative format
        duration_match = re.search(r'Duration: (\d+):(\d+):(\d+)', log_content)
        if duration_match:
            hours = int(duration_match.group(1))
            minutes = int(duration_match.group(2))
            seconds = int(duration_match.group(3))
            return hours * 3600 + minutes * 60 + seconds
        
        return None
