# Install the auto-selfie firmware

This firmware is for **M5Stack StickS3 (ESP32-S3, 8 MB Flash)**. It always boots
with auto-selfie enabled: face-up is unmirrored; hinging toward the subject mirrors
the preview and rotates the display 180°. Button B single-click cannot disable it.

## Download

Download **ricoh-auto-selfie-merged.bin** from
[this fork's latest release](https://github.com/wjhrdy/RICOH-GR-Live-View-Shooting/releases/latest).
Do not install the upstream M5Burner community image when you want this feature.

Before a change is merged, open its successful **PlatformIO CI** run under
[Actions](https://github.com/wjhrdy/RICOH-GR-Live-View-Shooting/actions/workflows/platformio.yml),
download the **auto-selfie-m5stack-sticks3** artifact, and unzip it. GitHub requires
sign-in for Actions artifact downloads. The release download does not require sign-in.

Use the universal `m5stack-sticks3` build unless you specifically want a
single-camera-family build. `build-info.json` records the source commit and confirms
`auto_selfie: true`; `SHA256SUMS` contains the file checksums.

## Install in your browser

1. Use desktop **Chrome or Edge** and a USB-C **data** cable. Close serial monitors.
2. Open [Espressif's ESP Tool](https://espressif.github.io/esptool-js/).
3. In **Program**, connect and select the StickS3 **USB JTAG/serial debug unit**.
4. Choose `ricoh-auto-selfie-merged.bin` and set **Flash Address** to **0x0**.
5. Set **Flash Mode: DIO**, **Flash Frequency: 80 MHz**, **Flash Size: 8 MB**.
   Leave **Erase all** unchecked. Start programming and wait for success.
6. Reset or power-cycle the StickS3. Select your camera family with Button B and
   confirm with Button A, then complete pairing. The preview shows `AUTO TOP` when
   flat and `AUTO SELFIE` when raised toward the subject.

The combined image includes the bootloader, partition table, `boot_app0`, and app.
**Installing it replaces settings and camera pairing** because its padding spans
the NVS region. You will need to pair again. Do not upload `firmware.bin` at `0x0`.

For an existing installation with the same partition layout, advanced users can
upload only `firmware.bin` at **0x10000**, leaving **Erase all** unchecked to preserve
settings and pairing.

## Build and install from source

`platformio.ini` enables `-DUI_AUTO_SELFIE=1` for all firmware environments.

```sh
pio run -e m5stack-sticks3 -t upload
```

To build the downloadable package without connecting hardware:

```sh
pio run -e m5stack-sticks3 -t package
```

Files are written to `dist/m5stack-sticks3/`. Packaging fails if auto-selfie is
disabled or if any required image is missing or misplaced in the combined binary.
Normal local builds still support `UI_AUTO_SELFIE=0` for manual mirroring.

## Maintainers

PR builds attach installation packages for all four firmware environments. A push
or merge to this fork's `main` branch also runs **Firmware Release**, tests the code,
and publishes a release named `auto-selfie-<commit>` with the universal firmware.
Its successful publication updates the **latest release** download link above.
The first release becomes available after this workflow change is merged.

Version tags (`v*`) and **Run workflow** with a version tag remain supported.
The release package uses the same checked `package` target as PR builds.
