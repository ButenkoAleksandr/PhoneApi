# PhoneApi
UPDATE full_names
SET status = (SELECT status FROM short_names WHERE short_names.filename = SUBSTRING_INDEX(full_names.filename, '.', 1))
