
# Vehicle Parking App – V2   
(A Smart 4-Wheeler Parking Management System)

This is a multi-user web application designed to manage parking lots, parking spots, and vehicle reservations.  
The system supports **Admin** and **User** roles and follows all constraints specified in the problem statement.

The application is built using **Flask (API)** and **Vue 3 (UI)** with **JWT-based authentication**, **Redis caching**, and **Celery for background jobs**.

---

##  Problem Scope

- 4-wheeler parking only
- Single admin (superuser) with root access
- Multiple users with reservation capabilities
- Parking spot allocation is automatic (users cannot select spots)
- Database created programmatically (no manual DB creation)

---

##  Roles & Capabilities

### Admin (Superuser)
- Exists by default when the database is created
- No registration required
- Create, edit, and delete parking lots
- Configure number of parking spots per lot (auto-generated)
- Set parking price per lot
- View real-time parking spot status
- View parked vehicle details for occupied spots
- View all registered users
- View analytics and summary charts
- Restriction: Parking lots cannot be deleted if active reservations exist

### User
- Register and login
- View available parking lots
- Reserve a parking spot (automatically allocated)
- Vacate / release a parking spot
- View active and past reservations
- View parking usage summary and analytics
- Export reservation history as CSV (async job)

---

##  Tech Stack

### Frontend
- Vue 3 (Composition API)
- Vue Router
- Bootstrap 5 (only styling framework used)
- Chart.js
- Axios

### Backend
- Flask (REST API)
- Flask Blueprints
- JWT Authentication
- Celery (background jobs)

### Database & Caching
- SQLite (only database used)
- Redis (caching + message broker)

---

##  Backend Jobs (Celery + Redis)

###  Daily Reminder Job (Scheduled)
- Runs once daily (evening)
- Notifies users who have not booked parking
- Sent via Email / Webhook (configurable)

###  Monthly Activity Report (Scheduled)
- Runs on the first day of every month
- Generates an HTML report
- Includes:
  - Parking usage count
  - Most used parking lot
  - Monthly expenditure
- Sent via email

###  CSV Export (User-triggered Async Job)
- User triggers export from dashboard
- CSV contains complete parking history
- Background job generates file
- User is notified once export is complete

---

##  Project Setup & Installation

###  Prerequisites
- Python 3.10+
- Node.js 18+
- Redis
- MailHog (for testing functionality)
- Linux / macOS  
  **Windows users should use WSL (recommended)**

---

###  Backend Setup

```bash
# Create virtual environment
cd backend
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Redis (Linux / WSL)
redis-server

# Run database setup (creates admin automatically)
python db_setup.py

# Start Flask server
python app.py
```

###  Celery Worker (Separate Terminal)
```bash
cd backend
source venv/bin/activate
celery -A app.celery_app --loglevel=info
```
###  Celery Beat (Scheduled Jobs)
```bash
cd backend
source venv/bin/activate
celery -A app.celery_app --loglevel=info
```
###  Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
