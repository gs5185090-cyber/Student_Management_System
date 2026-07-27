-- ============================================================
-- Student Management System - Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS student_management;
USE student_management;

DROP TABLE IF EXISTS student;

CREATE TABLE student (
    student_id      INT AUTO_INCREMENT PRIMARY KEY,
    first_name      VARCHAR(50)  NOT NULL,
    last_name       VARCHAR(50)  NOT NULL,
    gender          ENUM('Male', 'Female', 'Other') NOT NULL,
    age             INT NOT NULL CHECK (age BETWEEN 15 AND 100),
    department      VARCHAR(50)  NOT NULL,
    course          VARCHAR(50)  NOT NULL,
    email           VARCHAR(100) NOT NULL UNIQUE,
    phone           VARCHAR(15)  NOT NULL UNIQUE,
    address         VARCHAR(255),
    admission_date  DATE NOT NULL DEFAULT (CURRENT_DATE)
) ENGINE=InnoDB;

-- Helpful indexes for frequent lookups / sorting
CREATE INDEX idx_last_name  ON student (last_name);
CREATE INDEX idx_department ON student (department);

-- ============================================================
-- Sample Data
-- ============================================================
INSERT INTO student
    (first_name, last_name, gender, age, department, course, email, phone, address, admission_date)
VALUES
    ('Rahul', 'Sharma', 'Male', 20, 'Computer Science', 'B.Tech', 'rahul.sharma@example.com', '9876543210', 'Hyderabad, India', '2023-08-01'),
    ('Priya', 'Reddy', 'Female', 21, 'Electronics', 'B.Tech', 'priya.reddy@example.com', '9876543211', 'Bengaluru, India', '2023-08-01'),
    ('Ahmed', 'Rahman', 'Male', 22, 'Mechanical', 'B.Tech', 'ahmed.rahman@example.com', '9876543212', 'Chennai, India', '2022-08-01'),
    ('Sneha', 'Iyer', 'Female', 19, 'Computer Science', 'B.Tech', 'sneha.iyer@example.com', '9876543213', 'Pune, India', '2024-08-01');
