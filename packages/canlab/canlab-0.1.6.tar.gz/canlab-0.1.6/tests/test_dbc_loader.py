"""Unit tests for DBC loader functions."""
import pytest
import tempfile
import os

from dbc.dbc_loader import extract_messages
from dbc.message_data import MessageData
from exceptions.dbc_exception import DbcException


class TestExtractMessagesBasic:
    """Tests for extracting messages from basic DBC file."""

    @pytest.mark.unit
    def test_extract_messages_basic_count(self, test_data_dir):
        """Test extracting messages from a basic DBC file - message count."""
        dbc_path = os.path.join(test_data_dir, 'test_basic.dbc')
        messages = extract_messages(str(dbc_path))
        print(messages)
        
        assert len(messages) == 3

    @pytest.mark.unit
    def test_extract_messages_basic_ids(self, test_data_dir):
        """Test extracting messages from a basic DBC file - message IDs."""
        dbc_path = os.path.join(test_data_dir, 'test_basic.dbc')
        messages = extract_messages(str(dbc_path))
        
        assert messages[0].dbc_id == 2560874307
        assert messages[1].dbc_id == 2148529195
        assert messages[2].dbc_id == 695

    @pytest.mark.unit
    def test_extract_messages_basic_signal_counts(self, test_data_dir):
        """Test extracting messages from a basic DBC file - signal counts."""
        dbc_path = os.path.join(test_data_dir, 'test_basic.dbc')
        messages = extract_messages(str(dbc_path))
        
        assert len(messages[0].signals) == 3
        assert len(messages[1].signals) == 2
        assert len(messages[2].signals) == 3

    @pytest.mark.unit
    def test_extract_messages_basic_signal_names(self, test_data_dir):
        """Test extracting messages from a basic DBC file - signal names."""
        dbc_path = os.path.join(test_data_dir, 'test_basic.dbc')
        messages = extract_messages(str(dbc_path))
        
        # Message 0: EngineStatus
        assert messages[0].signals[0].name == "EngineSpeed"
        assert messages[0].signals[1].name == "EngineTemp"
        assert messages[0].signals[2].name == "ThrottlePosition"
        
        # Message 1: VehicleSpeed
        assert messages[1].signals[0].name == "Speed"
        assert messages[1].signals[1].name == "Odometer"

        # Message 2: SensorData
        assert messages[2].signals[0].name == "Temperature"
        assert messages[2].signals[1].name == "Humidity"
        assert messages[2].signals[2].name == "Pressure"

    @pytest.mark.unit
    def test_extract_messages_basic_signal_properties(self, test_data_dir):
        """Test extracting messages from a basic DBC file - signal properties."""
        dbc_path = os.path.join(test_data_dir, 'test_basic.dbc')
        messages = extract_messages(str(dbc_path))
        
        # EngineSpeed: 0|16@1+ (1,0)
        signal = messages[0].signals[0]
        assert signal.startBit == 0
        assert signal.numBits == 16
        assert signal.isLSB == True
        assert signal.isSigned == False
        assert signal.scale == 1.0
        assert signal.offset == 0.0
        
        # EngineTemp: 16|8@1+ (1,-40)
        signal = messages[0].signals[1]
        assert signal.startBit == 16
        assert signal.numBits == 8
        assert signal.isLSB == True
        assert signal.isSigned == False
        assert signal.scale == 1.0
        assert signal.offset == -40.0
        
        # Temperature (MSB): 0|16@0+ (0.1,-50)
        signal = messages[2].signals[0]
        assert signal.startBit == 0
        assert signal.numBits == 16
        assert signal.isLSB == False
        assert signal.isSigned == False
        assert signal.scale == 0.1
        assert signal.offset == -50.0


