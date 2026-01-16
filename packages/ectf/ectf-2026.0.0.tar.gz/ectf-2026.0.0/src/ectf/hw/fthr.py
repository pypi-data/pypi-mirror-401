"""Interface to the MITRE bootloader of the ADI MAX78000FTHR

Author: Sam Meyers
Date: 2025

This source file is part of an example system for MITRE's 2025 Embedded System CTF
(eCTF). This code is being provided only for educational purposes for the 2025 MITRE
eCTF competition, and may not meet MITRE standards for quality. Use this code at your
own risk!

Copyright: Copyright (c) 2025 The MITRE Corporation
"""

import hashlib
import hmac
import sys
from typing import ClassVar

import serial
from attrs import define
from loguru import logger
from tqdm import trange

from ectf.hw.bootloader import Bootloader


@define
class MAX78000FTHR(Bootloader):
    """Interface to the MITRE bootloader of the MAX78000FTHR"""

    ser: serial.Serial

    PAGE_SIZE: ClassVar[int] = 8192
    APP_PAGES: ClassVar[int] = 28
    TOTAL_SIZE: ClassVar[int] = APP_PAGES * PAGE_SIZE

    COMPLETE_CODE: ClassVar[int] = 20
    SUCCESS_CODES: ClassVar[frozenset[int]] = frozenset(
        {1, 2, 3, 4, 5, 7, 8, 10, 11, 13, 16, 18, 19, COMPLETE_CODE},
    )
    ERROR_CODES: ClassVar[frozenset[[int]]] = frozenset({6, 9, 12, 14, 15, 17})

    UPDATE_COMMAND: ClassVar[bytes] = b"\x00"
    BLOCK_SIZE: ClassVar[int] = 16

    # Wait for expected bootloader response byte
    # Exit if response does not match
    def _verify_resp(self) -> int:
        """Get and check the response code"""
        while (resp := self.ser.read(1)) == b"":
            pass
        resp = ord(resp)
        if resp in self.ERROR_CODES:
            logger.error(f"Bootloader responded with: {resp}")
            sys.exit(-1)
        if resp not in self.SUCCESS_CODES:
            logger.error(f"Unexpected bootloader response: {resp}")
            sys.exit(-2)
        return resp

    def flash(self, image: bytes) -> None:
        """Update the board with an image

        :param image: Raw image to be programmed to the board
        """
        self.ser.reset_input_buffer()

        # Pad image
        image = image + (b"\xff" * (self.TOTAL_SIZE - len(image)))

        # Send update command
        logger.info("Requesting update")
        self.ser.write(b"\x00")

        self._verify_resp()
        self._verify_resp()

        # Send image and verify each block
        logger.info("Update started")
        logger.info("Sending image data...")
        for idx in trange(0, len(image), self.BLOCK_SIZE):
            self.ser.write(image[idx : idx + self.BLOCK_SIZE])
            self._verify_resp()

        logger.info("Listening for installation status...\n")

        # Wait for update finish
        while self._verify_resp() != self.COMPLETE_CODE:
            pass

        logger.success("Update Complete!\n")

        self.ser.close()

    def unlock(self, secrets: dict) -> None:
        """Unlock the board, removing the secure bootloader

        :param secrets: Dictionary of the secrets to unlock the bootloader
        """
        self.ser.write(b"GC\r\n")

        # Get challenge
        self.ser.readline()
        challenge_bytes = self.ser.readline().decode("UTF-8")
        challenge_bytes = bytes.fromhex(challenge_bytes.strip())
        print(f"Challenge bytes: {challenge_bytes}")

        challenge_key = bytes.fromhex(secrets["challenge_key"])
        print(f"Challenge key: {challenge_key}")

        mac = hmac.new(challenge_key, msg=challenge_bytes, digestmod=hashlib.sha256)
        response = f"SR {mac.hexdigest().upper()}\r\n"
        print(f"Response: {response}")

        self.ser.write(response.encode())
        self.ser.write(b"UNLOCK\r\n")
