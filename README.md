# CampusConnect – Campus Placement Management System

**Live Demo:** https://campusconnect.onrender.com  
**Admin Panel:** https://campusconnect.onrender.com/admin  
**Officer Login:** `/officer/` (use your admin/officer account)

A full-featured, production-ready Django web application for managing campus placements — built for colleges and placement officers.

---

### Features

- Student Registration & Profile Management (CGPA, Branch, Resume Upload)
- Admin/Placement Officer Panel
- Job Posting with Eligibility Criteria (CGPA + Branch)
- Smart Application System (Auto eligibility check)
- Placement Officer Dashboard with Statistics
- PDF Report Generation with Charts (ReportLab + Matplotlib)
- Block/Unblock Students from Admin
- Email Notifications on Status Change
- Responsive Design (Bootstrap 5)
- Secure & Clean Code (No secret keys exposed)

---

### Tech Stack

- **Backend:** Django 5.0.3 (Python 3.12)
- **Database:** PostgreSQL (Production) / SQLite (Local)
- **Frontend:** Bootstrap 5 + Custom CSS
- **PDF Reports:** ReportLab + Matplotlib
- **Deployment:** Render.com (Free tier)
- **Static Files:** WhiteNoise

---

### Quick Start (Local Development)

```bash
# Clone repo
git clone https://github.com/sa-hil-29/campusconnect.git
cd campusconnect

# Create virtual environment
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (for admin/officer)
python manage.py createsuperuser

# Run server
python manage.py runserver
