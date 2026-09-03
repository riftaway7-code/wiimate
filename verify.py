#!/usr/bin/env python3
"""
WiiMate USB Verification Tool
Checks USB structure and file integrity
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from exploits import get_supported_consoles, get_supported_firmware

REQUIRED_FILES = {
	"boot.elf": "BootMii executable",
	"ios249.wad": "IOS patch file",
	"ios250.wad": "IOS patch file",
}

REQUIRED_DIRS = {
	"apps": "Homebrew applications",
	"apps/homebrew_launcher": "HBC launcher",
	"wads": "Additional WAD files",
	"backups": "Backup destination",
}

def verify_usb_structure(drive_path: str = "D:\\") -> bool:
	"""Verify USB has all required files and structure"""
	print("\n" + "="*60)
	print("WiiMate USB Verification")
	print("="*60)
	print(f"\nChecking drive: {drive_path}")

	all_good = True
	root = Path(drive_path)

	print("\nRequired directories:")
	for dir_path, desc in REQUIRED_DIRS.items():
		full_path = root / dir_path
		status = "✓" if full_path.exists() and full_path.is_dir() else "❌"
		print(f"  {status} {dir_path:<30} ({desc})")
		if not full_path.exists():
			all_good = False

	print("\nRequired files:")
	for filename, desc in REQUIRED_FILES.items():
		full_path = root / filename
		if full_path.exists():
			size = full_path.stat().st_size
			print(f"  ✓ {filename:<20} {size:>8} bytes  ({desc})")
		else:
			print(f"  ❌ {filename:<20} MISSING  ({desc})")
			all_good = False

	print("\nOptional files:")
	optional_files = [
		"README.md",
		"INSTALL_LOG.txt",
	]
	for filename in optional_files:
		full_path = root / filename
		status = "✓" if full_path.exists() else "○"
		print(f"  {status} {filename}")

	print("\n" + "-"*60)
	print("Homebrew Apps:")
	apps_dir = root / "apps"
	if apps_dir.exists():
		for app_dir in apps_dir.iterdir():
			if app_dir.is_dir():
				boot_dol = app_dir / "boot.dol"
				meta_xml = app_dir / "meta.xml"
				status = "✓" if (boot_dol.exists() and meta_xml.exists()) else "⚠"
				print(f"  {status} {app_dir.name}")

	print("\n" + "-"*60)
	print("Supported Configurations:")
	consoles = get_supported_consoles()
	for console in consoles:
		fw_versions = get_supported_firmware(console)
		console_names = {"RVL": "Original Wii", "RVL-201": "Wii Mini", "RVL-UPE": "WiiU"}
		name = console_names.get(console, console)
		print(f"  • {name}: {', '.join(fw_versions)}")

	print("\n" + "="*60)
	if all_good:
		print("✓ USB is properly configured!")
	else:
		print("⚠ USB has some missing files/directories")
	print("="*60 + "\n")

	return all_good

if __name__ == "__main__":
	drive = sys.argv[1] if len(sys.argv) > 1 else "D:\\"
	success = verify_usb_structure(drive)
	sys.exit(0 if success else 1)
