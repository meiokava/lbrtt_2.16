#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pydantic import BaseModel, ValidationError, validator


class FlightsSchema(BaseModel):
    dst: str
    nmb: int
    tpe: str


def get_flight():
    """
    requesting information about the flight
    """
    dst = input("What destination do you need? ")
    nmb = int(input("Which number of the flight do you need? "))
    tpe = input("Which type of plane do you need? ")

    # the сreation of dictionary
    return {
        'd': dst,
        'n': nmb,
        't': tpe,
    }


def display_flights(flights):
    """
    displaying the given information
    """
    if flights:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 18
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^18} |'.format(
                "№",
                "Destination",
                "Number of the flight",
                "Type of the plane"
            )
        )
        print(line)
        for idx, flight in enumerate(flights, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>18} |'.format(
                    idx,
                    flight.get('d', ''),
                    flight.get('n', ''),
                    flight.get('t', 0)
                )
            )
        print(line)
    else:
        print('list is empty')


def select_flights(flights, t):
    """
    selecting flights that are appropriate
    """
    result = []
    for flight in flights:
        if t in str(flight.values()):
            result.append(flight)
    return result


def save_flights(file_name, flights):
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(flights, fout, ensure_ascii=False, indent=4)


def load_flights(file_name):
    with open(file_name, "r", encoding="utf-8") as fin:
        indata = json.load(fin)
        try:
            for i in indata:
                FlightsSchema.parse_raw(str(i).replace("'", '"'))
            print("Validation was successful")
            return indata
        except ValidationError as err:
            print("Error in validation")
            print(err)


def main():
    """
    main function of the program
    """
    #list of the flights
    flights = []

    #organization of an endless loop
    while True:
        command = input(">>> ").lower()
        if command == 'exit':
            break
        elif command == 'add':
            flight = get_flight()
            flights.append(flight)
            if len(flights) > 1:
                flights.sort(key=lambda item: item.get('destination', ''))
        elif command == 'list':
            display_flights(flights)
        elif command.startswith('select'):
            a = input("choose type of the plane: ")
            selected = select_flights(flights, a)
            display_flights(selected)
        elif command.startswith("save "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            save_flights(file_name, flights)
        elif command.startswith("load "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]
            flights = load_flights(file_name)
        elif command == 'help':
            print("command list:\n")
            print("add - add information about a flight;")
            print("list - display the flight schedule;")
            print("select <type> - select the type of the plane;")
            print("load - download data from file;")
            print("save - save data from file;")
            print("help - show reference;")
            print("exit - leave a program.")
        else:
            print(f"unknown command {command}", file=sys.stderr)


if __name__ == '__main__':
    main()