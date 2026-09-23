DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS applications CASCADE;
DROP TYPE IF EXISTS application_status;


CREATE TYPE application_status AS ENUM ('applied','interviewing','offer','rejected');

CREATE TABLE users (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL

);

CREATE TABLE applications (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    date_applied DATE DEFAULT CURRENT_DATE NOT NULL,
    company_name TEXT NOT NULL,
    role_name TEXT NOT NULL,
    status application_status NOT NULL DEFAULT 'applied',
    notes TEXT,
    user_id INT NOT NULL,

    CONSTRAINT fk_user 
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
    
);

CREATE INDEX user_applications ON applications(user_id);