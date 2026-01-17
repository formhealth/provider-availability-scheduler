import json

from appointment_scheduler import AppointmentScheduler

if __name__ == "__main__":
    with open("inputs/level1_input.json") as f:
        input = json.load(f)

    scheduler = AppointmentScheduler(input)
    result = scheduler.get_slots()

    with open("outputs/L1_output.json", "w") as f:
        json.dump(result, f, indent=2)