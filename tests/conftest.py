import asyncio
import json
from unittest.mock import patch, MagicMock
import pytest
import plugin
from tests.website_mock import WebsiteClientMock



@pytest.fixture()
def create_plugin():
    def function():
        return plugin.BNetPlugin(MagicMock(), MagicMock(), None)

    return function


@pytest.fixture()
def load_database():
    db_content = '0A FB 01 0A 05 61 67 65 6E 74 12 05 61 67 65 6E 74 1A 39 0A 1F 43 3A 2F 50 72 6F 67 72 61 6D 44 61 74 61 2F 42 61 74 74 6C 65 2E 6E 65 74 2F 41 67 65 6E 74 12 02 65 75 18 00 20 00 28 00 32 00 3A 00 4A 00 52 00 5A 00 62 00 6A 00 22 A2 01 0A 73 08 01 10 01 18 01 20 00 28 01 3A 0B 32 2E 31 36 2E 33 2E 36 36 31 30 42 26 0A 02 65 75 12 20 32 65 65 39 65 37 62 64 66 62 32 34 38 34 32 31 62 66 39 37 36 30 31 37 35 34 31 31 34 63 31 38 42 28 0A 04 6C 61 73 74 12 20 32 65 65 39 65 37 62 64 66 62 32 34 38 34 32 31 62 66 39 37 36 30 31 37 35 34 31 31 34 63 31 38 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 11 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 00 28 00 2A 07 10 80 80 80 80 B0 57 32 00 38 00 0A 97 02 0A 02 73 31 12 02 73 31 1A 51 0A 20 43 3A 2F 50 72 6F 67 72 61 6D 20 46 69 6C 65 73 20 28 78 38 36 29 2F 53 74 61 72 43 72 61 66 74 12 02 65 75 18 02 20 02 28 03 32 04 65 6E 55 53 3A 04 65 6E 55 53 42 08 0A 04 65 6E 55 53 10 03 4A 00 52 00 5A 03 50 4F 4C 62 02 50 4C 6A 00 22 AC 01 0A 79 08 01 10 01 18 01 20 00 28 01 3A 0B 31 2E 32 32 2E 33 2E 35 33 35 34 42 26 0A 02 65 75 12 20 32 30 63 33 35 39 32 35 37 63 64 34 31 32 64 34 33 64 39 32 38 37 39 37 34 36 37 30 61 32 38 61 42 28 0A 04 6C 61 73 74 12 20 32 30 63 33 35 39 32 35 37 63 64 34 31 32 64 34 33 64 39 32 38 37 39 37 34 36 37 30 61 32 38 61 42 04 0A 00 12 00 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 15 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 C1 B4 C1 DF 17 28 00 2A 07 10 83 80 80 80 B0 57 32 00 38 00 0A 93 02 0A 0A 62 61 74 74 6C 65 2E 6E 65 74 12 03 62 6E 61 1A 4D 0A 21 43 3A 2F 50 72 6F 67 72 61 6D 20 46 69 6C 65 73 20 28 78 38 36 29 2F 42 61 74 74 6C 65 2E 6E 65 74 12 02 65 75 18 02 20 02 28 03 32 04 65 6E 47 42 3A 04 65 6E 47 42 42 08 0A 04 65 6E 47 42 10 03 4A 00 52 00 5A 00 62 00 6A 00 22 A3 01 0A 74 08 01 10 01 18 01 20 00 28 01 3A 0C 31 2E 31 32 2E 38 2E 31 30 39 34 39 42 26 0A 02 65 75 12 20 63 35 65 32 34 39 34 63 32 32 65 34 63 37 37 36 38 65 64 61 32 64 37 34 64 38 38 37 61 33 32 36 42 28 0A 04 6C 61 73 74 12 20 63 35 65 32 34 39 34 63 32 32 65 34 63 37 37 36 38 65 64 61 32 64 37 34 64 38 38 37 61 33 32 36 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 11 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 00 28 00 2A 07 10 80 80 80 80 C0 57 32 00 38 00 0A 9C 02 0A 0C 64 69 61 62 6C 6F 33 5F 70 6C 70 6C 12 02 64 33 1A 52 0A 21 43 3A 2F 50 72 6F 67 72 61 6D 20 46 69 6C 65 73 20 28 78 38 36 29 2F 44 69 61 62 6C 6F 20 49 49 49 12 02 65 75 18 02 20 02 28 03 32 04 70 6C 50 4C 3A 04 70 6C 50 4C 42 08 0A 04 70 6C 50 4C 10 03 4A 00 52 00 5A 03 50 4F 4C 62 02 50 4C 6A 00 22 A6 01 0A 73 08 01 10 01 18 01 20 00 28 01 3A 0B 32 2E 36 2E 34 2E 35 35 34 33 30 42 26 0A 02 65 75 12 20 63 38 63 66 66 36 62 37 34 62 37 36 38 39 37 61 39 36 36 31 30 61 38 33 36 37 30 34 33 39 63 32 42 28 0A 04 6C 61 73 74 12 20 63 38 63 66 66 36 62 37 34 62 37 36 38 39 37 61 39 36 36 31 30 61 38 33 36 37 30 34 33 39 63 32 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 15 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 D7 9F DE 9B 3F 28 00 2A 07 10 80 80 80 80 C0 57 32 00 38 00 1A 62 0A 30 43 3A 2F 50 72 6F 67 72 61 6D 20 46 69 6C 65 73 20 28 78 38 36 29 2F 42 61 74 74 6C 65 2E 6E 65 74 2F 42 61 74 74 6C 65 2E 6E 65 74 2E 65 78 65 10 F8 14 1A 15 2F 69 6E 73 74 61 6C 6C 2F 64 69 61 62 6C 6F 33 5F 70 6C 70 6C 1A 14 2F 75 70 64 61 74 65 2F 64 69 61 62 6C 6F 33 5F 70 6C 70 6C 1A 0F 0A 09 41 67 65 6E 74 2E 65 78 65 10 90 84 01 22 49 0A 05 61 67 65 6E 74 12 40 61 35 34 65 61 62 66 34 65 38 31 65 38 30 63 36 31 63 32 32 62 63 61 30 38 65 31 61 62 66 63 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 22 47 0A 03 62 6E 61 12 40 65 62 31 38 37 37 63 35 64 38 30 33 35 61 30 61 33 66 61 33 37 38 65 35 35 38 37 61 65 30 63 63 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 2A 06 08 00 10 A0 8D 06 30 8A 9B 05 3A 02 73 31 3A 0A 62 61 74 74 6C 65 2E 6E 65 74'
    return bytes.fromhex(db_content)


