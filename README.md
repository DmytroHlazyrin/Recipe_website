# Recipe website

This project was created for those who love to cook. Here you will be able to find a dish to your liking.
The site has the ability to leave reviews, add dishes to favorites. And of course, you can share your recipes.
If you have some product in your fridge, you will be able to find a dish that includes it.
### Live DEMO: [Recipe website](https://recipe-website-zmdf.onrender.com)
- You can use following superuser:
    - Login: ```testuser```
    - Password: ```testpassword123```

## _Installation & Run_
### Set up the environment 


 On Windows:
```python
python -m venv venv 
venv\Scripts\activate
 ```

 On Unix:
```python
python3 -m venv venv 
source venv/bin/activate
 ```

### Install requirements 
```python
pip install -r requirements.txt
```


### Database setup

```python
python manage.py migrate
```

### Fill the database with initial data
```python
python manage.py loaddata dump_json/data.json
```
_You can upload ready-made data to see what the project looks like in its entirety and in action._
_You can also delete this file if you are not going to use the already prepared data_


### Run the project
```python
python manage.py runserver
```
### Create your own superuser with following command:
```python
python manage.py createsuperuser
```

## Testing
You can run tests for the Django project using the following command:
```python
python manage.py test
```


## Contributing
If you want to contribute to the project, please follow these steps:
    1. Fork the repository.
    2. Create a new branch for your feature or bug fix.
    3. Make the necessary changes and commit them.
    4. Submit a pull request.
