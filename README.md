# ISIN Management System (FastAPI & SQLAlchemy)

## 🚀 Project Overview

The ISIN Management System is a web application built using FastAPI and Bootstrap 5 to provide **Full CRUD (Create, Read, Update, Delete)** operations for International Securities Identification Numbers (ISINs) and their associated company details.

The system features a clean data entry form and a dynamic dashboard for managing and exporting records.

### Key Features Implemented

* **Data Entry Form:** Single page for creating new company records with validation.
* **ISIN Dashboard:** Displays all company details in a responsive grid.
* **CRUD Operations:** API endpoints for creating, reading, updating, and deleting records.
* **Search & Filter:** Allows searching records by ISIN or Company Name.
* **Data Export:** One-click functionality to download all current records (or search results) to an **Excel file**.
* **Database:** Uses SQLAlchemy to connect to a MySQL database.

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend API** | Python 3.x, FastAPI | High-performance API foundation and routing. |
| **Web Server** | Uvicorn | ASGI Server to run the FastAPI application. |
| **Database** | SQLAlchemy, PyMySQL | ORM (Object-Relational Mapper) for database interaction (MySQL). |
| **Data Handling** | Pandas, OpenPyXL | Used for generating the Excel (`.xlsx`) export file. |
| **Frontend UI** | HTML5, Bootstrap 5, JavaScript | Responsive design, forms, modals, and dynamic API calls. |

---

## ⚙️ Setup and Installation

Follow these steps to get a local copy of the project running.

### Prerequisites

* Python 3.8+
* pip (Python package installer)
* A running **MySQL** database instance.

### Step 1: Clone the Repository
```bash
git clone https://github.com/lazymonarch/ISIN_InternProject.git
cd isin-management-system
```


### Step 2: Set up Virtual Environment and Dependencies

#### Create and activate virtual environment (Windows/macOS/Linux)
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install required Python packages
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

For security and portability, database credentials are set via a .env file.

Install python-dotenv:

```bash
pip install python-dotenv
```
Create a file named .env in the root directory and add your database connection string:

 .env (This file is in .gitignore and should NOT be committed to GitHub)
 ```bash
DATABASE_URL="mysql+pymysql://root:your_password@127.0.0.1:3333/isin_db"
```

### Step 4: Database Initialization

The application is configured to create the company_details table automatically on startup using models.Base.metadata.create_all(bind=database.engine). Ensure your MySQL server is running and accessible before launching the app.

 Running the Application
Start the FastAPI application using Uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