@pytest.fixture()
def another_database():
    db_content = '0A FE 01 0A 05 61 67 65 6E 74 12 05 61 67 65 6E 74 1A 39 0A 1F 43 3A 2F 50 72 6F 67 72 61 6D 44 61 74 61 2F 42 61 74 74 6C 65 2E 6E 65 74 2F 41 67 65 6E 74 12 02 65 75 18 00 20 00 28 00 32 00 3A 00 4A 00 52 00 5A 00 62 00 6A 00 22 A2 01 0A 73 08 01 10 01 18 01 20 00 28 01 3A 0B 32 2E 31 36 2E 33 2E 36 36 31 30 42 26 0A 02 65 75 12 20 32 65 65 39 65 37 62 64 66 62 32 34 38 34 32 31 62 66 39 37 36 30 31 37 35 34 31 31 34 63 31 38 42 28 0A 04 6C 61 73 74 12 20 32 65 65 39 65 37 62 64 66 62 32 34 38 34 32 31 62 66 39 37 36 30 31 37 35 34 31 31 34 63 31 38 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 11 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 00 28 00 2A 0A 10 81 80 80 80 F0 FF FF FF 7F 32 00 38 00 0A 93 02 0A 0A 62 61 74 74 6C 65 2E 6E 65 74 12 03 62 6E 61 1A 4D 0A 21 43 3A 2F 50 72 6F 67 72 61 6D 20 46 69 6C 65 73 20 28 78 38 36 29 2F 42 61 74 74 6C 65 2E 6E 65 74 12 02 65 75 18 02 20 02 28 03 32 04 70 6C 50 4C 3A 04 70 6C 50 4C 42 08 0A 04 70 6C 50 4C 10 03 4A 00 52 00 5A 00 62 00 6A 00 22 A3 01 0A 74 08 01 10 01 18 01 20 00 28 01 3A 0C 31 2E 31 32 2E 39 2E 31 30 39 37 39 42 26 0A 02 65 75 12 20 61 37 63 36 38 62 39 33 35 34 31 64 34 38 34 63 35 32 32 64 38 39 63 34 32 61 66 34 61 36 38 38 42 28 0A 04 6C 61 73 74 12 20 61 37 63 36 38 62 39 33 35 34 31 64 34 38 34 63 35 32 32 64 38 39 63 34 32 61 66 34 61 36 38 38 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 11 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 00 28 00 2A 07 10 80 80 80 80 C0 57 32 00 38 00 0A 91 02 0A 08 64 65 73 74 69 6E 79 32 12 04 64 73 74 32 1A 4C 0A 11 44 3A 2F 62 6E 65 74 2F 44 65 73 74 69 6E 79 20 32 12 02 65 75 18 02 20 02 28 03 32 04 65 6E 55 53 3A 04 65 6E 55 53 42 08 0A 04 70 6C 50 4C 10 03 42 08 0A 04 65 6E 55 53 10 03 4A 00 52 00 5A 03 50 4F 4C 62 02 50 4C 6A 00 22 A8 01 0A 79 08 01 10 01 18 01 20 00 28 01 3A 11 32 2E 31 2E 34 2E 31 20 28 35 36 32 35 39 37 37 29 42 26 0A 02 65 75 12 20 62 66 64 63 33 64 38 31 36 31 36 37 32 66 36 62 39 38 37 39 37 32 63 39 65 36 63 37 63 37 31 30 42 28 0A 04 6C 61 73 74 12 20 62 66 64 63 33 64 38 31 36 31 36 37 32 66 36 62 39 38 37 39 37 32 63 39 65 36 63 37 63 37 31 30 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 11 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 00 28 00 2A 02 10 00 32 00 38 00 0A 8E 02 0A 0C 64 69 61 62 6C 6F 33 5F 70 6C 70 6C 12 02 64 33 1A 43 0A 12 44 3A 2F 62 6E 65 74 2F 44 69 61 62 6C 6F 20 49 49 49 12 02 65 75 18 02 20 02 28 03 32 04 70 6C 50 4C 3A 04 70 6C 50 4C 42 08 0A 04 70 6C 50 4C 10 03 4A 00 52 00 5A 03 50 4F 4C 62 02 50 4C 6A 00 22 AC 01 0A 79 08 01 10 01 18 01 20 00 28 01 3A 0B 32 2E 36 2E 34 2E 35 35 34 33 30 42 26 0A 02 65 75 12 20 63 38 63 66 66 36 62 37 34 62 37 36 38 39 37 61 39 36 36 31 30 61 38 33 36 37 30 34 33 39 63 32 42 28 0A 04 6C 61 73 74 12 20 63 38 63 66 66 36 62 37 34 62 37 36 38 39 37 61 39 36 36 31 30 61 38 33 36 37 30 34 33 39 63 32 42 04 0A 00 12 00 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 15 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 D7 9F DE 9B 3F 28 00 2A 02 10 00 32 00 38 00 0A 87 02 0A 07 68 73 5F 62 65 74 61 12 03 68 73 62 1A 44 0A 13 44 3A 2F 62 6E 65 74 2F 48 65 61 72 74 68 73 74 6F 6E 65 12 02 65 75 18 02 20 02 28 03 32 04 70 6C 50 4C 3A 04 70 6C 50 4C 42 08 0A 04 70 6C 50 4C 10 03 4A 00 52 00 5A 03 50 4F 4C 62 02 50 4C 6A 00 22 A3 01 0A 74 08 01 10 01 18 01 20 00 28 01 3A 0C 31 33 2E 32 2E 30 2E 32 38 38 35 35 42 26 0A 02 65 75 12 20 66 34 65 38 37 39 63 33 30 32 65 64 63 32 33 62 66 39 32 61 63 61 36 66 62 65 30 38 35 66 35 66 42 28 0A 04 6C 61 73 74 12 20 66 34 65 38 37 39 63 33 30 32 65 64 63 32 33 62 66 39 32 61 63 61 36 66 62 65 30 38 35 66 35 66 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 11 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 00 28 00 2A 07 10 80 80 80 80 B0 57 32 00 38 00 0A 9D 02 0A 06 68 65 72 6F 65 73 12 04 68 65 72 6F 1A 4C 0A 1B 44 3A 2F 62 6E 65 74 2F 48 65 72 6F 65 73 20 6F 66 20 74 68 65 20 53 74 6F 72 6D 12 02 65 75 18 02 20 02 28 03 32 04 70 6C 50 4C 3A 04 70 6C 50 4C 42 08 0A 04 70 6C 50 4C 10 03 4A 00 52 00 5A 03 50 4F 4C 62 02 50 4C 6A 00 22 AD 01 0A 7A 08 01 10 01 18 01 20 00 28 01 3A 0C 32 2E 34 33 2E 32 2E 37 32 34 38 31 42 26 0A 02 65 75 12 20 37 34 31 30 38 62 34 38 37 37 63 62 35 62 37 63 38 34 39 64 35 35 63 31 37 39 36 35 61 31 35 66 42 28 0A 04 6C 61 73 74 12 20 37 34 31 30 38 62 34 38 37 37 63 62 35 62 37 63 38 34 39 64 35 35 63 31 37 39 36 35 61 31 35 66 42 04 0A 00 12 00 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 15 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 E9 9A AC EA 31 28 00 2A 07 10 80 80 80 80 B0 57 32 04 68 65 72 6F 38 00 0A 88 02 0A 02 73 31 12 02 73 31 1A 42 0A 11 44 3A 2F 62 6E 65 74 2F 53 74 61 72 43 72 61 66 74 12 02 65 75 18 02 20 02 28 03 32 04 70 6C 50 4C 3A 04 70 6C 50 4C 42 08 0A 04 70 6C 50 4C 10 03 4A 00 52 00 5A 03 50 4F 4C 62 02 50 4C 6A 00 22 AC 01 0A 79 08 01 10 01 18 01 20 00 28 01 3A 0B 31 2E 32 32 2E 33 2E 35 33 35 34 42 26 0A 02 65 75 12 20 32 30 63 33 35 39 32 35 37 63 64 34 31 32 64 34 33 64 39 32 38 37 39 37 34 36 37 30 61 32 38 61 42 28 0A 04 6C 61 73 74 12 20 32 30 63 33 35 39 32 35 37 63 64 34 31 32 64 34 33 64 39 32 38 37 39 37 34 36 37 30 61 32 38 61 42 04 0A 00 12 00 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 15 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 E8 CA A7 A0 18 28 00 2A 07 10 80 80 80 80 B0 57 32 00 38 00 0A 90 02 0A 07 73 32 5F 70 6C 70 6C 12 02 73 32 1A 45 0A 14 44 3A 2F 62 6E 65 74 2F 53 74 61 72 43 72 61 66 74 20 49 49 12 02 65 75 18 02 20 02 28 03 32 04 70 6C 50 4C 3A 04 70 6C 50 4C 42 08 0A 04 70 6C 50 4C 10 03 4A 00 52 00 5A 03 50 4F 4C 62 02 50 4C 6A 00 22 AC 01 0A 79 08 01 10 01 18 01 20 00 28 01 3A 0B 34 2E 38 2E 33 2E 37 32 32 38 32 42 26 0A 02 65 75 12 20 35 62 34 39 63 35 33 63 66 61 65 62 30 36 36 62 32 31 63 39 63 31 66 65 62 36 61 33 30 64 64 64 42 28 0A 04 6C 61 73 74 12 20 35 62 34 39 63 35 33 63 66 61 65 62 30 36 36 62 32 31 63 39 63 31 66 65 62 36 61 33 30 64 64 64 42 04 0A 00 12 00 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 15 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 F7 C9 DB AE 5D 28 00 2A 07 10 80 80 80 80 B0 57 32 00 38 00 0A AD 02 0A 08 77 6F 77 5F 65 6E 75 73 12 03 77 6F 77 1A 5C 0A 19 44 3A 2F 62 6E 65 74 2F 57 6F 72 6C 64 20 6F 66 20 57 61 72 63 72 61 66 74 12 02 65 75 18 02 20 02 28 03 32 04 72 75 52 55 3A 04 72 75 52 55 42 08 0A 04 72 75 52 55 10 03 42 08 0A 04 70 74 42 52 10 03 4A 00 52 00 5A 03 50 4F 4C 62 02 50 4C 6A 08 5F 72 65 74 61 69 6C 5F 22 AD 01 0A 79 08 01 10 01 18 01 20 00 28 01 3A 0B 38 2E 31 2E 30 2E 32 39 34 38 32 42 26 0A 02 65 75 12 20 32 37 66 63 30 33 31 37 62 31 61 34 38 37 31 66 33 33 61 61 36 35 38 30 64 66 34 34 37 38 39 62 42 28 0A 04 6C 61 73 74 12 20 32 37 66 63 30 33 31 37 62 31 61 34 38 37 31 66 33 33 61 61 36 35 38 30 64 66 34 34 37 38 39 62 42 04 0A 00 12 00 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 16 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 EE C3 BD 9C DC 01 28 00 2A 07 10 80 80 80 80 B0 57 32 03 77 6F 77 38 00 1A 86 01 0A 30 43 3A 2F 50 72 6F 67 72 61 6D 20 46 69 6C 65 73 20 28 78 38 36 29 2F 42 61 74 74 6C 65 2E 6E 65 74 2F 42 61 74 74 6C 65 2E 6E 65 74 2E 65 78 65 10 B8 96 03 1A 0A 2F 75 70 64 61 74 65 2F 73 31 1A 0F 2F 75 70 64 61 74 65 2F 73 32 5F 70 6C 70 6C 1A 0E 2F 75 70 64 61 74 65 2F 68 65 72 6F 65 73 1A 0F 2F 75 70 64 61 74 65 2F 68 73 5F 62 65 74 61 1A 10 2F 75 70 64 61 74 65 2F 77 6F 77 5F 65 6E 75 73 22 49 0A 05 61 67 65 6E 74 12 40 61 35 34 65 61 62 66 34 65 38 31 65 38 30 63 36 31 63 32 32 62 63 61 30 38 65 31 61 62 66 63 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 22 47 0A 03 62 6E 61 12 40 63 62 34 33 33 34 32 61 65 30 31 36 32 35 38 62 62 62 62 63 32 33 30 30 64 30 39 39 35 66 37 33 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 2A 06 08 00 10 A0 8D 06 30 8D A2 05'
    return bytes.fromhex(db_content)

