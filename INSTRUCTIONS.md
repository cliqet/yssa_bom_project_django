# Use Python 3.11

# Instructions

### For first time setup
- Clone the project in the directory where you want to save it using the command
```bash
git clone https://github.com/cliqet/yssa_bom_project_django.git .
```
- Inside the root directory (yssa_bom_django), create a virtual environment with the command 
```bash
python -m venv env
```
- Activate the virtual environment with the command 
```bash
source env/bin/activate
``` 
or on Windows 
```bash
.\env\Scripts\activate
``` 
- Install dependencies 
```bash
pip install -r requirements.txt
```
- Config config in templates directory and create a file named `config.toml` in the root directory
- To run using sqlite as the database, make sure your config.toml has `sqlite` as value for the variable `db_type`. When choosing postgres, make sure the value is `psql` and fill out the rest of the psql variables. Make sure you have no existing database with the same name
- Apply migrations to the database by running
```bash
python manage.py migrate
```
- Create a superuser for the application by running
```bash
python manage.py createsuperuser
```
- Answer the prompts
- Run the app with the command 
```bash
python manage.py runserver
```
- Login using your superuser credentials

### Setting up application
- Each employee created can access the application through their login credentials. As a superuser, you can create users yourself or create an employee user who has the privileges to create one.
- It is best to create a group first. When adding a group, you can add all the privileges that a user can do. Make sure to give only privileges that are necessary. For example, you may want to create a group of users as your managers and assign them roles such as creating a user. To do so, you need to give them both the add and change Employee as user permissions. Always make sure to check `is_active` so that they can login. Only a superuser can create a user that is also a superuser. Be careful when assigning a superuser status to a user as this user will have all the privileges in the application.
Once you created a group and assign permissions to it, any user created that is assigned to that group will automatically inherit those permission and will not need to be assigned individual permissions.

### Populating initial db from existing csv file
After running the migrations, you can use existing csv files to populate the db. Please take note of format of columns for each csv file. If your csv file has inconsistent data such as a value in the `sales_executive` for a job that does not exist in the db yet, the error will be printed out when the script runs. You will have to manually assign in the program the right value.
You can run the scripts in this order to make sure you create tables first that are depended on by other tables.
```bash
python manage.py populate_department <csv file name>
```

```bash
python manage.py populate_employee_position <csv file name>
```

```bash
python manage.py populate_employee <csv file name>
```

```bash
python manage.py populate_client <csv file name>
```

```bash
python manage.py populate_product <csv file name>
```

```bash
python manage.py populate_job <csv file name>
```