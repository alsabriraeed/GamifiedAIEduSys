# Teacher Controller Blueprint Guide

## Blueprint: BP_TeacherController

Controls the MetaHuman teacher's behavior, animations, lip sync, and audio playback.

---

## Components

Add these to the Blueprint:

```
[Default Scene Root]
├── [Skeletal Mesh] → MetaHuman body (from MetaHuman asset)
├── [Audio Component] → "TeacherVoice"
├── [Timeline Component] → "VisemeTimeline"
└── [Smart Board Reference] → (set in BeginPlay)
```

---

## Variables

```
MetaHumanMesh (Skeletal Mesh Component Reference)
AudioComponent (Audio Component Reference)
CurrentVisemes (Array of Viseme Structs)
CurrentActions (Array of Action Structs)
IsCurrentlySpeaking (Boolean) = false
SmartBoardRef (BP_SmartBoard Reference)
```

**Viseme Struct**:
```
VisemeStruct:
  - Time (Float)
  - VisemeName (String)
```

**Action Struct**:
```
ActionStruct:
  - Type (String): "goto_slide", "point_to", "nod", etc.
  - SlideID (Integer, optional)
  - Target (String, optional)
  - Timing (String): "before_speech", "during_speech", "after_speech"
  - AtWord (Integer, optional)
```

---

## Functions

### `SpeakAnswer(AudioBase64 String, VisemesArray Array, ActionsArray Array)`

**Description**: Main function to make teacher speak with lip sync and gestures

**Blueprint Nodes**:
```
1. [Check if Already Speaking]:
   - Branch: IsCurrentlySpeaking?
   - True → Print "Already speaking" → Return

2. [Set IsCurrentlySpeaking] = true

3. [Store Data]:
   - Set CurrentVisemes = VisemesArray
   - Set CurrentActions = ActionsArray

4. [Execute Before-Speech Actions]:
   - For Each action in ActionsArray:
     - If action.Timing == "before_speech":
       → [Call]: ExecuteAction(action)

5. [Decode Audio]:
   - Call: DecodeBase64ToSoundWave(AudioBase64)
   - Result → Sound Wave object

6. [Play Audio]:
   - AudioComponent.SetSound(Sound Wave)
   - AudioComponent.Play()

7. [Start Lip Sync]:
   - Call: StartVisemePlayback(CurrentVisemes)

8. [Start Gesture System]:
   - Call: MonitorActionsForTiming(CurrentActions)

9. [Bind to Audio Finished]:
   - AudioComponent.OnAudioFinished → [Custom Event: OnSpeechFinished]
```

---

### `DecodeBase64ToSoundWave(Base64String String) → Sound Wave`

**Description**: Convert backend's Base64 audio to Unreal Sound Wave

**Blueprint Nodes**:
```
1. [Decode Base64]:
   - Use VaRest or custom C++ function
   - Base64 String → Byte Array

2. [Create Sound Wave]:
   - Create USoundWave object at runtime
   - Set RawPCMData = Byte Array
   - Set NumChannels = 1 (mono)
   - Set SampleRate = 22050 (matches backend)
   - Set Duration = (Byte Array Size / SampleRate)

3. [Return]: Sound Wave
```

**C++ Helper** (recommended):
```cpp
// In your C++ helper class
USoundWave* UBackendAudioHelper::DecodeBase64ToSoundWave(const FString& Base64Audio)
{
    TArray<uint8> AudioData;
    FBase64::Decode(Base64Audio, AudioData);
    
    USoundWave* SoundWave = NewObject<USoundWave>();
    SoundWave->RawPCMData = AudioData;
    SoundWave->SampleRate = 22050;
    SoundWave->NumChannels = 1;
    SoundWave->Duration = (float)AudioData.Num() / 22050.0f;
    SoundWave->bLooping = false;
    
    return SoundWave;
}
```

---

### `StartVisemePlayback(VisemesArray Array)`

**Description**: Drive facial lip sync using viseme timeline

