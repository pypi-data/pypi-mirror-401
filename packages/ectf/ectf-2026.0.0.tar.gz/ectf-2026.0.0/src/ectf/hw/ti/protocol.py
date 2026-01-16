"""Interface to the MITRE bootloader of the TI MSPM0L2228

Author: Ben Janis
Date: 2025

This source file is part of an example system for MITRE's 2025 Embedded System CTF
(eCTF). This code is being provided only for educational purposes for the 2025 MITRE
eCTF competition, and may not meet MITRE standards for quality. Use this code at your
own risk!

Copyright: Copyright (c) 2025 The MITRE Corporation
"""

import struct
import zlib
from enum import IntEnum
from typing import ClassVar, Self

import serial
from attrs import field, frozen

from ectf.console import debug, error, trace, warning
from ectf.hw.bootloader import BootloaderError

CRC_SIZE = 4
NAME_SIZE = 8


def crc32(data: bytes) -> int:
    """Calculate a CRC-32/JAMCRC"""
    return 0xFFFFFFFF - zlib.crc32(data)


class Cmd(IntEnum):
    """Core command types"""

    UNDEFINED = -1
    CONNECTION = ord("C")
    IDENTITY = ord("I")
    ERASE = ord("E")
    UPDATE = ord("U")
    PROGRAM = ord("P")
    VERIFY = ord("V")
    DIGEST = ord("D")
    START = ord("S")


class CommandError(BootloaderError):
    """An error occurring during the command"""


class NoACKError(BootloaderError):
    """No ACK was received"""


class NACKError(CommandError):
    """Bootloader sent a negative ACK"""


class MessageError(CommandError):
    """Bootloader sent a negative Message response"""


class Ack(IntEnum):
    """ACK types"""

    ACK = 0
    ERR_HEADER_INCORRECT = 0x51
    ERR_CHECKSUM_INCORRECT = 0x52
    ERR_PACKET_SIZE_ZERO = 0x53
    ERR_PACKET_SIZE_TOO_BIG = 0x54
    ERR_UNKNOWN_ERROR = 0x55


class Message(IntEnum):
    """Message responses"""

    SUCCESS = 0
    UNKNOWN_COMMAND = 0x04
    INVALID_MEM_RANGE = 0x05
    INVALID_COMMAND = 0x06
    INVALID_ADDRESS = 0x0A
    COMMAND_REJECTED = 0xF0
    PROGRAM_FAILED = 0xF1
    ERASE_FAILED = 0xF2
    VERIFY_FAILED = 0xF3


class Resp(IntEnum):
    """Core response types"""

    MESSAGE = ord("M")
    IDENTITY = ord("I")
    DIGEST = ord("D")
    DETAILED_ERROR = ord("E")


@frozen
class CoreResponse:
    """Defines the core responses from the bootloader"""

    HDR: ClassVar[int] = 0x08

    @classmethod
    def unpack(cls, data: bytes) -> Self:
        """Unpack a generic response"""
        if data:
            warning(f"Unused data {data!r}")
        return cls()

    @classmethod
    def deserialize(cls, ser: serial.Serial) -> Self:
        """Deserialize a response"""
        raw = ser.read(3)
        trace(f"Received raw header {raw}")
        hdr, length = struct.unpack("<BH", raw)
        if hdr != cls.HDR:
            msg = f"Received bad header {hdr!r}"
            raise CommandError(msg)
        if length == 0:
            msg = "Received bad zero-length response"
            raise CommandError(msg)

        body = ser.read(length)
        trace(f"Received raw {len(body)}B body {body}")
        if len(body) != length:
            msg = f"Didn't receive full body {body} (expected {length}B)"
            raise CommandError(msg)

        raw_crc = ser.read(CRC_SIZE)
        trace(f"Received raw CRC {raw_crc}")
        if len(raw_crc) != CRC_SIZE:
            msg = f"Didn't receive full CRC {raw_crc} (expected {length}B"
            raise CommandError(msg)
        (sent_crc,) = struct.unpack("<I", raw_crc)

        calc_crc = crc32(body)
        if sent_crc != calc_crc:
            msg = f"CRC mismatch {sent_crc:8x} != {calc_crc:8x}"
            raise CommandError(msg)

        return unpack_response(Resp(body[0]), body[1:])


@frozen
class MessageResponse(CoreResponse):
    """MESSAGE response"""

    message: Message

    @classmethod
    def unpack(cls, data: bytes) -> Self:
        """Unpack the IDENTITY response data"""
        if len(data) != 1:
            msg = f"Bad MESSAGE data length {data}"
            raise CommandError(msg)

        return cls(Message(data[0]))


@frozen
class IdentityResponse(CoreResponse):
    """Response for the IDENTITY command"""

    year: int
    major_version: int
    minor_version: int
    secure: int
    buf_size: int
    app_start: int
    sector_size: int
    app_clear: int
    app_ready: int
    installed: bytes | None

    @classmethod
    def unpack(cls, data: bytes) -> Self:
        """Unpack the IDENTITY response data"""
        try:
            unpacked = struct.unpack("<BBBBIIIHH", data[:-NAME_SIZE])
        except struct.error as e:
            debug(e)
            msg = f"Could not unpack {len(data)}B identity response {data}"
            raise CommandError(msg) from e

        installed = data[-NAME_SIZE:]
        if installed == b"\xff" * NAME_SIZE:
            installed = None
        return cls(*unpacked, installed)


@frozen
class DigestResponse(CoreResponse):
    """Response for the DIGEST command"""

    digest: bytes

    @classmethod
    def unpack(cls, data: bytes) -> Self:
        """Unpack the DIGEST response data"""
        return cls(data)


