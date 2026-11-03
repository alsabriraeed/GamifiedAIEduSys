# Unreal Engine Quick Start Guide

## Prerequisites Checklist

### Software Installation
- [ ] Unreal Engine 5.3 or higher installed
  - Download from: [Epic Games Launcher](https://www.epicgames.com/store/download)
  - Requires ~45GB disk space
  - Requires GPU with 4GB+ VRAM

- [ ] Visual Studio 2022 (for C++ projects)
  - Or stick with Blueprint-only (recommended for faster iteration)

- [ ] MetaHuman Creator account
  - Sign up at: [metahuman.unrealengine.com](https://metahuman.unrealengine.com)

### Backend Verification
- [x] Backend running at `http://10.40.14.96:8000`
- [x] WebSocket endpoint: `ws://10.40.14.96:8000/ws`
- [x] Slides available at `/slides` endpoint

---

## Step-by-Step Setup

### 1. Create Unreal Project (10 minutes)

1. Open Epic Games Launcher
2. Go to Unreal Engine → Library
3. Click "Launch" on version 5.3+
4. Create New Project:
   - **Template**: Blank or Third Person
   - **Project Type**: Blueprint (easier) or C++ (more control)
   - **Platform**: Desktop
   - **Quality**: Maximum
   - **Starter Content**: ✓ Yes
   - **Location**: `/home/raed/GamifiedAIEduSys/Unreal`
   - **Name**: `AIClassroom`
5. Click "Create"

**Result**: Unreal Editor opens with blank project

---

### 2. Install Required Plugins (5 minutes)

#### A. VaRest (WebSocket + JSON)
1. Edit → Plugins
2. Search "VaRest"
3. Check "Enabled"
4. Restart editor

#### B. Pixel Streaming (if not already enabled)
1. Edit → Plugins
2. Search "Pixel Streaming"
3. Check "Enabled"
4. Restart editor

---

### 3. Create MetaHuman (30-60 minutes)

**Option A**: Use MetaHuman Creator (Recommended)
1. Visit [metahuman.unrealengine.com](https://metahuman.unrealengine.com)
2. Sign in with Epic account
3. Click "Create MetaHuman"
4. Customize appearance:
   - Professional look (teacher)
   - Business casual outfit
   - Age: 30-45
   - Friendly face
5. Name it: `Teacher_Primary`
6. Click "Download" → Quixel Bridge
7. In Unreal: Window → Quixel Bridge
8. Download `Teacher_Primary` to project

**Option B**: Use Sample MetaHuman (Faster)
1. In Unreal: Window → Quixel Bridge
2. Browse MetaHumans tab
3. Select any professional-looking character
4. Download to project
5. Rename to `Teacher_Primary`

**Result**: MetaHuman available in `Content/MetaHumans/Teacher_Primary`

---

### 4. Project Structure Setup (10 minutes)

Create these folders in Content Browser:

```
Content/
├── AIClassroom/
│   ├── Maps/
│   │   └── Classroom_Main (create new level here)
│   ├── Blueprints/
│   │   ├── BP_BackendConnection
│   │   ├── BP_TeacherController
│   │   ├── BP_SmartBoard
│   │   └── BP_GameMode
│   ├── Materials/
│   │   └── M_SmartBoard
│   ├── UI/
│   │   └── WBP_ClassroomHUD
│   └── Slides/
│       └── (import slide images here)
└── MetaHumans/
    └── Teacher_Primary/
```

**To create folders**:
- Right-click in Content Browser
- New Folder → Enter name

---

### 5. Import Slide Images (5 minutes)

1. Copy slide images from backend:
   ```bash
   cp /home/raed/GamifiedAIEduSys/backend/knowledge_base/slides/slide_*.png \
      /home/raed/GamifiedAIEduSys/Unreal/AIClassroom/Content/AIClassroom/Slides/
   ```

2. In Unreal Content Browser:
   - Right-click `Slides` folder → "Show in Explorer"
   - Slide images should auto-import

**Result**: `Slide_01`, `Slide_02`, ... `Slide_12` textures available

---

### 6. Create Main Level (15 minutes)

1. File → New Level → Empty Level
2. Save as `Classroom_Main` in `Content/AIClassroom/Maps/`
3. Add basic lighting:
   - Place Actors → Lights → Directional Light
   - Place Actors → Lights → Sky Light
4. Add floor:
   - Place Actors → Shapes → Plane (scale: 10, 10, 1)
5. Add camera:
   - Place Actors → Cameras → Camera Actor
   - Position: X=600, Y=0, Z=150 (6m from origin, at eye level)

---

### 7. Create Smart Board (20 minutes)

#### A. Create Plane Mesh
1. Place Actors → Shapes → Plane
2. Transform:
   - Location: X=0, Y=0, Z=200 (front wall, 2m high)
   - Rotation: Pitch=-90, Yaw=0 (vertical)
   - Scale: X=15, Y=10, Z=1 (3m × 2m)
3. Rename to `SmartBoard_Mesh`

#### B. Create Material
1. Content Browser → Right-click `Materials` folder
2. Material → Name: `M_SmartBoard`
3. Double-click to open Material Editor
4. Add nodes:
   - Texture Sample (for slide image)
   - Make Parameter → Name: `SlideTexture`
   - Connect to **Emissive Color**
5. Save

#### C. Apply Material
1. Select `SmartBoard_Mesh`
2. Details panel → Materials → Element 0 → `M_SmartBoard`

**Test**: Should see white emissive plane

---

### 8. Next Steps

You're now ready to implement the logic! Follow these guides in order:

1. **[Blueprint_WebSocket.md](file:///home/raed/GamifiedAIEduSys/Unreal/Blueprint_WebSocket.md)** - Connect to backend
2. **[Blueprint_TeacherController.md](file:///home/raed/GamifiedAIEduSys/Unreal/Blueprint_TeacherController.md)** - Control MetaHuman
3. **[Blueprint_SmartBoard.md](file:///home/raed/GamifiedAIEduSys/Unreal/Blueprint_SmartBoard.md)** - Display slides
4. **[Blueprint_UI.md](file:///home/raed/GamifiedAIEduSys/Unreal/Blueprint_UI.md)** - Student interface

---

## Troubleshooting

### "Plugin VaRest not found"
- Download from: [GitHub VaRest](https://github.com/ufna/VaRest)
- Or use Marketplace version (free)

### MetaHuman face rig not found
- Ensure MetaHuman plugin is enabled
- Re-download MetaHuman from Bridge

### Slides not importing
- Check file format: PNG only
- Max size: 2048×2048
- Check file permissions

---

## Estimated Time

- **Setup (Steps 1-7)**: 2-3 hours
- **Blueprint Implementation**: 8-12 hours
- **Testing & Polish**: 3-5 hours
- **Total**: 15-20 hours

Ready to start? Open the Blueprint guides next!
