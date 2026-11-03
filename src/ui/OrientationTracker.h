#pragma once

#include <cstdint>

#include "UiTypes.h"

namespace rvf {

class OrientationTracker {
public:
    explicit OrientationTracker(UiOrientation initial = UiOrientation::Portrait);

    void reset(UiOrientation orientation, uint32_t nowMs = 0);
    bool update(float accelX, float accelY, float accelZ, uint32_t nowMs);
    void setAvailable(bool available) { _available = available; }

    bool available() const { return _available; }
    bool initialized() const { return _initialized; }
    UiOrientation orientation() const { return _orientation; }
    UiOrientation candidate() const { return _candidate; }
    float filteredX() const { return _filteredX; }
    float filteredY() const { return _filteredY; }
    bool selfie() const { return _available && _selfie; }

private:
    UiOrientation classify(float x, float y) const;
    void updateSelfie(uint32_t nowMs);

    bool _available = true;
    bool _initialized = false;
    bool _candidateActive = false;
    UiOrientation _orientation = UiOrientation::Portrait;
    UiOrientation _candidate = UiOrientation::Portrait;
    float _filteredX = 0.0f;
    float _filteredY = 0.0f;
    float _filteredZ = 0.0f;
    uint32_t _candidateSinceMs = 0;
    uint32_t _lastCommittedAtMs = 0;
    bool _selfie = false;
    bool _selfieCandidateActive = false;
    uint32_t _selfieCandidateSinceMs = 0;
};

}  // namespace rvf
