# Use Cases Specification: Clinic Appointments System

## Context & Actors
- **Primary Actors:**
  - **Patient:** Views available doctor slots and requests appointment bookings.
  - **Doctor:** Manages schedule, reviews incoming booking requests, and accepts or declines them.
- **Secondary / Supporting Actor:**
  - **System (Automated Clinic Engine):** Verifies constraints (such as the limit of $N=3$ upcoming appointments) and sends notifications.

---

## 1. Use Cases Summary

| UC ID | Name | Primary Actor | Requirement | Use Case Description |
|---|---|---|---|---|
| **UC1** | View Doctor Availability | Patient | R1 | As a Patient, I can browse available dates and time slots for a specific doctor. |
| **UC2** | Book Appointment | Patient | R2 | As a Patient, I can request an appointment for a selected available time slot. |
| **UC3** | Review Appointment Request | Doctor | R3 | As a Doctor, I can accept or decline an incoming appointment request. |
| **UC4** | Enforce Upcoming Appointment Limit | System | R4 | As the System, I ensure that a patient has at most $N$ ($N = 3$) upcoming appointments at any given time. |
| **UC5** | Notify Decision | System | R3 | As the System, I notify the patient whether their appointment request was confirmed or declined. |

---

## 2. Detailed Flow of Events: UC2 - Book Appointment

### Main Success Flow
1. **Patient** browses doctor availability and selects a desired date and time slot (R1).
2. **Patient** submits a booking request for the selected slot (R2).
3. **System** verifies that the patient currently has fewer than $N$ ($N = 3$) upcoming appointments (R4).
4. **System** validates that the requested slot is currently free and marks it as `PENDING`.
5. **Doctor** receives the appointment request, reviews it, and chooses to **accept** (R3).
6. **System** updates the appointment status to `CONFIRMED`.
7. **System** notifies the patient with the confirmation details (UC5).

---

### Alternative Flows

#### Alternative Flow 3a: Maximum Upcoming Appointment Limit Reached ($N = 3$)
- **3a1.** At Step 3, the System checks the patient's existing active upcoming appointments and finds the count is already equal to $N$ ($N = 3$).
- **3a2.** The System blocks the booking request with the error: `"BOOKING_REFUSED: Maximum upcoming appointment limit (N=3) reached"`.
- **3a3.** The time slot remains unchanged (`AVAILABLE`).
- **3a4.** The use case ends in failure.

#### Alternative Flow 4a: Selected Time Slot Is No Longer Available
- **4a1.** At Step 4, the System checks the selected time slot and finds it has just been reserved by another patient or blocked by the clinic.
- **4a2.** The System notifies the patient: `"SLOT_UNAVAILABLE: Please choose another time slot"`.
- **4a3.** The patient is returned to Step 1 to select another slot.

#### Alternative Flow 5a: Doctor Declines Appointment Request
- **5a1.** At Step 5, the Doctor reviews the request and chooses to **decline** (e.g., due to an urgent surgery or scheduling conflict).
- **5a2.** The System marks the appointment status as `DECLINED`.
- **5a3.** The System releases the time slot back to `AVAILABLE`.
- **5a4.** The System notifies the patient that the booking was declined (UC5).
- **5a5.** The use case ends.
