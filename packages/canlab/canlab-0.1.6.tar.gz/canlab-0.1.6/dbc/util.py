"""A module containing simple DBC utility functions

This module provides high level functions for handling loading, storing, and cleaning DBCs.
"""
import sys
from pathlib import Path
from typing import Dict, List

from dbc.dbc_data import DbcData
from exceptions import DbcException, SignalFormatException
from .message_data import MessageData

def locate_message_dbc(message: MessageData, dbc_list: List[str]) -> str:
    for dbc in dbc_list:
        with open(dbc, 'r') as db:
            for line in db:
                if line.startswith("BO_"):
                    message_id = line.split()[1]
                    if message_id == message.dbc_id:
                        return dbc
    raise DbcException("The message was not found in any DBC")

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent.resolve()
    
def gen_path(path, base_dir):
    try:
        return str(Path(path).resolve().relative_to(base_dir))
    except ValueError:
        return str(Path(path).resolve())

def extract_signal_from_message(signal_name: str, message: MessageData) -> DbcData:
    """Extracts a specific instance of DbcData for a given signal.

    Args:
        signal_name: The name of the signal to extract from the DBC Message.
        message: the message containing the signal to extract.

    Returns:
        The data corresponding to the signal name within the DBC.
    """
    for signal in message.signals:
        if signal.name == signal_name:
            return signal
    raise SignalFormatException(f"The name {signal_name} does not appear in the message")