@pytest.fixture()
def db_under_installation():
    """heroes under installation, over "PLAYABLE"; s1 queued for installation"""
    db_content = '0A FB 01 0A 05 61 67 65 6E 74 12 05 61 67 65 6E 74 1A 39 0A 1F 43 3A 2F 50 72 6F 67 72 61 6D 44 61 74 61 2F 42 61 74 74 6C 65 2E 6E 65 74 2F 41 67 65 6E 74 12 02 65 75 18 00 20 00 28 00 32 00 3A 00 4A 00 52 00 5A 00 62 00 6A 00 22 A2 01 0A 73 08 01 10 01 18 01 20 00 28 01 3A 0B 32 2E 31 36 2E 33 2E 36 36 31 30 42 26 0A 02 65 75 12 20 32 65 65 39 65 37 62 64 66 62 32 34 38 34 32 31 62 66 39 37 36 30 31 37 35 34 31 31 34 63 31 38 42 28 0A 04 6C 61 73 74 12 20 32 65 65 39 65 37 62 64 66 62 32 34 38 34 32 31 62 66 39 37 36 30 31 37 35 34 31 31 34 63 31 38 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 11 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 00 28 00 2A 07 10 80 80 80 80 B0 57 32 00 38 00 0A 93 02 0A 0A 62 61 74 74 6C 65 2E 6E 65 74 12 03 62 6E 61 1A 4D 0A 21 43 3A 2F 50 72 6F 67 72 61 6D 20 46 69 6C 65 73 20 28 78 38 36 29 2F 42 61 74 74 6C 65 2E 6E 65 74 12 02 65 75 18 02 20 02 28 03 32 04 65 6E 55 53 3A 04 65 6E 55 53 42 08 0A 04 65 6E 55 53 10 03 4A 00 52 00 5A 00 62 00 6A 00 22 A3 01 0A 74 08 01 10 01 18 01 20 00 28 01 3A 0C 31 2E 31 32 2E 39 2E 31 30 39 37 39 42 26 0A 02 65 75 12 20 61 37 63 36 38 62 39 33 35 34 31 64 34 38 34 63 35 32 32 64 38 39 63 34 32 61 66 34 61 36 38 38 42 28 0A 04 6C 61 73 74 12 20 61 37 63 36 38 62 39 33 35 34 31 64 34 38 34 63 35 32 32 64 38 39 63 34 32 61 66 34 61 36 38 38 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 11 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 00 28 00 2A 07 10 80 80 80 80 C0 57 32 00 38 00 0A 9F 02 0A 07 73 32 5F 65 6E 67 62 12 02 73 32 1A 54 0A 23 43 3A 2F 50 72 6F 67 72 61 6D 20 46 69 6C 65 73 20 28 78 38 36 29 2F 53 74 61 72 43 72 61 66 74 20 49 49 12 02 65 75 18 02 20 02 28 03 32 04 65 6E 55 53 3A 04 65 6E 55 53 42 08 0A 04 65 6E 55 53 10 03 4A 00 52 00 5A 03 50 4F 4C 62 02 50 4C 6A 00 22 AC 01 0A 79 08 01 10 01 18 01 20 00 28 01 3A 0B 34 2E 38 2E 33 2E 37 32 32 38 32 42 26 0A 02 65 75 12 20 35 62 34 39 63 35 33 63 66 61 65 62 30 36 36 62 32 31 63 39 63 31 66 65 62 36 61 33 30 64 64 64 42 28 0A 04 6C 61 73 74 12 20 35 62 34 39 63 35 33 63 66 61 65 62 30 36 36 62 32 31 63 39 63 31 66 65 62 36 61 33 30 64 64 64 42 04 0A 00 12 00 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 15 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 9E 8C CF C1 5D 28 00 2A 07 10 80 80 80 80 B0 57 32 00 38 00 0A 9C 02 0A 0C 64 69 61 62 6C 6F 33 5F 65 6E 75 73 12 02 64 33 1A 52 0A 21 43 3A 2F 50 72 6F 67 72 61 6D 20 46 69 6C 65 73 20 28 78 38 36 29 2F 44 69 61 62 6C 6F 20 49 49 49 12 02 65 75 18 02 20 02 28 03 32 04 65 6E 55 53 3A 04 65 6E 55 53 42 08 0A 04 65 6E 55 53 10 03 4A 00 52 00 5A 03 50 4F 4C 62 02 50 4C 6A 00 22 A6 01 0A 73 08 01 10 01 18 01 20 00 28 01 3A 0B 32 2E 36 2E 34 2E 35 35 34 33 30 42 26 0A 02 65 75 12 20 63 38 63 66 66 36 62 37 34 62 37 36 38 39 37 61 39 36 36 31 30 61 38 33 36 37 30 34 33 39 63 32 42 28 0A 04 6C 61 73 74 12 20 63 38 63 66 66 36 62 37 34 62 37 36 38 39 37 61 39 36 36 31 30 61 38 33 36 37 30 34 33 39 63 32 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 15 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 95 E0 F6 AD 3E 28 00 2A 07 10 80 80 80 80 C0 57 32 00 38 00 0A 96 02 0A 07 68 73 5F 62 65 74 61 12 03 68 73 62 1A 53 0A 22 43 3A 2F 50 72 6F 67 72 61 6D 20 46 69 6C 65 73 20 28 78 38 36 29 2F 48 65 61 72 74 68 73 74 6F 6E 65 12 02 65 75 18 02 20 02 28 03 32 04 65 6E 55 53 3A 04 65 6E 55 53 42 08 0A 04 65 6E 55 53 10 03 4A 00 52 00 5A 03 50 4F 4C 62 02 50 4C 6A 00 22 A3 01 0A 74 08 01 10 01 18 01 20 00 28 01 3A 0C 31 33 2E 32 2E 30 2E 32 38 38 35 35 42 26 0A 02 65 75 12 20 66 34 65 38 37 39 63 33 30 32 65 64 63 32 33 62 66 39 32 61 63 61 36 66 62 65 30 38 35 66 35 66 42 28 0A 04 6C 61 73 74 12 20 66 34 65 38 37 39 63 33 30 32 65 64 63 32 33 62 66 39 32 61 63 61 36 66 62 65 30 38 35 66 35 66 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 11 0A 00 11 00 00 00 00 00 00 F0 3F 18 00 20 00 28 00 2A 07 10 80 80 80 80 B0 57 32 00 38 00 0A AC 02 0A 06 68 65 72 6F 65 73 12 04 68 65 72 6F 1A 5B 0A 2A 43 3A 2F 50 72 6F 67 72 61 6D 20 46 69 6C 65 73 20 28 78 38 36 29 2F 48 65 72 6F 65 73 20 6F 66 20 74 68 65 20 53 74 6F 72 6D 12 02 65 75 18 02 20 02 28 03 32 04 65 6E 55 53 3A 04 65 6E 55 53 42 08 0A 04 65 6E 55 53 10 03 4A 00 52 00 5A 03 50 4F 4C 62 02 50 4C 6A 00 22 AB 01 0A 74 08 01 10 01 18 00 20 00 28 01 3A 0C 32 2E 34 33 2E 33 2E 37 32 36 34 39 42 26 0A 02 65 75 12 20 65 63 30 65 32 36 33 65 65 65 31 36 39 30 39 64 35 33 63 36 38 31 30 64 38 37 63 63 35 66 64 37 42 28 0A 04 6C 61 73 74 12 20 65 63 30 65 32 36 33 65 65 65 31 36 39 30 39 64 35 33 63 36 38 31 30 64 38 37 63 63 35 66 64 37 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 19 0A 00 11 5B 45 E0 F1 1A 88 D8 3F 18 00 20 B8 E0 FC 9C 31 28 F3 85 B7 AD 1E 2A 09 08 00 10 80 80 80 80 C0 57 32 04 68 65 72 6F 38 00 0A B1 01 0A 02 73 31 12 02 73 31 1A 51 0A 20 43 3A 2F 50 72 6F 67 72 61 6D 20 46 69 6C 65 73 20 28 78 38 36 29 2F 53 74 61 72 43 72 61 66 74 12 02 65 75 18 02 20 02 28 03 32 04 65 6E 55 53 3A 04 65 6E 55 53 42 08 0A 04 65 6E 55 53 10 03 4A 00 52 00 5A 03 50 4F 4C 62 02 50 4C 6A 00 22 45 0A 16 08 00 10 00 18 00 20 00 28 01 3A 00 4A 06 0A 02 65 75 12 00 52 00 12 0D 09 00 00 00 00 00 00 00 00 10 00 18 00 1A 09 09 00 00 00 00 00 00 00 00 22 11 0A 00 11 00 00 00 00 00 00 00 00 18 00 20 00 28 00 2A 09 08 00 10 80 80 80 80 C0 57 32 00 38 00 1A 6F 0A 30 43 3A 2F 50 72 6F 67 72 61 6D 20 46 69 6C 65 73 20 28 78 38 36 29 2F 42 61 74 74 6C 65 2E 6E 65 74 2F 42 61 74 74 6C 65 2E 6E 65 74 2E 65 78 65 10 D0 45 1A 0F 2F 69 6E 73 74 61 6C 6C 2F 68 65 72 6F 65 73 1A 0E 2F 75 70 64 61 74 65 2F 68 65 72 6F 65 73 1A 0B 2F 69 6E 73 74 61 6C 6C 2F 73 31 1A 0A 2F 75 70 64 61 74 65 2F 73 31 1A 0E 0A 09 41 67 65 6E 74 2E 65 78 65 10 F8 1A 22 49 0A 05 61 67 65 6E 74 12 40 61 35 34 65 61 62 66 34 65 38 31 65 38 30 63 36 31 63 32 32 62 63 61 30 38 65 31 61 62 66 63 38 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 22 47 0A 03 62 6E 61 12 40 63 62 34 33 33 34 32 61 65 30 31 36 32 35 38 62 62 62 62 63 32 33 30 30 64 30 39 39 35 66 37 33 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 2A 06 08 00 10 A0 8D 06 30 83 AD 05 3A 0C 64 69 61 62 6C 6F 33 5F 65 6E 75 73 3A 07 68 73 5F 62 65 74 61 3A 07 73 32 5F 65 6E 67 62 3A 06 68 65 72 6F 65 73 3A 02 73 31 3A 0A 62 61 74 74 6C 65 2E 6E 65 74'
    return bytes.fromhex(db_content)

