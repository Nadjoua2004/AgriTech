# 🌾 AgriTrack — Worker Management Microservice (Nesrine's Part)

This is the independent microservice handling the Worker management module for AgriTrack. It runs on Django 4.2 Rest Framework and securely connects to a centralized Neon PostgreSQL database. 

---

## ⚠️ Report to Team: Mocks & Cross-Service Dependencies
To allow this service to be developed and tested fully independently, I temporarily implemented some elements that **belong to other team members**. Please coordinate with them on the following:

1. **Mock Endpoints (Created for testing purposes only):**
   * **Sarah (Land Service):** I created fake endpoints (`/mock/lands/`) to simulate fetching Parcelle data.
   * **Nadjoua (Cultures/Auth Service):** I created fake endpoints for (`/mock/cultures/`) and (`/mock/auth/me/`) because the Supabase integration wasn't ready. 
   * **Sid Ahmed (Equipment Service):** I created fake endpoints for (`/mock/equipments/`).
2. **Auth Headers Substitution:** Since Nadjoua's Auth JWT system isn't running yet, we bypass it using a header called `X-Mock-Role` directly in Postman and the frontend. Once Nadjoua finishes her auth proxy, we will switch to reading the raw JWT token.
3. **Frontend Testing UI:** I created a local testing interface (`templates/index.html`) running on `http://127.0.0.1:8001/` to simulate the application. The frontend team will eventually build the real one.

***Action Item for Team Integration:*** Once your teammates finish their services and deploy them, you must update the URLs in the `.env` file (e.g. `LAND_SERVICE_URL=...`) and set the mock flags to `false` (e.g. `USE_MOCK_LAND=false`).

---

## 🚀 Setup & Execution

### Running Locally
1. Activate your virtual environment.
2. Install requirements: `pip install -r requirements.txt`
3. Generate the external Neon PostgreSQL schemas: `python manage.py migrate`
4. Start the server: `python manage.py runserver 8001`

---

## 🧪 Postman API Reference & Test Payloads

When testing in Postman, you must include these **Headers** to simulate being logged in:
* `Content-Type`: `application/json`
* `X-Mock-Role`: `supervisor` *(Options: farm_manager, supervisor, field_worker, irrigation_worker, equipment_operator, agronomist, quality_inspector)*
* `X-Mock-UserId`: `1` 

### 👨‍🌾 1. Workers API
* **List Workers**
  * `GET http://127.0.0.1:8001/api/workers/`
* **Create Worker**
  * `POST http://127.0.0.1:8001/api/workers/`
  * JSON Body: 
    ```json
    {
      "first_name": "Ali",
      "last_name": "Ben",
      "phone": "0555123456",
      "hire_date": "2024-04-01",
      "worker_type": "field_worker",
      "zone": "Nord"
    }
    ```
* **Specific Worker Overview (Summary)**
  * `GET http://127.0.0.1:8001/api/workers/1/summary/?month=2024-04`
* **Deactivate Worker (Soft Delete)**
  * `DELETE http://127.0.0.1:8001/api/workers/1/`

### 📋 2. Daily Tasks API
* **List Tasks** *(Optionally add `?date=2024-04-03` or `?status=pending`)* 
  * `GET http://127.0.0.1:8001/api/tasks/`
* **Create/Assign a Task**
  * `POST http://127.0.0.1:8001/api/tasks/`
  * JSON Body:
    ```json
    {
      "worker": 1,
      "date": "2024-04-03",
      "description": "Planting seeds",
      "land_id": 1, 
      "culture_id": 2
    }
    ```
* **Mark Task as Done**
  * `PATCH http://127.0.0.1:8001/api/tasks/1/status/`
  * JSON Body: `{"status": "done"}`

### ⏱️ 3. Work Hours API
* **Log Work Hours**
  * `POST http://127.0.0.1:8001/api/hours/`
  * JSON Body:
    ```json
    {
      "worker": 1,
      "date": "2024-04-03",
      "hours_worked": "8.00",
      "overtime": "2.00",
      "notes": "Extra irrigation work"
    }
    ```
* **Total Hours Summary**
  * `GET http://127.0.0.1:8001/api/hours/summary/?worker=1&month=2024-04`

### 💰 4. Salaries API
* **Calculate Monthly Salary**
  * *Note: Calculates base_salary + overtime. Defaults to 1000.00 base if worker has no prior history.*
  * `POST http://127.0.0.1:8001/api/salaries/calculate/`
  * JSON Body:
    ```json
    {
      "worker_id": 1,
      "month": "2024-04"
    }
    ```

### 🧱 5. Testing Mock Connections
* *These test whether Sarah/Nadjoua/Sid Ahmed's data would correctly pipe in.*
* `GET http://127.0.0.1:8001/mock/lands/` 
* `GET http://127.0.0.1:8001/mock/cultures/` 
* `GET http://127.0.0.1:8001/mock/equipments/`
