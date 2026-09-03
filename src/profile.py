from dataclasses import dataclass, field
from typing import Optional

@dataclass
class WiiProfile:
	console_type: str
	firmware_version: str
	region: str
	mac_address: str
	nand_backup: Optional[str] = None
	region_code: Optional[str] = None

	def is_safe_to_write(self) -> bool:
		return bool(self.console_type and self.firmware_version)

	def get_display_name(self) -> str:
		console_names = {
			"RVL": "Original Wii",
			"RVL-201": "Wii Mini",
			"RVL-UPE": "WiiU",
		}
		return console_names.get(self.console_type, self.console_type)

def detect_profile() -> Optional[WiiProfile]:
	try:
		profile = WiiProfile(
			console_type="RVL",
			firmware_version="4.3",
			region="NTSC",
			mac_address="",
		)
		return profile
	except Exception:
		pass

	return None
