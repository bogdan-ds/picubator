# Picubator

A simple application for Raspberry Pi which for now uses a DHT type sensor to measure humidity and a relay board to control various devices.
The goal is to create an incubator environment for fermentation, fruiting, plants etc. I'll create a more detailed write up soon.

## Installation

Create a Python virtual environment and install the needed packages:

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Configuration

Edit the `config/__init__.py` file and set the correct pin numbers and the thresholds for each device.

## Running the tests

```
python -m unittest discover tests
```
