
#  Multiuser-Django-Project

This project is an introduction to a Multiuser Django application aimed at facilitating hotel bookings and restaurant management. Upon signing up, an initial default user account is created, granting access to various features of the platform. Users can browse available rooms, book hotels, and explore the site's functionalities.


## Features:

- User Roles: Upon sign-up, users are assigned default roles with specific permissions. Users have the option to upgrade their role to a seller, allowing them to add their restaurant or hotel details to generate online revenue.

- Permission Management: Users have permissions tailored to their roles. Sellers can add, remove, and manage various aspects of their restaurant or hotel, while admin users have comprehensive control over the entire website.

- Email Verification: To register, users must provide a valid email address. An activation code is sent to the user's email for account verification, ensuring security and authenticity.

## Screenshots
![Screenshot_9-4-2024_16283_127 0 0 1](https://github.com/Admin12121/Multiuser-Django-Project/assets/131951081/b7f7a803-c6da-47b3-8381-9fe1e561eec5)

![Screenshot_9-4-2024_162928_127 0 0 1](https://github.com/Admin12121/Multiuser-Django-Project/assets/131951081/ce3353d2-2874-4ac3-9067-4ffc8771f04b)

![Screenshot_9-4-2024_162851_127 0 0 1](https://github.com/Admin12121/Multiuser-Django-Project/assets/131951081/6b3ee2b4-f3da-4426-8a2c-9abe0708fb4e)


## Getting Started:


To set up and run this project locally, follow these steps:

Clone the repository to your local machine:
```bash
https://github.com/Admin12121/Multiuser-Django-Project.git
```
Install the necessary dependencies:

```bash
 pip install -r requirements.txt
```

Set up your local environment variables, in a .env file. For smpt server to send activation email to the user

Run the Django migrations to create the necessary database schema:
```bash
 python manage.py migrate
```

Start the development server:
```bash
 python manage.py runserver
```
