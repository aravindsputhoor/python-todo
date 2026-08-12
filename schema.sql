-- schema.sql
-- Run this once to set up the database and table for the To-Do app.
-- Usage: mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS todo_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE todo_db;

CREATE TABLE IF NOT EXISTS tasks (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    title         VARCHAR(255)      NOT NULL,
    description   TEXT,
    priority      ENUM('Low','Medium','High') NOT NULL DEFAULT 'Medium',
    due_date      DATE              NULL,
    is_completed  BOOLEAN           NOT NULL DEFAULT FALSE,
    created_at    TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP
                                    ON UPDATE CURRENT_TIMESTAMP
);
