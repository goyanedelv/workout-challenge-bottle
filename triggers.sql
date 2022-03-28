-- Register the deletion of a user in the log table
CREATE TRIGGER log_user_deletion
AFTER DELETE ON user
BEGIN
INSERT INTO log_table VALUES (' Deletion of user: '|| old.user_id || '; Email: '|| old.email ||'; Handle: '|| old.user_handle || '; Timestamps: '|| date('NOW'));
END;

-- When a team is deleted, un-enroll every user from that team
CREATE TRIGGER team_deletion
AFTER DELETE ON team
BEGIN
DELETE FROM user_teams
WHERE team_id = old.team_id;
END;

-- Integrity constraint: emails must be unique
CREATE TRIGGER unique_emails
BEFORE INSERT ON user
BEGIN 
SELECT CASE 
WHEN ((SELECT email FROM user WHERE email = new.email) NOT NULL)
THEN RAISE (ABORT, 'This is email already exists')
END;
END;

-- [Working] When a user is deleted, delete their workouts # NOTE THIS APPLIES TO THE APP -CASCADE DELETE OF RELATIONY
CREATE TRIGGER photoworkouts_deletion
AFTER DELETE ON user
BEGIN
DELETE FROM photoworkouts_user
WHERE user_id = old.user_id;
END;