def unpack_response(resp: Resp, data: bytes) -> CoreResponse:
    """Unpack the correct type of response"""
    match resp:
        case Resp.IDENTITY:
            unpack = IdentityResponse.unpack
        case Resp.MESSAGE:
            unpack = MessageResponse.unpack
        case Resp.DIGEST:
            unpack = DigestResponse.unpack
        case _:
            warning(f"Unhandled response {resp!r}")
            unpack = CoreResponse.unpack
    return unpack(data)


@frozen
class CommandPacket:
    """Representation of a command packet to interface with the bootloader"""

    data: bytes = field(default=b"", repr=False)
    CMD: ClassVar[Cmd] = Cmd.UNDEFINED
    HDR: ClassVar[int] = 0x80
    CORE_RESPONSE: ClassVar[bool] = False

    @property
    def length(self) -> int:
        """Calcualte the length of the data (data + command)"""
        return len(self.data) + 1

    @property
    def fmt(self) -> str:
        """Build the format string for struct.pack"""
        if self.data:
            return f"<BHB{len(self.data)}BI"
        return "<BHBI"

    @property
    def crc(self) -> int:
        """Calculate the CRC for the command"""
        # CRC-32/JAMCRC
        cmd = struct.pack("B", self.CMD)
        return crc32(cmd + self.data)

    def serialize(self) -> bytes:
        """Serialize the command into bytes"""
        return struct.pack(
            self.fmt, self.HDR, self.length, self.CMD, *self.data, self.crc
        )

    def __len__(self) -> int:
        """Calculate the length of the command"""
        return struct.calcsize(self.fmt)

    def send(self, ser: serial.Serial) -> None:
        """Send the command to the bootloader"""
        pkt = self.serialize()
        if len(pkt) > 100:  # noqa: PLR2004
            trace(f"Sending {len(pkt)}B, CRC: {self.crc:x}, ({pkt[:100]!r}...)")
        else:
            trace(f"Sending {len(pkt)}B, CRC: {self.crc:x}, ({pkt!r})")
        ser.write(pkt)

    def read_ack(self, ser: serial.Serial) -> Ack:
        """Read an ACK from the bootloader"""
        trace("Listening for ack")
        raw_ack = ser.read()
        if len(raw_ack) != 1:
            msg = "Did not receive ack!"
            raise NoACKError(msg)

        try:
            ack = Ack(raw_ack[0])
        except ValueError as e:
            msg = f"Bad ack received {raw_ack}"
            raise CommandError(msg) from e

        trace(f"Received {ack!r}")
        return ack

    def read_core_response(self, _: serial.Serial) -> CoreResponse | None:
        """Read the core response from the bootloader"""
        trace(f"No body expected for {self.CMD!r}")
        return None

    def read_response(self, ser: serial.Serial) -> CoreResponse | None:
        """Read the response from the bootloader"""
        ack = self.read_ack(ser)
        if ack != Ack.ACK:
            raise NACKError(ack)
        if self.CORE_RESPONSE:
            resp = CoreResponse.deserialize(ser)
            if isinstance(resp, MessageResponse) and not self.validate_message(resp):
                error(f"Received negative message {resp}")
                raise MessageError(resp)
            return resp
        return None

    def validate_message(self, msg: MessageResponse) -> bool:
        """Check if the message is an expected correct one"""
        return msg.message == Message.SUCCESS


@frozen
class ConnectionPacket(CommandPacket):
    """Interface for the CONNECTION command"""

    CMD: ClassVar[Cmd] = Cmd.CONNECTION


@frozen
class IdentityPacket(CommandPacket):
    """Interface for the IDENTITY command"""

    CMD: ClassVar[Cmd] = Cmd.IDENTITY
    CORE_RESPONSE: ClassVar[bool] = True


@frozen
class ErasePacket(CommandPacket):
    """Interface for the ERASE command"""

    CMD: ClassVar[Cmd] = Cmd.ERASE
    CORE_RESPONSE: ClassVar[bool] = True


@frozen
class UpdatePacket(CommandPacket):
    """Interface for the UPDATE command"""

    CMD: ClassVar[Cmd] = Cmd.UPDATE
    CORE_RESPONSE: ClassVar[bool] = True

    @classmethod
    def from_data(cls, name: str, size: int, verification_data: bytes) -> Self:
        """Generate a VerifyPacket from the sent image"""
        meta = struct.pack(f"<{NAME_SIZE}sI", name.encode(), size)
        return cls(meta + verification_data)


@frozen
class ProgramPacket(CommandPacket):
    """Interface for the PROGRAM command"""

    CMD: ClassVar[Cmd] = Cmd.PROGRAM
    CORE_RESPONSE: ClassVar[bool] = True

    @classmethod
    def from_data(cls, offset: int, data: bytes) -> Self:
        """Generate a VerifyPacket from the data to send"""
        return cls(struct.pack("<I", offset) + data)


@frozen
class VerifyPacket(CommandPacket):
    """Interface for the VERIFY command"""

    CMD: ClassVar[Cmd] = Cmd.VERIFY
    CORE_RESPONSE: ClassVar[bool] = True


@frozen
class StartPacket(CommandPacket):
    """Interface for the START command"""

    CMD: ClassVar[Cmd] = Cmd.START
    CORE_RESPONSE: ClassVar[bool] = True


@frozen
class DigestPacket(CommandPacket):
    """Interface for the DIGEST command"""

    CMD: ClassVar[Cmd] = Cmd.DIGEST
    CORE_RESPONSE: ClassVar[bool] = True

    @classmethod
    def from_slot(cls, slot: int) -> Self:
        """Generate a DigestPacket from the slot number"""
        slot = struct.pack("B", slot)
        return cls(slot)
