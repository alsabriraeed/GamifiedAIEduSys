# WebSocket Client Blueprint Guide

## Blueprint: BP_BackendConnection

This Blueprint connects to the Python backend WebSocket server and handles all communication.

---

## Variables

```
BackendURL (String) = "ws://10.40.14.96:8000/ws"
WebSocket (VaRest WebSocket Object)
IsConnected (Boolean) = false
CurrentSlideID (Integer) = 1
bAutoReconnect (Boolean) = true
ReconnectDelay (Float) = 5.0
```

---

## Functions

### `ConnectToBackend()`

**Description**: Initialize WebSocket connection to Python backend

**Blueprint Nodes**:
```
Event Graph:
1. [Create WebSocket] → VaRest Create WebSocket
   - URL: BackendURL
   
2. [Bind Events]:
   - On Connected → [Custom Event: OnWebSocketConnected]
   - On Disconnected → [Custom Event: OnWebSocketDisconnected]
   - On Message Received → [Custom Event: OnMessageReceived]
   - On Error → [Custom Event: OnWebSocketError]

3. [Connect]
   - Call: WebSocket.Connect()
   
4. [Print String]: "Connecting to backend..."
```

**C++ Equivalent** (if using C++):
```cpp
void ABackendConnection::ConnectToBackend()
{
    WebSocket = FVaRestWebSocketModule::Get().CreateWebSocket(BackendURL);
    
    WebSocket->OnConnected().AddDynamic(this, &ABackendConnection::OnWebSocketConnected);
    WebSocket->OnMessage().AddDynamic(this, &ABackendConnection::OnMessageReceived);
    WebSocket->OnDisconnected().AddDynamic(this, &ABackendConnection::OnWebSocketDisconnected);
    
    WebSocket->Connect();
    UE_LOG(LogTemp, Log, TEXT("Connecting to backend at %s"), *BackendURL);
}
```

---

### `OnWebSocketConnected()`

**Custom Event**:
```
1. [Set IsConnected] = true

2. [Print String]: "Connected to AI Backend!"

3. [Start Heartbeat Timer]:
   - Set Timer by Function Name
   - Function: SendHeartbeat
   - Time: 30.0 seconds
   - Looping: true
   
4. [Call Event]: OnBackendReady (dispatcher to notify other Blueprints)
```

---

### `OnWebSocketDisconnected()`

**Custom Event**:
```
1. [Set IsConnected] = false

2. [Print String]: "Disconnected from backend"

3. [Clear Timer]: SendHeartbeat

4. [Branch]: bAutoReconnect?
   - True → [Delay] 5 seconds → [ConnectToBackend]
   - False → Do nothing
```

---

### `SendQuestion(QuestionText String, SlideID Integer)`

**Description**: Send student question to backend

**Blueprint Nodes**:
```
1. [Check Connection]:
   - Branch: IsConnected?
   - False → Print "Not connected" → Return

2. [Build JSON]:
   - Create JSON Object (VaRest)
   - Set Field "type" = "student_question"
   - Set Field "text" = QuestionText
   - Set Field "current_slide_id" = SlideID
   - Set Field "timestamp" = [Get Unix Timestamp]

3. [Convert to String]:
   - JSON Object → To JSON String

4. [Send via WebSocket]:
   - WebSocket.Send(JSON String)

5. [Print String]: "Sent question: " + QuestionText
```

**JSON Output** (what gets sent):
```json
{
  "type": "student_question",
  "text": "What is backpropagation?",
  "current_slide_id": 5,
  "timestamp": 1707246890.0
}
```

---

### `OnMessageReceived(Message String)`

**Custom Event**: Called when backend sends a message

**Blueprint Nodes**:
```
1. [Print String]: "Received: " + Message

2. [Parse JSON]:
   - JSON String → Create JSON Object

3. [Get Message Type]:
   - JSON Object → Get String Field "type"

4. [Switch on String]: message_type
   
   Case "teacher_response":
     → [Call]: HandleTeacherResponse(JSON Object)
   
   Case "heartbeat":
     → [Call]: SendHeartbeat()
   
   Case "error":
     → [Print String]: "Backend error: " + [Get String Field "error_message"]
   
   Default:
     → [Print String]: "Unknown message type"
```

