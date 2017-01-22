ALTER TABLE users_user ADD COLUMN avatar character varying(255);
ALTER TABLE users_user ADD COLUMN activation_key character varying(127);
ALTER TABLE users_user ADD COLUMN fb_link character varying(255);
ALTER TABLE users_user ADD COLUMN twitter_link character varying(255);
ALTER TABLE users_user ADD COLUMN google_link character varying(255);
ALTER TABLE users_user ADD COLUMN gender character varying(255);



#bands
ALTER TABLE bands_band ADD COLUMN cover character varying(255);
ALTER TABLE bands_band ADD COLUMN updated_at not null default CURRENT_DATE;