class TestExtractMessagesSigned:
    """Tests for extracting messages from signed signals DBC file."""

    @pytest.mark.unit
    def test_extract_messages_signed_count(self, test_data_dir):
        """Test extracting messages from signed DBC file - message count."""
        dbc_path = os.path.join(test_data_dir, 'test_signed.dbc')
        messages = extract_messages(str(dbc_path))
        
        assert len(messages) == 3

    @pytest.mark.unit
    def test_extract_messages_signed_ids(self, test_data_dir):
        """Test extracting messages from signed DBC file - message IDs."""
        dbc_path = os.path.join(test_data_dir, 'test_signed.dbc')
        messages = extract_messages(str(dbc_path))
        
        assert messages[0].dbc_id == 100
        assert messages[1].dbc_id == 200
        assert messages[2].dbc_id == 300

    @pytest.mark.unit
    def test_extract_messages_signed_signal_counts(self, test_data_dir):
        """Test extracting messages from signed DBC file - signal counts."""
        dbc_path = os.path.join(test_data_dir, 'test_signed.dbc')
        messages = extract_messages(str(dbc_path))
        
        assert len(messages[0].signals) == 3
        assert len(messages[1].signals) == 4
        assert len(messages[2].signals) == 3

    @pytest.mark.unit
    def test_extract_messages_signed_signal_names(self, test_data_dir):
        """Test extracting messages from signed DBC file - signal names."""
        dbc_path = os.path.join(test_data_dir, 'test_signed.dbc')
        messages = extract_messages(str(dbc_path))
        
        # Message 0: MotorControl
        assert messages[0].signals[0].name == "MotorSpeed"
        assert messages[0].signals[1].name == "MotorTorque"
        assert messages[0].signals[2].name == "MotorCurrent"
        
        # Message 1: BatteryStatus
        assert messages[1].signals[0].name == "Voltage"
        assert messages[1].signals[1].name == "Current"
        assert messages[1].signals[2].name == "Temperature"
        assert messages[1].signals[3].name == "StateOfCharge"

        # Message 2: EnvironmentalData
        assert messages[2].signals[0].name == "AmbientTemp"
        assert messages[2].signals[1].name == "Altitude"
        assert messages[2].signals[2].name == "Pressure"

    @pytest.mark.unit
    def test_extract_messages_signed_properties(self, test_data_dir):
        """Test extracting messages from signed DBC file - signed properties."""
        dbc_path = os.path.join(test_data_dir, 'test_signed.dbc')
        messages = extract_messages(str(dbc_path))
        
        # MotorSpeed: 0|16@1- (1,0) - signed LSB
        signal = messages[0].signals[0]
        assert signal.startBit == 0
        assert signal.numBits == 16
        assert signal.isLSB == True
        assert signal.isSigned == True
        assert signal.scale == 1.0
        assert signal.offset == 0.0
        
        # Voltage: 0|16@1+ (0.01,0) - unsigned LSB
        signal = messages[1].signals[0]
        assert signal.startBit == 0
        assert signal.numBits == 16
        assert signal.isLSB == True
        assert signal.isSigned == False
        assert signal.scale == 0.01
        assert signal.offset == 0.0
        
        # Current: 16|16@1- (0.1,0) - signed LSB
        signal = messages[1].signals[1]
        assert signal.startBit == 16
        assert signal.numBits == 16
        assert signal.isLSB == True
        assert signal.isSigned == True
        assert signal.scale == 0.1
        assert signal.offset == 0.0
        
        # AmbientTemp: 0|12@0- (0.1,-50) - signed MSB
        signal = messages[2].signals[0]
        assert signal.startBit == 0
        assert signal.numBits == 12
        assert signal.isLSB == False
        assert signal.isSigned == True
        assert signal.scale == 0.1
        assert signal.offset == -50.0


