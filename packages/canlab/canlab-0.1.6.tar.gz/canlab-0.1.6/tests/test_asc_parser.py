"""Unit tests for ASC file parser."""
import pytest
import tempfile
import os

from log_reader.asc import parseASC, read_asc


class TestParseASCBasic:
    """Tests for parseASC function with basic ASC file."""

    @pytest.mark.unit
    def test_parse_asc_basic_structure(self, test_data_dir):
        """Test parsing a basic ASC file - structure."""
        asc_path = os.path.join(test_data_dir, 'test_basic.asc')
        target_ids = [0x98A3D743, 0xFF42B, 0x2b7]
        df = parseASC(str(asc_path), target_ids)
        
        assert df is not None
        assert len(df) > 0
        assert "message_id" in df.columns
        assert "timestamp" in df.columns
        assert "dlc" in df.columns
        assert "data_bytes" in df.columns

    @pytest.mark.unit
    def test_parse_asc_basic_filters_by_id(self, test_data_dir):
        """Test that parseASC filters messages by target IDs - basic file."""
        asc_path = os.path.join(test_data_dir, 'test_basic.asc')
        target_ids = [2560874307]
        df = parseASC(str(asc_path), target_ids)
        
        # All messages should have the target ID
        for row in df.iter_rows(named=True):
            assert row["message_id"] in target_ids

    @pytest.mark.unit
    def test_parse_asc_basic_message_count(self, test_data_dir):
        """Test parsing basic ASC file - message count."""
        asc_path = os.path.join(test_data_dir, 'test_basic.asc')
        target_ids = [2560874307, 2148529195, 695]
        df = parseASC(str(asc_path), target_ids)
        
        assert len(df) > 0


class TestParseASCSigned:
    """Tests for parseASC function with signed signals ASC file."""

    @pytest.mark.unit
    def test_parse_asc_signed_structure(self, test_data_dir):
        """Test parsing signed ASC file - structure."""
        asc_path = os.path.join(test_data_dir, 'test_signed.asc')
        target_ids = [100, 200, 300]
        df = parseASC(str(asc_path), target_ids)
        
        assert df is not None
        assert len(df) > 0
        assert "message_id" in df.columns
        assert "timestamp" in df.columns

    @pytest.mark.unit
    def test_parse_asc_signed_filters(self, test_data_dir):
        """Test that parseASC filters signed messages correctly."""
        asc_path = os.path.join(test_data_dir, 'test_signed.asc')
        target_ids = [100]
        df = parseASC(str(asc_path), target_ids)
        
        for row in df.iter_rows(named=True):
            assert row["message_id"] == 100


class TestParseASCMultiplexed:
    """Tests for parseASC function with multiplexed signals ASC file."""

    @pytest.mark.unit
    def test_parse_asc_multiplexed_structure(self, test_data_dir):
        """Test parsing multiplexed ASC file - structure."""
        asc_path = os.path.join(test_data_dir, 'test_multiplexed.asc')
        target_ids = [400, 500]
        df = parseASC(str(asc_path), target_ids)
        
        assert df is not None
        assert len(df) > 0
        assert "message_id" in df.columns

    @pytest.mark.unit
    def test_parse_asc_multiplexed_filters(self, test_data_dir):
        """Test that parseASC filters multiplexed messages correctly."""
        asc_path = os.path.join(test_data_dir, 'test_multiplexed.asc')
        target_ids = [400]
        df = parseASC(str(asc_path), target_ids)
        
        for row in df.iter_rows(named=True):
            assert row["message_id"] == 400


class TestParseASCMixedFormats:
    """Tests for parseASC function with mixed format ASC file."""

    @pytest.mark.unit
    def test_parse_asc_mixed_structure(self, test_data_dir):
        """Test parsing mixed format ASC file - structure."""
        asc_path = os.path.join(test_data_dir, 'test_mixed_formats.asc')
        target_ids = [292, 2560906132, 2147527525]
        df = parseASC(str(asc_path), target_ids)
        
        assert df is not None
        assert len(df) > 0

    @pytest.mark.unit
    def test_parse_asc_mixed_filters(self, test_data_dir):
        """Test that parseASC filters mixed format messages correctly."""
        asc_path = os.path.join(test_data_dir, 'test_mixed_formats.asc')
        target_ids = [292]
        df = parseASC(str(asc_path), target_ids)
        
        for row in df.iter_rows(named=True):
            assert row["message_id"] == 292


