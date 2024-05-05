# [CMSC388J](https://aspear.cs.umd.edu/388j) Final Project: UMD{C}

A simple transit itinerary for DC trips. Nathan Ho, Spring 2024

## Getting Started

### Clone the repository:

> via URL:
> ```console
> $ git clone https://github.com/ptrichr/388J-Final.git
> ```

> via SSH:
> ```console
> $ git clone git@github.com:ptrichr/388J-Final.git
> ```

> [!NOTE]
> If you are a contributor, pull the most recent update:
> ```console
> $ git pull origin master
> ```

### Install the required dependencies:

> In `root`:
> ```console
> $ pip3 install -r requirements.txt
> ```

### Configure Tailwind:

> #### [Install Tailwind](https://tailwindcss.com/docs/installation)
> #### [Install DaisyUI](https://daisyui.com/docs/install/)

### Configure the environment:

> Create `.env`, `config.py` files:
> ```console
> $ touch .env
> $ touch flask_app/config.py
> ```

> Format `.env` file:
> ```bash
> export GOOG_API_KEY = <replace with your API key>
> ```

> Format `config.py`:
> ```python
> SECRET_KEY = '{your csrf key here}'
> MONGODB_HOST = '{your URI here}'
> ```

## Running the Application:

### In split terminals:

> In `root`:
> ```console
> $ flask run
> ```
> In `root/tailwind`:
> ```console
> $ ./tw.sh
> ```

## Writeup

### Description of Your Final Project Idea:

This project is inteded to be a self-routing itinerary for trips from UMD to DC, you can input places that you would like to visit, and when you'd like to leave to go to the next location, and the application will automatically fetch a detailed metro route

### Describe What Functionality Will Only be Available to Logged-In Users:

Basically everything. You need to be logged in to create trips, view account information, edit trips, look at your trips

### 4 Forms:

- Login
- Registration
- Change Username
- Trip Title and Start Time
- Add Point of Interest

### List and Describe Your Routes/Blueprints:

There is a blueprint for user/account-related information routes, and another for actual metro route information/processing/requests routes

### Describe What Will be Stored/Retrived from MongoDB:

All user information is stored in Mongo as **"User"** documents, and all trips are stored in Mongo as **"Trip"** documents. 

**"User"** contains information such as as username and password.

**"Trip"** contains information such as:
- Author
- Title
- Start datetime
- Points of Interest
- Routes

### Describe What Python Package or API You Will Use or How it Will Affect the User Experience:

The original idea was to use the WMATA API. Due to difficulties with parsing information about stop times, a switch was made to the Google Maps API, specifically, Places and Routes. A combination of an open-source Python module (written by Google for the Maps API), and the Requests module for HTTP requests was used to get data from Google for usage in the app.
