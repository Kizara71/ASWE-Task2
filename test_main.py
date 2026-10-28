"""
Unit tests for Clinic Appointments System (Bonus)
Tests all main and alternative branches from the sequence diagram and class diagram.
"""

import unittest
from main import Patient, Doctor, Appointment, TimeSlot


class TestClinicAppointmentSystem(unittest.TestCase):

    def setUp(self):
        self.slot1 = TimeSlot(1, "2026-11-02 10:00")
        self.slot2 = TimeSlot(2, "2026-11-02 11:00")
        self.slot3 = TimeSlot(3, "2026-11-02 12:00")
        self.slot4 = TimeSlot(4, "2026-11-02 13:00")
        self.doctor = Doctor(1, "Dr. Sara", "Cardiology", [self.slot1, self.slot2, self.slot3, self.slot4])
        self.patient = Patient(1, "Ali")

    def test_view_availability(self):
        """R1: Patient can view available slots."""
        available = self.doctor.get_available_slots()
        self.assertEqual(len(available), 4)
        self.slot1.reserve()
        available = self.doctor.get_available_slots()
        self.assertEqual(len(available), 3)

    def test_successful_booking_and_doctor_accept(self):
        """R2, R3: Main flow - Booking submitted and doctor confirms."""
        app = self.patient.book_appointment(self.doctor, self.slot1)
        msg = app.submit()
        self.assertEqual(app.get_status(), "PENDING")
        self.assertFalse(self.slot1.is_available)

        decision = self.doctor.confirm_appointment(app, accept=True)
        self.assertTrue(decision)
        self.assertEqual(app.get_status(), "CONFIRMED")

    def test_doctor_declines_appointment(self):
        """R3, Alt 5a: Doctor declines request; slot is released."""
        app = self.patient.book_appointment(self.doctor, self.slot2)
        app.submit()
        self.assertEqual(app.get_status(), "PENDING")
        self.assertFalse(self.slot2.is_available)

        decision = self.doctor.confirm_appointment(app, accept=False)
        self.assertFalse(decision)
        self.assertEqual(app.get_status(), "DECLINED")
        self.assertTrue(self.slot2.is_available)  # Slot must be released

    def test_slot_already_taken(self):
        """Alt 4a: Booking unavailable slot is rejected."""
        self.slot1.reserve()
        app = self.patient.book_appointment(self.doctor, self.slot1)
        msg = app.submit()
        self.assertIn("SLOT_UNAVAILABLE", msg)
        self.assertEqual(app.get_status(), "REJECTED_UNAVAILABLE")

    def test_maximum_upcoming_appointments_limit_n3(self):
        """R4, Alt 3a: Patient cannot exceed N = 3 upcoming appointments."""
        # Book 3 appointments successfully
        app1 = self.patient.book_appointment(self.doctor, self.slot1)
        app1.submit()
        self.doctor.confirm_appointment(app1, accept=True)

        app2 = self.patient.book_appointment(self.doctor, self.slot2)
        app2.submit()
        self.doctor.confirm_appointment(app2, accept=True)

        app3 = self.patient.book_appointment(self.doctor, self.slot3)
        app3.submit()
        self.doctor.confirm_appointment(app3, accept=True)

        self.assertEqual(self.patient.get_upcoming_appointments_count(), 3)

        # 4th booking attempt must be refused
        app4 = self.patient.book_appointment(self.doctor, self.slot4)
        msg = app4.submit()
        self.assertIn("BOOKING_REFUSED", msg)
        self.assertEqual(app4.get_status(), "REJECTED_LIMIT")
        self.assertTrue(self.slot4.is_available)

    def test_appointment_cancellation(self):
        """Test cancellation frees the reserved slot."""
        app = self.patient.book_appointment(self.doctor, self.slot1)
        app.submit()
        self.assertFalse(self.slot1.is_available)
        cancelled = app.cancel()
        self.assertTrue(cancelled)
        self.assertEqual(app.get_status(), "CANCELLED")
        self.assertTrue(self.slot1.is_available)


if __name__ == "__main__":
    unittest.main()
