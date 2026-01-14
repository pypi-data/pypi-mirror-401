"""Contains functions for converting the data within DBCs to a usable format

The functions within this module transform the contents of a DBC file into the CANLab data format
"""
from typing import List

from .message_data import MessageData
from .dbc_data import DbcData
from exceptions.dbc_exception import DbcException

def extract_messages(src_path: str) -> List[MessageData]:
    """Extracts the messages contained in a .dbc file into a list of MessageData objects with all signals included.

    Args:
        src_path: The location of the .dbc to load.
    Returns:
        The messages with their signals contained within the DBC.
    """
    messages: List[MessageData] = []
    curr_line: str = ''
    try:
        with open(src_path, 'r') as dbc:
            current_message = None
            for line in dbc:
                curr_line = line
                # The wrapped try/except hurts code readability, but it is necessary to handle errors gracefully
                # Would like to find a better way to handle this
                try:
                    if curr_line.startswith("BA_"):
                        current_message = None
                        continue
                    if(curr_line.startswith("BO_")):
                        message = curr_line.split()
                        current_message = MessageData(dbc_id=int(message[1]))
                        messages.append(current_message)
                    elif ("SG_" in curr_line and current_message != None):
                        signal = curr_line.split()
                        block_data = signal[3]
                        transform_data = signal[4]
                        is_multiplexor = False
                        multiplexor_value = None
                        
                        if signal[2] == ('M'):
                            block_data = signal[4]
                            transform_data = signal[5]
                            is_multiplexor = True
                        elif 'm' in signal[2]:
                            mux_value_str = signal[2][1:]
                            multiplexor_value = int(mux_value_str)
                            transform_data = signal[5]
                            block_data = signal[4]

                        start_bit_str = block_data[:block_data.index('|')]
                        num_bits_str = block_data[block_data.index('|') + 1 : block_data.index('@')]
                        is_lsb = True if block_data[block_data.index('@') + 1] == '1' else False
                        is_signed = True if block_data[block_data.index('@') + 2] == '-' else False
                        scale_str = transform_data[1:transform_data.index(',')]
                        offset_str = transform_data[transform_data.index(',') + 1 : transform_data.index(')')]
                        
                        sig_data = DbcData(
                            value=0.0,
                            startBit=int(start_bit_str),
                            numBits=int(num_bits_str),
                            scale=float(scale_str),
                            offset=float(offset_str),
                            isSigned=is_signed,
                            name=signal[1],
                            isLSB=is_lsb,
                            is_multiplexor=is_multiplexor,
                            multiplexor_value=multiplexor_value
                        )
                        
                        # Add signal to appropriate location
                        if is_multiplexor:
                            current_message.multiplexor_signal = sig_data
                        elif multiplexor_value is not None:
                            if multiplexor_value not in current_message.multiplexed_signals:
                                current_message.multiplexed_signals[multiplexor_value] = []
                            current_message.multiplexed_signals[multiplexor_value].append(sig_data)
                        
                        current_message.signals.append(sig_data)
                except ValueError as e:
                    # Passing over signals that cannot properly be parsed - want to add better handling later
                    raise DbcException(f"The line {curr_line} is not valid") from e
        return messages
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file {src_path} was not found") from e
    except IndexError:
        raise DbcException("The DBC file is not valid")