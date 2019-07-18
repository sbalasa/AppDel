#!/bin/python3
"""
Main runner for ApplianceDelivery.
"""


import json
import math
import click
import random
import string
import logging


from typing import TextIO
from pprint import pprint
from .lookup import PRODUCT_INVENTORY


logger = logging.getLogger(__name__)


total_vehicles = []


class Vehicle:
    def __init__(self, vehicle_id, vehicle_type, packages_loaded, total_weight, displacement, cost, estimated_time):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.packages_loaded = packages_loaded
        self.total_weight = total_weight
        self.displacement = displacement
        self.cost = cost
        self.estimated_time = estimated_time

    def __repr__(self):
        return self.vehicle_id


def get_order(orders_file: str) -> json:
    """
    Function to get the list of orders from a json file
    Args:
        orders_file (str): Orders file in json format
    Returns:
        orders (json): Complete extracted list of orders
    """
    with open(orders_file, "r") as input_f:
        orders = json.load(input_f)
    return orders


def get_total_weight(products: list) -> float:
    """
    Function to get the total weight of the package from the orders
    Args:
        products (list): List of products
    Returns:
        total_weight (float): Total weight of the package
    """
    total_weight = 0
    for product in products:
        total_weight += PRODUCT_INVENTORY[product]["weight"]
    return total_weight


def get_displacement(distance: list) -> float:
    """
    Function to get the displacement to be delivered by the Vehicle
    Args:
        distance (list): Co-ordinates of the distance in (x, y) format
    Returns:
        displacement (float): Square root of the distance from origin (0, 0)
    """
    return math.sqrt(((distance[0]) ** 2) + ((distance[1]) ** 2))


def generate_vehicle(weight: float) -> (str, str):
    """
    Function to choose the vehicle of delivery from the orders based on weight and destination
    Args:
        weight (float): Total weight of the package
    Returns:
        vehicle_id, vehicle_type (tuple): Vehicle Id and Type of the vehicle either Drone or Cyclist
    """
    vehicle_type = "Cyclist" if weight > 5 else "Drone"
    vehicle_id = "".join(random.choice(string.ascii_letters).capitalize() for _ in range(2)) + "".join(
        [str(random.randint(1, 9)) for _ in range(4)]
    )
    return vehicle_id, vehicle_type


def schedule_orders(orders: dict) -> None:
    """
    Function to schedule orders
    Args:
        orders (dict): Complete list of orders
    """
    for order in orders:
        total_weight = get_total_weight(order["packages"])
        vehicle_id, vehicle_type = generate_vehicle(total_weight)
        displacement = get_displacement(order["destination"])  # Distance in km
        cost = displacement * 5  # Cost is £5 / km
        if vehicle_type == "Drone":
            estimated_time = displacement / 30.0  # Speed of Drones are 30 km/hr
        else:
            estimated_time = displacement / 15.0  # Speed of Cyclists are 15 km/hr
        vehicle_object = Vehicle(
            vehicle_id, vehicle_type, order["packages"], total_weight, displacement, cost, estimated_time
        )
        total_vehicles.append(vehicle_object)


@click.command()
@click.argument("orders_file")
def main(orders_file: TextIO) -> None:
    """
    Main function to schedule orders to be delivered either via Drone or Cyclist
    Args:
        orders_file (json): Complete list of orders in json file
    """
    logger.info(f"Processing orders from {orders_file}")
    orders = get_order(orders_file)
    schedule_orders(orders)
    for vehicle in total_vehicles:
        pprint(vars(vehicle))
