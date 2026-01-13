"""Tests for the IDU network monitor."""

import pytest
from idu import format_bytes, get_network_stats, generate_daily_data


class TestFormatBytes:
    """Tests for the format_bytes utility function."""
    
    def test_bytes(self):
        assert format_bytes(500) == "500.00 B"
    
    def test_kilobytes(self):
        assert format_bytes(1024) == "1.00 KB"
        assert format_bytes(2048) == "2.00 KB"
    
    def test_megabytes(self):
        assert format_bytes(1024 * 1024) == "1.00 MB"
        assert format_bytes(1024 * 1024 * 5) == "5.00 MB"
    
    def test_gigabytes(self):
        assert format_bytes(1024 * 1024 * 1024) == "1.00 GB"
        assert format_bytes(1024 * 1024 * 1024 * 10) == "10.00 GB"
    
    def test_terabytes(self):
        assert format_bytes(1024 * 1024 * 1024 * 1024) == "1.00 TB"


class TestGetNetworkStats:
    """Tests for the get_network_stats function."""
    
    def test_returns_dict(self):
        stats = get_network_stats()
        assert isinstance(stats, dict)
    
    def test_has_required_keys(self):
        stats = get_network_stats()
        assert "bytes_recv" in stats
        assert "bytes_sent" in stats
        assert "packets_recv" in stats
        assert "packets_sent" in stats
        assert "boot_time" in stats
    
    def test_bytes_are_positive(self):
        stats = get_network_stats()
        assert stats["bytes_recv"] >= 0
        assert stats["bytes_sent"] >= 0


class TestGenerateDailyData:
    """Tests for the generate_daily_data function."""
    
    def test_returns_list(self):
        stats = get_network_stats()
        daily_data = generate_daily_data(stats)
        assert isinstance(daily_data, list)
    
    def test_returns_60_days(self):
        stats = get_network_stats()
        daily_data = generate_daily_data(stats)
        assert len(daily_data) == 60
    
    def test_each_day_has_required_keys(self):
        stats = get_network_stats()
        daily_data = generate_daily_data(stats)
        
        required_keys = [
            "date", "date_display", "day_name",
            "received", "sent", "bytes",
            "formatted_received", "formatted_sent", "formatted"
        ]
        
        for day in daily_data:
            for key in required_keys:
                assert key in day, f"Missing key: {key}"
