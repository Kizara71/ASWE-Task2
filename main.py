from dataclasses import dataclass, field


@dataclass
class TimeSlot:
    slot_id: int
    date_time: str
    is_available: bool = True

    def reserve(self):
        if not self.is_available:
            return False
        self.is_available = False
        return True

    def release(self):
        self.is_available = True


@dataclass
class Doctor:
    doctor_id: int
    name: str
    specialty: str
    available_slots: list = field(default_factory=list)

    def get_available_slots(self):
        return [slot for slot in self.available_slots if slot.is_available]

    def confirm_appointment(self, appointment, accept):
        if appointment.doctor is not self or appointment.status != "PENDING":
            return False
        appointment.status = "CONFIRMED" if accept else "DECLINED"
        if not accept:
            appointment.slot.release()
        print(f"Notification for {appointment.patient.name}: Appointment {appointment.status.lower()}.")
        return True


@dataclass
class Patient:
    patient_id: int
    name: str
    upcoming_appointments: list = field(default_factory=list)

    def get_upcoming_appointments_count(self):
        return sum(a.status in ("PENDING", "CONFIRMED") for a in self.upcoming_appointments)

    def book_appointment(self, doctor, slot):
        appointment = Appointment(len(appointments) + 1, self, doctor, slot)
        message = appointment.submit()
        if appointment.status == "PENDING":
            appointments.append(appointment)
            self.upcoming_appointments.append(appointment)
        return message


@dataclass
class Appointment:
    appointment_id: int
    patient: Patient
    doctor: Doctor
    slot: TimeSlot
    status: str = "NEW"

    def submit(self):
        if self.patient.get_upcoming_appointments_count() >= 3:
            return "BOOKING_REFUSED: Maximum upcoming appointment limit (N=3) reached"
        if self.slot not in self.doctor.available_slots or not self.slot.reserve():
            return "SLOT_UNAVAILABLE: Please choose another time slot"
        self.status = "PENDING"
        return f"Appointment #{self.appointment_id} submitted. Waiting for doctor approval."

    def cancel(self):
        if self.status not in ("PENDING", "CONFIRMED"):
            return False
        self.status = "CANCELLED"
        self.slot.release()
        return True

    def get_status(self):
        return self.status


appointments = []
doctors = [
    Doctor(1, "Dr. Sara", "Cardiology", [TimeSlot(1, "2026-11-02 10:00"), TimeSlot(2, "2026-11-02 11:00")]),
    Doctor(2, "Dr. Omar", "Dermatology", [TimeSlot(3, "2026-11-03 12:00"), TimeSlot(4, "2026-11-03 13:00")]),
]
patients = [Patient(1, "Ali"), Patient(2, "Mona")]


def choose(items, description):
    for item in items:
        print(f"{item[0]}. {item[1]}")
    try:
        choice = int(input(f"Choose {description}: "))
    except ValueError:
        return None
    return next((choice for number, _ in items if number == choice), None)


def main():
    while True:
        print("\n=== Clinic Appointment System ===")
        print("1. View doctor availability\n2. Book appointment\n3. Review requests (doctor)\n4. View patient appointments\n5. Exit")
        option = input("Choose an option: ").strip()

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
                print(patient.book_appointment(doctor, slot))

        elif option == "3":
            doctor_id = choose([(d.doctor_id, d.name) for d in doctors], "doctor")
            doctor = next((d for d in doctors if d.doctor_id == doctor_id), None)
            if not doctor:
                print("Invalid doctor.")
                continue
            pending = [a for a in appointments if a.doctor is doctor and a.status == "PENDING"]
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


if __name__ == "__main__":
    main()
