# Subscription_Based_Enterprise_Customer_API
Django app to track enterprise customers who pay a monthly subscription for a phone and data plan.

### Technologies used
***
* Django
* DRF


### Installation
***
```
$ git clone https://github.com/jobayer-rahman/Subscription_Based_Enterprise_Customer_API.git
$ cd Subscription_Based_Enterprise_Customer_API
$ python3 -m venv venv
hello
$ source venv/bin/activate                   (for Unix or MacOS)
$ venv\Scripts\activate.bat                  (for windows)
$ python -m pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser


```
* After creating the superuser go to the admin panel and add the 'plans'
* Then go to ```http://127.0.0.1:8000/company/``` and add some companies
* After creating some companies ```http://127.0.0.1:8000/company/<int:pk>/``` (here pk is the company id)
* Then you can go to the ```http://127.0.0.1:8000/customer/``` and provide the customer name and the system will generate a random phone number from the companies that you have provided. 
* For customer details ```http://127.0.0.1:8000/customer//<int:pk>/``` (pk is the users phone number)
* For subscription ```http://127.0.0.1:8000/customer//<int:pk>/subs/```
* For subscription cancellation ```http://127.0.0.1:8000/customer//<int:pk>/subs/cancel```


### Demonstration
```https://www.youtube.com/watch?v=WMgOenyrWJo```
