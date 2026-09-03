import os
from pathlib import Path
from profile import WiiProfile
from exploits import get_exploit_chain
from payloads import get_payload, verify_payload
from storage import ensure_wii_folders

def write_payload_file(drive_path: str, filename: str, data: bytes) -> bool:
	try:
		file_path = Path(drive_path) / filename
		with open(file_path, "wb") as f:
			f.write(data)
		return True
	except Exception as e:
		print(f"Failed to write {filename}: {e}")
		return False

def setup_exploit_structure(drive_path: str, exploit_chain) -> dict[str, bool]:
	results = {}

	for required_file in exploit_chain.required_files:
		payload = get_payload(required_file.replace(".wad", "_wad").replace(".elf", "_elf").replace(".bin", "_bin"))
		if payload and verify_payload(payload):
			results[required_file] = write_payload_file(drive_path, required_file, payload)
		else:
			results[required_file] = False

	return results

def setup_homebrew_launcher(drive_path: str) -> bool:
	try:
		apps_dir = Path(drive_path) / "apps" / "homebrew_launcher"
		apps_dir.mkdir(parents=True, exist_ok=True)

		boot_dol = b"DOLSTUB_HBL_LAUNCHER"
		boot_path = apps_dir / "boot.dol"
		with open(boot_path, "wb") as f:
			f.write(boot_dol)

		meta_xml = """<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>
<app version=\"1\">
	<name>Homebrew Launcher</name>
	<coder>Authors</coder>
	<version>1.1.0</version>
	<release_date>230101120000</release_date>
	<short_description>Loads homebrew apps</short_description>
	<long_description>A tool to launch homebrew applications</long_description>
</app>"""
		meta_path = apps_dir / "meta.xml"
		with open(meta_path, "w") as f:
			f.write(meta_xml)

		return True
	except Exception as e:
		print(f"Failed to setup HBL: {e}")
		return False

def setup_backup_structure(drive_path: str) -> bool:
	try:
		backups_dir = Path(drive_path) / "backups"
		backups_dir.mkdir(parents=True, exist_ok=True)

		nand_stub = b"NANDBACKUP_STUB_v1" + (b"\x00" * 1024)
		nand_path = backups_dir / "nand.bin.stub"
		with open(nand_path, "wb") as f:
			f.write(nand_stub)

		return True
	except Exception as e:
		print(f"Failed to setup backups: {e}")
		return False

def build_usb_payload(profile: WiiProfile, drive_path: str) -> dict[str, bool]:
	results = {
		"folders": False,
		"exploit_chain": False,
		"homebrew_launcher": False,
		"backup_structure": False,
	}

	if not profile.is_safe_to_write():
		print("Error: Profile not safe to write")
		return results

	exploit_chain = get_exploit_chain(profile.console_type, profile.firmware_version)
	if not exploit_chain:
		print(f"Error: No exploit chain for {profile.console_type} {profile.firmware_version}")
		return results

	results["folders"] = ensure_wii_folders(drive_path)

	if results["folders"]:
		exploit_results = setup_exploit_structure(drive_path, exploit_chain)
		results["exploit_chain"] = all(exploit_results.values())

		results["homebrew_launcher"] = setup_homebrew_launcher(drive_path)
		results["backup_structure"] = setup_backup_structure(drive_path)

	return results
