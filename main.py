"""
Clinic Appointments System
ASWE Task 2 - Implementation (Student 4)

Implements the domain classes and workflows designed in the UML Class Diagram (Student 2)
and Sequence Diagram (Student 3). Enforces the business twist rule (N = 3 maximum upcoming appointments).
"""

from dataclasses import dataclass, field
import sys
from typing import List, Optional


@dataclass
class TimeSlot:
    slot_id: int
    date_time: str
    is_available: bool = True

    # Diagram method aliases
    @property
    def slotId(self) -> int:
        return self.slot_id

    @property
    def dateTime(self) -> str:
        return self.date_time

    @property
    def isAvailable(self) -> bool:
        return self.is_available

    def reserve(self) -> bool:
        """Reserves this time slot if it is available."""
        if not self.is_available:
            return False
        self.is_available = False
        return True

    def release(self) -> None:
        """Releases the reservation, marking the slot available again."""
        self.is_available = True

    def get_date_time(self) -> str:
        return self.date_time

    # CamelCase alias matching UML Class Diagram
    getDateTime = get_date_time


@dataclass
class Doctor:
    doctor_id: int
    name: str
    specialty: str
    available_slots: List[TimeSlot] = field(default_factory=list)

    # Diagram attribute aliases
    @property
    def doctorId(self) -> int:
        return self.doctor_id

    @property
    def availableSlots(self) -> List[TimeSlot]:
        return self.available_slots

    def get_available_slots(self) -> List[TimeSlot]:
        """Returns list of time slots that are currently available."""
        return [slot for slot in self.available_slots if slot.is_available]

    # CamelCase alias matching UML Class Diagram
    getAvailableSlots = get_available_slots

    def confirm_appointment(self, appointment: "Appointment", accept: bool) -> bool:
        """Doctor confirms (accepts) or declines an appointment request."""
        if appointment.doctor is not self or appointment.status != "PENDING":
            return False
        if accept:
            appointment.status = "CONFIRMED"
            print(f"[Notification] To Patient {appointment.patient.name}: Appointment #{appointment.appointment_id} with {self.name} is CONFIRMED.")
        else:
            appointment.status = "DECLINED"
            appointment.slot.release()
            print(f"[Notification] To Patient {appointment.patient.name}: Appointment #{appointment.appointment_id} with {self.name} was DECLINED. Slot released.")
        return accept

    # CamelCase alias matching UML Class Diagram
    confirmAppointment = confirm_appointment


@dataclass
class Patient:
    patient_id: int
    name: str
    upcoming_appointments: List["Appointment"] = field(default_factory=list)

    # Diagram attribute aliases
    @property
    def patientId(self) -> int:
        return self.patient_id

    @property
    def upcomingAppointments(self) -> List["Appointment"]:
        return self.upcoming_appointments

    def get_upcoming_appointments_count(self) -> int:
        """Returns the number of active upcoming appointments (PENDING or CONFIRMED)."""
        return sum(1 for a in self.upcoming_appointments if a.status in ("PENDING", "CONFIRMED"))

    # CamelCase alias matching UML Class Diagram
    getUpcomingAppointmentsCount = get_upcoming_appointments_count

    def book_appointment(self, doctor: Doctor, slot: TimeSlot) -> "Appointment":
        """Initiates booking an appointment for an available slot."""
        appointment = Appointment(
            appointment_id=len(global_appointments) + 1,
            patient=self,
            doctor=doctor,
            slot=slot
        )
        return appointment

    # CamelCase alias matching UML Class Diagram
    bookAppointment = book_appointment


