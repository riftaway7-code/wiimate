#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from profile import WiiProfile
from builder import build_usb_payload
from storage import ensure_wii_folders
from steps import render_setup_guide
from exploits import get_exploit_chain

def setup_wiimate_usb_auto(drive_path: str = "D:\\"):
	"""Auto-setup WiiMate USB without prompts"""

	print("\n" + "="*60)
	print("WiiMate - Auto Setup Mode")
	print("="*60 + "\n")

	print(f"Target drive: {drive_path}")

	profile = WiiProfile(
		console_type="RVL",
		firmware_version="4.3",
		region="NTSC",
		mac_address="",
	)

	print(f"Profile: {profile.get_display_name()} (Firmware {profile.firmware_version})")
	print("Exploit: Letterbomb")

	print("\nBuilding homebrew USB...")
	print("-"*60)

	build_results = build_usb_payload(profile, drive_path)

	for step, success in build_results.items():
		status = "✓" if success else "❌"
		print(f"  {status} {step}")

	if not all(build_results.values()):
		print("\n❌ Build failed!")
		return False

	print("\n" + "="*60)
	print("✓ USB Setup Complete!")
	print("="*60)
	print(render_setup_guide(profile))

	return True

if __name__ == "__main__":
	drive = sys.argv[1] if len(sys.argv) > 1 else "D:\\"
	success = setup_wiimate_usb_auto(drive)
	sys.exit(0 if success else 1)
