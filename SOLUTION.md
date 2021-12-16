Ultramar CRUD Test 
====

Here you can find info about this CRUD test project. Next the systems characteristics where this project was tested:
* OS: Windows 11
* Python version: 3.10

Python libraries and its versions can be founded in **requirements.txt** file.

Quickstart:
-----------
```bash
#clone the repo
git clone https://github.com/jarh1992/ultramar-test.git

#entrer to the repo dir, create a virtual env and activate it (windows example)
python -m venv venv
.\venv\Scripts\activate

#activate virtual env and install requirements
pip install -r requirements.txt

# Run migrations for database creation
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

open the web page (localhost:8000, 127.0.0.1:8000) and you wil get a login page. 
You can use the superuser credentials or you can create your own user through de link "I don't have a membership".

Technical details:
------------------
Let's start with the **logistic** Django app and its files:
* models.py: three models were created:
  * Booking (as specified in **README.md**)
  * Vehicle (as specified in **README.md**)
  * Transport: it was added to associate Bookings and Vehicles, and it will be used to take from it
  the info to generate reports quickly.
* forms.py: four classes were created:
  * VehicleCreationForm 
  * VehicleChangeForm
  * BookingCreationForm
  * BookingChangeForm
  
  they are used in the panel to create/modify logistic app models
* multiForm.py: used to load more than one form on a same class view/page. It was taken from
https://gist.github.com/jamesbrobb/748c47f46b9bd224b07f
* views.py: it was used class based view than function base views due class based view have pros like:
  * Code reusability
  * Reduce code duplication

Let's continue with **user_app** Django app and its files:
* models.py:
  * CustomUser
* forms.py: four classes were created:
  * CustomUserCreationForm 
  * CustomUserChangeForm
  
  they are used in the panel to create/modify user_app app models
* views.py: they were created two clases:
  * UserView
  * CustomUserCreationView

  Both clases are focused on user management: the first is to get and update info about current logged user,
  the second is to create a new user if you have you don't have a membership, and you would like one.

Let's pass to the frontend. 
It was used a template called AdminLte. The forms were created reusing block of html code with help
of DTL.