# Use Case Diagram: Clinic Appointments System

This diagram visualizes the primary actors, system boundary, and use cases according to the lab methodology.

```mermaid
flowchart LR
    P([Patient])
    D([Doctor])

    subgraph ClinicSystem["Clinic Appointment System"]
        UC1["UC1: View Doctor Availability"]
        UC2["UC2: Book Appointment"]
        UC3["UC3: Review Appointment Request"]
        UC4["UC4: Enforce Limit (N=3)"]
        UC5["UC5: Notify Decision"]
    end

    %% Actor Associations
    P --- UC1
    P --- UC2
    UC3 --- D

    %% Extensions
    UC4 -.->|"«extend»"| UC2
    UC5 -.->|"«extend»"| UC3
```

### Explanation of Diagram Elements
- **Actors outside boundary:** `Patient` and `Doctor` interact with the system.
- **System boundary:** The box represents the `Clinic Appointment System`.
- **Primary Use Cases:**
  - `UC1` and `UC2` are triggered by the **Patient**.
  - `UC3` is handled by the **Doctor**.
- **Extension Use Cases:**
  - `UC4` (`Enforce Limit N=3`) extends `UC2` as a condition check before booking is accepted.
  - `UC5` (`Notify Decision`) extends `UC3` to dispatch acceptance or rejection notifications.
