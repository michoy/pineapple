# pineapple

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
This installation of pineapple is for demonstration purposes only. For deployment version see pineappleDeploymen package. 

### Requirements
* Python 3.4 or newer
* Django 1.11

### Instructions
On windows simply cd into the project folder and run
```
py manage.py runserver
```
Open the given IP adress in your browser to use the webapp.

## In use
Start with registering a new user. From the *overview* page, type in a course name and click *add*. For demonstration purposes the following courses have allready been added:
* TTM4100
* TDT4140
* TFY4125
Press *Go to course* to se the courses page. Here you can see statistics of how you're doing in the course, as well as avalible exercises. Next, choose one of the exercises and answer the given questions. After you're finished the exercise, you will see updated statistics on the course page.
