"""
Benchmark Reporters for NeuralForge.

Provides HTML and Markdown report generation
for benchmark results.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class BenchmarkMetrics:
    """Metrics for a single benchmark run."""
    name: str
    count: int = 0
    min_ms: float = 0.0
    max_ms: float = 0.0
    mean_ms: float = 0.0
    median_ms: float = 0.0
    p50_ms: float = 0.0
    p90_ms: float = 0.0
    p95_ms: float = 0.0
    p99_ms: float = 0.0
    throughput: float = 0.0
    
    @classmethod
    def from_dict(cls, name: str, data: Dict[str, Any]) -> "BenchmarkMetrics":
        return cls(
            name=name,
            count=data.get("count", 0),
            min_ms=data.get("min", data.get("min_ms", 0)),
            max_ms=data.get("max", data.get("max_ms", 0)),
            mean_ms=data.get("mean", data.get("mean_ms", 0)),
            median_ms=data.get("median", data.get("median_ms", 0)),
            p50_ms=data.get("p50", data.get("p50_ms", 0)),
            p90_ms=data.get("p90", data.get("p90_ms", 0)),
            p95_ms=data.get("p95", data.get("p95_ms", 0)),
            p99_ms=data.get("p99", data.get("p99_ms", 0)),
            throughput=data.get("throughput", 0),
        )


@dataclass
class BenchmarkReport:
    """Complete benchmark report data."""
    title: str = "NeuralForge Benchmark Report"
    version: str = "1.1.0"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    environment: Dict[str, str] = field(default_factory=dict)
    benchmarks: List[BenchmarkMetrics] = field(default_factory=list)
    comparisons: Dict[str, Dict[str, float]] = field(default_factory=dict)
    summary: Dict[str, Any] = field(default_factory=dict)


class MarkdownReporter:
    """
    Generate Markdown benchmark reports.
    
    Example:
        ```python
        reporter = MarkdownReporter()
        report = BenchmarkReport(
            benchmarks=[...],
            comparisons={...}
        )
        markdown = reporter.generate(report)
        reporter.save(report, "benchmark_report.md")
        ```
    """
    
    def generate(self, report: BenchmarkReport) -> str:
        """Generate Markdown report."""
        lines = []
        
        # Header
        lines.append(f"# {report.title}")
        lines.append("")
        lines.append(f"**Version**: {report.version}")
        lines.append(f"**Generated**: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        lines.append("")
        
        # Environment
        if report.environment:
            lines.append("## Environment")
            lines.append("")
            lines.append("| Property | Value |")
            lines.append("|----------|-------|")
            for key, value in report.environment.items():
                lines.append(f"| {key} | {value} |")
            lines.append("")
        
        # Summary
        if report.summary:
            lines.append("## Summary")
            lines.append("")
            for key, value in report.summary.items():
                lines.append(f"- **{key}**: {value}")
            lines.append("")
        
        # Benchmark Results
        lines.append("## Benchmark Results")
        lines.append("")
        
        if report.benchmarks:
            lines.append("| Benchmark | Count | Throughput | Mean | p50 | p95 | p99 |")
            lines.append("|-----------|-------|------------|------|-----|-----|-----|")
            
            for b in report.benchmarks:
                lines.append(
                    f"| {b.name} | {b.count:,} | {b.throughput:.1f} req/s | "
                    f"{b.mean_ms:.2f}ms | {b.p50_ms:.2f}ms | "
                    f"{b.p95_ms:.2f}ms | {b.p99_ms:.2f}ms |"
                )
            lines.append("")
        
        # Detailed Results
        lines.append("### Detailed Latency Distribution")
        lines.append("")
        
        for b in report.benchmarks:
            lines.append(f"#### {b.name}")
            lines.append("")
            lines.append(f"- **Requests**: {b.count:,}")
            lines.append(f"- **Throughput**: {b.throughput:.1f} req/s")
            lines.append(f"- **Latency**:")
            lines.append(f"  - Min: {b.min_ms:.2f}ms")
            lines.append(f"  - Mean: {b.mean_ms:.2f}ms")
            lines.append(f"  - Median (p50): {b.p50_ms:.2f}ms")
            lines.append(f"  - p90: {b.p90_ms:.2f}ms")
            lines.append(f"  - p95: {b.p95_ms:.2f}ms")
            lines.append(f"  - p99: {b.p99_ms:.2f}ms")
            lines.append(f"  - Max: {b.max_ms:.2f}ms")
            lines.append("")
        
        # Competitor Comparisons
        if report.comparisons:
            lines.append("## Competitor Comparison")
            lines.append("")
            
            # Get all competitors
            all_competitors = set()
            for metrics in report.comparisons.values():
                all_competitors.update(metrics.keys())
            competitors = sorted(all_competitors)
            
            # Table header
            header = "| Metric | NeuralForge |"
            separator = "|--------|-------------|"
            for c in competitors:
                header += f" {c} |"
                separator += "------|"
            lines.append(header)
            lines.append(separator)
            
            # Table rows
            for metric_name, values in report.comparisons.items():
                row = f"| {metric_name} | {values.get('neuralforge', 'N/A')} |"
                for c in competitors:
                    row += f" {values.get(c, 'N/A')} |"
                lines.append(row)
            lines.append("")
        
        # Footer
        lines.append("---")
        lines.append("")
        lines.append("*Generated by NeuralForge Benchmark Suite*")
        
        return "\n".join(lines)
    
    def save(self, report: BenchmarkReport, filepath: str):
        """Save report to file."""
        content = self.generate(report)
        Path(filepath).write_text(content, encoding='utf-8')


class HTMLReporter:
    """
    Generate HTML benchmark reports.
    
    Creates visually appealing reports with charts.
    """
    
    def __init__(self, include_charts: bool = True):
        self.include_charts = include_charts
    
    def generate(self, report: BenchmarkReport) -> str:
        """Generate HTML report."""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report.title}</title>
    <style>
        :root {{
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --bg: #0f172a;
            --bg-card: #1e293b;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            padding: 2rem;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem;
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            border-radius: 1rem;
        }}
        
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .meta {{
            color: rgba(255,255,255,0.8);
            font-size: 0.9rem;
        }}
        
        .card {{
            background: var(--bg-card);
            border-radius: 0.75rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid var(--border);
        }}
        
        .card h2 {{
            font-size: 1.25rem;
            margin-bottom: 1rem;
            color: var(--primary);
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        th, td {{
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        
        th {{
            color: var(--text-muted);
            font-weight: 500;
            font-size: 0.85rem;
            text-transform: uppercase;
        }}
        
        .metric {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: var(--primary);
            border-radius: 0.25rem;
            font-size: 0.85rem;
            font-weight: 600;
        }}
        
        .metric.success {{
            background: var(--success);
        }}
        
        .metric.warning {{
            background: var(--warning);
        }}
        
        .metric.danger {{
            background: var(--danger);
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
        }}
        
        .stat-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 0.75rem;
            padding: 1.5rem;
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
        }}
        
        .stat-label {{
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-top: 0.25rem;
        }}
        
        .bar {{
            height: 8px;
            background: var(--border);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 0.5rem;
        }}
        
        .bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--success), var(--primary));
            border-radius: 4px;
        }}
        
        footer {{
            text-align: center;
            padding: 2rem;
            color: var(--text-muted);
            font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 {report.title}</h1>
            <p class="meta">
                Version {report.version} | 
                Generated: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}
            </p>
        </header>
        
        {self._generate_summary_section(report)}
        {self._generate_benchmarks_section(report)}
        {self._generate_comparison_section(report)}
        
        <footer>
            <p>Generated by NeuralForge Benchmark Suite v{report.version}</p>
        </footer>
    </div>
</body>
</html>"""
        return html
    
    def _generate_summary_section(self, report: BenchmarkReport) -> str:
        """Generate summary cards."""
        if not report.benchmarks:
            return ""
        
        total_requests = sum(b.count for b in report.benchmarks)
        avg_throughput = sum(b.throughput for b in report.benchmarks) / len(report.benchmarks)
        avg_p99 = sum(b.p99_ms for b in report.benchmarks) / len(report.benchmarks)
        
        return f"""
        <div class="grid" style="margin-bottom: 1.5rem;">
            <div class="stat-card">
                <div class="stat-value">{total_requests:,}</div>
                <div class="stat-label">Total Requests</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{avg_throughput:.0f}</div>
                <div class="stat-label">Avg Throughput (req/s)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{avg_p99:.1f}ms</div>
                <div class="stat-label">Avg p99 Latency</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(report.benchmarks)}</div>
                <div class="stat-label">Benchmarks Run</div>
            </div>
        </div>
        """
    
    def _generate_benchmarks_section(self, report: BenchmarkReport) -> str:
        """Generate benchmarks table."""
        if not report.benchmarks:
            return ""
        
        rows = ""
        for b in report.benchmarks:
            # Color code p99
            p99_class = "success"
            if b.p99_ms > 50:
                p99_class = "warning"
            if b.p99_ms > 100:
                p99_class = "danger"
            
            rows += f"""
            <tr>
                <td>{b.name}</td>
                <td>{b.count:,}</td>
                <td><span class="metric">{b.throughput:.0f} req/s</span></td>
                <td>{b.mean_ms:.2f}ms</td>
                <td>{b.p50_ms:.2f}ms</td>
                <td>{b.p95_ms:.2f}ms</td>
                <td><span class="metric {p99_class}">{b.p99_ms:.2f}ms</span></td>
            </tr>
            """
        
        return f"""
        <div class="card">
            <h2>📊 Benchmark Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Benchmark</th>
                        <th>Requests</th>
                        <th>Throughput</th>
                        <th>Mean</th>
                        <th>p50</th>
                        <th>p95</th>
                        <th>p99</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        """
    
    def _generate_comparison_section(self, report: BenchmarkReport) -> str:
        """Generate competitor comparison."""
        if not report.comparisons:
            return ""
        
        # Get competitors
        all_competitors = set()
        for metrics in report.comparisons.values():
            all_competitors.update(metrics.keys())
        competitors = sorted([c for c in all_competitors if c != 'neuralforge'])
        
        # Build header
        header = "<th>Metric</th><th>NeuralForge</th>"
        for c in competitors:
            header += f"<th>{c}</th>"
        
        # Build rows
        rows = ""
        for metric_name, values in report.comparisons.items():
            nf_value = values.get('neuralforge', 'N/A')
            row = f"<td>{metric_name}</td><td><strong>{nf_value}</strong></td>"
            for c in competitors:
                row += f"<td>{values.get(c, 'N/A')}</td>"
            rows += f"<tr>{row}</tr>"
        
        return f"""
        <div class="card">
            <h2>⚔️ Competitor Comparison</h2>
            <table>
                <thead>
                    <tr>{header}</tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        """
    
    def save(self, report: BenchmarkReport, filepath: str):
        """Save report to file."""
        content = self.generate(report)
        Path(filepath).write_text(content, encoding='utf-8')


