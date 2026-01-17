from appointment_scheduler import AppointmentScheduler

def base_input():
    return {
        "providers": [
            {
                "id": 1,
                "name": "Dr. Smith",
                "timezone": "America/New_York",
                "availability_rules": [
                    {"day_of_week": "monday", "start_time": "09:00", "end_time": "11:00"}
                ],
                "exceptions": []
            }
        ],
        "date_range": {"start_date": "2025-01-06", "end_date": "2025-01-06"},
        "output_timezone": "America/New_York",
        "duration_minutes": 30,
        "appointments": [],
        "patient_preference": {}
    }

def test_basic_slot_generation():
    data = base_input()
    scheduler = AppointmentScheduler(data)
    result = scheduler.get_slots()

    assert result["total_slots"] == 4

def test_exception_blocks_slot():
    data = base_input()
    data["providers"][0]["exceptions"] = [
        {"date": "2025-01-06", "start_time": "09:30", "end_time": "10:00"}
    ]

    scheduler = AppointmentScheduler(data)
    result = scheduler.get_slots()

    assert result["total_slots"] == 3

def test_appointment_blocks_slot():
    data = base_input()
    data["appointments"] = [
        {
            "provider_id": 1,
            "start_time": "2025-01-06T10:00:00-05:00",
            "end_time": "2025-01-06T10:30:00-05:00"
        }
    ]
    scheduler = AppointmentScheduler(data)
    result = scheduler.get_slots()

    assert result["total_slots"] == 3

def test_preference_filters_out_non_matching_slots():
    data = base_input()
    data["patient_preference"] = {"preferred_time": "evening"}

    scheduler = AppointmentScheduler(data)
    result = scheduler.get_slots()

    assert result["total_slots"] == 0