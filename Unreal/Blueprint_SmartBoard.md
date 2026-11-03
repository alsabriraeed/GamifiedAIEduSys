# Smart Board Blueprint Guide

## Blueprint: BP_SmartBoard

Displays slides on a 3D screen mesh in the classroom.

---

## Components

```
[Default Scene Root]
└── [Static Mesh] → "BoardMesh" (Plane, 3m × 2m, vertical)
```

---

## Variables

```
BoardMesh (Static Mesh Component Reference)
SlideTextures (Map: Integer → Texture 2D)
  - Key: Slide ID (1-12)
  - Value: Texture asset reference
CurrentSlideID (Integer) = 1
DynamicMaterialInstance (Material Instance Dynamic)
```

---

## Functions

### `ConstructionScript()`

**Description**: Initialize slide texture map

**Blueprint Nodes**:
```
1. [Initialize Map]:
   - Create Map: SlideTextures

2. [Load Slide Textures]:
   - For i = 1 to 12:
     - Load Texture: "/Game/AIClassroom/Slides/Slide_" + (i as String padded to 2 digits)
     - Add to Map: [Key=i, Value=Texture]
   
3. [Print]: "Loaded " + SlideTextures.Length + " slides"
```

---

### `BeginPlay()`

**Blueprint Nodes**:
```
1. [Get Mesh Component]:
   - BoardMesh = Get Component by Class (Static Mesh)

2. [Create Dynamic Material]:
   - Get Material: M_SmartBoard (static material)
   - Create Dynamic Material Instance
   - Set DynamicMaterialInstance

3. [Apply to Mesh]:
   - BoardMesh.SetMaterial(0, DynamicMaterialInstance)

4. [Load Initial Slide]:
   - Call: LoadSlide(1)
```

---

### `LoadSlide(SlideID Integer)`

**Description**: Change the displayed slide

**Blueprint Nodes**:
```
1. [Validate Slide ID]:
   - Branch: SlideID >= 1 AND SlideID <= 12?
   - False → Print "Invalid slide ID" → Return

2. [Get Texture]:
   - Find in Map: SlideTextures[SlideID]
   - Result → SlideTexture

3. [Check Texture]:
   - Branch: SlideTexture is Valid?
   - False → Print "Slide texture not found" → Use placeholder

4. [Update Material]:
   - DynamicMaterialInstance.SetTextureParameterValue("SlideTexture", SlideTexture)

5. [Play Transition]:
   - Call: PlaySlideTransition()

6. [Update State]:
   - Set CurrentSlideID = SlideID

7. [Print]: "Loaded slide " + SlideID
```

---

### `PlaySlideTransition()`

**Description**: Smooth fade-in effect when changing slides

**Blueprint Nodes**:
```
1. [Create Timeline]:
   - Timeline Component: "FadeTimeline"
   - Duration: 0.3 seconds
   - Curve: 0.0 → 1.0 (fade in)

2. [Timeline Update Event]:
   - Get Alpha (0-1)
   - Set Scalar Parameter: "Opacity" = Alpha

3. [Play Timeline]:
   - FadeTimeline.PlayFromStart()
```

**Alternative** (simpler):
```
Just set texture directly - instant update
(Use transition if you want polish)
```

---

### `HighlightRegion(X Float, Y Float, Width Float, Height Float, Duration Float)`

**Description**: Draw a red rectangle overlay to highlight part of slide

**Blueprint Nodes**:
```
1. [Create Highlight Widget]:
   - Spawn Widget Component
   - Widget Class: WBP_Highlight (simple colored rectangle)
   - Attach to BoardMesh

2. [Set Widget Transform]:
   - Calculate UV position on mesh
   - X, Y = UV coordinates (0-1 range)
   - Width, Height = size in UV space

3. [Widget Properties]:
   - Rectangle color: Red (255, 0, 0)
   - Opacity: 0.5

4. [Fade Out After Duration]:
   - Delay node: Duration seconds
   - Timeline: Fade opacity 1.0 → 0.0
   - On Complete: Destroy Widget
```

**Simpler Alternative** (Material-based):
```
1. Add highlight parameters to M_SmartBoard material
2. DynamicMaterialInstance.Set Vector Parameter "HighlightRect" = (X, Y, Width, Height)
3. Set Float Parameter "HighlightOpacity" = 1.0
4. Timeline to fade opacity to 0.0
```

---

### `GoToNextSlide()`

**Blueprint Nodes**:
```
1. [Calculate Next]:
   - NextSlideID = CurrentSlideID + 1

2. [Wrap Around]:
   - If NextSlideID > 12:
     → NextSlideID = 1

3. [Load Slide]:
   - Call: LoadSlide(NextSlideID)
```

---

### `GoToPreviousSlide()`

**Blueprint Nodes**:
```
1. [Calculate Previous]:
   -PrevSlideID = CurrentSlideID - 1

2. [Wrap Around]:
   - If PrevSlideID < 1:
     → PrevSlideID = 12

3. [Load Slide]:
   - Call: LoadSlide(PrevSlideID)
```

---

## Material Setup: M_SmartBoard

### Nodes

```
[Texture Sample] "SlideTexture" (Parameter)
  ↓
[Multiply] × Scalar "Brightness" (1.2 for slight glow)
  ↓
[Emissive Color] (makes screen glow)

[Constant 3] (white) for Base Color

Optional Highlight Overlay:
[Vector Parameter] "HighlightRect" (X, Y, W, H)
[Float Parameter] "HighlightOpacity"
  ↓
[Draw Rectangle Function] (custom or use TextureCoordinates + comparisons)
  ↓
[Lerp] between slide and highlight color
  ↓
[Emissive Color]
```

### Material Parameters

- `SlideTexture` (Texture 2D)
- `Brightness` (Float) = 1.2
- `HighlightRect` (Vector4) = (0, 0, 0, 0)
- `HighlightOpacity` (Float) = 0.0

---

## Testing

### Test 1: Load All Slides
```
Create custom event with For Loop (1 to 12):
  - LoadSlide(i)
  - Delay 2 seconds
  - Next iteration
  
Press Play → Should cycle through all slides
```

### Test 2: Highlight
```
On Keyboard key "H":
  - Call: HighlightRegion(0.2, 0.3, 0.4, 0.3, 3.0)
  
Should show red rectangle for 3 seconds
```

### Test 3: Navigation
```
Keyboard "Right Arrow" → GoToNextSlide()
Keyboard "Left Arrow" → GoToPreviousSlide()
```

---

## Integration with Backend

When backend sends `goto_slide` action:
```
In BP_TeacherController.ExecuteAction():
  Case "goto_slide":
    → Get Actor of Class: BP_SmartBoard
    → Call: SmartBoard.LoadSlide(Action.SlideID)
```

---

## Common Issues

### Slides appear black
- **Check**: Textures are imported correctly
- **Check**: Material has Emissive connected (not Base Color alone)
- **Fix**: Increase Brightness parameter

### Texture is flipped/rotated wrong
- **Fix**: Adjust mesh rotation or UV coordinates in material

### Slides are blurry
- **Check**: Texture compression settings
- **Fix**: Set texture to "UserInterface2D" compression (no compression)

---

## Next Steps

1. **[Blueprint_UI.md](file:///home/raed/GamifiedAIEduSys/Unreal/Blueprint_UI.md)** - Student interface
2. **Full Integration Testing** - Test complete Q&A flow
