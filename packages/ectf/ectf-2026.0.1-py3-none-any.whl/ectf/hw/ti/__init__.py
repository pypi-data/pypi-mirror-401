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
import sys
import time
from collections.abc import Iterator
from typing import ClassVar, Self

from attrs import define, field, frozen

from ectf.console import debug, error, info, warning
from ectf.hw.bootloader import Bootloader, BootloaderError
from ectf.hw.ti.protocol import (
    NAME_SIZE,
    CommandError,
    CommandPacket,
    ConnectionPacket,
    CoreResponse,
    DigestPacket,
    ErasePacket,
    IdentityPacket,
    IdentityResponse,
    ProgramPacket,
    StartPacket,
    UpdatePacket,
    VerifyPacket,
    crc32,
)


class EraseNeededError(BootloaderError):
    """An erase is needed before the requested operation"""


class ImageMismatchError(BootloaderError):
    """Image not compatible with the provisioned bootloader"""


@frozen
class Image:
    """An image to be sent to the bootloader, either protected or unprotected"""

    name: str
    size: int
    protected: bool
    verification_data: bytes = field(repr=False)
    _body: bytes = field(repr=False)
    chunks: list[tuple[int, bytes]] = field()
    PROTECTED_MAGIC: ClassVar[bytes] = b"SECURE!!"
    PROT_HDR_FMT: ClassVar[str] = f"8s{NAME_SIZE}sI32s"
    CHUNK_META_SIZE = 32

    @classmethod
    def deserialize(cls, image: bytes, name: str | None = None) -> Self:
        """Generate an Image from the raw file"""
        if image.startswith(cls.PROTECTED_MAGIC):
            hdr_size = struct.calcsize(cls.PROT_HDR_FMT)
            _, name, size, ver_data = struct.unpack(cls.PROT_HDR_FMT, image[:hdr_size])
            return cls(
                name.decode(),
                size,
                True,  # noqa: FBT003
                ver_data,
                image[hdr_size:],
            )

        if name is None:
            msg = "Must provide name for unprotected image"
            raise ValueError(msg)

        ver_data = struct.pack("<I", crc32(image))
        return cls(name, len(image), False, ver_data, image)  # noqa: FBT003

    def _chunk_unprotected(self) -> Iterator[tuple[int, bytes]]:
        """Chunk an unprotected image"""
        sector_size = MSPM0L2228.SECTOR_SIZE
        step = ((MSPM0L2228.CHUNK_SIZE // sector_size) - 1) * sector_size
        for offset in range(0, len(self.body), step):
            block = self.body[offset : offset + step]
            pad_len = (sector_size - (len(block) % sector_size)) % sector_size
            if pad_len:
                debug(f"Padding {pad_len}B")
                block += b"\xff" * pad_len

            yield offset, block

    def _chunk_protected(self) -> Iterator[tuple[int, bytes]]:
        """Chunk a protected image"""
        # discard header
        offset = 0
        image = self._body
        while image:
            # extract chunk size
            (size,) = struct.unpack("<I", image[:4])

            # yield offset and chunk
            yield offset, image[4 : 4 + size]

            # move to next chunk
            offset += size - self.CHUNK_META_SIZE
            image = image[4 + size :]

    @chunks.default
    def _chunks(self) -> list[tuple[int, bytes]]:
        """Get the correct chunked body to send"""
        if self.protected:
            return list(self._chunk_protected())
        return list(self._chunk_unprotected())

    @property
    def body(self) -> bytes:
        """The raw body to send"""
        if self.protected:
            return b"".join(chunk for (_, chunk) in self.chunks)
        debug("RETURNING NON PROTECTED BODY")
        return self._body

    def gen_update(self) -> UpdatePacket:
        """Generate an UpdatePacket"""
        return UpdatePacket.from_data(self.name, self.size, self.verification_data)

    def __len__(self) -> int:
        """Length of the raw body being sent"""
        return len(self.body)


@define
class MSPM0L2228(Bootloader):
    """Interface to the MITRE bootloader of the MSPM0L2228"""

    PAGE_SIZE: ClassVar[int] = 0x400
    APP_PAGES: ClassVar[int] = 104
    TOTAL_SIZE: ClassVar[int] = APP_PAGES * PAGE_SIZE

    COMPLETE_CODE: ClassVar[int] = 20
    SUCCESS_CODES: ClassVar[frozenset[int]] = frozenset(
        {1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 14, 17, 20, 21, COMPLETE_CODE},
    )
    SUCCESSFUL_RECV_CODES: ClassVar[frozenset[int]] = frozenset({4, 5, 6, 7, 8, 9})
    ERROR_CODES: ClassVar[frozenset[[int]]] = frozenset({6, 10, 13, 15, 16, 18})

    UPDATE_COMMAND: ClassVar[bytes] = b"\x00"
    SECTOR_SIZE: ClassVar[int] = 1024
    CHUNK_SIZE: ClassVar[int] = 0x2C00

    # Wait for expected bootloader response byte
    # Exit if response does not match
    def _verify_resp(self) -> int:
        """Get and check the response code"""
        while (resp := self.ser.read(1)) == b"":
            pass
        resp = ord(resp)
        if resp in self.ERROR_CODES:
            error(f"Bootloader responded with: {resp}")
            sys.exit(-1)
        if resp not in self.SUCCESS_CODES:
            error(f"Unexpected bootloader response: {resp}")
            sys.exit(-2)
        return resp

    def _execute(
        self, packet: CommandPacket, *, retries: int = 0
    ) -> CoreResponse | None:
        start = time.time()
        try:
            while True:
                debug(f"Sending {packet}")
                packet.send(self.ser)
                try:
                    resp = packet.read_response(self.ser)
                except CommandError:
                    if retries:
                        retries -= 1
                        continue
                    raise
                end = time.time()
                debug(f"Executed command in {end - start:0.2f} seconds")
                return resp
        finally:
            if self.ser.in_waiting:
                time.sleep(2)
                resp = self.ser.read(self.ser.in_waiting)
                warning(f"Unconsumed data: {resp}")

    def connect(self) -> None:
        """Connect to the bootloader"""
        try:
            self._execute(ConnectionPacket())
        except BootloaderError as e:
            msg = "Could not connect to the bootloader"
            raise BootloaderError(msg) from e

    def status(self) -> IdentityResponse:
        """Get the status of the bootloader"""
        identity: IdentityResponse = self._execute(IdentityPacket())
        debug(identity)
        return identity

    def erase(self) -> None:
        """Erase an image from the bootloader"""
        info("Erasing old image")
        self._execute(ErasePacket())

        identity = self.status()
        if not identity.app_clear:
            msg = "Erase failed"
            raise BootloaderError(msg)

    def flash(self, image: Image) -> None:
        """Update the board with an image

        :param image: Raw image to be programmed to the board
        """
        self._execute(ConnectionPacket())

        identity = self.status()
        if image.protected and not identity.secure:
            msg = "Tried to load protected image onto design bootloader"
            raise ImageMismatchError(msg)

        if not image.protected and identity.secure:
            msg = "Tried to load unprotected image onto attack bootloader"
            raise ImageMismatchError(msg)

        if not identity.app_clear:
            msg = "Board must be erased before flashing"
            raise EraseNeededError(msg)

        info("Requesting update")
        pkt = image.gen_update()
        resp = self._execute(pkt)
        debug(resp)

        if identity.sector_size != self.SECTOR_SIZE:
            msg = "Bad sector size reported!"
            raise BootloaderError(msg)
        if identity.buf_size < self.CHUNK_SIZE:
            msg = "Bad chunk size reported!"
            raise BootloaderError(msg)

        debug(f"Sending {len(image.chunks)} chunks")
        start_t = time.time()
        for offset, chunk in image.chunks:
            pkt = ProgramPacket.from_data(offset, chunk)
            resp = self._execute(pkt)
            debug(resp)
        stop_t = time.time()
        debug(f"Sent {len(image)}B in {stop_t - start_t:0.2f} seconds")

        resp = self._execute(VerifyPacket())
        debug(resp)

        identity = self.status()
        if not identity.app_ready:
            error("Image not ready after verification! Reboot board and try again")
            msg = "Verification failed"
            raise BootloaderError(msg)

    def start(self) -> None:
        """Start the image, handing off from the bootloader"""
        self._execute(StartPacket())

    def digest(self, slot: int) -> bytes:
        """Get a file digest"""
        identity = self.status()
        if not identity.secure:
            msg = "Digest only possible on secure bootloader"
            raise ImageMismatchError(msg)
        if not identity.app_ready:
            msg = "Design must be flashed before requesting digest"
            raise BootloaderError(msg)

        resp = self._execute(DigestPacket.from_slot(slot))
        return resp.digest
