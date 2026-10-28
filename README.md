# ASWE Task 2 – Clinic Appointments System

A modular Doctor Appointment Booking System designed and implemented using model-driven engineering principles, UML diagrams, and clean object-oriented architecture.

---

## 👥 Team Information Table

| Student ID | Full Name | Assigned Task | Branch | Pull Request Link |
|---|---|---|---|---|
| 20240149 | Joy Magdy | Use Cases (Student 1) | `Documentation` | *[Pending PR]* |
| 20240149 | Joy Magdy | Class Diagram (Student 2) | `Class-Diagrams` | *[Pending PR]* |
| 20240094 | Andrew Remon | Sequence Diagram (Student 3) | `sequence-diagram` | *[Pending PR]* |
| 20240094 | Andrew Remon | Implementation (Student 4) | `implementation` | *[Pending PR]* |

> **Note:** As per instructions for 2-member teams, tasks are shared between the two members, and Docker is optional (not required for teams of 2–4).

> **Conflict Drill:** Joy Magdy, Andrew Remon

---

## 📌 Business Twist: Maximum Upcoming Appointments ($N$)

- **Chosen Value:** **$N = 3$**
- **Rule Definition:** A single patient is permitted to have at most **3** upcoming appointments simultaneously. If a patient attempts to schedule a fourth upcoming appointment before completing or canceling earlier ones, the system automatically rejects the request.

---

## 📁 Repository Structure & Deliverables

| File | Responsible Member | Description |
|---|---|---|
| [`requirements.txt`](./requirements.txt) | Joy Magdy (Student 1) | The 7 system requirements (R1–R7) and $N$ definition. |
| [`use_cases.md`](./use_cases.md) | Joy Magdy (Student 1) | Detailed use case specifications and main/alternative flows. |
| [`use_case_diagram.md`](./use_case_diagram.md) | Joy Magdy (Student 1) | Mermaid flowchart use case diagram. |
| `class_diagram.md` | Joy Magdy (Student 2) | Domain model & Mermaid class diagram. |
| `sequence_diagram.md` | Andrew Remon (Student 3) | Sequence diagram illustrating booking, confirmation, and alt/else flows. |
| `main.py` | Andrew Remon (Student 4) | Executable Python implementation matching both diagrams. |

---

## 🚀 How to Run the Application

### Prerequisites
- Python 3.8+ installed.

### Execution
Run the standalone simulation script:
```bash
python main.py
```
*(The script demonstrates doctor availability browsing, successful appointment bookings, appointment acceptance/decline by doctors, and enforcement of the $N=3$ appointment limit).*
