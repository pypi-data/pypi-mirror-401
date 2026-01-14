"""Unit tests for encoder and decoder modules."""
import pytest

from dbc.dbc_data import DbcData
from encoder.frame_encoder import values_to_lsb, values_to_msb
from decoder.frame_decoder import lsb_to_value, msb_to_value


def hex_dump(frame: bytearray) -> str:
    """Helper function to format bytearray as hex string."""
    return ' '.join(f'{b:02X}' for b in frame)


class TestLSBEncoderDecoder:
    """Tests for LSB (Intel) encoding and decoding."""

    @pytest.mark.unit
    def test_lsb_roundtrip(self):
        """Test LSB encoding and decoding roundtrip."""
        sig = DbcData(
            value=98.6,
            startBit=0,
            numBits=16,
            scale=0.1,
            offset=0.0,
            isSigned=False,
            name="test_signal",
            isLSB=True
        )

        frame = values_to_lsb([sig])
        decoded = lsb_to_value(frame, sig)

        assert abs(decoded - sig.value) < 0.01

    @pytest.mark.unit
    def test_lsb_zero_value(self):
        """Test LSB encoding/decoding with zero value."""
        sig = DbcData(
            value=0.0,
            startBit=0,
            numBits=8,
            scale=1.0,
            offset=0.0,
            isSigned=False,
            name="zero_signal",
            isLSB=True
        )

        frame = values_to_lsb([sig])
        decoded = lsb_to_value(frame, sig)

        assert decoded == 0.0

    @pytest.mark.unit
    def test_lsb_max_value(self):
        """Test LSB encoding/decoding with maximum value."""
        sig = DbcData(
            value=6553.5,
            startBit=0,
            numBits=16,
            scale=0.1,
            offset=0.0,
            isSigned=False,
            name="max_signal",
            isLSB=True
        )

        frame = values_to_lsb([sig])
        decoded = lsb_to_value(frame, sig)

        assert abs(decoded - sig.value) < 0.1

    @pytest.mark.unit
    def test_lsb_signed_negative(self):
        """Test LSB encoding/decoding with negative signed value."""
        sig = DbcData(
            value=-100.0,
            startBit=0,
            numBits=16,
            scale=0.1,
            offset=0.0,
            isSigned=True,
            name="negative_signal",
            isLSB=True
        )

        frame = values_to_lsb([sig])
        decoded = lsb_to_value(frame, sig)

        assert abs(decoded - sig.value) < 0.1


class TestMSBEncoderDecoder:
    """Tests for MSB (Motorola) encoding and decoding."""

    @pytest.mark.unit
    def test_msb_roundtrip(self):
        """Test MSB encoding and decoding roundtrip."""
        sig = DbcData(
            value=22.0,
            startBit=11,
            numBits=12,
            scale=0.1,
            offset=-40.0,
            isSigned=False,
            name="test_signal",
            isLSB=False
        )

        frame = values_to_msb([sig])
        decoded = msb_to_value(frame, sig)

        assert abs(decoded - sig.value) < 0.01

    @pytest.mark.unit
    def test_signed_current(self):
        """Test MSB encoding/decoding with signed negative value."""
        sig = DbcData(
            value=-120.0,
            startBit=31,
            numBits=16,
            scale=0.1,
            offset=0.0,
            isSigned=True,
            name="signed_current",
            isLSB=False
        )

        frame = values_to_msb([sig])
        decoded = msb_to_value(frame, sig)

        assert abs(decoded - sig.value) < 0.01

    @pytest.mark.unit
    def test_msb_boundary_values(self):
        """Test MSB encoding/decoding with boundary values."""
        # Test minimum value
        sig_min = DbcData(
            value=-40.0,
            startBit=0,
            numBits=12,
            scale=0.1,
            offset=-40.0,
            isSigned=False,
            name="min_signal",
            isLSB=False
        )

        frame_min = values_to_msb([sig_min])
        decoded_min = msb_to_value(frame_min, sig_min)
        assert abs(decoded_min - sig_min.value) < 0.1

        # Test maximum value
        sig_max = DbcData(
            value=369.5,
            startBit=0,
            numBits=12,
            scale=0.1,
            offset=-40.0,
            isSigned=False,
            name="max_signal",
            isLSB=False
        )

        frame_max = values_to_msb([sig_max])
        decoded_max = msb_to_value(frame_max, sig_max)
        print(f"decoded max: {decoded_max}")
        assert abs(decoded_max - sig_max.value) < 0.1