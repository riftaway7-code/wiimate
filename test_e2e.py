#!/usr/bin/env python3
"""
WiiMate E2E Test Suite
Tests all functionality end-to-end
"""

import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from profile import WiiProfile
from exploits import get_exploit_chain, get_supported_consoles, get_supported_firmware
from builder import build_usb_payload
from storage import ensure_wii_folders
from steps import render_setup_guide
from payloads import get_payload, verify_payload

def test_all_exploit_chains():
	print("\n" + "="*60)
	print("Testing All Exploit Chains")
	print("="*60)

	consoles = get_supported_consoles()
	total = 0
	passed = 0

	for console in consoles:
		fw_versions = get_supported_firmware(console)
		for fw in fw_versions:
			total += 1
			chain = get_exploit_chain(console, fw)
			if chain:
				print(f"  ✓ {console} {fw}: {chain.chain_name}")
				passed += 1
			else:
				print(f"  ❌ {console} {fw}: No chain found")

	print(f"\nResult: {passed}/{total} chains valid")
	return passed == total

def test_all_profiles():
	print("\n" + "="*60)
	print("Testing Profile Creation")
	print("="*60)

	configs = [
		("RVL", "4.3"),
		("RVL", "4.1"),
		("RVL-201", "4.3"),
		("RVL-UPE", "5.5"),
	]

	for console, fw in configs:
		profile = WiiProfile(
			console_type=console,
			firmware_version=fw,
			region="",
			mac_address="",
		)
		print(f"  ✓ {profile.get_display_name()} {fw}")

	return True

def test_payloads():
	print("\n" + "="*60)
	print("Testing Payload Generation")
	print("="*60)

	payloads_to_test = [
		("boot_elf", "BootMii"),
		("ios249_wad", "IOS249"),
		("ios250_wad", "IOS250"),
	]

	for payload_name, desc in payloads_to_test:
		payload = get_payload(payload_name)
		if payload and verify_payload(payload):
			print(f"  ✓ {desc:<20} ({len(payload)} bytes)")
		else:
			print(f"  ❌ {desc:<20} Failed")
			return False

	return True

def test_full_build(temp_dir: str) -> bool:
	print("\n" + "="*60)
	print("Testing Full Build Process")
	print("="*60)

	profile = WiiProfile(
		console_type="RVL",
		firmware_version="4.3",
		region="NTSC",
		mac_address="",
	)

	print(f"Building for: {profile.get_display_name()}")
	results = build_usb_payload(profile, temp_dir)

	all_passed = True
	for step, success in results.items():
		status = "✓" if success else "❌"
		print(f"  {status} {step}")
		if not success:
			all_passed = False

	if all_passed:
		print("\n✓ Build completed successfully")
		print(f"Files created:")
		for f in Path(temp_dir).rglob("*"):
			if f.is_file():
				size = f.stat().st_size
				rel_path = str(f.relative_to(temp_dir))
				print(f"    - {rel_path:<30} ({size} bytes)")

	return all_passed

def test_setup_guide():
	print("\n" + "="*60)
	print("Testing Setup Guide Generation")
	print("="*60)

	configs = [
		("RVL", "4.3", "Letterbomb"),
		("RVL", "4.1", "Twilight Hack"),
		("RVL-201", "4.3", "Letterbomb"),
		("RVL-UPE", "5.5", "Haxchi"),
	]

	for console, fw, expected_exploit in configs:
		profile = WiiProfile(
			console_type=console,
			firmware_version=fw,
			region="",
			mac_address="",
		)
		guide = render_setup_guide(profile)
		if expected_exploit in guide:
			print(f"  ✓ {profile.get_display_name()} {fw}")
		else:
			print(f"  ❌ {profile.get_display_name()} {fw} (missing {expected_exploit})")
			return False

	return True

def main():
	print("\n" + "="*70)
	print("WIIMATE END-TO-END TEST SUITE")
	print("="*70)

	results = []

	results.append(("Exploit Chains", test_all_exploit_chains()))
	results.append(("Profile Creation", test_all_profiles()))
	results.append(("Payloads", test_payloads()))
	results.append(("Setup Guides", test_setup_guide()))

	with tempfile.TemporaryDirectory() as temp_dir:
		results.append(("Full Build", test_full_build(temp_dir)))

	print("\n" + "="*70)
	print("TEST SUMMARY")
	print("="*70)

	passed = 0
	for test_name, result in results:
		status = "✓ PASS" if result else "❌ FAIL"
		print(f"  {status:<10} {test_name}")
		if result:
			passed += 1

	print("\n" + "="*70)
	if passed == len(results):
		print(f"✓ ALL {len(results)} TESTS PASSED")
		print("="*70 + "\n")
		return 0
	else:
		print(f"❌ {len(results) - passed} TEST(S) FAILED")
		print("="*70 + "\n")
		return 1

if __name__ == "__main__":
	sys.exit(main())
