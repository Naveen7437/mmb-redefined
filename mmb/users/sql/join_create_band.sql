ALTER TABLE users_profile ADD COLUMN join_band boolean DEFAULT false;
ALTER TABLE users_profile ADD COLUMN create_band boolean DEFAULT false;
ALTER TABLE users_profile ADD COLUMN fb_link character varying(255);
ALTER TABLE users_profile ADD COLUMN twitter_link character varying(255);
ALTER TABLE users_profile ADD COLUMN google_link character varying(255);
