import json
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

PREFERENCE_WINDOWS = {
    "morning": (time(6, 0), time(12, 0)),
    "afternoon": (time(12, 0), time(18, 0)),
    "evening": (time(18, 0), time(22, 0)),
}

class AppointmentScheduler:
    def __init__(self, input):
        self.providers = input.get("providers", [])
        self.start_date = datetime.fromisoformat(input["date_range"]["start_date"]).date()
        self.end_date = datetime.fromisoformat(input["date_range"]["end_date"]).date()

        self.output_timezone = ZoneInfo(input["output_timezone"])
        self.duration = timedelta(minutes=input["duration_minutes"])
        self.weekdays = self.get_weekdays_in_range()

        self.appointments = input.get("appointments", [])
        self.patient_preference = input.get("patient_preference", {})

    def get_slots(self):
        slots = []
        for provider in self.providers:
            provider_timezone = ZoneInfo(provider["timezone"])
            provider_id = provider["id"]
            provider_name = provider["name"]

            exceptions = self.get_exceptions(provider.get("exceptions", []), provider_timezone)

            for day in self.weekdays:
                for rule in provider["availability_rules"]:
                    if rule["day_of_week"] != self.weekdays[day]:
                        continue

                    y, m, d = map(int, day.split("-"))
                    sh, sm = map(int, rule["start_time"].split(":"))
                    eh, em = map(int, rule["end_time"].split(":"))

                    current = datetime(y, m, d, sh, sm, tzinfo=provider_timezone)
                    end_time = datetime(y, m, d, eh, em, tzinfo=provider_timezone)

                    while current + self.duration <= end_time:
                        slot_start = current.astimezone(self.output_timezone)
                        slot_end = (current + self.duration).astimezone(self.output_timezone)

                        if not self.is_blocked(slot_start, slot_end, exceptions):
                            slots.append({
                                "provider_id": provider_id,
                                "provider_name": provider_name,
                                "start_time": slot_start,
                                "end_time": slot_end,
                                "duration_minutes": int(self.duration.total_seconds() // 60),
                            })

                        current += self.duration

        slots = self.apply_appointments(slots)
        slots = self.apply_preference(slots)
        slots = self.format_slots(slots)

        return {"slots": slots, "total_slots": len(slots)}

    def get_weekdays_in_range(self):
        if self.start_date > self.end_date:
            return {}

        return {
            (day := self.start_date + timedelta(days=i)).strftime("%Y-%m-%d"):
                day.strftime("%A").lower()
            for i in range((self.end_date - self.start_date).days + 1)
        }

    def get_exceptions(self, exception_list, provider_tz):
        exceptions = []
        for ex in exception_list:
            y, m, d = map(int, ex["date"].split("-"))
            sh, sm = map(int, ex["start_time"].split(":"))
            eh, em = map(int, ex["end_time"].split(":"))

            start = datetime(y, m, d, sh, sm, tzinfo=provider_tz).astimezone(self.output_timezone)
            end = datetime(y, m, d, eh, em, tzinfo=provider_tz).astimezone(self.output_timezone)

            exceptions.append({
                "start_time": start,
                "end_time": end
            })
        return exceptions

    def is_blocked(self, slot_start, slot_end, exceptions):
        for ex in exceptions:
            if ex["start_time"] < slot_end and slot_start < ex["end_time"]:
                return True
        return False

    def apply_appointments(self, slots):
        filtered = []
        for slot in slots:
            taken = False
            for appt in self.appointments:
                appt_start = datetime.fromisoformat(appt["start_time"])
                appt_end = datetime.fromisoformat(appt["end_time"])

                if appt["provider_id"] == slot["provider_id"] and appt_start < slot["end_time"] and slot[
                    "start_time"] < appt_end:
                    taken = True
                    break

            if not taken:
                filtered.append(slot)
        return filtered

    def apply_preference(self, slots):
        if not self.patient_preference:
            return slots

        filtered = []
        preferred_start, preferred_end = PREFERENCE_WINDOWS[self.patient_preference["preferred_time"]]

        for slot in slots:
            slot_start_time = slot["start_time"].astimezone(self.output_timezone).time()
            if preferred_start <= slot_start_time < preferred_end:
                filtered.append(slot)

        return filtered

    def format_slots(self, slots):
        return [
            {
                "provider_id": s["provider_id"],
                "provider_name": s["provider_name"],
                "start_time": s["start_time"].isoformat(),
                "end_time": s["end_time"].isoformat(),
                "duration_minutes": s["duration_minutes"],
            }
            for s in slots
        ]

if __name__ == "__main__":
    with open("inputs/level1_input.json") as f:
        input = json.load(f)

    scheduler = AppointmentScheduler(input)
    result = scheduler.get_slots()

    with open("outputs/L1_output.json", "w") as f:
        json.dump(result, f, indent=2)
