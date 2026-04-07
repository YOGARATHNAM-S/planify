# Planify Process Flow & Architecture Diagram

To view this diagram as a clear image, **right-click anywhere in this file and select "Open Preview"** (or click the magnifying glass with a split-screen icon in the top right corner of VS Code).

```mermaid
graph TD
    %% Styling
    classDef user fill:#ff9999,stroke:#333,stroke-width:2px,color:black,font-weight:bold;
    classDef interface fill:#99ccff,stroke:#333,stroke-width:1px,color:black;
    classDef ai fill:#e6ccff,stroke:#333,stroke-width:1px,color:black;
    classDef tool fill:#ccffcc,stroke:#333,stroke-width:1px,color:black;
    classDef db fill:#ffcc99,stroke:#333,stroke-width:2px,color:black,font-weight:bold;

    User((User)):::user

    subgraph Client_Interfaces [Client Interfaces]
        Chat[AI Chat Interface]:::interface
        REST[REST APIs Endpoint]:::interface
    end

    subgraph AI_Layer [AI Orchestration Layer / ADK]
        Root[Root Agent]:::ai
        Flow[Workflow Agent]:::ai
        Gemini[Workspace Agent / Gemini]:::ai
    end

    subgraph Tool_Layer [MCP Capabilities]
        TaskTools[Task Manager APP]:::tool
        NoteTools[Notes Manager APP]:::tool
        CalTools[Calendar Manager APP]:::tool
    end

    Database[(Google Cloud Datastore)]:::db

    %% Connections
    User -->|Natural Language| Chat
    User -->|JSON Data| REST

    Chat --> Root
    Root --> Flow
    Flow --> Gemini

    Gemini -->|Extracts Intent & Routes| TaskTools
    Gemini -->|Extracts Intent & Routes| NoteTools
    Gemini -->|Extracts Intent & Routes| CalTools

    REST -->|Direct CRUD| TaskTools
    REST -->|Direct CRUD| NoteTools
    REST -->|Direct CRUD| CalTools

    TaskTools <-->|Read / Write| Database
    NoteTools <-->|Read / Write| Database
    CalTools <-->|Read / Write| Database
```