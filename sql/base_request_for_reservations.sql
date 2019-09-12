SELECT reservations.id, reason_short, reason_details, rooms.name as "salle", users.sigle, start_date, end_date, student_group, owner_id, duration, timeslots.start_time, timeslots.end_time, weekdays.name
FROM reservations
INNER JOIN rooms ON rooms.id = reservations.room_id
INNER JOIN reservations_users ON reservations_users.reservation_id = reservations.id
INNER JOIN users ON users.id = reservations_users.user_id
INNER JOIN reservations_timeslots ON reservations_timeslots.reservation_id = reservations.id
INNER JOIN timeslots ON timeslots.id = reservations_timeslots.timeslot_id
INNER JOIN weekdays ON weekdays.id = reservations.weekday_id

WHERE end_date = '2020-07-03 00:00:00' and owner_id = 1