---

### `HandleTeacherResponse(ResponseJSON Object)`

**Description**: Process teacher's answer from backend

**Blueprint Nodes**:
```
1. [Extract Fields]:
   - answer_text = Get String Field "answer_text"
   - audio_data = Get String Field "audio_data"
   - visemes = Get Array Field "visemes"
   - actions = Get Array Field "actions"
   - confidence = Get Number Field "confidence"

2. [Validate]:
   - Branch: answer_text not empty?
   - False → Print "Empty response" → Return

3. [Execute Pre-Speech Actions]:
   - For Each action in actions:
     - If action.timing == "before_speech":
       → [Call]: BP_ActionExecutor.ExecuteAction(action)

4. [Play Teacher Response]:
   - Get Actor of Class: BP_TeacherController
   - Call: TeacherController.SpeakAnswer(audio_data, visemes, actions)

5. [Update UI]:
   - Get Widget of Class: WBP_ClassroomHUD
   - Call: HUD.ShowResponse(answer_text, confidence)
```

**Expected JSON** (from backend):
```json
{
  "type": "teacher_response",
  "answer_text": "Backpropagation is the key algorithm...",
  "audio_data": "UklGRiQAAABXQVZF...",
  "visemes": [
    {"time": 0.0, "viseme": "sil"},
    {"time": 0.2, "viseme": "PP"}
  ],
  "actions": [
    {
      "type": "goto_slide",
      "slide_id": 5,
      "timing": "before_speech"
    }
  ],
  "confidence": 0.88
}
```

---

### `SendHeartbeat()`

**Description**: Keep connection alive

**Blueprint Nodes**:
```
1. [Check Connection]:
   - Branch: IsConnected?
   - False → Return

2. [Build JSON]:
   - Create JSON Object
   - Set Field "type" = "heartbeat"
   - Set Field "timestamp" = [Get Unix Timestamp]

3. [Send]:
   - JSON Object → To JSON String
   - WebSocket.Send(JSON String)
```

---

## Event Graph Setup

### BeginPlay Event
```
Begin Play
  → [Delay] 1.0 second (let other actors initialize)
  → [ConnectToBackend]
```

### EndPlay Event
```
End Play
  → [Check]: IsConnected?
  → True: WebSocket.Disconnect()
```

---

## Testing in Editor

### Test 1: Connection
1. Press Play in Editor
2. Check Output Log for "Connected to AI Backend!"
3. Verify backend logs show new WebSocket connection

### Test 2: Send Question
1. Create a test button in your HUD
2. On Click → Call: `BP_BackendConnection.SendQuestion("What is a neural network?", 1)`
3. Check backend logs for received question
4. Check Output Log for response

### Test 3: Auto-Reconnect
1. Stop Python backend while playing
2. Wait 5 seconds
3. Restart backend
4. Should auto-reconnect

---

## Common Issues

### "Cannot connect to ws://..."
- **Check**: Backend is running (`python main.py`)
- **Check**: Firewall allows port 8000
- **Fix**: Try localhost if on same machine: `ws://localhost:8000/ws`

### "JSON parse error"
- **Check**: Message format matches schema
- **Fix**: Print raw message before parsing to debug

### "WebSocket is nullptr"
- **Check**: VaRest plugin is enabled
- **Fix**: Restart Unreal Editor

---

## Next Steps

Once WebSocket is working:
1. **[Blueprint_TeacherController.md](file:///home/raed/GamifiedAIEduSys/Unreal/Blueprint_TeacherController.md)** - Handle responses
2. **[Blueprint_SmartBoard.md](file:///home/raed/GamifiedAIEduSys/Unreal/Blueprint_SmartBoard.md)** - Display slides
3. **[Blueprint_UI.md](file:///home/raed/GamifiedAIEduSys/Unreal/Blueprint_UI.md)** - Student interface
