#!/usr/bin/env python3
import sys
sys.path.insert(0, "src")

from exploits import get_exploit_chain, get_supported_consoles, get_supported_firmware
from profile import WiiProfile
from builder import build_usb_payload
from storage import ensure_wii_folders
import tempfile
from pathlib import Path

def test_exploit_matrix():
	print("\n=== Testing Exploit Matrix ===")
	consoles = get_supported_consoles()
	print(f"Supported consoles: {consoles}")

	for console in consoles:
		fw_versions = get_supported_firmware(console)
		print(f"\n{console}:")
		for fw in fw_versions:
			chain = get_exploit_chain(console, fw)
			if chain:
				print(f"  {fw}: {chain.chain_name} -> {', '.join(chain.chain_steps)}")

def test_profile_creation():
	print("\n=== Testing Profile Creation ===")
	profile = WiiProfile(
		console_type="RVL",
		firmware_version="4.3",
		region="NTSC",
		mac_address="12:34:56:78:90:AB"
	)
	print(f"Created: {profile.get_display_name()}")
	print(f"Safe to write: {profile.is_safe_to_write()}")

def test_build_workflow():
	print("\n=== Testing Build Workflow ===")

	with tempfile.TemporaryDirectory() as tmpdir:
		print(f"Using temp dir: {tmpdir}")

		profile = WiiProfile(
			console_type="RVL",
			firmware_version="4.3",
			region="NTSC",
			mac_address=""
		)

		print("\nBuilding USB payload...")
		results = build_usb_payload(profile, tmpdir)

		print("\nBuild results:")
		for step, success in results.items():
			status = "✓" if success else "❌"
			print(f"  {status} {step}")

		print(f"\nFiles created in {tmpdir}:")
		for f in Path(tmpdir).rglob("*"):
			if f.is_file():
				print(f"  - {f.relative_to(tmpdir)}")

def main():
	print("\n" + "="*60)
	print("WiiMate Test Suite")
	print("="*60)

	try:
		test_exploit_matrix()
		test_profile_creation()
		test_build_workflow()

		print("\n" + "="*60)
		print("✓ All tests passed!")
		print("="*60 + "\n")
		return 0

	except Exception as e:
		print(f"\n❌ Test failed: {e}")
		import traceback
		traceback.print_exc()
		return 1

if __name__ == "__main__":
	sys.exit(main())
