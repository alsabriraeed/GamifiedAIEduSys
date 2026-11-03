# Testing Guide

## Complete Integration Test Checklist

Follow this checklist to verify your AI Classroom is working end-to-end.

---

## Pre-Test Requirements

### Backend
- [ ] Backend server running at `http://10.40.14.96:8000`
- [ ] Test health endpoint: `curl http://10.40.14.96:8000/`
- [ ] WebSocket endpoint accessible: `ws://10.40.14.96:8000/ws`
- [ ] Ollama running with `llama3.2:latest`
- [ ] All 12 slides loaded in knowledge base

### Unreal
- [ ] All Blueprints created (BP_BackendConnection, BP_TeacherController, BP_SmartBoard, WBP_ClassroomHUD, BP_AIClassroom_GameMode)
- [ ] MetaHuman Teacher imported and placed in level
- [ ] Smart Board mesh created with M_SmartBoard material
- [ ] Camera positioned correctly
- [ ] All 12 slide textures imported to `/Content/AIClassroom/Slides/`
- [ ] VaRest plugin enabled

---

## Test 1: Backend Connection

**Goal**: Verify Unreal connects to Python backend

1. In Unreal, open `BP_BackendConnection`
2. Check `BackendURL` = `"ws://10.40.14.96:8000/ws"`
3. Press Play in Editor
4. Check Output Log for:
   ```
   LogTemp: Connecting to backend...
   LogTemp: Connected to AI Backend!
   ```
5. Check backend terminal for:
   ```
   INFO: WebSocket connected (total: 1)
   ```

**✅ Pass**: "Connected to AI Backend!" appears in log  
**❌ Fail**: Check firewall, backend running, URL correct

---

## Test 2: Slide Display

**Goal**: Verify slides load on smart board

1. Press Play
2. Check smart board shows Slide 1
3. Open console (`) and type: `ce BP_SmartBoard LoadSlide 5`
4. Press Enter
5. Smart board should change to Slide 5

**✅ Pass**: Slides change correctly  
**❌ Fail**: Check textures imported, material setup correct

---

## Test 3: Slide Navigation

**Goal**: Verify UI controls work

1. Press Play
2. Click "Next" button in HUD
3. Slide counter should say "Slide 2 / 12"
4. Smart board shows Slide 2
5. Click "Previous" button
6. Slide counter says "Slide 1 / 12"

**✅ Pass**: Navigation works both directions  
**❌ Fail**: Check button click events, SmartBoard reference

---

## Test 4: Question Submission (Text)

**Goal**: Verify question reaches backend

1. Press Play
2. Type in question box: `"What is a neural network?"`
3. Click Submit (or press Enter)
4. Check Unreal Output Log for:
   ```
   LogTemp: Sent question: What is a neural network?
   ```
5. Check backend terminal for:
   ```
   INFO: Received message type: student_question
   INFO: Generating answer for: 'What is a neural network?...'
   ```

**✅ Pass**: Backend receives and processes question  
**❌ Fail**: Check WebSocket connection, JSON formatting

---

## Test 5: Teacher Response (Without Audio)

**Goal**: Verify backend sends response back

1. Submit question: `"What is backpropagation?"`
2. Wait 3-5 seconds
3. Check Unreal Output Log for:
   ```
   LogTemp: Received: {"type":"teacher_response", ...}
   ```
4. Check response includes:
   - `answer_text` (not empty)
   - `visemes` array
   - `actions` array

**✅ Pass**: Response received with all fields  
**❌ Fail**: Check backend LLM/RAG services, response format

---

## Test 6: Audio Playback (if Audio Works)

**Goal**: Verify teacher speaks

1. Submit question
2. Wait for response
3. Teacher should play audio
4. Hear TTS voice speaking answer
5. Check Unreal logs for:
   ```
   LogTemp: Generated speech for '...'
   LogTemp: Finished speaking
   ```

**✅ Pass**: Audio plays  
**❌ Fail**: Check TTS service, audio decoding, AudioComponent

---

## Test 7: Lip Sync

**Goal**: Verify visemes drive facial animation

1. Submit question
2. Wait for teacher to speak
3. Watch MetaHuman's lips
4. Lips should move (even if not perfectly synced)
5. Check Output Log for viseme application

**✅ Pass**: Lips move during speech  
**❌ Fail**: Check viseme timeline, MetaHuman face rig

---

## Test 8: Slide Actions

**Goal**: Verify `goto_slide` actions work

1. Ask: `"Tell me about backpropagation"` (Slide 5 topic)
2. Wait for response
3. Teacher should:
   - Load Slide 5 (before speaking)
   - Speak answer
4. Smart board shows Slide 5

**✅ Pass**: Slide changes automatically  
**❌ Fail**: Check action execution in BP_TeacherController

---

## Test 9: Pointing Animation (if Implemented)

**Goal**: Verify teacher points at screen

1. Ask question that triggers `point_to` action
2. During speech, teacher should:
   - Extend arm toward smart board
   - Look at screen
3. Return to idle after

**✅ Pass**: Pointing animation plays  
**❌ Fail**: Check animation montage, action execution

---

## Test 10: Full Pipeline

**Goal**: Complete end-to-end test

### Scenario:
1. Press Play
2. Slide 1 is displayed
3. Ask: *"What are loss functions?"*
4. Expected behavior:
   - UI shows "Processing..."
   - Backend retrieves context from Slide 4
   - Teacher goes to Slide 4 (before speaking)
   - Teacher speaks answer with lip sync
   - Answer appears in UI overlay
   - Teacher returns to idle
   - UI shows "Ready"

**✅ Pass**: All steps execute smoothly  
**❌ Fail**: Debug each component individually

---

## Performance Benchmarks

Target metrics:
- **Connection Time**: < 2 seconds
- **Response Latency**: 3-8 seconds (question → start speaking)
- **Frame Rate**: 60+ FPS
- **Memory**: < 8GB VRAM (Unreal)

---

## Troubleshooting

### Teacher doesn't speak
1. Check audio_data in response (not empty?)
2. Check AudioComponent is valid
3. Check sound wave creation
4. Check system audio not muted

### Lip sync is off
1. Viseme timestamps may be inaccurate
2. Try manual timing adjustment
3. Verify MetaHuman face rig setup

### Actions don't execute
1. Check action.timing field
2. Print actions array to debug
3. Verify ExecuteAction switch statement

### Questions timeout
1. Check backend LLM is responding
2. Increase timeout in WebSocket
3. Check Ollama is running

---

## Next: Pixel Streaming

Once all tests pass, proceed to:
1. Package Unreal project
2. Setup Pixel Streaming signaling server
3. Test browser access
4. Deploy!

---

## Test Report Template

```
Test Date: ______
Tester: ______

Backend Connection: ✅ / ❌
Slide Display: ✅ / ❌
Slide Navigation: ✅ / ❌
Question Submission: ✅ / ❌
Teacher Response: ✅ / ❌
Audio Playback: ✅ / ❌
Lip Sync: ✅ / ❌
Slide Actions: ✅ / ❌
Pointing Animation: ✅ / ❌
Full Pipeline: ✅ / ❌

Issues Found:
1. _________________________
2. _________________________
3. _________________________

Notes:
_________________________
_________________________
```
