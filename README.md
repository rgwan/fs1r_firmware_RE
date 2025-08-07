FS1R Reverse engineering
=========================
This repository contains YAMAHA FS1R's rom loader image, and some ghidra databases to help you emulate, or repair, even make an FS1R from scratch.

Folder <dmps> contains dumps of YAMAHA FS1R's firmware.

Folder <fs1r_gdr> contains ghidra databases.

Folder <pics> contains useful photos and screenshots.


About repairing
------------------------
When you want to replace the CPU(HD64F7044F) of FS1R, please flash it at least with <fs1r_loader.bin>, I suggest to flash it with <fs1r_sh7044_flash_1.20_256k.bin>.

Note: <fs1r_sh7044_flash_1.20_256k.bin> have to use with <Yamaha FS1R v1.20 EPROM Firmware.bin> flashed in external Flash/EPROM(IC4) together, otherwise the synthesizer may not boot.

The suggested IC4 replacement chip is MX29F1615 NOR flash in DIP-42 package, it won't need UV-light to erase and can be easily programmed by XGecu T48 programmer.


Author
-----------------
Zhiyuan Wan, 2025/8/7