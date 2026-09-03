from pathlib import Path
from typing import Optional
import base64

PAYLOAD_STUBS = {
	"boot_elf": b"ELFSTUB_BOOTMII_v1",
	"ios249_wad": b"WADSTUB_IOS249_v4",
	"ios250_wad": b"WADSTUB_IOS250_v4",
	"cios249_wad": b"WADSTUB_CIOS249_v4",
	"cios250_wad": b"WADSTUB_CIOS250_v4",
	"haxchi_elf": b"ELFSTUB_HAXCHI_v2",
	"exploit_bin": b"BINSTUB_IOSUEXPLOIT_v3",
}

def get_payload(payload_name: str) -> Optional[bytes]:
	return PAYLOAD_STUBS.get(payload_name)

def verify_payload(data: bytes) -> bool:
	if not data:
		return False
	if data.startswith(b"ELF"):
		return True
	if data.startswith(b"WAD"):
		return True
	if data.startswith(b"ELFSTUB_") or data.startswith(b"WADSTUB_") or data.startswith(b"BINSTUB_"):
		return True
	return len(data) > 100

def get_required_payloads(exploit_chain) -> list[str]:
	return exploit_chain.required_files if hasattr(exploit_chain, 'required_files') else []
