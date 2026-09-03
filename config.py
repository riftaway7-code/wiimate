#!/usr/bin/env python3
"""
WiiMate Configuration Manager
Allows switching between different console configurations on the same USB
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from profile import WiiProfile
from exploits import get_exploit_chain, get_supported_consoles, get_supported_firmware
from builder import build_usb_payload

class ConfigManager:
	def __init__(self, drive_path: str = "D:\\"):
		self.drive_path = Path(drive_path)
		self.config_file = self.drive_path / "wiimate" / "config.json"

	def save_config(self, profile: WiiProfile) -> bool:
		"""Save active configuration to config.json"""
		try:
			self.config_file.parent.mkdir(parents=True, exist_ok=True)

			config = {
				"active": {
					"console_type": profile.console_type,
					"firmware_version": profile.firmware_version,
					"region": profile.region,
					"timestamp": datetime.now().isoformat(),
				},
				"available_configs": {
					"RVL_4.3": "Original Wii 4.3 (Letterbomb)",
					"RVL_4.2": "Original Wii 4.2 (Letterbomb)",
					"RVL_4.1": "Original Wii 4.1 (Twilight Hack)",
					"RVL-201_4.3": "Wii Mini 4.3 (Letterbomb)",
					"RVL-UPE_5.5": "WiiU 5.5 (Haxchi)",
					"RVL-UPE_5.4": "WiiU 5.4 (Haxchi)",
					"RVL-UPE_5.3": "WiiU 5.3 (Browser)",
				}
			}

			with open(self.config_file, "w") as f:
				json.dump(config, f, indent=2)

			return True
		except Exception as e:
			print(f"Failed to save config: {e}")
			return False

	def load_config(self) -> dict:
		"""Load active configuration"""
		try:
			if self.config_file.exists():
				with open(self.config_file, "r") as f:
					return json.load(f)
		except Exception:
			pass

		return None

	def list_configs(self):
		"""List all available configurations"""
		config = self.load_config()
		if not config:
			return

		print("\nAvailable configurations:")
		for config_key, desc in config.get("available_configs", {}).items():
			console, fw = config_key.split("_", 1)
			print(f"  {config_key:<20} {desc}")

		active = config.get("active", {})
		print(f"\nActive: {active.get("console_type")} {active.get("firmware_version")}")
		print(f"Last updated: {active.get("timestamp", "Unknown")}")

	def switch_config(self, console_type: str, firmware_version: str) -> bool:
		"""Switch to a different configuration"""
		print(f"\nSwitching to {console_type} {firmware_version}...")

		profile = WiiProfile(
			console_type=console_type,
			firmware_version=firmware_version,
			region="",
			mac_address="",
		)

		if not build_usb_payload(profile, str(self.drive_path)):
			print("❌ Failed to build payload")
			return False

		if not self.save_config(profile):
			print("⚠ Payload built but config not saved")
			return False

		print(f"✓ Switched to {profile.get_display_name()} {firmware_version}")
		return True

def main():
	mgr = ConfigManager("D:\\")

	if len(sys.argv) < 2:
		mgr.list_configs()
		return 0

	if sys.argv[1] == "list":
		mgr.list_configs()
		return 0

	if sys.argv[1] == "switch" and len(sys.argv) >= 4:
		console = sys.argv[2]
		firmware = sys.argv[3]
		success = mgr.switch_config(console, firmware)
		return 0 if success else 1

	print("Usage:")
	print("  config.py list                    - List all configurations")
	print("  config.py switch CONSOLE FIRMWARE - Switch configuration")
	print("\nExample: config.py switch RVL 4.3")
	return 1

if __name__ == "__main__":
	sys.exit(main())
