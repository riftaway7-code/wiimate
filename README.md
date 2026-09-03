# WiiMate

Automated homebrew installation for Wii, Wii Mini, and WiiU consoles.

**Status:** v1.0 Ready for Testing | **License:** MIT | **Community:** r/WiiHacks

## Quick Start

### 1. Download & Setup

```bash
git clone https://github.com/riftaway7-code/wiimate.git
cd wiimate
```

### 2. Choose Your Path

**Option A: Automatic (Original Wii 4.3)**
```bash
python auto_setup.py D:
```
Done in ~2 seconds. No prompts.

**Option B: Interactive (Any Console/Firmware)**
```bash
python interactive_setup.py
```
Step-by-step wizard. Select your console and firmware version.

### 3. Plug Into Your Console

- Insert USB drive into your Wii/WiiU
- Follow the setup guide that appears
- **IMPORTANT: Backup your NAND immediately after installation**

## Supported Consoles & Firmware

| Console | Firmware | Exploit | Notes |
|---------|----------|---------|-------|
| **Original Wii** | 4.3, 4.2 | Letterbomb | Mail Channel required |
| **Original Wii** | 4.1, 3.4 | Twilight Hack | Twilight Princess save required |
| **Wii Mini** | 4.3 | Letterbomb | ⚠️ Permanent installation (no BootMii) |
| **WiiU** | 5.5, 5.4 | Haxchi | DS VC title required |
| **WiiU** | 5.3 | Browser Exploit | IOSU-based |

**Total: 8 supported configurations**

## What's on Your USB

After running setup, you get:
- **boot.elf** - BootMii executable
- **ios249.wad, ios250.wad** - IOS patches
- **apps/homebrew_launcher** - Pre-configured Homebrew Channel
- **SETUP_GUIDE.md** - Detailed step-by-step instructions
- **Configuration tools** - Switch between console types

## Tools

```bash
# Verify USB is properly set up
python verify.py D:

# Switch to a different console/firmware
python config.py list
python config.py switch RVL-201 4.3

# Run full test suite
python test_e2e.py
```

## Setup Instructions by Console

### Original Wii 4.3 (Letterbomb)

1. Ensure Mail Channel is installed (Settings > Wii Message Board)
2. Plug USB into Port 2 (lower USB port)
3. Power ON your Wii
4. Go to Message Board → Check Mail
5. You should see a red "Letterbomb"
6. Boot.elf will load automatically
7. Follow BootMii installer on screen
8. **Backup your NAND** (critical!)

### Original Wii 4.1 / 3.4 (Twilight Hack)

1. Ensure Twilight Princess is inserted
2. Exploit save file should be on USB
3. Launch Twilight Princess
4. Navigate to your save - exploit triggers automatically
5. Follow BootMii installer
6. **Backup your NAND**

### Wii Mini 4.3 (Letterbomb)

1. Mail Channel must be installed
2. Plug USB into USB port
3. Same process as Original Wii 4.3
4. ⚠️ **No BootMii backup support - installation is permanent**

### WiiU 5.5 / 5.4 (Haxchi)

1. Must have DS Virtual Console title installed
2. Run Haxchi installer from Homebrew App Store
3. Select your DS VC title
4. Inject exploit
5. Launch DS VC title from WiiU Menu
6. CFW loads automatically

### WiiU 5.3 (Browser Exploit)

1. Navigate to Homebrew App Store via internet
2. Use browser exploit to load installer
3. Install and run Homebrew Launcher
4. CFW loads on next boot

## Features

✓ **Multi-console support** - One USB, any console  
✓ **Autonomous mode** - No prompts, instant setup  
✓ **Interactive mode** - Guided console selection  
✓ **Config manager** - Switch consoles on same USB  
✓ **Verification tools** - Check USB integrity  
✓ **Full test suite** - All tests passing  
✓ **Comprehensive guides** - Step-by-step instructions

## Test Results

```
✓ Exploit Chains        (8/8 valid)
✓ Profile Creation      (4/4 success)
✓ Payload Generation    (3/3 valid)
✓ Setup Guide Gen       (4/4 success)
✓ Full Build Process    (complete)
```

## Architecture

**Core Modules (~1,500 lines):**
- `exploits.py` - Exploit chain matrix (8 configurations)
- `profile.py` - Console profile management
- `storage.py` - USB detection & file handling
- `builder.py` - Payload preparation
- `payloads.py` - Exploit file management
- `steps.py` - Setup instruction generation
- `wiimate.py` - Main entry point

**Tools:**
- `auto_setup.py` - Automatic Original Wii 4.3
- `interactive_setup.py` - Guided setup wizard
- `config.py` - Configuration manager
- `verify.py` - USB integrity check
- `test_e2e.py` - Full test suite

## Important Safety Notes

⚠️ **CRITICAL BEFORE YOU START**
- Read the setup guide for YOUR specific console
- Keep your console powered throughout the entire process
- Do NOT unplug USB during installation
- **Back up your NAND immediately after installation** (this is your console in a file)
- Keep your original games if you used them for exploits

⚠️ **PERMANENT CHANGES**
- Installing custom firmware modifies your console
- Wii Mini has NO backup support - it's permanent
- If something goes wrong, you may need your NAND backup to recover
- Some features (like disc reading) may be affected

## Troubleshooting

**Letterbomb not showing up?**
- Verify Mail Channel is installed
- Check your Wii's MAC address
- Try reinstalling Mail Channel from System Menu

**boot.elf not launching?**
- Make sure USB is in Port 2 (not Port 1)
- Try launching from System Settings → Internet Settings
- May need multiple attempts on some consoles

**Installation frozen?**
- Don't power off - wait 5+ minutes
- Some steps take time
- If frozen for >30 minutes, power off and try again

## Known Limitations

- Currently uses payload stubs for testing
- Real exploit files required for production deployment
- Tested on Windows (code is cross-platform Python)

## Contributing

Want to help? Great!
- Test on actual hardware (all 8 configs)
- Real payload file integration
- Additional console support
- Documentation improvements

## Community

- **r/WiiHacks** - Main community
- **wii.guide** - Installation guides
- **GBATemp** - Technical discussion

## Credits

Built using research from the Wii community:
- Letterbomb & Twilight Hack developers
- BootMii/BootEmu9 team
- wii.guide contributors
- r/WiiHacks community

## License

MIT License - See LICENSE file

---

**Questions?** Check SETUP_GUIDE.md or ask r/WiiHacks

**Ready to test?** Start with `python interactive_setup.py` 🎮
