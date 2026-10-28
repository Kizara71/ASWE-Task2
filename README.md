# ASWE Task 2 – Clinic Appointments System

A modular Doctor Appointment Booking System designed and implemented using model-driven engineering principles, UML diagrams, and clean object-oriented architecture.

---

## 👥 Team Information Table

| Student ID | Full Name | Assigned Task | Branch | Pull Request Link |
|---|---|---|---|---|
| *[Student 1 ID]* | *[Student 1 Name]* | Use Cases (Student 1) | `Documentation` | *[PR Link]* |
| *[Student 2 ID]* | *[Student 2 Name]* | Class Diagram (Student 2) | `class-diagram` | *[PR Link]* |
| *[Student 3 ID]* | *[Student 3 Name]* | Sequence Diagram (Student 3) | `sequence-diagram` | *[PR Link]* |
| *[Student 4 ID]* | *[Student 4 Name]* | Implementation (Student 4) | `implementation` | *[PR Link]* |
| *[Student 5 ID]* | *[Student 5 Name]* | Docker (if applicable) | `docker-setup` | *[PR Link]* |

> **Conflict Drill:** UNCLAIMED

---

## 📌 Business Twist: Maximum Upcoming Appointments ($N$)

- **Chosen Value:** **$N = 3$**
- **Rule Definition:** A single patient is permitted to have at most **3** upcoming appointments simultaneously. If a patient attempts to schedule a fourth upcoming appointment before completing or canceling earlier ones, the system automatically rejects the request.

---

## 📁 Repository Structure & Deliverables

| File | Responsible Member | Description |
|---|---|---|
| [`requirements.txt`](./requirements.txt) | Student 1 | The 7 system requirements (R1–R7) and $N$ definition. |
| [`use_cases.md`](./use_cases.md) | Student 1 | Detailed use case specifications and main/alternative flows. |
| [`use_case_diagram.md`](./use_case_diagram.md) | Student 1 | Mermaid flowchart use case diagram. |
| `class_diagram.md` | Student 2 | Domain model & Mermaid class diagram. |
| `sequence_diagram.md` | Student 3 | Sequence diagram illustrating booking, confirmation, and alt/else flows. |
| `main.py` | Student 4 | Executable Python implementation matching both diagrams. |
| `Dockerfile` | Student 5 (Optional) | Containerization configuration (for 5-member teams). |

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
