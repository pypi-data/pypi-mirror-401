import binascii
import lzma
from typing import Self

from by_square.serialize import Serializable, SquareReader


class DecodingError(Exception):
    pass


def encode_for_qr(header: bytes, data: str) -> str:
    # https://github.com/matusf/pay-by-square/blob/c3078b222e2a385a8f4e76159b8a645d85c3c019/pay_by_square.py

    # Add checksum
    checksum = binascii.crc32(data.encode()).to_bytes(4, "little")
    total = checksum + data.encode()

    # Compress
    compressed = lzma.compress(
        total,
        format=lzma.FORMAT_RAW,
        filters=[
            {
                "id": lzma.FILTER_LZMA1,
                "lc": 3,
                "lp": 0,
                "pb": 2,
                "dict_size": 128 * 1024,
            }
        ],
    )

    # Prepend header and length
    compressed_with_length = header + len(total).to_bytes(2, "little") + compressed

    # Convert to binary
    binary = "".join(
        [bin(single_byte)[2:].zfill(8) for single_byte in compressed_with_length]
    )

    # Pad to multiple of 5 bits
    length = len(binary)
    remainder = length % 5
    if remainder:
        binary += "0" * (5 - remainder)
        length += 5 - remainder

    # Encode to Base32Hex
    subst = "0123456789ABCDEFGHIJKLMNOPQRSTUV"
    return "".join(
        [subst[int(binary[5 * i : 5 * i + 5], 2)] for i in range(length // 5)]
    )


def decode_from_qr(encoded: str) -> tuple[bytes, str]:
    subst = "0123456789ABCDEFGHIJKLMNOPQRSTUV"
    subst_map = {c: i for i, c in enumerate(subst)}

    try:
        binary = "".join([bin(subst_map[c])[2:].zfill(5) for c in encoded])
    except KeyError:
        raise DecodingError("Invalid character in encoded data.")

    padded_length = len(binary)

    # Convert binary to bytes
    byte_array = bytearray()
    for i in range(0, padded_length, 8):
        byte_str = binary[i : i + 8]
        if len(byte_str) == 8:
            byte_array.append(int(byte_str, 2))

    if len(byte_array) < 4:
        raise DecodingError("Encoded data is too short, expected at least 4 bytes.")

    # Extract header, length, and data
    header = byte_array[:2]
    data_length = int.from_bytes(byte_array[2:4], "little")
    compressed_data = bytes(byte_array[4:])

    # Decompress
    decompressor = lzma.LZMADecompressor(
        format=lzma.FORMAT_RAW,
        filters=[
            {
                "id": lzma.FILTER_LZMA1,
                "lc": 3,
                "lp": 0,
                "pb": 2,
                "dict_size": 128 * 1024,
            }
        ],
    )

    decompressed = decompressor.decompress(compressed_data)
    if len(decompressed) != data_length:
        raise DecodingError(
            f"Decompressed data is too short, expected {data_length} bytes, got {len(compressed_data)}."
        )

    # Verify checksum
    if len(decompressed) < 4:
        raise DecodingError("Decompressed data is missing checksum.")

    checksum = int.from_bytes(decompressed[:4], "little")
    data_bytes = decompressed[4:]

    if binascii.crc32(data_bytes) != checksum:
        raise DecodingError("Decompressed data checksum is invalid.")

    # Covnert back to string
    data = data_bytes.decode("utf-8")
    return bytes(header), data


class Encodeable(Serializable):
    BY_SQUARE_TYPE = 15
    VERSION = 15
    DOCUMENT_TYPE = 15

    @classmethod
    def header(cls) -> bytes:
        header = 0
        header |= cls.BY_SQUARE_TYPE << 4 * 3
        header |= cls.VERSION << 4 * 2
        header |= cls.DOCUMENT_TYPE << 4

        return header.to_bytes(length=2, byteorder="big")

    def encode(self) -> str:
        data = "\t".join(self.to_square())
        return encode_for_qr(self.header(), data)

    @classmethod
    def decode(cls, encoded: str) -> Self:
        header, data = decode_from_qr(encoded)

        if header != cls.header():
            raise DecodingError("Invalid data header.")

        return cls.from_square(SquareReader(data.split("\t")))


def decode_universal(encoded: str) -> Encodeable:
    """Decode by-square data by inspecting the header and selecting the right class."""
    from by_square.types import (
        AdvanceInvoiceQR,
        CreditNoteQR,
        DebitNoteQR,
        InvoiceQR,
        PayQR,
        ProformaInvoiceQR,
    )

    types = [
        PayQR,
        InvoiceQR,
        ProformaInvoiceQR,
        CreditNoteQR,
        DebitNoteQR,
        AdvanceInvoiceQR,
    ]

    header, data = decode_from_qr(encoded)

    for type_ in types:
        if type_.header() == header:
            return type_.from_square(SquareReader(data.split("\t")))

    raise DecodingError(f"Unknown document type: header {header}")
