"""
IDU - Internet Data Usage Monitor

A network data usage monitor that generates beautiful HTML reports
with interactive charts showing usage statistics over the last 60 days.
"""

from .report import generate_report, get_network_stats, generate_daily_data
from .utils import format_bytes

__version__ = "0.1.0"
__author__ = "IDU Development Team"
__all__ = [
    "generate_report",
    "get_network_stats",
    "generate_daily_data",
    "format_bytes",
    "main",
]


def main():
    """CLI entry point for generating the network usage report."""
    from .report import main as report_main
    report_main()
