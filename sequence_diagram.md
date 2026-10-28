# Clinic Appointments System — Appointment Booking Sequence Diagram

This sequence diagram illustrates the appointment booking process using the `Patient`, `Doctor`, `Appointment`, and `TimeSlot` classes.

```mermaid
sequenceDiagram
    autonumber

    actor P as Patient
    participant D as Doctor
    participant A as Appointment
    participant T as TimeSlot

    P->>D: getAvailableSlots()
    D-->>P: List of available TimeSlots

    P->>P: bookAppointment(doctor, slot)
    P->>A: submit()

    A->>P: getUpcomingAppointmentsCount()
    P-->>A: count

    alt count >= 3
        A-->>P: Booking rejected (limit reached)
    else count < 3
        A->>T: Check isAvailable

        alt Slot unavailable
            T-->>A: false
            A-->>P: Booking rejected (slot unavailable)
        else Slot available
            T-->>A: true
            A->>T: reserve()
            T-->>A: true

            Note over A,D: Appointment status: Pending

            A->>D: confirmAppointment(appointment, accept)

            alt Doctor accepts
                D-->>A: true
                Note over A: Status: Confirmed
                A-->>P: Appointment confirmed
            else Doctor declines
                D-->>A: false
                Note over A: Status: Declined
                A->>T: release()
                T-->>A: Slot available again
                A-->>P: Appointment declined
            end
        end
    end
```

## Booking flow

1. The patient views available slots using `Doctor.getAvailableSlots()`.
2. The patient selects a slot and submits an appointment request.
3. The appointment checks whether the patient has fewer than three upcoming appointments.
4. The appointment checks the selected slot's availability.
5. If available, the slot is reserved and the appointment becomes pending.
6. The doctor accepts or declines the request. If declined, the reserved slot is released.

## Design assumptions

- The selected slot is reserved while the appointment awaits the doctor's decision.
- Declining an appointment releases its reserved slot.
- The availability check reads the `isAvailable` attribute; it is not a separately defined public method in the class diagram.
