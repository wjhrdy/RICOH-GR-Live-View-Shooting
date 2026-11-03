"""PlatformIO `package` target: verified auto-selfie images for USB installation."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess

from SCons.Script import COMMAND_LINE_TARGETS

Import("env")

if "package" in COMMAND_LINE_TARGETS:
    definitions = [
        item[1] for item in env["CPPDEFINES"]
        if isinstance(item, (tuple, list)) and item[0] == "UI_AUTO_SELFIE"
    ]
    if len(definitions) != 1 or str(definitions[0]) != "1":
        raise RuntimeError("Published firmware requires exactly one -DUI_AUTO_SELFIE=1")


def package_firmware(source, target, env):
    root = Path(env.subst("$PROJECT_DIR"))
    output = root / "dist" / env.subst("$PIOENV")
    output.mkdir(parents=True, exist_ok=True)
    images = [(int(offset, 0), Path(env.subst(str(path))))
              for offset, path in env["FLASH_EXTRA_IMAGES"]]
    images.append((int(env.subst("$ESP32_APP_OFFSET"), 0), Path(str(source[0]))))
    images.sort()
    if [(offset, path.name) for offset, path in images] != [
        (0x0, "bootloader.bin"), (0x8000, "partitions.bin"),
        (0xE000, "boot_app0.bin"), (0x10000, "firmware.bin"),
    ]:
        raise RuntimeError("Unexpected StickS3 flash layout; review packaging before publishing")

    command = [env.subst("$PYTHONEXE"), env.subst("$UPLOADER"),
               "--chip", "esp32s3", "merge_bin", "--flash_mode", "dio",
               "--flash_freq", "80m", "--flash_size", "8MB",
               "-o", str(output / "ricoh-auto-selfie-merged.bin")]
    for offset, path in images:
        shutil.copyfile(path, output / path.name)
        command.extend([hex(offset), str(path)])
    subprocess.run(command, check=True)

    merged = (output / "ricoh-auto-selfie-merged.bin").read_bytes()
    if merged[:1] != b"\xe9" or merged[2:4] != b"\x02\x3f" or len(merged) > 8 * 1024 * 1024:
        raise RuntimeError("Merged image does not have the expected ESP DIO/80MHz/8MB header")
    # esptool may patch the bootloader header and digest; other segments must match byte-for-byte.
    for offset, path in images[1:]:
        data = path.read_bytes()
        if merged[offset:offset + len(data)] != data:
            raise RuntimeError(f"Merged image is missing or corrupt at {hex(offset)}: {path.name}")

    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    info = {"commit": commit, "environment": env.subst("$PIOENV"),
            "board": "M5Stack StickS3", "auto_selfie": True,
            "flash_mode": "dio", "flash_frequency": "80m", "flash_size": "8MB",
            "merged_offset": "0x0",
            "images": [{"offset": hex(offset), "file": path.name} for offset, path in images]}
    (output / "build-info.json").write_text(json.dumps(info, indent=2) + "\n")
    shutil.copyfile(root / "docs" / "install-auto-selfie.md", output / "INSTALL.md")
    names = [path.name for _, path in images] + [
        "ricoh-auto-selfie-merged.bin", "build-info.json", "INSTALL.md"]
    checksums = [f"{hashlib.sha256((output / name).read_bytes()).hexdigest()}  {name}\n"
                 for name in names]
    (output / "SHA256SUMS").write_text("".join(checksums))
    print(f"Auto-selfie firmware verified and packaged in {output}")


env.AddCustomTarget(
    name="package",
    dependencies="$BUILD_DIR/${PROGNAME}.bin",
    actions=env.VerboseAction(package_firmware, "Packaging auto-selfie firmware"),
    title="Package auto-selfie firmware",
    description="Build and verify complete StickS3 flash images with auto-selfie enabled",
)
