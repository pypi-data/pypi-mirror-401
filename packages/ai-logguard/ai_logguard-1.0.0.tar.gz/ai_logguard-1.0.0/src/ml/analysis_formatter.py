"""
Analysis Formatter - Format kết quả phân tích thành Markdown/Rich output
Chỉ tập trung vào: Tóm tắt và Phân tích Root Cause
"""
from typing import List
from .log_analyzer import PipelineAnalysis, DetectedError, ErrorLayer


class AnalysisFormatter:
    """Format kết quả phân tích để hiển thị"""
    
    LAYER_EMOJI = {
        ErrorLayer.CI: "🏃",
        ErrorLayer.BUILD: "📦",
        ErrorLayer.CODE: "💻",
        ErrorLayer.ENV: "🔧",
        ErrorLayer.APP: "🧪",
        ErrorLayer.INFRA: "☸️",
        ErrorLayer.PLATFORM: "🏢",
        ErrorLayer.DATA: "🗄️",
        ErrorLayer.SECURITY: "🔒",
        ErrorLayer.UNKNOWN: "❓",
    }
    
    def format_markdown(self, analysis: PipelineAnalysis) -> str:
        """Format analysis result as Markdown"""
        sections = []
        
        # Header
        sections.append(self._format_header(analysis))
        
        # Summary
        sections.append(self._format_summary(analysis))
        
        # Root Causes
        sections.append(self._format_root_causes(analysis.root_causes))
        
        # Stage Details
        sections.append(self._format_stages(analysis.stages))
        
        return "\n\n".join(sections)
    
    def _format_header(self, analysis: PipelineAnalysis) -> str:
        """Format header section"""
        summary = analysis.summary
        
        status_emoji = "❌" if summary['failed_stages'] > 0 else "✅"
        
        lines = [
            f"# {status_emoji} Pipeline Analysis Report",
            "",
            f"**Status:** {summary['failed_stages']}/{summary['total_stages']} stages failed",
            f"**Root Causes:** {summary['root_cause_count']}",
            f"**Total Errors:** {summary['total_errors']}",
        ]
        
        return "\n".join(lines)
    
    def _format_summary(self, analysis: PipelineAnalysis) -> str:
        """Format summary section"""
        summary = analysis.summary
        
        lines = [
            "## 📊 Summary",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Total Stages | {summary['total_stages']} |",
            f"| Failed Stages | {summary['failed_stages']} |",
            f"| Total Errors | {summary['total_errors']} |",
            f"| Root Causes | {summary['root_cause_count']} |",
            f"| Layers Affected | {', '.join(summary.get('layers_affected', [])) if summary.get('layers_affected') else 'None'} |",
        ]
        
        if summary.get('first_failure_stage'):
            lines.append(f"| First Failure | {summary['first_failure_stage']} |")
        
        return "\n".join(lines)
    
    def _format_root_causes(self, root_causes: List[DetectedError]) -> str:
        """Format root causes section"""
        if not root_causes:
            return "## 🔍 Root Causes\n\nNo root causes identified - Pipeline appears to be successful."
        
        lines = [
            "## 🔍 Root Causes (theo thứ tự ưu tiên)",
            "",
            "> Đây là những lỗi GỐC cần xử lý.",
            "",
        ]
        
        for i, error in enumerate(root_causes, 1):
            emoji = self.LAYER_EMOJI.get(error.layer, "❓")
            
            lines.append(f"### {i}. {emoji} [{error.layer.value}] {error.stage}")
            lines.append("")
            lines.append(f"**Error Type:** `{error.error_type}`")
            lines.append("")
            lines.append(f"**Message:** {error.message}")
            lines.append("")
            
            if error.raw_lines:
                lines.append("**Log excerpt:**")
                lines.append("```")
                for line in error.raw_lines[:5]:
                    lines.append(line[:150])
                lines.append("```")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_stages(self, stages) -> str:
        """Format stages detail section"""
        lines = [
            "## 📋 Stage Details",
            "",
        ]
        
        for stage in stages:
            status_emoji = "✅" if stage.status == "SUCCESS" else "❌" if stage.status == "FAILED" else "⚠️"
            
            lines.append(f"### Stage {stage.stage_number}: {stage.stage_name} {status_emoji}")
            lines.append("")
            lines.append(f"**Status:** {stage.status}")
            
            if stage.errors:
                lines.append(f"**Errors:** {len(stage.errors)}")
                for error in stage.errors:
                    root_marker = " 🎯 ROOT CAUSE" if error.is_root_cause else ""
                    lines.append(f"- `{error.error_type}`{root_marker}")
            else:
                lines.append("**Errors:** None")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def format_compact(self, analysis: PipelineAnalysis) -> str:
        """Format compact version for quick view"""
        lines = []
        
        # Quick status
        summary = analysis.summary
        status = "FAILED" if summary['failed_stages'] > 0 else "SUCCESS"
        lines.append(f"Pipeline: {status} ({summary['root_cause_count']} root causes)")
        lines.append("")
        
        # Root causes only
        if analysis.root_causes:
            lines.append("Root Causes:")
            for i, error in enumerate(analysis.root_causes, 1):
                emoji = self.LAYER_EMOJI.get(error.layer, "")
                lines.append(f"  {i}. {emoji} [{error.layer.value}] {error.message[:80]}")
        else:
            lines.append("No errors detected - Pipeline successful")
        
        return "\n".join(lines)


# Singleton
formatter = AnalysisFormatter()


def format_analysis(analysis: PipelineAnalysis, format_type: str = "markdown") -> str:
    """
    Format analysis result
    
    Args:
        analysis: PipelineAnalysis object
        format_type: "markdown" or "compact"
        
    Returns:
        Formatted string
    """
    if format_type == "compact":
        return formatter.format_compact(analysis)
    return formatter.format_markdown(analysis)
