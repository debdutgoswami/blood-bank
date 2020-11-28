<br />
<p align="center">
    <img src="assets/favicon.png" width="350px" alt="Logo" >
    <h3 align="center">Blood Bank</h3>
    <br />
    <p align="center">
      All-in-one portal for Blood Donation 🩸
      <br />
      <br />
      <a href="https://github.com/debdutgoswami/blood-bank/issues/new?assignees=&labels=&template=bug_report.md&title=">Report Bug</a>
      ·
      <a href="https://github.com/debdutgoswami/blood-bank/issues/new?assignees=&labels=&template=feature_request.md&title=">Request Feature</a>
    </p>
</p>



An all-in-one portal for providing Blood. It helps people in emergency to find blood quicker.

---

## Features

1. Creating Donors

2. Looking for Donors

3. Raising Request Tickets

4. Sorting Request Tickets

5. Notification system for new Requests

---

## Technologies used

1. Flask

2. React

3. [Flutter](https://github.com/flametron/Delhihacks-Bloodbankapp) 

4. Google Cloud Platform (GCP)

5. Django (added later, has the same functionalities)


This project contains the APIs built for `HACKNPITCH`, a hackathon conducted by `Jadavpur University`. We worked on the `Blood Bank` problem statement.

---

## UPDATE

The entire code is later on refactored and implemented using `Django Rest Framework (DRF)`.
The previous flask code is moved into `flask` folder.

---

## Getting Started

### Installation (Django)

1. Clone the repository and go to `flask` folder

   ```
   https://github.com/debdutgoswami/blood-bank.git
   cd blood-bank/django
   ```
   
2. Setup virtual environment and install the dependencies

   ```
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```
   
3. Configuration for using Django `PointField` (`from django.contrib.gis.db.models import PointField`) in `models.py`

   ```
   sudo apt-get install binutils libproj-dev gdal-bin
   sudo apt-get install libsqlite3-mod-spatialite
   ```
  
4. Run migrations

   ```
   python manage.py makemigrations core
   python manage.py migrate
   ```
 
 5. Create a `.env` file using the `sample.env`

6. Run the server

   ```
   python manage.py runserver
   ```

### Installation (Flask)

1. Clone the repository and go to `flask` folder

   ```
   https://github.com/debdutgoswami/blood-bank.git
   cd blood-bank/flask
   ```
   
2. Setup virtual environment and install the dependencies

   ```
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. Run the server

   ```
   python app.py
   ```