class JSONReporter:
    """Generate JSON benchmark reports."""
    
    def generate(self, report: BenchmarkReport) -> str:
        """Generate JSON report."""
        data = {
            "title": report.title,
            "version": report.version,
            "timestamp": report.timestamp.isoformat(),
            "environment": report.environment,
            "summary": report.summary,
            "benchmarks": [
                {
                    "name": b.name,
                    "count": b.count,
                    "throughput": b.throughput,
                    "latency": {
                        "min_ms": b.min_ms,
                        "max_ms": b.max_ms,
                        "mean_ms": b.mean_ms,
                        "median_ms": b.median_ms,
                        "p50_ms": b.p50_ms,
                        "p90_ms": b.p90_ms,
                        "p95_ms": b.p95_ms,
                        "p99_ms": b.p99_ms,
                    }
                }
                for b in report.benchmarks
            ],
            "comparisons": report.comparisons,
        }
        return json.dumps(data, indent=2)
    
    def save(self, report: BenchmarkReport, filepath: str):
        """Save report to file."""
        content = self.generate(report)
        Path(filepath).write_text(content, encoding='utf-8')


def generate_report(
    results: Dict[str, Any],
    format: str = "html",
    title: str = "NeuralForge Benchmark Report",
    version: str = "1.1.0",
    environment: Optional[Dict[str, str]] = None,
    comparisons: Optional[Dict[str, Dict[str, float]]] = None,
    output_path: Optional[str] = None
) -> str:
    """
    Convenience function to generate benchmark reports.
    
    Args:
        results: Benchmark results dictionary
        format: Output format ("html", "markdown", "json")
        title: Report title
        version: NeuralForge version
        environment: Environment info
        comparisons: Competitor comparison data
        output_path: Optional file path to save report
    
    Returns:
        Generated report content
    """
    # Build report
    report = BenchmarkReport(
        title=title,
        version=version,
        environment=environment or {},
        comparisons=comparisons or {},
    )
    
    # Convert results to metrics
    for name, data in results.items():
        if isinstance(data, dict):
            report.benchmarks.append(BenchmarkMetrics.from_dict(name, data))
    
    # Generate report
    if format == "html":
        reporter = HTMLReporter()
    elif format == "markdown":
        reporter = MarkdownReporter()
    elif format == "json":
        reporter = JSONReporter()
    else:
        raise ValueError(f"Unknown format: {format}")
    
    content = reporter.generate(report)
    
    if output_path:
        reporter.save(report, output_path)
    
    return content