@pytest.fixture()
def config_data():
    return json.loads("""{
    "Client": {
        "Version": {
            "FirstRun": "false",
            "Release": {
                "FirstRun": "false",
                "LastBuildVersion": "10979",
                "LastSeenPatchNotesVersion": "10979"
            }
        },
        "Toasts": {
            "ScreenPosition": "BottomRight",
            "Monitor": "0"
        },
        "GaClientId": "E70E3DEC-4C76-44D1-BA97-F3B87D7D5A4E",
        "AutoLogin": "true",
        "SavedAccountNames": "example-mail@example.com",
        "GameSearch": {
            "PerformedSearch": "true"
        }
    },
    "5a61123b37cafce1": {
        "Client": {
            "Language": "plPL",
            "LoginSettings": {
                "AllowedRegions": "",
                "AllowedLocales": ""
            }
        },
        "Path": "C:/Program Files (x86)/Battle.net",
        "Services": {
            "LastLoginAddress": "eu.actual.battle.net",
            "LastLoginRegion": "EU",
            "LastLoginTassadar": "eu.battle.net\/login"
        }
    },
    "Games": {
        "battle_net": {
            "ServerUid": "battle.net"
        },
        "destiny2": {
            "ServerUid": "destiny2"
        },
        "diablo3": {
            "ServerUid": "diablo3_plpl"
        },
        "heroes": {
            "LastPlayed": "1441712029"
        },
        "hs_beta": {
            "ServerUid": "hs_beta",
            "Resumable": "false"
        },
        "s1": {
            "ServerUid": "s1",
            "Resumable": "false"
        },
        "s2": {
            "ServerUid": "s2_plpl",
            "Resumable": "false"
        },
        "wow": {
            "ServerUid": "wow_enus",
            "Resumable": "true"
        }
    }
}""")


