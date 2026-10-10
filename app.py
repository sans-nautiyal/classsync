import json
import os

import pandas as pd
import streamlit as st

st.set_page_config(page_title="ClassSync", page_icon="📅", layout="wide")

# =====================================================
# 1. DATA  (replace with your department's real data)
# =====================================================
DATA_FILE = "data.json"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
START_HOUR, END_HOUR = 9, 17          # college hours: 9:00 to 17:00
LUNCH_HOUR = 13                       # 13:00 - 14:00 is never suggested

teachers = {
    "t1": "Dr. Sharma",
    "t2": "Prof. Verma",
    "t3": "Dr. Singh",
    "t4": "Dr. Mehta",
    "t5": "Prof. Kapoor",
}
sections = ["EE-1A", "EE-1B", "EE-1C", "EE-1D", "EE-1E"]
rooms = {
    "r1": {"name": "Room 101", "smart_board": True},
    "r2": {"name": "Room 102", "smart_board": False},
    "r3": {"name": "Room 201", "smart_board": True},
    "r4": {"name": "Room 202", "smart_board": False},
    "r5": {"name": "Room 301", "smart_board": True},
    "r6": {"name": "Room 302", "smart_board": False},
}

# One line per class: (day, start hour, subject, teacher id, section, room id)
# Each class is 1 hour long. Start hour is 24h format: 9 means 9:00, 14 means 2 PM.
# To add a class, copy a line and change its values. Lunch break is 13:00 - 14:00.
CLASSES = [
    # ---- Monday ----
    ("Monday", 9, "Maths", "t1", "EE-1A", "r1"),
    ("Monday", 11, "Physics", "t2", "EE-1A", "r2"),
    ("Monday", 14, "C Programming", "t3", "EE-1A", "r3"),
    ("Monday", 10, "Physics", "t2", "EE-1B", "r2"),
    ("Monday", 12, "C Programming", "t3", "EE-1B", "r3"),
    ("Monday", 15, "Circuits", "t4", "EE-1B", "r4"),
    ("Monday", 9, "C Programming", "t3", "EE-1C", "r3"),
    ("Monday", 11, "Circuits", "t4", "EE-1C", "r4"),
    ("Monday", 14, "English", "t5", "EE-1C", "r5"),
    ("Monday", 10, "Circuits", "t4", "EE-1D", "r4"),
    ("Monday", 12, "English", "t5", "EE-1D", "r5"),
    ("Monday", 15, "Maths", "t1", "EE-1D", "r6"),
    ("Monday", 9, "English", "t5", "EE-1E", "r5"),
    ("Monday", 11, "Maths", "t1", "EE-1E", "r6"),
    ("Monday", 14, "Physics", "t2", "EE-1E", "r1"),
    # ---- Tuesday ----
    ("Tuesday", 10, "Physics", "t2", "EE-1A", "r1"),
    ("Tuesday", 12, "C Programming", "t3", "EE-1A", "r2"),
    ("Tuesday", 15, "Circuits", "t4", "EE-1A", "r3"),
    ("Tuesday", 9, "C Programming", "t3", "EE-1B", "r2"),
    ("Tuesday", 11, "Circuits", "t4", "EE-1B", "r3"),
    ("Tuesday", 14, "English", "t5", "EE-1B", "r4"),
    ("Tuesday", 10, "Circuits", "t4", "EE-1C", "r3"),
    ("Tuesday", 12, "English", "t5", "EE-1C", "r4"),
    ("Tuesday", 15, "Maths", "t1", "EE-1C", "r5"),
    ("Tuesday", 9, "English", "t5", "EE-1D", "r4"),
    ("Tuesday", 11, "Maths", "t1", "EE-1D", "r5"),
    ("Tuesday", 14, "Physics", "t2", "EE-1D", "r6"),
    ("Tuesday", 10, "Maths", "t1", "EE-1E", "r5"),
    ("Tuesday", 12, "Physics", "t2", "EE-1E", "r6"),
    ("Tuesday", 15, "C Programming", "t3", "EE-1E", "r1"),
    # ---- Wednesday ----
    ("Wednesday", 9, "C Programming", "t3", "EE-1A", "r1"),
    ("Wednesday", 11, "Circuits", "t4", "EE-1A", "r2"),
    ("Wednesday", 14, "English", "t5", "EE-1A", "r3"),
    ("Wednesday", 10, "Circuits", "t4", "EE-1B", "r2"),
    ("Wednesday", 12, "English", "t5", "EE-1B", "r3"),
    ("Wednesday", 15, "Maths", "t1", "EE-1B", "r4"),
    ("Wednesday", 9, "English", "t5", "EE-1C", "r3"),
    ("Wednesday", 11, "Maths", "t1", "EE-1C", "r4"),
    ("Wednesday", 14, "Physics", "t2", "EE-1C", "r5"),
    ("Wednesday", 10, "Maths", "t1", "EE-1D", "r4"),
    ("Wednesday", 12, "Physics", "t2", "EE-1D", "r5"),
    ("Wednesday", 15, "C Programming", "t3", "EE-1D", "r6"),
    ("Wednesday", 9, "Physics", "t2", "EE-1E", "r5"),
    ("Wednesday", 11, "C Programming", "t3", "EE-1E", "r6"),
    ("Wednesday", 14, "Circuits", "t4", "EE-1E", "r1"),
    # ---- Thursday ----
    ("Thursday", 10, "Circuits", "t4", "EE-1A", "r1"),
    ("Thursday", 12, "English", "t5", "EE-1A", "r2"),
    ("Thursday", 15, "Maths", "t1", "EE-1A", "r3"),
    ("Thursday", 9, "English", "t5", "EE-1B", "r2"),
    ("Thursday", 11, "Maths", "t1", "EE-1B", "r3"),
    ("Thursday", 14, "Physics", "t2", "EE-1B", "r4"),
    ("Thursday", 10, "Maths", "t1", "EE-1C", "r3"),
    ("Thursday", 12, "Physics", "t2", "EE-1C", "r4"),
    ("Thursday", 15, "C Programming", "t3", "EE-1C", "r5"),
    ("Thursday", 9, "Physics", "t2", "EE-1D", "r4"),
    ("Thursday", 11, "C Programming", "t3", "EE-1D", "r5"),
    ("Thursday", 14, "Circuits", "t4", "EE-1D", "r6"),
    ("Thursday", 10, "C Programming", "t3", "EE-1E", "r5"),
    ("Thursday", 12, "Circuits", "t4", "EE-1E", "r6"),
    ("Thursday", 15, "English", "t5", "EE-1E", "r1"),
    # ---- Friday ----
    ("Friday", 9, "English", "t5", "EE-1A", "r1"),
    ("Friday", 11, "Maths", "t1", "EE-1A", "r2"),
    ("Friday", 14, "Physics", "t2", "EE-1A", "r3"),
    ("Friday", 10, "Maths", "t1", "EE-1B", "r2"),
    ("Friday", 12, "Physics", "t2", "EE-1B", "r3"),
    ("Friday", 15, "C Programming", "t3", "EE-1B", "r4"),
    ("Friday", 9, "Physics", "t2", "EE-1C", "r3"),
    ("Friday", 11, "C Programming", "t3", "EE-1C", "r4"),
    ("Friday", 14, "Circuits", "t4", "EE-1C", "r5"),
    ("Friday", 10, "C Programming", "t3", "EE-1D", "r4"),
    ("Friday", 12, "Circuits", "t4", "EE-1D", "r5"),
    ("Friday", 15, "English", "t5", "EE-1D", "r6"),
    ("Friday", 9, "Circuits", "t4", "EE-1E", "r5"),
    ("Friday", 11, "English", "t5", "EE-1E", "r6"),
    ("Friday", 14, "Maths", "t1", "EE-1E", "r1"),
]