class TestExtractMessagesMultiplexed:
    """Tests for extracting messages from multiplexed signals DBC file."""

    @pytest.mark.unit
    def test_extract_messages_multiplexed_count(self, test_data_dir):
        """Test extracting messages from multiplexed DBC file - message count."""
        dbc_path = os.path.join(test_data_dir, 'test_multiplexed.dbc')
        messages = extract_messages(str(dbc_path))
        
        assert len(messages) == 2

    @pytest.mark.unit
    def test_extract_messages_multiplexed_ids(self, test_data_dir):
        """Test extracting messages from multiplexed DBC file - message IDs."""
        dbc_path = os.path.join(test_data_dir, 'test_multiplexed.dbc')
        messages = extract_messages(str(dbc_path))
        
        assert messages[0].dbc_id == 400
        assert messages[1].dbc_id == 500

    @pytest.mark.unit
    def test_extract_messages_multiplexed_signal_counts(self, test_data_dir):
        """Test extracting messages from multiplexed DBC file - total signal counts."""
        dbc_path = os.path.join(test_data_dir, 'test_multiplexed.dbc')
        messages = extract_messages(str(dbc_path))
        
        # MultiplexedSensors: 1 multiplexor + 6 multiplexed signals
        assert len(messages[0].signals) == 7
        # DiagnosticData: 1 multiplexor + 6 multiplexed signals
        assert len(messages[1].signals) == 7

    @pytest.mark.unit
    def test_extract_messages_multiplexed_multiplexor(self, test_data_dir):
        """Test extracting messages from multiplexed DBC file - multiplexor signals."""
        dbc_path = os.path.join(test_data_dir, 'test_multiplexed.dbc')
        messages = extract_messages(str(dbc_path))
        
        # Check multiplexor signal in first message
        assert messages[0].multiplexor_signal is not None
        assert messages[0].multiplexor_signal.name == "SensorID"
        assert messages[0].multiplexor_signal.is_multiplexor == True
        assert messages[0].multiplexor_signal.startBit == 0
        assert messages[0].multiplexor_signal.numBits == 8
        
        # Check multiplexor signal in second message
        assert messages[1].multiplexor_signal is not None
        assert messages[1].multiplexor_signal.name == "DiagID"
        assert messages[1].multiplexor_signal.is_multiplexor == True
        assert messages[1].multiplexor_signal.startBit == 0
        assert messages[1].multiplexor_signal.numBits == 4

    @pytest.mark.unit
    def test_extract_messages_multiplexed_groups(self, test_data_dir):
        """Test extracting messages from multiplexed DBC file - multiplexed groups."""
        dbc_path = os.path.join(test_data_dir, 'test_multiplexed.dbc')
        messages = extract_messages(str(dbc_path))
        
        # MultiplexedSensors should have 3 multiplexed groups (m0, m1, m2)
        msg = messages[0]
        assert 0 in msg.multiplexed_signals
        assert 1 in msg.multiplexed_signals
        assert 2 in msg.multiplexed_signals
        
        # m0 should have 2 signals
        assert len(msg.multiplexed_signals[0]) == 2
        assert msg.multiplexed_signals[0][0].name == "SensorValue1"
        assert msg.multiplexed_signals[0][1].name == "SensorStatus1"
        
        # m1 should have 2 signals
        assert len(msg.multiplexed_signals[1]) == 2
        assert msg.multiplexed_signals[1][0].name == "SensorValue2"
        assert msg.multiplexed_signals[1][1].name == "SensorStatus2"
        
        # m2 should have 2 signals
        assert len(msg.multiplexed_signals[2]) == 2
        assert msg.multiplexed_signals[2][0].name == "SensorValue3"
        assert msg.multiplexed_signals[2][1].name == "SensorStatus3"

    @pytest.mark.unit
    def test_extract_messages_multiplexed_signal_properties(self, test_data_dir):
        """Test extracting messages from multiplexed DBC file - signal properties."""
        dbc_path = os.path.join(test_data_dir, 'test_multiplexed.dbc')
        messages = extract_messages(str(dbc_path))
        
        # SensorValue1 m0: 8|16@1+ (0.1,0)
        signal = messages[0].multiplexed_signals[0][0]
        assert signal.name == "SensorValue1"
        assert signal.multiplexor_value == 0
        assert signal.startBit == 8
        assert signal.numBits == 16
        assert signal.isLSB == True
        assert signal.isSigned == False
        assert signal.scale == 0.1
        
        # SensorValue3 m2: 8|32@1+ (0.001,0)
        signal = messages[0].multiplexed_signals[2][0]
        assert signal.name == "SensorValue3"
        assert signal.multiplexor_value == 2
        assert signal.startBit == 8
        assert signal.numBits == 32
        assert signal.isLSB == True


