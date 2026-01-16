"""Generic MITRE bootloader interface

Author: Ben Janis
Date: 2025

This source file is part of an example system for MITRE's 2025 Embedded System CTF
(eCTF). This code is being provided only for educational purposes for the 2025 MITRE
eCTF competition, and may not meet MITRE standards for quality. Use this code at your
own risk!

Copyright: Copyright (c) 2025 The MITRE Corporation
"""

from abc import ABC, abstractmethod
from typing import Self

import serial
from attrs import define


class BootloaderError(Exception):
    """Error occurred during bootloader operation"""


@define
class Bootloader(ABC):
    """Standard bootloader interface

    See https://rules.ectf.mitre.org/2025/getting_started/boot_reference
    """

    ser: serial.Serial

    @classmethod
    def from_port(cls, port: str, **serial_kwargs) -> Self:  # noqa: ANN003
        """Open a serial port and generate a Bootloader instance

        :param port: Serial port to the board
        :param serial_kwargs: Args to pass to the serial interface construction
        """
        # Open serial port
        ser = serial.Serial(port=port, baudrate=115200, **serial_kwargs)
        return cls(ser)

    @abstractmethod
    def flash(self, secrets: dict) -> None:
        """Flash a design onto the board"""

    def unlock(self, secrets: dict) -> None:
        """Unlock the board"""
        msg = f"Unlocking {self.__class__.__name__} is not supported"
        raise NotImplementedError(msg)
