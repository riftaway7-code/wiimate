#!/usr/bin/env python3
import sys
import os
from pathlib import Path

from storage import detect_wii_drives, scan_nand_backup
from profile import WiiProfile, detect_profile
from exploits import get_exploit_chain, get_supported_consoles, get_supported_firmware
from builder import build_usb_payload
from steps import render_setup_guide

def print_banner():
	print("\n" + "="*60)
	print("WiiMate - Wii/WiiU Homebrew Installation")
	print("="*60 + "\n")

def main_workflow_auto():
	print_banner()
	print("Mode: Automatic Setup")
	print("-"*60)

	print("\nScanning for Wii consoles and storage...")
	wii_drives = detect_wii_drives()

	if not wii_drives:
		print("❌ No Wii consoles or USB drives detected.")
		print("Please ensure your Wii is connected or USB drive is inserted.")
		return False

	print(f"\n✓ Found {len(wii_drives)} device(s):")
	for i, (path, dev_type, info) in enumerate(wii_drives, 1):
		print(f"  {i}. {path} ({dev_type}) - {info}")

	if len(wii_drives) == 1:
		selected_path, selected_type, _ = wii_drives[0]
		print(f"\nUsing: {selected_path}")
	else:
		choice = input(f"Select device (1-{len(wii_drives)}): ").strip()
		selected_path, selected_type, _ = wii_drives[int(choice) - 1]

	profile = None
	if selected_type == "usb":
		print("\nAttempting to detect existing Wii profile from USB...")
		profile = scan_nand_backup(selected_path)

	if not profile:
		print("\nNo existing profile found. Querying Wii console...")
		print("Select your console:")
		print("  1. Original Wii (RVL)")
		print("  2. Wii Mini (RVL-201)")
		print("  3. WiiU (RVL-UPE)")
		choice = input("Enter choice (1-3): ").strip()

		console_map = {"1": "RVL", "2": "RVL-201", "3": "RVL-UPE"}
		console_type = console_map.get(choice, "RVL")

		consoles = get_supported_consoles()
		if console_type not in consoles:
			print(f"❌ Unsupported console: {console_type}")
			return False

		firmware_opts = get_supported_firmware(console_type)
		print(f"\nSupported firmware versions: {', '.join(firmware_opts)}")
		firmware = input(f"Enter firmware version: ").strip()

		if (console_type, firmware) not in get_supported_firmware(console_type):
			print(f"❌ Unsupported firmware: {firmware}")
			return False

		profile = WiiProfile(
			console_type=console_type,
			firmware_version=firmware,
			region="",
			mac_address="",
		)

	print(f"\n{'='*60}")
	print(f"Profile: {profile.console_type} on firmware {profile.firmware_version}")
	print(f"Device: {selected_path}")
	print("="*60)

	print("\nBuilding homebrew USB...")
	print("-"*60)

	build_results = build_usb_payload(profile, selected_path)

	for step, success in build_results.items():
		status = "✓" if success else "❌"
		print(f"  {status} {step}")

	if not all(build_results.values()):
		print("\n❌ Build failed. Some files could not be written.")
		return False

	print("\n" + "="*60)
	print("USB Setup Complete!")
	print("="*60)
	print(render_setup_guide(profile))

	print("\n⚠️  IMPORTANT: Keep USB powered during installation.")
	print("If anything fails, you can restore your backups.")

	return True

def main():
	print_banner()
	try:
		success = main_workflow_auto()
		return 0 if success else 1
	except KeyboardInterrupt:
		print("\n\nInterrupted by user.")
		return 1
	except Exception as e:
		print(f"\n❌ Unexpected error: {e}")
		import traceback
		traceback.print_exc()
		return 1

if __name__ == "__main__":
	sys.exit(main())
