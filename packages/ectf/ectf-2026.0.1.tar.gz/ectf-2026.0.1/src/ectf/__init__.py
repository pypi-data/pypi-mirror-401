"""Tools for interacting with MITRE's eCTF

This source file is part of an example system for MITRE's 2025 Embedded System CTF
(eCTF). This code is being provided only for educational purposes for the 2025 MITRE
eCTF competition, and may not meet MITRE standards for quality. Use this code at your
own risk!

Copyright: Copyright (c) 2025 The MITRE Corporation
"""

CONFIG = {"VERBOSE": 0}

if __name__ == "__main__":
    from ectf.cli import app

    app()
