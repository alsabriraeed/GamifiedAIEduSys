# UI Widget Blueprint Guide

## Blueprint: WBP_ClassroomHUD

The main HUD widget for student interaction.

---

## Canvas Structure

```
Canvas Panel
├── [Vertical Box] "TopBar"
│   ├── [Text Block] "SlideCounter" (e.g., "Slide 5 / 12")
│   └── [Text Block] "StatusIndicator" (e.g., "Teacher is speaking...")
│
├── [Horizontal Box] "QuestionInputBox" (Bottom-Center)
│   ├── [Editable Text] "QuestionTextBox"
│   ├── [Button] "SubmitButton"
│   └── [Button] "MicButton" (toggle microphone)
│
├── [Horizontal Box] "SlideNavigation" (Bottom-Right)
│   ├── [Button] "PrevSlideButton" ("←")
│   └── [Button] "NextSlideButton" ("→")
│
└── [Overlay] "ResponseOverlay" (Full screen, initially hidden)
    └── [Text Block] "TeacherAnswerText"
```

---

## Variables

```
BackendConnection (BP_BackendConnection Reference)
SmartBoard (BP_SmartBoard Reference)
CurrentSlideID (Integer) = 1
TotalSlides (Integer) = 12
IsProcessing (Boolean) = false
IsMicActive (Boolean) = false
```

---

## Events

### Event Construct

**Description**: Initialize widget on creation

**Blueprint Nodes**:
```
1. [Get References]:
   - BackendConnection = Get Actor of Class (BP_BackendConnection)
   - SmartBoard = Get Actor of Class (BP_SmartBoard)

2. [Bind Events]:
   - BackendConnection.OnBackendReady → [Update UI Status]

3. [Initialize UI]:
   - Call: UpdateSlideCounter()
   - Set StatusIndicator text = "Ready"
   - Set QuestionTextBox placeholder = "Ask a question..."

4. [Set Initial State]:
   - ResponseOverlay.SetVisibility(Collapsed)
```

---

### SubmitButton - OnClicked

**Blueprint Nodes**:
```
1. [Get Question]:
   - QuestionText = QuestionTextBox.GetText()

2. [Validate]:
   - Branch: QuestionText is empty?
   - True → Print "Enter a question" → Return

3. [Check Connection]:
   - Branch: BackendConnection.IsConnected?
   - False → Show error "Not connected to backend" → Return

4. [Send to Backend]:
   - Call: BackendConnection.SendQuestion(QuestionText, CurrentSlideID)

5. [Update UI]:
   - Clear QuestionTextBox
   - Set StatusIndicator = "Processing..."
   - Set IsProcessing = true
   - Disable SubmitButton
```

---

### MicButton - OnClicked

**Description**: Toggle microphone recording

**Blueprint Nodes**:
```
1. [Toggle State]:
   - IsMicActive = NOT IsMicActive

2. [Branch on State]:
   
   If IsMicActive = true:
     → Start Audio Capture (use Voice Capture plugin)
     → Change button color to Red
     → Set button text = "🔴 Recording..."
     → Set StatusIndicator = "Listening..."
   
   Else:
     → Stop Audio Capture
     → Get recorded audio buffer
     → Encode to Base64
     → Call: BackendConnection.SendQuestion("", CurrentSlideID)
       (send audio_data instead of text)
     → Change button color to default
     → Set button text = "🎤 Ask"
     → Set StatusIndicator = "Processing..."
```

**Note**: Audio capture requires C++ plugin or marketplace asset

---

### PrevSlideButton - OnClicked

**Blueprint Nodes**:
```
1. [Check if not processing]:
   - Branch: IsProcessing?
   - True → Return (don't allow navigation while processing)

2. [Navigate]:
   - Call: SmartBoard.GoToPreviousSlide()

3. [Update Counter]:
   - CurrentSlideID = SmartBoard.CurrentSlideID
   - Call: UpdateSlideCounter()
```

---

### NextSlideButton - OnClicked

**Blueprint Nodes**:
```
1. [Check if not processing]:
   - Branch: IsProcessing?
   - True → Return

2. [Navigate]:
   - Call: SmartBoard.GoToNextSlide()

3. [Update Counter]:
   - CurrentSlideID = SmartBoard.CurrentSlideID
   - Call: UpdateSlideCounter()
```

