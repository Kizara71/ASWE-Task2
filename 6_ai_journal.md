# AI Co-Pilot Journal & Review Log (Prompt P1–P7)

This journal documents the prompts given, human peer reviews conducted at each transition arrow, mistakes identified in AI-generated drafts, and the final verification of the running application.

---

## 1. Review Summary by Step

### Step 1: Requirements Classification (Prompt P1)
- **What we checked:** Checked each of the 7 raw requirements (R1–R7) against the definition of Functional (system behaviors/capabilities) vs. Non-Functional (qualities, security, constraints).
- **AI draft mistake identified:**
  - *What the AI did:* The AI co-pilot initially classified **R5** (*"Patient medical data shall be accessible only to authorized staff"*) as a **Functional** requirement under "Data Access".
  - *Why it was wrong:* As taught in the lab, access restrictions and confidentiality rules are **Non-Functional** quality requirements (Security & Privacy), not user interaction functions.
  - *How we noticed & corrected:* Caught during peer review against the lab slides checklist (slide 9). Reclassified R5 as `Non-Functional (Security)`.

---

### Step 2: Use Cases & Use Case Diagram (Prompts P2 & P3)
- **What we checked:** Verified actors (`Patient`, `Doctor`), system boundaries, main success flow, and alternative flows.
- **AI draft mistake identified:**
  - *What the AI did:* The AI included "System" and "DeliveryPerson / NotificationService" as external human actors in the Mermaid use case diagram.
  - *Why it was wrong:* The automated clinic engine is inside the system boundary; only external users who initiate or interact with the system are actors.
  - *How we noticed & corrected:* Placed only `Patient` and `Doctor` outside the system box as stadium nodes (`P([Patient])`, `D([Doctor])`), and modeled limit enforcement ($N = 3$) and notifications as `«extend»` use cases inside the system subgraph.

---

### Step 3: Candidate Classes & Class Diagram (Prompts P4 & P5)
- **What we checked:** Multiplicities on every association, composition vs. aggregation, attribute visibility, and method naming.
- **AI draft mistake identified:**
  - *What the AI did:* The AI drew a simple plain association `Doctor "1" -- "0..*" TimeSlot` and omitted the unit interval/date attribute on `TimeSlot`.
  - *Why it was wrong:* A `TimeSlot` in a clinic schedule cannot exist independently of the `Doctor` who offers it. Deleting or canceling a doctor's schedule destroys their slots. Therefore, it is a **Composition (`*--`)**.
  - *How we noticed & corrected:* Changed the relationship to `Doctor "1" *-- "1..*" TimeSlot : offers` and added `-dateTime: String` and `-isAvailable: bool`.

---

### Step 4: Sequence Diagram (Prompt P6)
- **What we checked:** Chronological message ordering, dashed return arrows, `alt / else` branching, and consistency with class diagram method signatures.
- **AI draft mistake identified:**
  - *What the AI did:* The AI had the Patient directly invoke `confirmAppointment()` on the Doctor, skipping the `Appointment` entity, and forgot to model what happens when the Doctor declines or when the patient exceeds limit $N$.
  - *Why it was wrong:* In the domain model, the Patient creates/submits an `Appointment`, and the `Appointment` delegates confirmation to the `Doctor`. Furthermore, declining an appointment must release the reserved time slot.
  - *How we noticed & corrected:* Restructured the sequence diagram with participants `Patient`, `Doctor`, `Appointment`, and `TimeSlot`, using nested `alt / else` blocks for:
    1. Count $\ge 3$ vs. Count $< 3$ (Limit check).
    2. Slot unavailable vs. Slot available.
    3. Doctor accepts (Confirmed) vs. Doctor declines (Declined + slot released).

---

### Step 5: Diagram to Python Code (Prompt P7)
- **What we checked:** Executability, consistency with diagram names, enforcement of $N = 3$, and automated demonstration without interactive hang.
- **AI draft mistake identified:**
  - *What the AI did:* The AI initially generated an interactive CLI with an infinite `while True: input(...)` loop as the only execution path.
  - *Why it was wrong:* Running `python main.py` non-interactively in automated test runners or CI environments resulted in `EOFError` or hung waiting for input.
  - *How we noticed & corrected:* Refactored `main.py` so that executing `python main.py` directly executes an automated end-to-end demonstration covering every branch of the sequence diagram, with an optional `--interactive` flag for manual CLI exploration. Added method aliases ensuring 100% diagram-to-code naming parity.

---

## 2. Terminal Output of `python main.py`

```text
=================================================================
CLINIC APPOINTMENT SYSTEM - AUTOMATED DEMONSTRATION (N = 3)
=================================================================

--- Step 1: Viewing Availability (R1) ---
Dr. Sara available slots: ['2026-11-02 10:00', '2026-11-02 11:00', '2026-11-02 12:00', '2026-11-02 14:00']

--- Scenario 1: Main Flow - Successful Booking & Doctor Accepts ---
Ali submits booking: Appointment #1 submitted. Waiting for doctor approval. (Status: PENDING)
[Notification] To Patient Ali: Appointment #1 with Dr. Sara is CONFIRMED.
Final Status: CONFIRMED | Slot 1 available? False

--- Scenario 2: Alternative Flow - Doctor Declines Request ---
Mona submits booking: Appointment #2 submitted. Waiting for doctor approval. (Status: PENDING)
[Notification] To Patient Mona: Appointment #2 with Dr. Sara was DECLINED. Slot released.
Final Status: DECLINED | Slot 2 available? True (released)

--- Scenario 3: Alternative Flow - Slot Already Taken ---
Mona attempts booking already-taken Slot 1: SLOT_UNAVAILABLE: Please choose another time slot
Status: REJECTED_UNAVAILABLE

--- Scenario 4: Alternative Flow - Twist Rule N = 3 Limit Reached ---
[Notification] To Patient Ali: Appointment #3 with Dr. Sara is CONFIRMED.
[Notification] To Patient Ali: Appointment #4 with Dr. Sara is CONFIRMED.
Ali's active upcoming appointments count: 3 (Limit N = 3)
Ali attempts 4th booking: BOOKING_REFUSED: Maximum upcoming appointment limit (N=3) reached
Status: REJECTED_LIMIT | Slot remains available: True

=================================================================
DEMO COMPLETE: All sequence diagram branches executed successfully.
=================================================================

Tip: Run with 'python main.py --interactive' to launch the interactive CLI.
```

---

## 3. Terminal Output of `python -m unittest`

```text
......
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
```
