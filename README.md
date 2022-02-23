# kuro-ride-api

API that allows you to join circles that share rides.
Circles are a group of users that join with an invitation, only the admin of the circle can edit circle settings.
Rides are invitations to share vehicles with other users.

## API overview

![image](https://user-images.githubusercontent.com/87244716/155367212-33f230c0-a184-42e2-ad48-a8856e99ae15.png)

## Prerequisites
**Making venv**

Make a virtual environment by running:

```py -m venv venv```

To activate run:

In windows: 
```.\venv\Scripts\activate```

In Linux: 
```source venv/bin/activate```

**Installing dependencies**

Install all dependencies that are required for the project by running:

```pip install -r requirements.txt```

## Running django server

```bash
cd kuro-store-django
```
```bash
python3 manage.py runserver
```
