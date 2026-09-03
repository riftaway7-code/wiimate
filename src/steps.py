from profile import WiiProfile

def render_setup_guide(profile: WiiProfile) -> str:
	console_name = profile.get_display_name()

	if profile.console_type == "RVL":
		if profile.firmware_version == "4.3":
			guide = f"""
Setup Guide for {console_name} (Firmware {profile.firmware_version})
Using: Letterbomb Exploit

STEP 1: Prepare Console
  • Make sure your Wii is powered OFF
  • Ensure Mail Channel is installed (Settings > Wii Message Board)
  • Note your Wii's MAC address (in System Settings)

STEP 2: Insert USB Drive
  • Plug the prepared USB drive into Port 2 (lower USB port)
  • Power on your Wii

STEP 3: Trigger Letterbomb
  • Go to Message Board
  • Check Mail - you should see a red Letterbomb
  • DO NOT open it - just have it present in your inbox
  • Go back and open the Wii Settings again
  • Navigate through normally until boot.elf loads
  • Follow the BootMii installer prompts

STEP 4: Finalize Installation
  • After BootMii installation completes
  • Your Wii will automatically load Homebrew Launcher
  • Install additional apps via the HBC as desired

⚠️  CRITICAL: Backup your NAND immediately!
"""
		elif profile.firmware_version in ["4.1", "3.4"]:
			guide = f"""
Setup Guide for {console_name} (Firmware {profile.firmware_version})
Using: Twilight Hack Exploit

STEP 1: Prepare Console & Game
  • Ensure Twilight Princess is inserted
  • Save file must exist in the game's save slot
  • Have a save game injected with the exploit (on USB)

STEP 2: Load Exploit
  • Launch Twilight Princess from Wii Menu
  • Play until the exploit triggers
  • boot.elf will load automatically

STEP 3: Install BootMii
  • Follow the BootMii installer prompts
  • Install IOS249 and IOS250

STEP 4: Finalize
  • Homebrew Launcher will be ready
  • Backup NAND immediately

STEP 5: Restore Save (Optional)
  • Use the original save file if desired
  • Or keep the hacked save installed
"""
	elif profile.console_type == "RVL-201":
		guide = f"""
Setup Guide for Wii Mini (Firmware {profile.firmware_version})
Using: Letterbomb Exploit

⚠️  NOTE: Wii Mini has NO BootMii support
  • Backup functionality is limited
  • Installation is PERMANENT - verify drive is clean first

STEP 1: Prepare
  • Ensure Mail Channel is present
  • Plug USB drive into USB port

STEP 2: Trigger
  • Go to Message Board
  • Check Mail for red Letterbomb
  • Boot into setup via Settings

STEP 3: Install cIOS
  • cIOS249 and cIOS250 will be installed
  • These replace system IOS versions
  • Allows homebrew to run

⚠️  CRITICAL: No way to restore if something goes wrong!
"""
	elif profile.console_type == "RVL-UPE":
		guide = f"""
Setup Guide for WiiU (Firmware {profile.firmware_version})

STEP 1: Check Hacked DS VC Title
  • You need a DS Virtual Console title already installed
  • If you have one, Haxchi can be injected into it
  • If not, browser exploit will be used instead

STEP 2: Inject Haxchi (if DS VC available)
  • Run the Haxchi installer
  • Select your DS VC title
  • Inject the exploit

STEP 3: Boot CFW
  • Launch the DS VC title from WiiU Menu
  • CFW will load automatically
  • Homebrew Launcher will be available

STEP 4: Finalize
  • Install Haxchi permanently if desired
  • Remove from disc if using browser exploit

⚠️  WARNING: WiiU CFW installation can't be undone!
"""
	else:
		guide = f"""
Setup Guide for {console_name} (Firmware {profile.firmware_version})
  • Consult r/WiiHacks for detailed instructions
  • USB drive has been prepared with required files
"""

	return guide
