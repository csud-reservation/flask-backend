-- requête permettant d'afficher les cours à vérifier depuis la table de backup
-- reservations_to_check
SELECT r.id, r.start_date, r.end_date, reason_short, reason_details, duration, student_group, u.sigle as "owner", rooms.name as "salle", wd.name as "jour", ts.start_time AS "plage"
FROM reservations_to_check as r
INNER JOIN rooms ON rooms.id =  r.room_id
INNER JOIN weekdays as wd ON wd.id = r.weekday_id
INNER JOIN reservations_timeslots as rts ON rts.reservation_id = r.id
INNER JOIN timeslots as ts ON ts.id = rts.timeslot_id
INNER JOIN users AS u ON u.id = r.owner_id