@pytest.fixture()
def create_authenticated_plugin(create_plugin):
    @patch('pathlib.Path.exists', MagicMock())
    def function():
        loop = asyncio.get_event_loop()

        with patch("plugin.BackendClient", new=WebsiteClientMock):
            pg = create_plugin()

            credentials = {
                "cookie_jar": "80036372657175657374732e636f6f6b6965730a5265717565737473436f6f6b69654a61720a7100298171017d71022858070000005f706f6c696379710363687474702e636f6f6b69656a61720a44656661756c74436f6f6b6965506f6c6963790a7104298171057d71062858080000006e657473636170657107885807000000726663323936357108895813000000726663323130395f61735f6e6574736361706571094e580c000000686964655f636f6f6b696532710a89580d0000007374726963745f646f6d61696e710b89581b0000007374726963745f726663323936355f756e76657269666961626c65710c8858160000007374726963745f6e735f756e76657269666961626c65710d8958100000007374726963745f6e735f646f6d61696e710e4b00581c0000007374726963745f6e735f7365745f696e697469616c5f646f6c6c6172710f8958120000007374726963745f6e735f7365745f7061746871108958100000005f626c6f636b65645f646f6d61696e7371112958100000005f616c6c6f7765645f646f6d61696e7371124e58040000005f6e6f7771134a75c2775c756258080000005f636f6f6b69657371147d711528580d00000065752e626174746c652e6e657471167d71172858070000002f6f617574682f71187d7119580a0000004a53455353494f4e4944711a63687474702e636f6f6b69656a61720a436f6f6b69650a711b2981711c7d711d28580700000076657273696f6e711e4b0058040000006e616d65711f580a0000004a53455353494f4e49447120580500000076616c75657121583c00000031463246434233383730354237304144384133433532344245344331313746342e626c61646530375f65755f615f6f617574685f70726f766964657271225804000000706f727471234e580e000000706f72745f7370656369666965647124895806000000646f6d61696e7125580d00000065752e626174746c652e6e657471265810000000646f6d61696e5f7370656369666965647127885812000000646f6d61696e5f696e697469616c5f646f74712889580400000070617468712958070000002f6f617574682f712a580e000000706174685f737065636966696564712b885806000000736563757265712c88580700000065787069726573712d4e580700000064697363617264712e885807000000636f6d6d656e74712f4e580b000000636f6d6d656e745f75726c71304e58070000007266633231303971318958050000005f7265737471327d71335808000000487474704f6e6c797134887375627358070000002f6c6f67696e2f71357d7136580a0000004a53455353494f4e49447137681b298171387d713928681e4b00681f580a0000004a53455353494f4e4944713a6821583700000032646136373230652d356130372d343432352d383735652d6534363136376261663839632e626c61646530355f65755f615f6c6f67696e713b68234e6824896825580d00000065752e626174746c652e6e6574713c682788682889682958070000002f6c6f67696e2f713d682b88682c88682d4e682e88682f4e68304e68318968327d713e6834887375627375580b0000002e626174746c652e6e6574713f7d71402858010000002f71417d714228580d0000006c6f67696e2e636f6f6b6965737143681b298171447d714528681e4b00681f580d0000006c6f67696e2e636f6f6b69657371466821580100000031714768234e6824896825580b0000002e626174746c652e6e6574714868278868288868296841682b88682c89682d4e682e88682f4e68304e68318968327d714968344e73756258060000007765622e6964714a681b2981714b7d714c28681e4b00681f58060000007765622e6964714d6821582700000045552d37383963396431612d306537322d343861312d613031332d333361616262376331393864714e68234e6824896825580b0000002e626174746c652e6e6574714f68278868288868296841682b88682c88682d8a0552b177dc00682e88682f4e68304e68318968327d715068348873756258030000005f67617151681b298171527d715328681e4b00681f58030000005f676171546821581a0000004741312e322e3137373430323136362e31353531333531363532715568234e6824896825580b0000002e626174746c652e6e6574715668278868288868296841682b88682c89682d4a53183a60682e88682f4e68304e68318968327d715768344e73756258040000005f6769647158681b298171597d715a28681e4b00681f58040000005f676964715b6821581b0000004741312e322e323035343230383433372e31353531333531363532715c68234e6824896825580b0000002e626174746c652e6e6574715d68278868288868296841682b88682c89682d4ad302795c682e88682f4e68304e68318968327d715e68344e737562580c0000005f6761745f626e657467746d715f681b298171607d716128681e4b00681f580c0000005f6761745f626e657467746d71626821684768234e6824896825580b0000002e626174746c652e6e6574716368278868288868296841682b88682c89682d4a8fb1775c682e88682f4e68304e68318968327d716468344e73756258050000005f67616c697165681b298171667d716728681e4b00681f58050000005f67616c697168682158060000007375626d6974716968234e6824896825580b0000002e626174746c652e6e6574716a68278868288868296841682b88682c89682d4a7db1775c682e88682f4e68304e68318968327d716b68344e737562581500000042412d74617373616461722d6c6f67696e2e6b6579716c681b2981716d7d716e28681e4b00681f581500000042412d74617373616461722d6c6f67696e2e6b6579716f682158200000003339336637623138616435343933663731323566633130353965383133386532717068234e6824896825580b0000002e626174746c652e6e6574717168278868288868296841682b88682c89682d4ac7e4466f682e88682f4e68304e68318968327d717268348873756258090000006c6f67696e2e6b65797173681b298171747d717528681e4b00681f58090000006c6f67696e2e6b65797176682158200000003339336637623138616435343933663731323566633130353965383133386532717768234e6824896825580b0000002e626174746c652e6e6574717868278868288868296841682b88682c89682d4ac7e4466f682e88682f4e68304e68318968327d717968348873756258030000006f7074717a681b2981717b7d717c28681e4b00681f58030000006f7074717d6821684768234e6824896825580b0000002e626174746c652e6e6574717e68278868288868296841682b88682c89682d4ac7e4466f682e88682f4e68304e68318968327d717f68344e7375627558060000002f6c6f67696e71807d718128580a000000626e65742e65787472617182681b298171837d718428681e4b00681f580a000000626e65742e657874726171856821586c0000004155712d35376a454b4d365a385a68536864374d764c53666a32332d513237706d594a35505f48534e46356d704653484e516649754a73684d56666e544d4f456c3635786a59775a447759476d534a6d424968726f59432d4c684f6a423870466956576967774831514a6b56718668234e6824896825580b0000002e626174746c652e6e65747187682788682888682958060000002f6c6f67696e7188682b88682c88682d8a055eb177dc00682e88682f4e68304e68318968327d7189683488737562580b00000042412d7461737361646172718a681b2981718b7d718c28681e4b00681f580b00000042412d7461737361646172718d6821582d00000045552d64323235363234646530633037303364653037333739353566316131383430332d343734353439373434718e68234e6824896825580b0000002e626174746c652e6e6574718f682788682888682958060000002f6c6f67696e7190682b88682c88682d4ac7e4466f682e88682f4e68304e68318968327d7191683488737562580e00000042412d74617373616461722d636c7192681b298171937d719428681e4b00681f580e00000042412d74617373616461722d636c7195682158200000006335623739653731353635353536636165326638613732303136653539396534719668234e6824896825580b0000002e626174746c652e6e65747197682788682888682958060000002f6c6f67696e7198682b88682c88682d4e682e88682f4e68304e68318968327d71996834887375625802000000636c719a681b2981719b7d719c28681e4b00681f5802000000636c719d682158200000006335623739653731353635353536636165326638613732303136653539396534719e68234e6824896825580b0000002e626174746c652e6e6574719f682788682888682958060000002f6c6f67696e71a0682b88682c88682d4e682e88682f4e68304e68318968327d71a16834887375627575580e0000002e65752e626174746c652e6e657471a27d71a368417d71a42858030000005f676171a5681b298171a67d71a728681e4b00681f58030000005f676171a86821581a0000004741312e332e3137373430323136362e3135353133353136353271a968234e6824896825580e0000002e65752e626174746c652e6e657471aa68278868288868296841682b88682c89682d4a5f183a60682e88682f4e68304e68318968327d71ab68344e73756258040000005f67696471ac681b298171ad7d71ae28681e4b00681f58040000005f67696471af6821581b0000004741312e332e323035343230383433372e3135353133353136353271b068234e6824896825580e0000002e65752e626174746c652e6e657471b168278868288868296841682b88682c89682d4adf02795c682e88682f4e68304e68318968327d71b268344e73756258120000005f6761745f55412d35303234393630302d3171b3681b298171b47d71b528681e4b00681f58120000005f6761745f55412d35303234393630302d3171b66821684768234e6824896825580e0000002e65752e626174746c652e6e657471b768278868288868296841682b88682c89682d4a9bb1775c682e88682f4e68304e68318968327d71b868344e7375627573581700000065752e6163636f756e742e626c697a7a6172642e636f6d71b97d71ba68417d71bb28580900000053455353494f4e494471bc681b298171bd7d71be28681e4b00681f580900000053455353494f4e494471bf6821582400000061396231303637332d653664362d346634372d386534362d39643665613036366164333671c068234e6824896825581700000065752e6163636f756e742e626c697a7a6172642e636f6d71c168278968288968296841682b88682c88682d4e682e88682f4e68304e68318968327d71c25808000000487474704f6e6c7971c34e737562580a000000585352462d544f4b454e71c4681b298171c57d71c628681e4b00681f68c46821582400000034363639393638312d656132382d343730352d613636652d37653033613862353361643571c768234e6824896825581700000065752e6163636f756e742e626c697a7a6172642e636f6d71c868278968288968296841682b88682c88682d4e682e88682f4e68304e68318968327d71c975627573580d0000002e626c697a7a6172642e636f6d71ca7d71cb68417d71cc2858030000005f676171cd681b298171ce7d71cf28681e4b00681f68cd6821581b0000004741312e322e313935363436373733302e3135353133353136363571d068234e682489682568ca68278868288868296841682b88682c89682d4a61183a60682e88682f4e68304e68318968327d71d168344e73756258040000005f67696471d2681b298171d37d71d428681e4b00681f68d26821581b0000004741312e322e313831333131363532312e3135353133353136363571d568234e6824896825580d0000002e626c697a7a6172642e636f6d71d668278868288868296841682b88682c89682d4ae102795c682e88682f4e68304e68318968327d71d768344e73756258120000005f6761745f55412d35303234393630302d3171d8681b298171d97d71da28681e4b00681f68d86821684768234e6824896825580d0000002e626c697a7a6172642e636f6d71db68278868288868296841682b88682c89682d4a9cb1775c682e88682f4e68304e68318968327d71dc68344e73756275737558040000005f6e6f7771dd4a75c2775c75622e",
                "access_token": "ACCESS_TOKEN",
                "user_details_cache": {
                    "battletag": "MOCK",
                    "id": 420,
                    "sub": "420"
                },
                "region": "eu"
            }
            loop.run_until_complete(pg.authenticate(credentials))

        return pg

    return function


#@pytest.fixture()
#def plugin(create_plugin):
#    return create_plugin()