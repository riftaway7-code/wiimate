import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple, List
from profile import WiiProfile

def detect_wii_drives() -> List[Tuple[str, str, str]]:
	drives = []

	try:
		result = subprocess.run(
			["powershell", "-Command", 
			 "Get-Volume | Where-Object {$_.DriveType -eq 'Removable'} | Select-Object -ExpandProperty DriveLetter"],
			capture_output=True, text=True, timeout=5
		)
		for line in result.stdout.strip().split("\n"):
			drive_letter = line.strip()
			if drive_letter and len(drive_letter) == 1:
				path = f"{drive_letter}:\\"
				if os.path.exists(path):
					drives.append((path, "usb", f"Removable USB Drive {drive_letter}:"))
	except Exception:
		pass

	if not drives:
		try:
			result = subprocess.run(
				["wmic", "logicaldisk", "get", "name"],
				capture_output=True, text=True, timeout=5
			)
			for line in result.stdout.strip().split("\n")[1:]:
				line = line.strip()
				if line and line[-1] == ":":
					path = line + "\\"
					if os.path.exists(path):
						size_result = subprocess.run(
							["powershell", "-Command",
							 f"(Get-Volume -DriveLetter {line[0]}).DriveType"],
							capture_output=True, text=True, timeout=2
						)
						if "Removable" in size_result.stdout:
							drives.append((path, "usb", f"USB Drive {line}"))
		except Exception:
			pass

	return drives

def scan_nand_backup(drive_path: str) -> Optional[WiiProfile]:
	try:
		nand_path = Path(drive_path) / "nand.bin"
		if nand_path.exists():
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

def ensure_wii_folders(drive_path: str) -> bool:
	try:
		required_folders = [
			Path(drive_path) / "apps",
			Path(drive_path) / "wads",
			Path(drive_path) / "backups",
		]

		for folder in required_folders:
			folder.mkdir(parents=True, exist_ok=True)

		return True
	except Exception as e:
		print(f"Failed to create folders: {e}")
		return False

def backup_drive_structure(drive_path: str, backup_dest: str) -> bool:
	try:
		import shutil
		Path(backup_dest).mkdir(parents=True, exist_ok=True)

		for item in Path(drive_path).iterdir():
			if item.is_file():
				shutil.copy2(item, Path(backup_dest) / item.name)

		return True
	except Exception as e:
		print(f"Failed to backup: {e}")
		return False
