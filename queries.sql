SELECT
    timeslots.id AS [timeslot_id],
    weekdays.id as [weekday_id],
    weekdays.name as [day],
    reservations.reason_short,
    group_concat(users.sigle, ' - ') AS [users]
FROM timeslots
LEFT OUTER JOIN reservations_timeslots ON reservations_timeslots.timeslot_id = timeslots.id
LEFT OUTER JOIN reservations ON reservations.id = reservations_timeslots.reservation_id
LEFT OUTER JOIN rooms ON reservations.room_id = rooms.id
LEFT OUTER JOIN reservations_users ON reservations_users.reservation_id = reservations.id
LEFT OUTER JOIN users ON reservations_users.user_id = users.id
LEFT OUTER JOIN weekdays ON reservations.weekday_id = weekdays.id
WHERE 
    rooms.name LIKE '%102%'
GROUP BY timeslots.id, weekdays.id
ORDER BY weekdays.id, timeslots.id;

SELECT
    rooms.name,
    timeslots.id AS [timeslot_id],
    weekdays.id as [weekday_id],
    weekdays.name as [day],
    reservations.reason_short [reason],
    group_concat(users.sigle, ' - ') AS [users]
FROM timeslots
    LEFT JOIN reservations_timeslots
        ON reservations_timeslots.timeslot_id = timeslots.id
    LEFT JOIN reservations
        ON reservations.id = reservations_timeslots.reservation_id
    LEFT JOIN rooms
        ON reservations.room_id = rooms.id
    LEFT JOIN reservations_users
        ON reservations_users.reservation_id = reservations.id
    LEFT JOIN users
        ON reservations_users.user_id = users.id
    LEFT JOIN weekdays
        ON reservations.weekday_id = weekdays.id
WHERE 
    rooms.id = 5
GROUP BY timeslots.id, weekdays.id
        ORDER BY timeslots.id, weekdays.id;
    
SELECT timeslots.id as [timeslot_id], 
FROM timeslots
LEFT OUTER JOIN reservations_timeslots ON reservations_timeslots.timeslot_id = timeslots.id;

SELECT * FROM rooms;

SELECT rooms.name
FROM rooms
LEFT JOIN reservations ON reservations.room_id = rooms.id
LEFT OUTER JOIN reservations_timeslots ON reservations_timeslots.reservation_id = reservations.id
WHERE 
    timeslot_id = 3
GROUP BY rooms.id;


SELECT users.id, reservations.id
FROM users
LEFT JOIN reservations ON reservations.owner_id = users.id;

SELECT rooms.name FROM reservations JOIN rooms ON rooms.id = reservations.room_id WHERE reason_short LIKE 'PPI';