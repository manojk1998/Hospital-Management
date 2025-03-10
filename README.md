# Hospital Instrument Management System

A comprehensive system for managing hospital instruments, including sales, rentals, and storage. This application helps companies track instruments, manage clients (hospitals), handle staff, and generate bills efficiently.

## Tech Stack

- **Backend**: Django (Django REST Framework)
- **Frontend**: React Native (for web app)
- **Styling**: Bootstrap (responsive, clean, and attractive UI)
- **Database**: PostgreSQL

## Features

1. **Authentication & Roles Management**
   - User authentication (JWT-based login, signup)
   - Different user roles: Admin, Staff, Client (Hospitals)
   - Role-based access control (RBAC)

2. **Instruments Management**
   - Add, update, and delete hospital instruments
   - Categorize instruments based on type, usage, and availability
   - Track instruments (available, rented, sold, stored)
   - QR code/barcode integration for quick identification

3. **Client (Hospitals) Management**
   - Add and manage hospital details
   - Assign rented or sold instruments to hospitals
   - Track payment status (pending, completed)

4. **Staff Management**
   - Add, update, and manage staff details
   - Assign roles (Technician, Sales, Support, etc.)
   - Attendance and salary tracking

5. **Orders & Billing**
   - Generate invoices for sold or rented instruments
   - Payment tracking and history
   - GST/tax calculations in billing

6. **Reporting & Analytics**
   - Dashboard with real-time data visualization (Chart.js)
   - Reports on sales, rentals, instrument availability, and revenue
   - Export reports in PDF/Excel

7. **Notifications & Alerts**
   - Email/SMS notifications for due payments, stock alerts
   - Reminder system for rental renewals

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Start the server: `python manage.py runserver`

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm start`

## License
MIT