**Blueprint Nodes**:
```
1. [Create Timeline Track]:
   - Timeline Component: VisemeTimeline
   - Duration = Last viseme's time + 0.5 seconds

2. [For Each Viseme] in VisemesArray:
   - Add Key to Timeline:
     - Time = viseme.Time
     - Event = ApplyViseme(viseme.VisemeName)

3. [Timeline Settings]:
   - Play Rate = 1.0
   - Looping = false

4. [Play Timeline]:
   - VisemeTimeline.PlayFromStart()
```

---

### `ApplyViseme(VisemeName String)`

**Description**: Set facial morph target for lip sync

**MetaHuman Visemes** (built-in blend shapes):
- `sil` - Silence (mouth closed)
- `PP` - P, B, M sounds
- `FF` - F, V sounds
- `TH` - Th sounds
- `DD` - D, T sounds
- `kk` - K, G sounds
- `CH` - Ch, Sh sounds
- `SS` - S, Z sounds
- `nn` - N sounds
- `RR` - R sounds
- `aa` - Ah (open mouth)
- `E` - E, eh sounds
- `I` - I sounds
- `O` - O sounds
- `U` - Oo sounds

**Blueprint Nodes**:
```
1. [Get Face Control Rig]:
   - MetaHumanMesh → Get Anim Instance → Cast to MetaHuman Face Anim BP

2. [Reset All Visemes]:
   - Set all viseme morph targets to 0.0

3. [Apply New Viseme]:
   - Switch on String: VisemeName
     - Case "PP": Set morph "CTRL_L_mouth_phonemeBMP" = 1.0
     - Case "FF": Set morph "CTRL_L_mouth_phonemeFV" = 1.0
     - Case "aa": Set morph "CTRL_L_mouth_phonemeAA" = 1.0
     - (etc. for all visemes)

4. [Smooth Transition]:
   - Interpolate morph values over 0.05 seconds (50ms) for smooth animation
```

