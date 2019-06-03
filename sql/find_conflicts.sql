-- requête pour trouver les conflits entre réservations

SELECT r1.*, r2.*, rooms.name
FROM (SELECT * FROM reservations WHERE end_date > '2019-05-24') as r1
INNER JOIN reservations_timeslots as rts1 ON r1.id = rts1.reservation_id
INNER JOIN (SELECT * FROM reservations WHERE end_date > '2019-05-24') as r2 ON r1.room_id = r2.room_id and r1.weekday_id = r2.weekday_id and r1.id <> r2.id
INNER JOIN reservations_timeslots as rts2 ON r2.id = rts2.reservation_id and rts1.timeslot_id = rts2.timeslot_id
INNER JOIN rooms ON rooms.id = r1.room_id
WHERE NOT (r1.end_date < r2.start_date OR r2.end_date < r1.start_date)

SELECT r1.*, r2.*, rooms.name
FROM reservations as r1
INNER JOIN reservations_timeslots as rts1 ON r1.id = rts1.reservation_id
INNER JOIN reservations as r2 ON r1.room_id = r2.room_id and r1.weekday_id = r2.weekday_id and r1.id <> r2.id
INNER JOIN reservations_timeslots as rts2 ON r2.id = rts2.reservation_id and rts1.timeslot_id = rts2.timeslot_id
INNER JOIN rooms ON rooms.id = r1.room_id
WHERE NOT (r1.end_date < r2.start_date OR r2.end_date < r1.start_date)

-- un peu plus élaboré ... avec quelques dates à changer en dur ... Ce serait
-- super d'avoir une route qui sort tous ces conflits
SELECT r1.id, r1.start_date, r1.end_date, r1.reason_short, r1.reason_details, u1.sigle as "owner1", r2.id, r2.start_date, r2.end_date, r2.reason_short, r2.reason_details, u2.sigle as "owner2", rooms.name as "salle", timeslots.start_time, timeslots.end_time, weekdays.name
FROM (SELECT * FROM reservations WHERE end_date > '2019-05-24') as r1
INNER JOIN reservations_timeslots as rts1 ON r1.id = rts1.reservation_id
INNER JOIN (SELECT * FROM reservations WHERE end_date > '2019-05-24') as r2 ON r1.room_id = r2.room_id and r1.weekday_id = r2.weekday_id and r1.id <> r2.id
INNER JOIN reservations_timeslots as rts2 ON r2.id = rts2.reservation_id and rts1.timeslot_id = rts2.timeslot_id
INNER JOIN rooms ON rooms.id = r1.room_id
INNER JOIN weekdays ON weekdays.id = r1.weekday_id
INNER JOIN timeslots ON rts1.timeslot_id = timeslots.id
INNER JOIN users as u1 ON u1.id = r1.owner_id
INNER JOIN users as u2 ON u2.id = r2.owner_id
WHERE 
	-- filtrer les les réservations qui n'ont pas de conflit de date
	NOT (r1.end_date < r2.start_date OR r2.end_date < r1.start_date)
	-- il ne sert à rien de considérer les conflits intentionnels comme des
	-- conflits (par exemple TPs / branches spéciales dans la même salle, ceci
	-- est voulu par escada
	AND NOT (r1.end_date = '2019-07-05' and r2.end_date = '2019-07-05')
	-- pour casser la symétrie ... sinon chaque conflit apparaît deux fois de
	-- suite
	AND r1.id < r2.id