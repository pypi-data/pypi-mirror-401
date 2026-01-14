"""Export module for TraceKit protocol definitions.

This module provides functionality to export TraceKit protocol definitions
to various formats for integration with other tools and workflows.

Supported export formats:
- Wireshark Lua dissectors
- (Future) Scapy packet definitions
- (Future) Kaitai Struct definitions
- (Future) C/C++ parser code

Example:
    >>> from tracekit.export.wireshark import WiresharkDissectorGenerator
    >>> from tracekit.inference.protocol_dsl import ProtocolDefinition
    >>> protocol = ProtocolDefinition(name="myproto", description="My Protocol")
    >>> generator = WiresharkDissectorGenerator()
    >>> generator.generate(protocol, Path("myproto.lua"))
"""

# Import main exports
from . import wireshark

__all__ = [
    "wireshark",
]
