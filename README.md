# Varrock

Varrock is an asynchronous consumer of messages from a RabbitMQ queue.
His purpose is to process the messages and send them to the appropriate destination.

## Requirements
Python 3.10+ <br>
RabbitMQ 3.* <br>

## Installation
1. Create virtual environment
```
python3.10 -m venv venv
source venv/bin/activate
```
2. Install requirements
```
pip3 install -Ur requirements.txt
```
3. RabbitMQ <br>
Can skip if RabbitMQ is already installed. <br>
Assuming Docker is already installed. <br>
Copy following to the terminal:
```
docker run -d --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```
