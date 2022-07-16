# Order-System

## Project Statement
The goal of this project is to design a application for a taking orders from a restaurant

## Project Features - 
1. The application provides basic dine in order system, where we store data of each and every action (customers, orders, billing, payments, inventory etc.)
2. You should then be able to perform 4 basic operations: create new entries in your tables, read the entries, update entries by editing any of the properties,and delete the entries.
3. Each operation is linked with every related field in database.
(Ex :- Adding new items to order should update bill, Table gets automatically cleared after clearing the bill etc.)

## Project Implementation Details -

1. Database Used - MySQL
2. Created API for all 4 basic CRUD operations for every table in database and added basic functionality.

## --------------------------------------------------------------------------------------------------------

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This is a simple order system where we manage order at restaurent with the help of database using API's.

## Technologies
Project is created with:
* Python 3.9
* Django 3.1.1
* Django Rest Framework 3.12.4
* MySQL Server

## Setup

1. Installation
      * Install Python 3.9 from [Python](https://www.python.org/downloads/).
      * To install Django, open Terminal/Command prompt and run the following command
      ```
      pip install django==3.1.1
      ```
      * To install Django Rest Framework, open Terminal/Command prompt and run the following command
      ```
      pip install djangorestframework==3.12.4
      ```
      * Install MySQL Server from [MySQL](https://dev.mysql.com/downloads/mysql/).
      * Install Postman from [Postman](https://www.postman.com/downloads/).

    2. Download the zip and extract it.

3. After Setting up your MySQL server, create a Database with name "order_system" and Enter the user and Password of root user in order_system/settings.py

    
4. To make migrations and run the server, Right click in the folder and select *Open in Terminal* and run the following command
      ```
      python manage.py makemigrations
      ```
      ```
      python manage.py migrate
      ```

      ```
      python manage.py runserver
      ```
5. Now, You can perform all the basic operations in order system using API's.

(Note :- More functionality not yet added.But mentioned in repository.[More Features](https://github.com/chellurikeshav/Order-System/blob/main/more_featues(yet%20to%20add).pdf)) 
