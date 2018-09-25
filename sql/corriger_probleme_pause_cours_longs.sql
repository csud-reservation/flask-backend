UPDATE reservations_timeslots SET timeslot_id = 4 WHERE timeslot_id = 3 and reservation_id IN (
SELECT reservations.id FROM reservations
LEFt JOIN reservations_timeslots ON reservations.id = reservations_timeslots.reservation_id
LEFT JOIN timeslots ON timeslots.id = reservations_timeslots.timeslot_id
LEFT JOIN rooms ON reservations.room_id = rooms.id
LEFT JOIN weekdays ON reservations.weekday_id = weekdays.id
WHERE reservations_timeslots.timeslot_id = 3 
	AND reservations.duration > 1
	AND reservations.start_date = '2018-09-17' and reservations.end_date = '2019-07-05');