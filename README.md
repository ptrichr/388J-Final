# [CMSC388J](https://aspear.cs.umd.edu/388j) Final Project: UMD(C)

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

> [!IMPORTANT]
> This project uses CLI Tailwind, not CDN, the script to compile is included in the tailwind directory

#### [Install Tailwind](https://tailwindcss.com/docs/installation)

#### [Install DaisyUI](https://daisyui.com/docs/install/)

> In `root/tailwind`:
> ```console
> $ chmod +x tw.sh
> ```


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
`TODO`