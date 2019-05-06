SELECT reservations.*, rooms.name as [Salle], weekdays.name as [Jour] FROM reservations
LEFT JOIN rooms on reservations.room_id = rooms.id
LEFT JOIN weekdays on reservations.weekday_id = weekdays.id
WHERE end_date between '2018-05-29' and '2018-06-29' and start_date <> '2018-05-28';