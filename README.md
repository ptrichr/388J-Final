# CMSC388J Final Project: UMD(c)

Nathan Ho, Spring 2024

## Getting Started

Clone the repository:
> via URL
```console
$ git clone https://github.com/ptrichr/388J-Final.git
```

> via SSH
```console
$ git clone <>
```

Or, if you are a contributor, pull the most recent update:
```console
$ git pull origin master
```

Install the required dependencies:
```console
$ pip3 install -r requirements.txt
```

Create .env file:
```console
$ touch .env
```

Format .env file:
```java
export SECRET_KEY = <replace with your csrf key>
export MONGODB_HOST = <replace with your mongo uri>
export GOOG_API_KEY = <repalce with your API key>
```