@dataclass
class Appointment:
    appointment_id: int
    patient: Patient
    doctor: Doctor
    slot: TimeSlot
    status: str = "NEW"

    # Diagram attribute aliases
    @property
    def appointmentId(self) -> int:
        return self.appointment_id

    def submit(self) -> str:
        """
        Executes the appointment submission flow:
        1. Checks upcoming appointment limit N = 3.
        2. Checks slot availability and reserves it.
        3. Sets status to PENDING.
        """
        # Limit rule check (R4: at most N = 3 upcoming appointments)
        if self.patient.get_upcoming_appointments_count() >= 3:
            self.status = "REJECTED_LIMIT"
            return "BOOKING_REFUSED: Maximum upcoming appointment limit (N=3) reached"

        # Slot availability check
        if self.slot not in self.doctor.available_slots or not self.slot.reserve():
            self.status = "REJECTED_UNAVAILABLE"
            return "SLOT_UNAVAILABLE: Please choose another time slot"

        self.status = "PENDING"
        if self not in global_appointments:
            global_appointments.append(self)
        if self not in self.patient.upcoming_appointments:
            self.patient.upcoming_appointments.append(self)

        return f"Appointment #{self.appointment_id} submitted. Waiting for doctor approval."

    def cancel(self) -> bool:
        """Cancels a pending or confirmed appointment and frees the slot."""
        if self.status not in ("PENDING", "CONFIRMED"):
            return False
        self.status = "CANCELLED"
        self.slot.release()
        return True

    def get_status(self) -> str:
        return self.status

    # CamelCase alias matching UML Class Diagram
    getStatus = get_status


# Global state store for demonstration and CLI
global_appointments: List[Appointment] = []
doctors: List[Doctor] = [
    Doctor(1, "Dr. Sara", "Cardiology", [
        TimeSlot(1, "2026-11-02 10:00"),
        TimeSlot(2, "2026-11-02 11:00"),
        TimeSlot(3, "2026-11-02 12:00"),
        TimeSlot(4, "2026-11-02 14:00"),
    ]),
    Doctor(2, "Dr. Omar", "Dermatology", [
        TimeSlot(5, "2026-11-03 09:00"),
        TimeSlot(6, "2026-11-03 10:00"),
    ]),
]
patients: List[Patient] = [
    Patient(1, "Ali"),
    Patient(2, "Mona"),
]


def run_demo():
    """
    Automated demonstration executing all sequence diagram branches:
    - Branch 1: Successful booking & Doctor accepts (CONFIRMED)
    - Branch 2: Doctor declines request (DECLINED, slot released)
    - Branch 3: Twist rule N = 3 limit reached (BOOKING_REFUSED)
    - Branch 4: Slot already taken (SLOT_UNAVAILABLE)
    """
    print("=" * 65)
    print("CLINIC APPOINTMENT SYSTEM - AUTOMATED DEMONSTRATION (N = 3)")
    print("=" * 65)

    dr_sara = doctors[0]
    dr_omar = doctors[1]
    ali = patients[0]
    mona = patients[1]

    # 1. View availability (R1)
    print("\n--- Step 1: Viewing Availability (R1) ---")
    available_sara = dr_sara.get_available_slots()
    print(f"Dr. Sara available slots: {[s.date_time for s in available_sara]}")

    # 2. Main Success Flow (CONFIRMED)
    print("\n--- Scenario 1: Main Flow - Successful Booking & Doctor Accepts ---")
    slot1 = available_sara[0]
    app1 = ali.book_appointment(dr_sara, slot1)
    submit_msg1 = app1.submit()
    print(f"Ali submits booking: {submit_msg1} (Status: {app1.get_status()})")
    dr_sara.confirm_appointment(app1, accept=True)
    print(f"Final Status: {app1.get_status()} | Slot 1 available? {slot1.is_available}")

    # 3. Alternative Flow - Doctor Declines (DECLINED)
    print("\n--- Scenario 2: Alternative Flow - Doctor Declines Request ---")
    slot2 = available_sara[1]
    app2 = mona.book_appointment(dr_sara, slot2)
    submit_msg2 = app2.submit()
    print(f"Mona submits booking: {submit_msg2} (Status: {app2.get_status()})")
    dr_sara.confirm_appointment(app2, accept=False)
    print(f"Final Status: {app2.get_status()} | Slot 2 available? {slot2.is_available} (released)")

    # 4. Alternative Flow - Slot Unavailable
    print("\n--- Scenario 3: Alternative Flow - Slot Already Taken ---")
    app_conflict = mona.book_appointment(dr_sara, slot1)  # slot1 is already reserved by app1
    conflict_msg = app_conflict.submit()
    print(f"Mona attempts booking already-taken Slot 1: {conflict_msg}")
    print(f"Status: {app_conflict.get_status()}")

    # 5. Alternative Flow - Maximum Limit Reached (N = 3)
    print("\n--- Scenario 4: Alternative Flow - Twist Rule N = 3 Limit Reached ---")
    # Ali books 2 more appointments to reach N = 3 upcoming appointments
    slot3 = available_sara[2]
    slot4 = available_sara[3]
    app3 = ali.book_appointment(dr_sara, slot3)
    app3.submit()
    dr_sara.confirm_appointment(app3, accept=True)

    app4 = ali.book_appointment(dr_sara, slot4)
    app4.submit()
    dr_sara.confirm_appointment(app4, accept=True)

    print(f"Ali's active upcoming appointments count: {ali.get_upcoming_appointments_count()} (Limit N = 3)")

    # Ali attempts to book a 4th appointment
    slot_omar = dr_omar.get_available_slots()[0]
    app5 = ali.book_appointment(dr_omar, slot_omar)
    limit_msg = app5.submit()
    print(f"Ali attempts 4th booking: {limit_msg}")
    print(f"Status: {app5.get_status()} | Slot remains available: {slot_omar.is_available}")

    print("\n" + "=" * 65)
    print("DEMO COMPLETE: All sequence diagram branches executed successfully.")
    print("=" * 65)


