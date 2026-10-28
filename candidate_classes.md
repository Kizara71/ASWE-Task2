# Candidate Domain Classes (Prompt P4)

This table records the identification and classification of candidate classes from the requirements:

| Class | Evidence in Requirements | Classification | Why / Description |
|---|---|---|---|
| **Patient** | R1, R2, R4 | **Explicit** | Explicitly named in requirements; views availability, books appointments, constrained by upcoming appointment limit $N = 3$. |
| **Doctor** | R1, R3 | **Explicit** | Explicitly named in requirements; publishes available slots, reviews and accepts/declines appointment requests. |
| **Appointment** | R2, R3, R4 | **Explicit** | Explicitly named; core transaction entity representing a scheduled meeting between a patient and a doctor. |
| **TimeSlot** | R1, R2 ("days and times when a doctor is available", "available time slot") | **Inferred** | Represents specific dates and time intervals offered by a doctor. Essential for tracking schedule availability. |
| **Payment / Billing** | None | **Rejected** | No requirement asks for payments or invoicing. |
| **MedicalRecord** | R5 ("Patient medical data") | **Rejected** | Out of scope for the appointment booking core model. |
| **NotificationService** | None | **Rejected** | Handled via method responses rather than a dedicated domain class. |
