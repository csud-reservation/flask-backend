SELECT
            timeslots.id AS [timeslot_id],
            roles.name AS [owner_role],
            weekdays.id AS [weekday_id],
            weekdays.name AS [day],
            reservations.id AS [res_id],
            reservations.start_date AS [start_date],
            reservations.end_date AS [end_date],
            rooms.name AS [room_number],
            reservations.reason_short AS [reason],
            reservations.reason_details AS [reason_details],
            reservations.student_group,
            group_concat(users.sigle, ' - ') AS [users]
        FROM timeslots
            LEFT JOIN reservations_timeslots
                ON reservations_timeslots.timeslot_id = timeslots.id
            LEFT JOIN reservations
                ON reservations.id = reservations_timeslots.reservation_id
            LEFT JOIN users AS owner
                ON reservations.owner_id = owner.id
            LEFT JOIN roles
                ON owner.role_id = roles.id
            LEFT JOIN rooms
                ON reservations.room_id = rooms.id
            LEFT JOIN reservations_users
                ON reservations_users.reservation_id = reservations.id
            LEFT JOIN users
                ON reservations_users.user_id = users.id
            LEFT JOIN weekdays
                ON reservations.weekday_id = weekdays.id
        WHERE 
            users.sigle IN ('DONC', 'SIMF', 'MADA', 'FIDL')
        AND NOT (
            reservations.start_date > '2019-08-26' OR reservations.end_date < '2019-08-30'
        )
        GROUP BY timeslots.id, weekdays.id
        ORDER BY weekdays.id, timeslots.id;