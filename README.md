# Provider Availability Scheduler - Code Challenge

Build a service that finds available appointment time slots across multiple providers, handling timezones and recurring weekly schedules.

**Time Estimate**: 30-60 minutes for a senior engineer

## The Problem

Given a list of providers with their timezones and recurring weekly availability, generate available appointment slots for a specified date range and duration.

### Requirements

**Core (Required)**:
- Parse provider availability rules (recurring weekly schedule)
- Generate time slots for the specified duration
- Handle timezone conversions correctly
- Output slots in the requested timezone

**Bonus Features** (if you finish early):
- Level 2: Handle availability exceptions (blocked time periods)
- Level 3: Filter out existing appointments
- Level 4: Filter by patient time-of-day preferences

---

## Getting Started

### 1. Review the Input Format

Check out `inputs/level1_input.json` to see the structure:

```json
{
  "providers": [
    {
      "id": "prov_123",
      "name": "Dr. Sarah Chen",
      "timezone": "America/Los_Angeles",
      "availability_rules": [
        {
          "day_of_week": "monday",
          "start_time": "09:00",
          "end_time": "17:00"
        }
      ]
    }
  ],
  "date_range": {
    "start_date": "2026-01-20",
    "end_date": "2026-01-24"
  },
  "duration_minutes": 30,
  "output_timezone": "America/Chicago"
}
```

### 2. Check the Expected Output

See `outputs/level1_output.json` for what your solution should produce:

```json
{
  "slots": [
    {
      "provider_id": "prov_123",
      "provider_name": "Dr. Sarah Chen",
      "start_time": "2026-01-20T11:00:00-06:00",
      "end_time": "2026-01-20T11:30:00-06:00",
      "duration_minutes": 30
    }
  ],
  "total_slots": 56
}
```

### 3. Build Your Solution

Create a Ruby class (or your preferred language) that:
- Takes the input parameters
- Generates slots for each provider's availability
- Converts timestamps to the output timezone
- Returns the formatted output

---

## Test Data

### Level 1: Core Slot Generation

**Input**: `inputs/level1_input.json`
- 2 providers across different timezones
- 5-day date range (Jan 20-24, 2026)
- 30-minute appointment slots
- Output timezone: America/Chicago

**Expected**: `outputs/level1_output.json`
- 56 total slots

### Level 2: Availability Exceptions

**Input**: `inputs/level2_input.json`

Providers can have exceptions (blocked time periods):

```json
{
  "exceptions": [
    {
      "type": "unavailable",
      "date": "2026-01-20",
      "start_time": "14:00",
      "end_time": "15:30"
    }
  ]
}
```

**Expected**: `outputs/level2_output.json`
- 47 slots (9 fewer due to exceptions)

### Level 3: Existing Appointments

**Input**: `inputs/level3_input.json`

Filter out slots that overlap with existing appointments:

```json
{
  "appointments": [
    {
      "provider_id": "prov_123",
      "start_time": "2026-01-20T09:00:00-08:00",
      "end_time": "2026-01-20T10:00:00-08:00"
    }
  ]
}
```

**Expected**: `outputs/level3_output.json`
- 40 slots (7 fewer due to appointments)

### Level 4: Patient Preferences

**Input**: `inputs/level4_input.json`

Filter slots based on patient's preferred time of day:

```json
{
  "patient_preference": {
    "preferred_time": "afternoon"
  }
}
```

Time preferences (in output timezone):
- **Morning**: 6:00 AM - 12:00 PM
- **Afternoon**: 12:00 PM - 6:00 PM
- **Evening**: 6:00 PM - 10:00 PM

**Expected**: `outputs/level4_output.json`
- 34 slots (only afternoon slots)

---

## Implementation Guide

### Core Algorithm

1. **For each day in the date range:**
   - Find matching day of week in availability rules
   - Generate contiguous slots (e.g., 9:00-9:30, 9:30-10:00)
   - Only include slots that fit entirely within availability window

2. **Timezone Handling:**
   - Provider availability rules are in their local timezone
   - Convert each slot to the output timezone
   - Preserve timezone offset in output (ISO 8601 format)

3. **Slot Generation Rules:**
   - Slots should be contiguous (no gaps)
   - Don't create slots that extend past the end time
   - Example: If available until 5:00 PM and duration is 30 min, last slot is 4:30-5:00 PM

### Example

**Provider**: Available Monday 9am-5pm PST
**Date Range**: Monday, Jan 20, 2026
**Duration**: 30 minutes
**Output Timezone**: CST (2 hours ahead of PST)

**Generated Slots**:
```
11:00-11:30 CST (9:00-9:30 PST)
11:30-12:00 CST (9:30-10:00 PST)
...
18:30-19:00 CST (4:30-5:00 PST)
```

Total: 16 slots

---

## Submission

### What to Include

1. **Code**: Your solution (Ruby preferred, but any language is fine)
2. **Tests**: At least 2-3 test cases showing it works
3. **README**: Brief explanation of your approach
4. **Time**: Note how long it took you

### How to Run

Provide a simple way to execute your solution:

```ruby
# example.rb
require_relative 'availability_scheduler'

input = JSON.parse(File.read('inputs/level1_input.json'))

scheduler = AvailabilityScheduler.new
slots = scheduler.find_slots(
  providers: input['providers'],
  date_range: Date.parse(input['date_range']['start_date'])..Date.parse(input['date_range']['end_date']),
  duration_minutes: input['duration_minutes'],
  output_timezone: input['output_timezone']
)

puts JSON.pretty_generate({ slots: slots, total_slots: slots.length })
```

---

## Tips

- Ruby's `ActiveSupport::TimeZone` is helpful for timezone handling
- The `tzinfo` gem provides timezone data
- Watch out for edge cases:
  - Slots that would partially extend past availability end time
  - Timezone conversions across DST boundaries
  - Phoenix (America/Phoenix) doesn't observe DST
- Performance matters: think about generating slots for a 3-month range across 50 providers

---

## Questions?

If anything is unclear, make a reasonable assumption and document it in your README. We're more interested in seeing how you think through problems than getting every edge case perfect.

Good luck! 🚀