---

## Functions

### `UpdateSlideCounter()`

**Blueprint Nodes**:
```
1. [Format Text]:
   - Text = "Slide " + (CurrentSlideID as String) + " / " + (TotalSlides as String)

2. [Update Widget]:
   - SlideCounter.SetText(Text)
```

---

### `ShowResponse(AnswerText String, Confidence Float)`

**Description**: Display teacher's answer (called by BP_BackendConnection)

**Blueprint Nodes**:
```
1. [Update Status]:
   - Set StatusIndicator = "Teacher is speaking..."

2. [Show Answer]:
   - TeacherAnswerText.SetText(AnswerText)
   - ResponseOverlay.SetVisibility(Visible)

3. [Add Confidence Badge]:
   - If Confidence < 0.7:
     → Text color = Yellow
     → Append "(Low confidence)"
   - Else:
     → Text color = White

4. [Auto-Hide]:
   - Delay: 15 seconds
   - ResponseOverlay.SetVisibility(Collapsed)
```

---

### `OnTeacherFinishedSpeaking()` (Custom Event)

**Description**: Reset UI when teacher finishes

**Blueprint Nodes**:
```
1. [Update Status]:
   - Set StatusIndicator = "Ready"
   - Set IsProcessing = false

2. [Enable Input]:
   - Enable SubmitButton
   - Enable QuestionTextBox

3. [Hide Response]:
   - ResponseOverlay.SetVisibility(Collapsed)
```

---

## Styling

### Colors
- Background: Semi-transparent dark (0, 0, 0, 0.7)
- Primary Text: White (255, 255, 255)
- Accent: Blue (67, 126, 234)
- Button Hover: Light Blue (100, 150, 255)

### Fonts
- Headers: Roboto Bold 24pt
- Body: Roboto Regular 18pt
- Buttons: Roboto Medium 16pt

### Layout
- Padding: 20px around all elements
- Spacing: 10px between elements
- Corner Radius: 8px for buttons

---

## Advanced: Mode Toggle

Add a toggle for **Lecture Mode** vs **Q&A Mode**:

### Additional UI Element
```
[Horizontal Box] "ModeToggle" (Top-Center)
├── [Button] "LectureModeButton"
└── [Button] "QAModeButton"
```

### LectureModeButton - OnClicked
```
1. [Start Lecture]:
   - For CurrentSlideID = 1 to TotalSlides:
     - SmartBoard.LoadSlide(CurrentSlideID)
     - Request narration from backend
     - Wait for teacher to finish speaking
     - Delay 2 seconds
     - Next slide

2. [Update UI]:
   - Disable question input
   - Enable slide navigation
   - Show "Lecture in progress..."
```

### QAModeButton - OnClicked
```
1. [Enable Q&A]:
   - Stop lecture loop (if running)
   - Enable question input
   - Enable slide navigation
   - Show "Ask questions anytime"
```

---

## Testing

### Test 1: Question Input
```
1. Press Play
2. Type "What is a neural network?"
3. Click Submit
4. Check:
   - Status changes to "Processing..."
   - Button disables
   - Backend logs show question received
```

### Test 2: Slide Navigation
```
1. Click Next button → Slide advances
2. Click Previous → Slide goes back
3. Verify counter updates
```

### Test 3: Full Q&A Flow
```
1. Ask question
2. Wait for backend response
3. Check:
   - Answer appears in overlay
   - Teacher speaks
   - UI re-enables after speaking
```

---

## Common Issues

### Button doesn't respond
- **Check**: Is widget added to viewport?
- **Fix**: Call "Add to Viewport" in Game Mode BeginPlay

### Text is invisible
- **Check**: Text color vs background color
- **Fix**: Change text color to White

### Widget doesn't get input focus
- **Check**: Player Controller → Show Mouse Cursor enabled
- **Fix**: Set Input Mode to "UI Only" or "Game and UI"

---

## Integration

### In Game Mode BeginPlay:
```
1. Create Widget: WBP_ClassroomHUD
2. Add to Viewport
3. Set Input Mode: Game and UI
4. Show Mouse Cursor
```

---

## Next Steps

1. **Test Complete Pipeline** - Question → Answer → Speech
2. **Polish UI** - Add animations, better styling
3. **Pixel Streaming** - Prepare for browser deployment
