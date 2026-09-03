#!/usr/bin/env python3
"""
WiiMate Interactive Configuration Tool
Allows users to select their console and firmware, then builds the optimal USB
"""

import sys
import os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from profile import WiiProfile
from builder import build_usb_payload
from exploits import get_exploit_chain, get_supported_consoles, get_supported_firmware
from steps import render_setup_guide

def log_installation(drive_path: str, profile: WiiProfile, results: dict):
	"""Log the installation to INSTALL_LOG.txt"""
	try:
		log_path = Path(drive_path) / "INSTALL_LOG.txt"
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		log_content = f"""WiiMate Installation Log
=========================
Timestamp: {timestamp}
Drive: {drive_path}

Console: {profile.get_display_name()}
Firmware: {profile.firmware_version}
Region: {profile.region or "Unknown"}

Exploit Chain:
"""
		chain = get_exploit_chain(profile.console_type, profile.firmware_version)
		if chain:
			log_content += f"  Name: {chain.chain_name}\n"
			log_content += f"  Steps: {', '.join(chain.chain_steps)}\n"

		log_content += "\nBuild Results:\n"
		for step, success in results.items():
			status = "SUCCESS" if success else "FAILED"
			log_content += f"  {step}: {status}\n"

		log_content += "\nSetup Instructions:\n"
		log_content += render_setup_guide(profile)

		with open(log_path, "w") as f:
			f.write(log_content)

		return True
	except Exception as e:
		print(f"Warning: Could not write log: {e}")
		return False

def interactive_console_selection() -> WiiProfile:
	"""Prompt user to select console and firmware"""
	print("\n" + "="*60)
	print("WiiMate Console Selection")
	print("="*60)

	consoles_map = {
		"1": ("RVL", "Original Wii"),
		"2": ("RVL-201", "Wii Mini"),
		"3": ("RVL-UPE", "WiiU"),
	}

	print("\nSelect your console:")
	for key, (_, name) in consoles_map.items():
		print(f"  {key}. {name}")
	print("  4. Exit")

	choice = input("\nEnter choice (1-4): ").strip()

	if choice == "4":
		print("Exiting.")
		sys.exit(0)

	if choice not in consoles_map:
		print("Invalid choice.")
		sys.exit(1)

	console_type, console_name = consoles_map[choice]
	print(f"\nSelected: {console_name}")

	firmware_versions = get_supported_firmware(console_type)
	print(f"\nSupported firmware versions:")
	for i, fw in enumerate(firmware_versions, 1):
		print(f"  {i}. {fw}")

	fw_choice = input("\nSelect firmware (enter number): ").strip()
	try:
		fw_index = int(fw_choice) - 1
		if 0 <= fw_index < len(firmware_versions):
			selected_fw = firmware_versions[fw_index]
		else:
			print("Invalid choice.")
			sys.exit(1)
	except ValueError:
		print("Invalid input.")
		sys.exit(1)

	profile = WiiProfile(
		console_type=console_type,
		firmware_version=selected_fw,
		region="",
		mac_address="",
	)

	return profile

def main():
	if len(sys.argv) > 1 and sys.argv[1] == "--auto":
		profile = WiiProfile(
			console_type="RVL",
			firmware_version="4.3",
			region="NTSC",
			mac_address="",
		)
		drive_path = "D:\\"
	else:
		profile = interactive_console_selection()
		drive_path = "D:\\"

	print(f"\n{'='*60}")
	print(f"Building USB for {profile.get_display_name()}")
	print(f"Firmware: {profile.firmware_version}")
	print(f"Drive: {drive_path}")
	print("="*60)

	print("\nBuilding...")
	results = build_usb_payload(profile, drive_path)

	print("\nBuild results:")
	for step, success in results.items():
		status = "✓" if success else "❌"
		print(f"  {status} {step}")

	if not all(results.values()):
		print("\n❌ Build had failures!")
		return 1

	log_installation(drive_path, profile, results)

	print("\n" + "="*60)
	print("✓ USB Configuration Complete!")
	print("="*60)
	print(render_setup_guide(profile))

	print("\nSetup guide also saved to: INSTALL_LOG.txt on USB")
	return 0

if __name__ == "__main__":
	sys.exit(main())
