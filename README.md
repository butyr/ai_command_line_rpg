# D&D Text Adventure Game

A modular implementation of a D&D text adventure game using LangChain and Rich for the interface.

## Architecture Overview

The game is built with a modular architecture that separates concerns and maintains clear boundaries between components. Below is the architectural diagram showing the relationships between different modules:

```mermaid
graph TD
    subgraph Data Models
        PM[PlayerStats Model] --> GSM[GameState Model]
        CM[GameCommand Enum] --> GSM
    end

    subgraph Core Services
        SM[State Manager] --> GSM
        DS[Display Service] --> GSM
        AS[AI Service] --> GSM
        GE[Game Engine] --> GSM
    end

    subgraph Service Dependencies
        SM --> |Manages State| GE
        AS --> |Provides AI Responses| GE
        GE --> |Updates State| SM
        DS --> |Reads State| SM
    end

    subgraph External Dependencies
        RC[Rich Console] --> DS
        LO[LangChain Ollama] --> AS
        PD[Pydantic] --> GSM
    end

    subgraph Main Game Loop
        ML[Main Loop] --> |User Input| GE
        ML --> |Commands| DS
        ML --> |Error Handling| DS
        DS --> |Display Output| ML
    end

    classDef models fill:#f9f,stroke:#333,stroke-width:2px
    classDef services fill:#bbf,stroke:#333,stroke-width:2px
    classDef external fill:#bfb,stroke:#333,stroke-width:2px
    classDef main fill:#fbb,stroke:#333,stroke-width:2px

    class PM,GSM,CM models
    class SM,DS,AS,GE services
    class RC,LO,PD external
    class ML main
```

### Component Description

1. **Data Models**
   - `PlayerStats Model`: Handles character statistics
   - `GameState Model`: Central state representation
   - `GameCommand Enum`: Available game commands

2. **Core Services**
   - `State Manager`: Maintains game state
   - `Display Service`: Handles UI rendering
   - `AI Service`: Manages LLM interactions
   - `Game Engine`: Orchestrates game flow

3. **External Dependencies**
   - Rich Console: Terminal UI
   - LangChain Ollama: AI model integration
   - Pydantic: Data validation

## Game Flow

The following sequence diagram shows how the components interact during a typical game turn:

```mermaid
sequenceDiagram
    participant U as User
    participant M as Main Loop
    participant GE as Game Engine
    participant SM as State Manager
    participant AS as AI Service
    participant DS as Display Service

    U->>M: Input Command/Action
    M->>GE: Process Turn
    GE->>SM: Get Current State
    SM-->>GE: GameState
    
    alt is_command
        GE->>DS: Display Command Result
        DS->>SM: Get State for Display
        SM-->>DS: GameState
        DS-->>M: Display Output
    else is_game_action
        GE->>AS: Get AI Response
        AS->>SM: Get State for Context
        SM-->>AS: GameState
        AS-->>GE: AI Response
        GE->>SM: Update State
        GE->>DS: Display Response
        DS-->>M: Display Output
    end

    M-->>U: Show Result

    opt message_count > 6
        GE->>AS: Request Summary
        AS->>SM: Get Messages
        SM-->>AS: Message History
        AS-->>SM: New Summary
        SM->>SM: Update State
    end
```

### Flow Description

1. **Input Processing**
   - User input is received by the Main Loop
   - Game Engine determines if it's a command or game action

2. **Command Handling**
   - Commands are processed directly through the Display Service
   - State is retrieved and displayed accordingly

3. **Game Action Processing**
   - Actions are sent to the AI Service for response
   - State is updated based on the AI response
   - Results are displayed to the user

4. **Auto-Summarization**
   - After 6 messages, conversation is automatically summarized
   - Summary is stored in state for context

## Installation

```bash
pip install pydantic langchain-ollama langchain-core rich
```

## Usage

1. Create separate files for each module:
   - models.py
   - state_manager.py
   - display_service.py
   - ai_service.py
   - game_engine.py
   - main.py

2. Run the game:
```bash
python main.py
```

## Available Commands

- `/inventory` - Check your items
- `/stats` - View character stats
- `/quests` - Review active quests
- `/summary` - Recall recent adventures
- `quit` - Exit game

## Error Handling

The game includes comprehensive error handling at multiple levels:
- Input validation through Pydantic models
- Service-level error catching
- Rich error display to user
- State preservation on error

## Development Notes

- All state modifications go through State Manager
- Display Service handles all UI concerns
- AI Service manages all LLM interactions
- Game Engine orchestrates flow control