
# Pineapple


## PineappleDeployment - What is different?
This is the 'proper' version of Pineapple, meant for deployment on an existing server. 
Set-up is more difficult than on the demo-branch, but in return you get Pineapple the way it always was intended.

## What is it?
Pineapple is a learning tool, designed to be used on the institution level. It's goal is to improve
awareness and understanding of where learning difficulties are located and offer help where needed.

With Pineapple students will gain the ability to anonymously compare their progress with the rest of
the class. The adaptive exercise and reading material system make sure that improvement comes easily
where it is needed most.

At the same time, lecturers are proveded with both information and tools to help steer focus to specific
topics as the class progresses. Do you teach a new course? No problem, with Pineapple you can adjust and
fix issues on the fly. Maintaining an established course? Perfect, fine-tuning has never been easier.

## Set-up
The unchanged server depends on an instance of MySQL running in the background. 
Details such as server-name, username and password can be set in the pineapple/settings.py file. 
The defaults are "pinedatabase", "admin" and "admin".

### Requirements
* Python 3.4
* Django 1.11
* mysql-connector-python 2.1.6
* MySQL (57 tested)

### Instructions
Step 1: Reconsider because the Pineapple team can't make any guarantees about security

If that step fails:

cd into the project folder and run
```
py manage.py runserver
```
Make migrations and migrate in order to set up the database with the correct tables
```
py manage.py makemigrations
py manage.py migrate
```
In order to insert example entries run the main() method in /exercise/populate.py

Connect Pineapple to your server of choice according to its instructions.
This will most likely involve changing some values in /pineapple/settings.py.

## In use
To test pineapple as a student, start by registering a new user. From the *overview* page, type in a course name and click *add*. For demonstration purposes the following courses have allready been added:
* TTM4100
* TDT4140
* TFY4125

Press *Go to course* to se the student course page. Here you can see statistics of how you're doing in the course, as well as avalible exercises. Next, choose one of the exercises and answer the given questions. After you're finished the exercise, you will see updated statistics on the student course page.

To test pineapple as a lecturer, log inn with the following credentials:

Username: Pekka

Password: passord

From the *overview* page, go to one of the allready added courses. Here you can see the statistics of how your class is doing, cards you can use to add new reading materials, questions and exercises. Press on one of the exercises to see an overview of the selected exercise. 