class TestExtractMessagesMixedFormats:
    """Tests for extracting messages from mixed format DBC file."""

    @pytest.mark.unit
    def test_extract_messages_mixed_count(self, test_data_dir):
        """Test extracting messages from mixed format DBC file - message count."""
        dbc_path = os.path.join(test_data_dir, 'test_mixed_formats.dbc')
        messages = extract_messages(str(dbc_path))
        
        assert len(messages) == 3

    @pytest.mark.unit
    def test_extract_messages_mixed_ids(self, test_data_dir):
        """Test extracting messages from mixed format DBC file - message IDs."""
        dbc_path = os.path.join(test_data_dir, 'test_mixed_formats.dbc')
        messages = extract_messages(str(dbc_path))
        
        assert messages[0].dbc_id == 292
        assert messages[1].dbc_id == 2560906132
        assert messages[2].dbc_id == 2147527525

    @pytest.mark.unit
    def test_extract_messages_mixed_signal_counts(self, test_data_dir):
        """Test extracting messages from mixed format DBC file - signal counts."""
        dbc_path = os.path.join(test_data_dir, 'test_mixed_formats.dbc')
        messages = extract_messages(str(dbc_path))
        
        assert len(messages[0].signals) == 4
        assert len(messages[1].signals) == 4
        assert len(messages[2].signals) == 3

    @pytest.mark.unit
    def test_extract_messages_mixed_signal_names(self, test_data_dir):
        """Test extracting messages from mixed format DBC file - signal names."""
        dbc_path = os.path.join(test_data_dir, 'test_mixed_formats.dbc')
        messages = extract_messages(str(dbc_path))
        
        # Message 0: MixedFormatMessage
        assert messages[0].signals[0].name == "LSB_Signal1"
        assert messages[0].signals[1].name == "MSB_Signal1"
        assert messages[0].signals[2].name == "LSB_Signal2"
        assert messages[0].signals[3].name == "MSB_Signal2"
        
        # Message 1: ComplexMixedMessage
        assert messages[1].signals[0].name == "Position_LSB"
        assert messages[1].signals[1].name == "Velocity_MSB"
        assert messages[1].signals[2].name == "Acceleration_LSB"
        assert messages[1].signals[3].name == "Status_MSB"

        # Message 2: LargeSignalMessage
        assert messages[2].signals[0].name == "Counter"
        assert messages[2].signals[1].name == "DataField1"
        assert messages[2].signals[2].name == "DataField2"

    @pytest.mark.unit
    def test_extract_messages_mixed_formats(self, test_data_dir):
        """Test extracting messages from mixed format DBC file - byte order verification."""
        dbc_path = os.path.join(test_data_dir, 'test_mixed_formats.dbc')
        messages = extract_messages(str(dbc_path))
        
        # MixedFormatMessage has both LSB and MSB signals
        assert messages[0].signals[0].isLSB == True  # LSB_Signal1
        assert messages[0].signals[1].isLSB == False  # MSB_Signal1
        assert messages[0].signals[2].isLSB == True  # LSB_Signal2
        assert messages[0].signals[3].isLSB == False  # MSB_Signal2
        
        # ComplexMixedMessage has both LSB and MSB signals
        assert messages[1].signals[0].isLSB == True  # Position_LSB
        assert messages[1].signals[1].isLSB == False  # Velocity_MSB
        assert messages[1].signals[2].isLSB == True  # Acceleration_LSB
        assert messages[1].signals[3].isLSB == False  # Status_MSB

    @pytest.mark.unit
    def test_extract_messages_mixed_signal_properties(self, test_data_dir):
        """Test extracting messages from mixed format DBC file - detailed signal properties."""
        dbc_path = os.path.join(test_data_dir, 'test_mixed_formats.dbc')
        messages = extract_messages(str(dbc_path))
        
        # LSB_Signal1: 0|16@1+ (0.1,0)
        signal = messages[0].signals[0]
        assert signal.startBit == 0
        assert signal.numBits == 16
        assert signal.isLSB == True
        assert signal.isSigned == False
        assert signal.scale == 0.1
        
        # MSB_Signal1: 16|12@0+ (1,0)
        signal = messages[0].signals[1]
        assert signal.startBit == 16
        assert signal.numBits == 12
        assert signal.isLSB == False
        assert signal.isSigned == False
        assert signal.scale == 1.0
        
        # LSB_Signal2: 28|16@1- (0.01,-100)
        signal = messages[0].signals[2]
        assert signal.startBit == 28
        assert signal.numBits == 16
        assert signal.isLSB == True
        assert signal.isSigned == True
        assert signal.scale == 0.01
        assert signal.offset == -100.0
        
        # Position_LSB: 0|24@1+ (0.001,0)
        signal = messages[1].signals[0]
        assert signal.startBit == 0
        assert signal.numBits == 24
        assert signal.isLSB == True
        assert signal.isSigned == False
        assert signal.scale == 0.001


