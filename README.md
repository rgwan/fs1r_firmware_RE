# FS1R Reverse engineering

This repository contains YAMAHA FS1R's rom loader image, and some ghidra databases to help you emulate, or repair, even make an FS1R from scratch.

* Folder `dmps` contains dumps of YAMAHA FS1R's firmware.

* Folder `fs1r_gdr` contains ghidra databases.

* Folder `pics` contains useful photos and screenshots.

* Folder `la` contains waveforms captured by logical analyzer.

## About the boot process and firmware upgrading procedure

The CPU(SH7044, IC1)'s boot mode configuration is 4'b1010, which means it runs on flash mode, and external bus is mapped normally. The flash is constructed by lots of EBs (erase block), but I'm not going to dig into the detail here.

### Detailed structure of FS1R's firmware scheme

* `External EPROM`, mapped at `0x200000-0x3fffff` (2MB).

* `Internal flash`, mapped at `0x0-0x3ffff` (256KB).

* `Loader` stays in flash, at `0x0000-0x7fff` (32KB, the first EB), and other spaces being used by some parts of firmware. I believe that Yamaha use internal flash to store timing sensitive programs, and other program stays in slower EPROM, and be XIP'd by CPU. 


### Boot and upgrade procedure

When the system starts, the CPU fetchs the reset vector and stack top from address 0 and 4, which is located in the flash.

Then CPU executes `loader program`, this program will do RAM clearing, some bus / peripheral configuration and eventually check whether or not the flash and external EPROM's firmware version are the same. If it is the same, then the system boots into normal mode. 

If it's not the same, then the `loader` jumps to `upgrade program` which located at the EPROM, erase all EBs except EB0 (which `loader` stays), then copy the codes from external EPROM (bus address: 0x3c8000-0x3fffff, file offset: 0x1c8000-0x1fffff) to flash (address: 0x8000 - 0x1fffff), finally it will clears the NVRAM to make upgrade procedure complete.

### Upgrade notes

If you want to upgrade FS1R's firmware by changing external EPROM, please short the JP1 jumper near to the CPU at the first boot (This jumper actually controls the flash hardware write protect pin of the CPU, when it is open, the flash controller inside the CPU will reject any operation to flash), otherwise it won't boot (maybe stuck at "FLASH ROM INITIALIZE" screen) because the internal flash is write-protected. If you got everything right, `FLASH ROM ??%` will shows up on the screen. 

When your synthesizer first boot up after changed EPROM. **DO NOT POWER OFF THE SYNTHESIZER NOW, OTHERWISE THE DATA IN FLASH MAY LOSE!** 

If the `loader program` being mis-erased, you have to desolder it from the board (Typically that in-system-programming protocol will work without desoldering, but SH7044 ISP protocol use SCI1, which is configured other function in FS1R, to communicate with HOST. So you have to desolder it), reprogram it with `Z-FTAT`, `openh8writer` or *some old, bulky and expensive programmers*, considering the quality of Yamaha's PCB is not that good, that's really troublesome. I have some spare pre-programmed CPU parts of FS1R but I wish you'll never need it.

When the screen backs to normal, the upgrade procedure is completed, you must to remove the short wire from the JP1 jumper. Normally, the FS1R will never erase or write to flash, because it's setting is stored in on-board NVRAM, remove the jumper will keep it's internal flash safe. 


## About repairment

When you want to replace the CPU(HD64F7044F) of FS1R, please flash it at least with `fs1r_loader.bin`, I suggest to flash it with `fs1r_sh7044_flash_1.20_256k.bin`.

Note: `fs1r_sh7044_flash_1.20_256k.bin` have to use with `Yamaha FS1R v1.20 EPROM Firmware.bin` flashed in external Flash/EPROM(IC4) together, otherwise the synthesizer may not boot.

The suggested IC4 replacement chip is MX29F1615 NOR flash in DIP-42 package, it won't need UV-light to erase and can be easily programmed by XGecu T48 programmer.


## Author

Zhiyuan Wan <h@iloli.bid>, 2025/8/7
