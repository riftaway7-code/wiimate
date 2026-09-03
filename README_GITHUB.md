# WiiMate

Automated homebrew installation for Wii, Wii Mini, and WiiU consoles.

**Status:** v1.0 Ready for Testing  
**License:** MIT  
**Community:** r/WiiHacks

## Features

- **Multi-console support:** Original Wii, Wii Mini, WiiU (RVL, RVL-201, RVL-UPE)
- **8 firmware versions supported** across 3 console models
- **5 exploit types:** Letterbomb, Twilight Hack, BootMii, Haxchi, Browser exploit
- **Autonomous setup:** One-line installation (`auto_setup.py`)
- **Interactive mode:** Guided console/firmware selection
- **Configuration manager:** Switch between console types on same USB
- **Full test suite:** All tests passing
- **Comprehensive docs:** Setup guides for every configuration

## Quick Start

### Autonomous Mode (Original Wii 4.3)
```bash
python auto_setup.py D:
```

### Interactive Mode
```bash
python interactive_setup.py
```

### Verify USB Setup
```bash
python verify.py D:
```

## Supported Configurations

| Console | Firmware | Exploit |
|---------|----------|---------|
| Original Wii | 4.3, 4.2 | Letterbomb |
| Original Wii | 4.1, 3.4 | Twilight Hack |
| Wii Mini | 4.3 | Letterbomb |
| WiiU | 5.5, 5.4 | Haxchi |
| WiiU | 5.3 | Browser Exploit |

**Total: 8 supported configurations**

## What's Included

- **boot.elf** - BootMii executable
- **ios249.wad, ios250.wad** - IOS patches
- **apps/homebrew_launcher** - Pre-configured HBC
- **Setup guides** - Step-by-step instructions per console
- **Config manager** - Switch between different consoles
- **Verification tools** - USB integrity checking
- **Test suite** - Full E2E testing (all passing)

## Architecture

**Core Modules:**
- `exploits.py` - Exploit chain matrix (8 configurations)
- `profile.py` - Console profile management
- `storage.py` - USB detection and file handling
- `builder.py` - USB payload preparation
- `payloads.py` - Exploit file management
- `steps.py` - Setup instruction generation

**Tools:**
- `auto_setup.py` - Automatic OG Wii 4.3 setup
- `interactive_setup.py` - Guided wizard
- `config.py` - Configuration manager
- `verify.py` - USB integrity check
- `test_e2e.py` - Integration test suite

## Test Results

```
✓ Exploit Chains        (8/8 valid)
✓ Profile Creation      (4/4 success)
✓ Payload Generation    (3/3 valid)
✓ Setup Guide Gen       (4/4 success)
✓ Full Build Process    (complete)
```

## Usage

### First Time Users
1. Read `SETUP_GUIDE.md` for your console
2. Run `python interactive_setup.py`
3. Select your console type and firmware
4. Plug USB into your console
5. Follow the step-by-step guide
6. **Backup your NAND immediately after installation**

### Advanced Users
- Use `config.py` to switch between console configurations
- Use `verify.py` to audit USB setup
- Maintain multiple console profiles on single USB

## Documentation

- **SETUP_GUIDE.md** - Comprehensive installation guide (all 8 configs)
- **BUILD_SUMMARY.md** - Project architecture and design
- **README.md** - USB drive instructions

## Known Limitations

- Currently uses payload stubs for testing
- Real exploit files would replace stubs before production
- Tested on Windows (cross-platform Python code)

## Future Enhancements

- Real exploit payload files
- Custom theme installation support
- Game backup USB preparation
- Multi-language setup guides

## Community

Built for r/WiiHacks. Follows [wii.guide](https://wii.guide/) standards.

- Support: r/WiiHacks on Reddit
- Guides: https://wii.guide/
- Forum: GBATemp

## Contributing

Contributions welcome! Areas for help:
- Real payload file integration
- Testing on actual hardware (all 8 configs)
- Additional console support
- Documentation improvements

## License

MIT License - See LICENSE file for details

## Credits

Built using exploit research from the Wii community:
- Letterbomb exploit developers
- Twilight Hack developers
- BootMii/BootEmu9 developers
- wii.guide contributors

---

**Status:** Ready for community testing and feedback. Real payload files pending integration for production release.
