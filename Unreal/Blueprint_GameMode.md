# Game Mode Setup Guide

## Blueprint: BP_AIClassroom_GameMode

Main game mode that orchestrates all systems.

---

## Class Defaults

- **Default Pawn Class**: None (we use fixed camera)
- **HUD Class**: None (we use Widget instead)
- **Player Controller Class**: BP_AIClassroom_PlayerController

---

## Variables

```
BackendConnection (BP_BackendConnection Reference)
TeacherController (BP_TeacherController Reference)
SmartBoard (BP_SmartBoard Reference)
ClassroomHUD (WBP_ClassroomHUD Widget Reference)
```

---

## Event BeginPlay

```
1. [Spawn Backend Connection]:
   - Spawn Actor: BP_BackendConnection
   - Store reference

2. [Find Classroom Actors]:
   - Get Actor of Class: BP_TeacherController
   - Get Actor of Class: BP_SmartBoard
   - Store references

3. [Create and Show HUD]:
   - Create Widget: WBP_ClassroomHUD
   - Add to Viewport
   - Store reference

4. [Set Input Mode]:
   - Get Player Controller
   - Set Input Mode: UI Only
   - Show Mouse Cursor = true

5. [Initialize]:
   - Wait 1 second
   - SmartBoard.LoadSlide(1)
   - TeacherController.SetIdlePose()

6. [Print]: "AI Classroom initialized"
```

---

## Player Controller

Create `BP_AIClassroom_PlayerController` for input handling:

### Variables
```
GameModeRef (BP_AIClassroom_GameMode Reference)
```

### Event BeginPlay
```
1. [Get Game Mode]:
   - Get Game Mode → Cast to BP_AIClassroom_GameMode
   - Store reference

2. [Setup Camera]:
   - Get Actor of Class: Camera Actor
   - Set View Target with Blend
```

### Input Bindings

Create these in Project Settings → Input:

**Action Mappings**:
- `NextSlide` → Right Arrow
- `PrevSlide` → Left Arrow
- `SubmitQuestion` → Enter

**Axis Mappings**: (none needed)

### Input Events

```
Event: NextSlide (Pressed)
  → Get UI → Call: NextSlideButton.OnClicked()

Event: PrevSlide (Pressed)
  → Get UI → Call: PrevSlideButton.OnClicked()

Event: SubmitQuestion (Pressed)
  → Get UI → Call: SubmitButton.OnClicked()
```

---

## Testing Checklist

Before running, verify:
- [ ] BP_BackendConnection exists in Content Browser
- [ ] BP_TeacherController exists in level
- [ ] BP_SmartBoard exists in level
- [ ] Camera Actor exists in level
- [ ] All 12 slide textures imported
- [ ] WBP_ClassroomHUD widget created
- [ ] Backend server is running

---

## Quick Test

1. Set Game Mode in World Settings → `BP_AIClassroom_GameMode`
2. Press Play
3. Should see:
   - HUD appears
   - Slide 1 on screen
   - Teacher in idle pose
   - Mouse cursor visible
4. Type question → Press Enter
5. Should see teacher respond

---

## File Locations

```
Content/AIClassroom/
├── Blueprints/
│   ├── BP_AIClassroom_GameMode.uasset
│   ├── BP_AIClassroom_PlayerController.uasset
│   ├── BP_BackendConnection.uasset
│   ├── BP_TeacherController.uasset
│   └── BP_SmartBoard.uasset
├── UI/
│   └── WBP_ClassroomHUD.uasset
├── Maps/
│   └── Classroom_Main.umap
└── Materials/
    └── M_SmartBoard.uasset
```

Save everything and you're ready to test!
