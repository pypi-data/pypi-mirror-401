from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dbc.dbc_data import DbcData

def phys_to_raw(sig: "DbcData") -> int:
    raw = (sig.value - sig.offset) / sig.scale
    r = int(round(raw))

    if sig.numBits < 64:
        if sig.isSigned:
            minv = -(1 << (sig.numBits - 1))
            maxv = (1 << (sig.numBits - 1)) - 1
        else:
            minv = 0
            maxv = (1 << sig.numBits) - 1
        r = max(minv, min(maxv, r))
    return r


def gen_bus_id(dbcID: int) -> int:
    can_id = hex(dbcID)[2:]
    if can_id.startswith('9'):
        can_id = can_id.replace('9', '1', 1)
    elif can_id.startswith('8') and len(can_id) == 8:
        can_id = can_id.replace('8', '0', 1)
    elif len(can_id) == 3:
        can_id = int(can_id, 16)
        can_id >>= 5
        can_id |= 0x80000000
        can_id = hex(can_id)[2:]
    return int(can_id, 16)

def gen_dbc_id(bus_id: int | str) -> int:
    if isinstance(bus_id, int):
        bus_id = hex(bus_id)

    # Split into 2 functions calls to handle when there is a leading 0x or a leading or trailing x
    bus_id = bus_id.lstrip('0')
    bus_id = bus_id.replace('x', '')
    dbc_id = bus_id
    print(f"Stripped bus id {dbc_id}")
    if dbc_id.startswith('18') and len(bus_id) == 8:
        dbc_id = dbc_id.replace('1', '9', 1)
    elif len(bus_id) == 3:
        dbc_id = f'80000' + dbc_id
    print(f"DBC ID: {dbc_id}")    
    return int(dbc_id, 16)