def choose(items, description):
    for item in items:
        print(f"{item[0]}. {item[1]}")
    try:
        choice = int(input(f"Choose {description}: "))
    except (ValueError, EOFError):
        return None
    return next((choice for number, _ in items if number == choice), None)


def interactive_menu():
    """Interactive CLI menu for manual exploration."""
    while True:
        print("\n=== Clinic Appointment System ===")
        print("1. View doctor availability")
        print("2. Book appointment")
        print("3. Review requests (doctor)")
        print("4. View patient appointments")
        print("5. Exit")
        try:
            option = input("Choose an option: ").strip()
        except EOFError:
            break

        if option in ("1", "2"):
            doctor_id = choose([(d.doctor_id, f"{d.name} ({d.specialty})") for d in doctors], "doctor")
            doctor = next((d for d in doctors if d.doctor_id == doctor_id), None)
            if not doctor:
                print("Invalid doctor.")
                continue
            slots = doctor.get_available_slots()
            if not slots:
                print("No available slots.")
                continue
            if option == "1":
                for slot in slots:
                    print(f"{slot.slot_id}. {slot.date_time}")
            else:
                patient_id = choose([(p.patient_id, p.name) for p in patients], "patient")
                patient = next((p for p in patients if p.patient_id == patient_id), None)
                if not patient:
                    print("Invalid patient.")
                    continue
                slot_id = choose([(s.slot_id, s.date_time) for s in slots], "slot")
                slot = next((s for s in doctor.available_slots if s.slot_id == slot_id), None)
                if not slot:
                    print("Invalid slot.")
                    continue
                appointment = patient.book_appointment(doctor, slot)
                print(appointment.submit())

        elif option == "3":
            doctor_id = choose([(d.doctor_id, d.name) for d in doctors], "doctor")
            doctor = next((d for d in doctors if d.doctor_id == doctor_id), None)
            if not doctor:
                print("Invalid doctor.")
                continue
            pending = [a for a in global_appointments if a.doctor is doctor and a.status == "PENDING"]
            if not pending:
                print("No pending requests.")
                continue
            appointment_id = choose([(a.appointment_id, f"{a.patient.name} - {a.slot.date_time}") for a in pending], "appointment")
            appointment = next((a for a in pending if a.appointment_id == appointment_id), None)
            if not appointment:
                print("Invalid appointment.")
                continue
            decision = input("Accept or decline? (a/d): ").strip().lower()
            if decision in ("a", "d"):
                doctor.confirm_appointment(appointment, decision == "a")
            else:
                print("Invalid decision.")

        elif option == "4":
            patient_id = choose([(p.patient_id, p.name) for p in patients], "patient")
            patient = next((p for p in patients if p.patient_id == patient_id), None)
            if not patient:
                print("Invalid patient.")
                continue
            if not patient.upcoming_appointments:
                print("No appointment history.")
            for appointment in patient.upcoming_appointments:
                print(f"#{appointment.appointment_id}: {appointment.doctor.name}, {appointment.slot.date_time} - {appointment.get_status()}")

        elif option == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


def main():
    if "--interactive" in sys.argv or "-i" in sys.argv:
        interactive_menu()
    else:
        run_demo()
        print("\nTip: Run with 'python main.py --interactive' to launch the interactive CLI.")


if __name__ == "__main__":
    main()
