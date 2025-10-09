Overview
CampusConnect is a full-stack web application built with Django for managing campus placements in educational institutions. It automates the recruitment process, connecting students, placement officers, and companies through secure authentication, profile management, job postings, application tracking, and analytics. This project addresses inefficiencies in manual placement systems, providing transparency and reducing administrative workload.
Key highlights:

Role-based access (Students, Placement Officers/Admins, Companies).
Secure user management with bcrypt hashing.
Responsive UI using Bootstrap.
Analytics dashboard with Chart.js visualizations.

This project was developed as a college capstone, following IEEE standards for documentation (SRS, ERD, diagrams).
Features
Core Modules

User Management: Secure registration, login/logout, role assignment (Student/Admin/Company).
Student Profile Management: Create/update profiles with CGPA, branch, skills, and resume upload.
Job Posting and Management: Admins post/edit jobs with eligibility criteria and deadlines.
Application Management: Students apply for eligible jobs; track statuses (Applied, Shortlisted, Selected, Rejected).
Admin Dashboard: Overview of applications, jobs, and students; status updates.

Optional Modules

Analytics and Reporting: Visual reports (e.g., placements by branch) using Chart.js.
Notifications: Email alerts for application updates (via Django's email backend).
Company Management: Companies post jobs and view applicants.
Interview Scheduling: Calendar-based scheduling with notifications.

Tech Stack

Backend: Django 4.2+ (ORM, Auth, Admin).
Frontend: HTML/CSS, Bootstrap 5, Django Templates, Chart.js.
Database: SQLite (prototype); MySQL (scalable).
Security: Bcrypt for password hashing.
Deployment: Heroku (with Gunicorn).
Tools: Git/GitHub, VS Code, Postman (testing).

Installation
Prerequisites

Python 3.8+.
Git.
