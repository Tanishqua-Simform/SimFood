# SimFood

Kitchen Management System for our Comapny, Simform. Created using Django and DRF, as part of my training @Simform.

### Features -

#### 1. Food Management -

- Menu creation and updation by Headchef.
- Menu sent through mail to active subscribers.
- Consumers can change preferences for their availability each day as well as their choice of food (Regular/Jain).
- Monthly Analysis of Wastage and Savings of Food.
- Headchef gets count of people going to have lunch so as to plan accordingly.

#### 2. Task Management -

- Task Creation and Assignment by Headchef.
- Task Listing and Status Updation by Cooks.

#### 3. Subscription Management -

- Reminder mails to make the payments.
- Menu and Preference chanign features available to active subscribers.

### Tech Stack -

- PostgreSQL
- Django
- Django Rest Framework
- Jinja
- JWT Auth
- Redis
- Celery
- Celery-beat

### Implementation of Project Requirements -

**1. PostgreSQL -** To create SimfoodUser and other required models.

**2. DRF -** To create API endpoints for our business logic. The apps I have created are -

- Users
- Headchef
- Cook
- Consumer
- Monitor

**3. Jinja -** To send menu from mail.

**4. Authentication -** JWT Tokens, to create stateless authentication.

**5. Caching -** To cache menu and monthly and daily analysis as they are frequesntly requested data.

**6. Middleware -** To log each request the server has served (on daily basis)

**7. Throttling -** To throttle requests as per the request methods (GET, POST, PUT)

**8. Scheduled Tasks -** To perform following actions at timely basis.

- Payment Reminder mail (On 23rd and 28th of every month)
- Email to set availability status (Everyday @8 Am)
- Sending Menu through mail (Everyday @6 Pm)
- Setting the status for next day's lunch to false everyday after lunch.
- Setting subscription status (On 1st of every month)
- Filling the Stats table everyday after lunch

**9. Stored Procedures -** To perform repeated task in Database for faste performance.

- Filling the Stats table with data of food consumption.
- Setting Subscription active/inactive.
- Unsetting the next days status for all consumers.

**10. Redis -** For Caching and as a message broker for Celery.
**11. Validation -** In serializers to validate fields like email, date, and so on.
**12. Celery -** To perform scheduled Tasks, along with celery-beat.
**13. Test Cases -** For views and urls or all modules.

### API Endpoints -

    SimFood Application/
    ├── Auth/
    |   ├── Register - http://127.0.0.1:8000/api/register
    |   ├── JWT Token - http://127.0.0.1:8000/api/token/
    |   ├── JWT Refresh - http://127.0.0.1:8000/api/token/refresh/
    |   └── Protected View - http://127.0.0.1:8000/api/protected/
    │── Headchef/
    |   ├── Tasks (List & Create) - http://127.0.0.1:8000/headchef/task/
    |   ├── Task (Retrieve, Update & Delete) - http://127.0.0.1:8000/headchef/task/22
    |   ├── Menu (List & Create) - http://127.0.0.1:8000/headchef/menu/
    |   ├── Menu (Retrieve, Update & Delete) - http://127.0.0.1:8000/headchef/menu/26
    |   └── Consumer Count - http://127.0.0.1:8000/headchef/count/
    │── Cook/
    |   ├── Tasks (List) - http://127.0.0.1:8000/cook/tasks/
    |   └── Task (Retrieve & Update) - http://127.0.0.1:8000/cook/task/9
    │── Consumer/
    |   ├── Menu (List), Preference (Retrieve & Update) - http://127.0.0.1:8000/consumer/menu/
    |   ├── Attendance Scanner - http://127.0.0.1:8000/consumer/scanner/
    |   └── Payment - http://127.0.0.1:8000/consumer/payment/
    └── Monitor/
        └── Dashboard - http://127.0.0.1:8000/monitor/dashboard/

### Installation -

To run this project, CLone thie repository and connect your postgres database by providing credentials.

Install all required libraries from - [requirements.txt](/requirements.txt)

Then make migrations and start tinkering with all API's on Postman after writing the foloowing commands -

- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver

###### Thank you for stopping by!