DEFAULT_TIMETABLE = [
    {"day": d, "start": s, "end": s + 1, "subject": sub,
     "teacher_id": t, "section": sec, "room_id": r}
    for (d, s, sub, t, sec, r) in CLASSES
]


def default_data():
    return {
        "timetable": [dict(c) for c in DEFAULT_TIMETABLE],
        "requests": [],   # reschedule requests
        "changes": [],    # "recent changes" notices for students
    }


def load_data():
    """Read data.json if it exists, otherwise start with the sample data."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return default_data()


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# Loaded on every rerun, so a CR on one device and a teacher on another
# both see the same, up-to-date data.
data = load_data()
timetable = data["timetable"]


# =====================================================
# 2. CORE LOGIC
# =====================================================
def overlaps(s1, e1, s2, e2):
    """Two time ranges overlap if each one starts before the other ends."""
    return s1 < e2 and s2 < e1


def find_free_slots(day, teacher_id, section, need_smart_board, ignore=None):
    """Hours on `day` when the teacher, the section AND at least one room are free.
    `ignore` = index of the class being moved (so it doesn't block itself)."""
    results = []
    classes_today = [c for i, c in enumerate(timetable)
                     if c["day"] == day and i != ignore]

    for start in range(START_HOUR, END_HOUR):
        end = start + 1
        if start == LUNCH_HOUR:
            continue

        teacher_busy = any(c["teacher_id"] == teacher_id and
                           overlaps(start, end, c["start"], c["end"])
                           for c in classes_today)
        section_busy = any(c["section"] == section and
                           overlaps(start, end, c["start"], c["end"])
                           for c in classes_today)
        if teacher_busy or section_busy:
            continue

        free_rooms = []
        for room_id, room in rooms.items():
            if need_smart_board and not room["smart_board"]:
                continue
            room_busy = any(c["room_id"] == room_id and
                            overlaps(start, end, c["start"], c["end"])
                            for c in classes_today)
            if not room_busy:
                free_rooms.append(room_id)

        if free_rooms:
            results.append({"start": start, "end": end, "free_rooms": free_rooms})
    return results


def free_rooms_at(day, hour, need_smart_board):
    """All rooms that are free at a given day and hour."""
    found = []
    for room_id, room in rooms.items():
        if need_smart_board and not room["smart_board"]:
            continue
        busy = any(c["room_id"] == room_id and c["day"] == day and
                   overlaps(hour, hour + 1, c["start"], c["end"])
                   for c in timetable)
        if not busy:
            found.append(room_id)
    return found


# =====================================================
# 3. SMALL HELPERS FOR DISPLAY
# =====================================================
def room_name(room_id):
    r = rooms[room_id]
    return r["name"] + (" (smart board)" if r["smart_board"] else "")


def sort_classes(classes):
    return sorted(classes, key=lambda c: (DAYS.index(c["day"]), c["start"]))


def weekly_grid(classes):
    """Build a Day x Hour table from a list of classes."""
    hours = [f"{h}:00" for h in range(START_HOUR, END_HOUR)]
    cells = {d: {} for d in DAYS}
    for c in classes:
        for h in range(c["start"], c["end"]):
            cells[c["day"]][f"{h}:00"] = f"{c['subject']} | {c['section']} | {rooms[c['room_id']]['name']}"
    table = {d: [cells[d].get(h, "") for h in hours] for d in DAYS}
    return pd.DataFrame(table, index=hours)


def class_rows(classes):
    return [{
        "Day": c["day"],
        "Time": f"{c['start']}:00 - {c['end']}:00",
        "Subject": c["subject"],
        "Teacher": teachers[c["teacher_id"]],
        "Section": c["section"],
        "Room": room_name(c["room_id"]),
    } for c in sort_classes(classes)]


def room_finder(prefix):
    """A small tool: pick a day and hour, see which rooms are free."""
    with st.expander("Room finder (which rooms are free?)"):
        d = st.selectbox("Day", DAYS, key=f"{prefix}_rf_day")
        h = st.selectbox("Hour", list(range(START_HOUR, END_HOUR)),
                         format_func=lambda x: f"{x}:00 - {x + 1}:00", key=f"{prefix}_rf_hour")
        sb = st.checkbox("Smart board only", key=f"{prefix}_rf_sb")
        free = free_rooms_at(d, h, sb)
        if free:
            st.success("Free: " + ", ".join(room_name(r) for r in free))
        else:
            st.warning("No free room at this time.")


# =====================================================
# 4. SCREENS
# =====================================================
st.title("📅 ClassSync")
st.caption("One place to find a free slot, get it approved, and tell everyone.")

role = st.sidebar.radio("Login as", ["Student", "CR", "Teacher"])
st.sidebar.markdown("---")
if st.sidebar.button("Reset demo data"):
    data.update(default_data())
    save_data()
    st.rerun()

# ---------------- STUDENT ----------------
if role == "Student":
    st.header("Student view")

    section = st.selectbox("Your section", sections)
    st.subheader(f"Weekly timetable: {section}")
    st.table(weekly_grid([c for c in timetable if c["section"] == section]))

    st.subheader("Recent changes")
    if not data["changes"]:
        st.write("No changes yet.")
    for note in reversed(data["changes"]):
        st.info(note)

    st.subheader("Check a teacher's timetable")
    t_id = st.selectbox("Teacher", list(teachers.keys()), format_func=lambda t: teachers[t])
    st.table(weekly_grid([c for c in timetable if c["teacher_id"] == t_id]))

    room_finder("student")

# ---------------- CR ----------------
elif role == "CR":
    st.header("CR view: request a reschedule")

    labels = [f"{c['subject']} | {c['section']} | {c['day']} {c['start']}:00 | {teachers[c['teacher_id']]}"
              for c in timetable]
    idx = st.selectbox("Class to reschedule", range(len(timetable)),
                       format_func=lambda i: labels[i])
    cls = timetable[idx]

    new_day = st.selectbox("Move it to which day?", DAYS)
    need_sb = st.checkbox("Need a smart board room")

    slots = find_free_slots(new_day, cls["teacher_id"], cls["section"], need_sb, ignore=idx)

    if not slots:
        st.warning("No common free slot found on this day. Try another day.")
    else:
        st.write("Slots where the **teacher, the section and a room** are all free:")
        slot_i = st.selectbox("Free slots", range(len(slots)),
                              format_func=lambda i: f"{slots[i]['start']}:00 - {slots[i]['end']}:00")
        room_id = st.selectbox("Free rooms in that slot", slots[slot_i]["free_rooms"],
                               format_func=room_name)
        if st.button("Request this slot"):
            data["requests"].append({
                "class_index": idx,
                "new_day": new_day,
                "new_start": slots[slot_i]["start"],
                "new_end": slots[slot_i]["end"],
                "new_room": room_id,
                "status": "pending",
            })
            save_data()
            st.success("Request sent to the teacher.")

    st.subheader("All requests")
    if not data["requests"]:
        st.write("No requests yet.")
    for r in data["requests"]:
        c = timetable[r["class_index"]]
        st.write(f"{c['subject']} ({c['section']}) to {r['new_day']} "
                 f"{r['new_start']}:00, {rooms[r['new_room']]['name']}: **{r['status']}**")

    room_finder("cr")

# ---------------- TEACHER ----------------
else:
    st.header("Teacher view")
    teacher_id = st.selectbox("You are", list(teachers.keys()), format_func=lambda t: teachers[t])

    st.subheader("Your weekly timetable")
    st.table(weekly_grid([c for c in timetable if c["teacher_id"] == teacher_id]))

    st.subheader("Pending requests")
    found = False
    for i, r in enumerate(data["requests"]):
        c = timetable[r["class_index"]]
        if r["status"] != "pending" or c["teacher_id"] != teacher_id:
            continue
        found = True
        st.write(f"**{c['subject']}** ({c['section']}): from {c['day']} {c['start']}:00 "
                 f"to {r['new_day']} {r['new_start']}:00 in {rooms[r['new_room']]['name']}")
        col1, col2 = st.columns(2)

        if col1.button("Approve", key=f"approve{i}"):
            # Re-check: another request may have taken this slot or room meanwhile.
            ok_slots = [s for s in find_free_slots(r["new_day"], c["teacher_id"], c["section"],
                                                   False, ignore=r["class_index"])
                        if s["start"] == r["new_start"] and r["new_room"] in s["free_rooms"]]
            if not ok_slots:
                r["status"] = "rejected (slot no longer free)"
            else:
                note = (f"{c['subject']} ({c['section']}) moved from {c['day']} {c['start']}:00 "
                        f"to {r['new_day']} {r['new_start']}:00, {rooms[r['new_room']]['name']}")
                c["day"] = r["new_day"]
                c["start"] = r["new_start"]
                c["end"] = r["new_end"]
                c["room_id"] = r["new_room"]
                r["status"] = "approved"
                data["changes"].append(note)
            save_data()
            st.rerun()

        if col2.button("Reject", key=f"reject{i}"):
            r["status"] = "rejected"
            save_data()
            st.rerun()

    if not found:
        st.write("No pending requests.")

    room_finder("teacher")