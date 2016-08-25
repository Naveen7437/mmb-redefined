ALTER TABLE users_profile ADD COLUMN join_band boolean DEFAULT false;
ALTER TABLE users_profile ADD COLUMN create_band boolean DEFAULT false;
ALTER TABLE muse_song ADD COLUMN tags CHARACTER VARYING (50);