class TestExtractMessagesEdgeCases:
    """Tests for edge cases and error handling."""

    @pytest.mark.unit
    def test_extract_messages_file_not_found(self):
        """Test extract_messages with non-existent file."""
        with pytest.raises(FileNotFoundError):
            extract_messages("nonexistent.dbc")

    @pytest.mark.unit
    def test_extract_messages_empty_file(self, test_data_dir):
        """Test extract_messages with empty DBC file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.dbc', delete=False) as f:
            f.write("VERSION \"\"\n\nBS_:\n\nBU_: ECU1\n")
            temp_path = f.name

        try:
            messages = extract_messages(temp_path)
            assert len(messages) == 0
        finally:
            os.unlink(temp_path)

    @pytest.mark.unit
    def test_extract_messages_malformed_dbc(self, test_data_dir):
        """Test extract_messages with malformed DBC file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.dbc', delete=False) as f:
            f.write("BO_ invalid line\n")
            temp_path = f.name

        try:
            # Should handle malformed lines gracefully or raise appropriate exception
            with pytest.raises((ValueError, DbcException)):
                extract_messages(temp_path)
        finally:
            os.unlink(temp_path)

class TestMessageData:
    """Tests for MessageData class."""

    @pytest.mark.unit
    def test_message_data_with_dbc_id(self):
        """Test MessageData initialization with dbc_id."""
        msg = MessageData(dbc_id=100)
        assert msg.dbc_id == 100
        assert msg.bus_id is not None
        assert isinstance(msg.signals, list)
        assert len(msg.signals) == 0

    @pytest.mark.unit
    def test_message_data_with_bus_id(self):
        """Test MessageData initialization with bus_id."""
        msg = MessageData(bus_id=0x100)
        assert msg.bus_id == 0x100
        assert msg.dbc_id is not None
        assert isinstance(msg.signals, list)

    @pytest.mark.unit
    def test_message_data_no_id(self):
        """Test MessageData initialization without ID raises exception."""
        from exceptions.id_exception import IDException
        with pytest.raises(IDException):
            MessageData()

    @pytest.mark.unit
    def test_message_data_add_signals(self):
        """Test adding signals to MessageData."""
        from dbc.dbc_data import DbcData
        
        msg = MessageData(dbc_id=100)
        signal = DbcData(
            value=10.0,
            startBit=0,
            numBits=8,
            scale=1.0,
            offset=0.0,
            isSigned=False,
            name="test",
            isLSB=True
        )
        msg.signals.append(signal)
        
        assert len(msg.signals) == 1
        assert msg.signals[0].name == "test"