class TestParseASCEdgeCases:
    """Tests for edge cases and error handling."""

    @pytest.mark.unit
    def test_parse_asc_empty_file(self):
        """Test parsing an empty ASC file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.asc', delete=False) as f:
            f.write("date Mon Jan 01 00:00:00.000000 2024\n")
            f.write("base hex  timestamps absolute\n")
            temp_path = f.name

        try:
            df = parseASC(temp_path, [0x100])
            assert len(df) == 0
        finally:
            os.unlink(temp_path)

    @pytest.mark.unit
    def test_parse_asc_no_matching_ids(self, test_data_dir):
        """Test parsing ASC file with no matching message IDs."""
        asc_path = os.path.join(test_data_dir, 'test_basic.asc')
        target_ids = [0x999999]
        df = parseASC(str(asc_path), target_ids)
        
        assert len(df) == 0

    @pytest.mark.unit
    def test_parse_asc_malformed_line(self):
        """Test parsing ASC file with malformed lines."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.asc', delete=False) as f:
            f.write("date Mon Jan 01 00:00:00.000000 2024\n")
            f.write("base hex  timestamps absolute\n")
            f.write("invalid line\n")
            f.write("    0.000000 1  100        Rx   d 8 00 64 00 00 00 00 00 00\n")
            temp_path = f.name

        try:
            target_ids = [0x100]
            df = parseASC(temp_path, target_ids)
            # Should skip malformed lines and process valid ones
            assert df is not None
        finally:
            os.unlink(temp_path)


class TestReadAscBasic:
    """Tests for read_asc function with basic file."""

    @pytest.mark.unit
    def test_read_asc_basic_structure(self, test_data_dir):
        """Test reading a basic ASC file - structure."""
        asc_path = os.path.join(test_data_dir, 'test_basic.asc')
        df = read_asc(str(asc_path))
        
        assert df is not None
        assert len(df) > 0
        assert "messageID" in df.columns
        assert "timestamp" in df.columns
        assert "dlc" in df.columns
        assert "data_bytes" in df.columns

    @pytest.mark.unit
    def test_read_asc_basic_data_types(self, test_data_dir):
        """Test that read_asc returns correct data types."""
        asc_path = os.path.join(test_data_dir, 'test_basic.asc')
        df = read_asc(str(asc_path))
        
        # Check that data_bytes is a list
        for row in df.iter_rows(named=True):
            assert isinstance(row["data_bytes"], list)
            assert isinstance(row["messageID"], int)
            assert isinstance(row["timestamp"], float)
            assert isinstance(row["dlc"], int)


class TestReadAscSigned:
    """Tests for read_asc function with signed signals file."""

    @pytest.mark.unit
    def test_read_asc_signed_structure(self, test_data_dir):
        """Test reading signed ASC file - structure."""
        asc_path = os.path.join(test_data_dir, 'test_signed.asc')
        df = read_asc(str(asc_path))
        
        assert df is not None
        assert len(df) > 0


class TestReadAscMultiplexed:
    """Tests for read_asc function with multiplexed signals file."""

    @pytest.mark.unit
    def test_read_asc_multiplexed_structure(self, test_data_dir):
        """Test reading multiplexed ASC file - structure."""
        asc_path = os.path.join(test_data_dir, 'test_multiplexed.asc')
        df = read_asc(str(asc_path))
        
        assert df is not None
        assert len(df) > 0


class TestReadAscMixedFormats:
    """Tests for read_asc function with mixed format file."""

    @pytest.mark.unit
    def test_read_asc_mixed_structure(self, test_data_dir):
        """Test reading mixed format ASC file - structure."""
        asc_path = os.path.join(test_data_dir, 'test_mixed_formats.asc')
        df = read_asc(str(asc_path))
        
        assert df is not None
        assert len(df) > 0


class TestReadAscEdgeCases:
    """Tests for edge cases and error handling."""

    @pytest.mark.unit
    def test_read_asc_empty_file(self):
        """Test reading an empty ASC file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.asc', delete=False) as f:
            f.write("date Mon Jan 01 00:00:00.000000 2024\n")
            f.write("base hex  timestamps absolute\n")
            temp_path = f.name

        try:
            df = read_asc(temp_path)
            assert len(df) == 0
        finally:
            os.unlink(temp_path)

    @pytest.mark.unit
    def test_read_asc_file_not_found(self):
        """Test read_asc with non-existent file."""
        with pytest.raises(FileNotFoundError):
            read_asc("nonexistent.asc")
