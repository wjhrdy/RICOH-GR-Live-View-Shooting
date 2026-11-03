#pragma once

#include <cstdint>

#include "UiTypes.h"

#ifndef UI_AUTO_SELFIE
#define UI_AUTO_SELFIE 0
#endif

namespace rvf {

constexpr bool kAutoSelfieEnabled = UI_AUTO_SELFIE != 0;

enum class ViewfinderMode : uint8_t { Normal, Mirrored, AutoSelfie };

inline ViewfinderMode configuredViewfinderMode(bool mirrored) {
    if (kAutoSelfieEnabled) return ViewfinderMode::AutoSelfie;
    return mirrored ? ViewfinderMode::Mirrored : ViewfinderMode::Normal;
}

inline bool viewfinderMirrored(ViewfinderMode mode, bool selfie) {
    return mode == ViewfinderMode::Mirrored || (mode == ViewfinderMode::AutoSelfie && selfie);
}

inline uint8_t viewfinderRotation(UiOrientation orientation, ViewfinderMode mode, bool selfie) {
    const uint8_t base = orientation == UiOrientation::Portrait ? 0 : 1;
    return mode == ViewfinderMode::AutoSelfie && selfie ? base + 2 : base;
}

inline UiOrientation viewfinderOrientation(ViewfinderMode mode, UiOrientation sensed) {
    // Flat on the hot shoe has no useful in-plane gravity axis; keep preview on.
    return mode == ViewfinderMode::AutoSelfie ? UiOrientation::Landscape : sensed;
}

inline const char* viewfinderLabel(ViewfinderMode mode, bool selfie) {
    if (mode == ViewfinderMode::AutoSelfie) return selfie ? "AUTO SELFIE" : "AUTO TOP";
    return mode == ViewfinderMode::Mirrored ? "MIRROR" : "NORMAL";
}

}  // namespace rvf