**Alternative** (use MetaHuman's built-in system):
```
MetaHuman comes with a "Control Rig" that has viseme curves.
1. Get MetaHuman Mesh Component
2. Get Control Rig Component
3. Set Control Value: "Jaw_Open" based on viseme
4. Set Control Value: "Lips_Pucker" based on viseme
etc.
```

---

### `ExecuteAction(ActionStruct Action)`

**Description**: Execute actions like pointing, going to slide, etc.

**Blueprint Nodes**:
```
1. [Switch on String]: Action.Type

   Case "goto_slide":
     → Get SmartBoardRef
     → Call: SmartBoardRef.LoadSlide(Action.SlideID)
     → Print: "Going to slide " + Action.SlideID
   
   Case "point_to":
     → If Action.Target == "screen":
       → Play Animation: Anim_PointToScreen
       → Look At: SmartBoardRef.GetActorLocation()
     → Else:
       → Print: "Unknown target"
   
   Case "nod":
     → Play Animation Montage: Anim_Nod
   
   Case "gesture_emphasis":
     → Play Animation: Anim_HandGesture01
   
   Default:
     → Print: "Unknown action type: " + Action.Type
```

---

### `MonitorActionsForTiming(ActionsArray Array)`

**Description**: Execute "during_speech" actions at the right moment

**Blueprint Nodes**:
```
1. [Filter Actions]:
   - For Each action in ActionsArray:
     - If action.Timing == "during_speech":
       → Add to DuringSpeechActions array

2. [If DuringSpeechActions not empty]:
   - Set Timer by Function Name:
     - Function: CheckSpeechProgress
     - Time: 0.1 seconds
     - Looping: true
```

---

### `CheckSpeechProgress()`

**Description**: Periodically check audio progress to trigger timed actions

**Blueprint Nodes**:
```
1. [Get Current Playback Time]:
   - AudioComponent.GetPlaybackPercent() * TotalDuration

2. [For Each action] in DuringSpeechActions:
   - If action.AtWord exists:
     → Estimate time from word count (rough: AtWord * 0.4 seconds)
     → If CurrentTime >= EstimatedTime AND not executed:
       → ExecuteAction(action)
       → Mark as executed

3. [If All Actions Executed]:
   - Clear Timer: CheckSpeechProgress
```

---

### `OnSpeechFinished()`

**Custom Event**: Called when audio playback ends

**Blueprint Nodes**:
```
1. [Stop Viseme Timeline]:
   - VisemeTimeline.Stop()

2. [Reset to Idle Pose]:
   - Call: SetIdlePose()

3. [Execute After-Speech Actions]:
   - For Each action in CurrentActions:
     - If action.Timing == "after_speech":
       → ExecuteAction(action)

4. [Clear State]:
   - Set IsCurrentlySpeaking = false
   - Clear CurrentVisemes
   - Clear CurrentActions

5. [Print]: "Finished speaking"
```

---

### `SetIdlePose()`

**Description**: Return teacher to neutral, idle state

**Blueprint Nodes**:
```
1. [Stop All Animations]:
   - Stop current montage

2. [Play Idle Animation]:
   - Play Animation: Anim_Idle_Breathing
   - Looping: true

3. [Reset Face]:
   - Set all viseme morphs to 0.0 (neutral face)

4. [Look at Camera]:
   - Look At target = Player Camera
   - Smooth interpolation over 1 second
```

---

## Animation Setup

### Required Animations
Create or import these animation montages:

1. **Anim_Idle_Breathing** - Looping idle with subtle breathing
2. **Anim_PointToScreen** - Extend arm toward smart board
3. **Anim_Nod** - Simple head nod
4. **Anim_HandGesture01-05** - Various hand gestures for emphasis

### Animation Blueprint
1. Create Animation Blueprint for MetaHuman
2. State Machine:
   - **Idle State** → Anim_Idle_Breathing
   - **Speaking State** → Upper body gestures
   - **Pointing State** → Anim_PointToScreen
3. Blend facial animations with body animations

---

## Event Graph

### BeginPlay
```
Begin Play
  → [Get Components]:
    - MetaHumanMesh = Get Component by Class (Skeletal Mesh)
    - AudioComponent = Get Component by Class (Audio)
  
  → [Find Smart Board]:
    - Get Actor of Class: BP_SmartBoard
    - Set SmartBoardRef
  
  → [Set Initial State]:
    - Call: SetIdlePose()
```

---

## Testing

### Test 1: Basic Speech
1. Create test button in HUD
2. On Click:
   - Hardcode test audio (Base64 of "Hello")
   - Hardcode test visemes: [0.0/sil, 0.2/HH, 0.4/E, 0.6/L, 0.8/O, 1.0/sil]
   - Call: SpeakAnswer(audio, visemes, [])
3. Press Play → Click button
4. **Expected**: Teacher plays audio with lip movements

### Test 2: With Actions
1. Create test data:
   - Action: {Type="goto_slide", SlideID=3, Timing="before_speech"}
   - Action: {Type="point_to", Target="screen", Timing="during_speech", AtWord=10}
2. Call: SpeakAnswer(audio, visemes, [actions])
3. **Expected**: Slide changes before speech, pointing happens mid-speech

### Test 3: Full Integration
1. Send REAL question via BP_BackendConnection
2. Wait for response
3. **Expected**: Teacher responds with proper lip sync and actions

---

## Common Issues

### Lip sync doesn't match audio
- **Check**: Backend TTS is generating correct viseme timestamps
- **Fix**: Adjust viseme timing manually or improve TTS viseme generation

### Teacher doesn't look at camera
- **Check**: Camera reference is set correctly
- **Fix**: Use "Look At" node targeting player camera

### Animation montages don't play
- **Check**: Animation Blueprint state machine
- **Fix**: Ensure "Allow AnimMontage To Override" is enabled

---

## Next Steps

1. **[Blueprint_SmartBoard.md](file:///home/raed/GamifiedAIEduSys/Unreal/Blueprint_SmartBoard.md)** - Display slides
2. **[Blueprint_UI.md](file:///home/raed/GamifiedAIEduSys/Unreal/Blueprint_UI.md)** - Student interface
3. **Testing** - Full pipeline test
