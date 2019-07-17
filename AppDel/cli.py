#!/bin/python3
"""
Main runner for ApplianceDelivery.
"""


import json
import click
import random
import string
import logging


from typing import TextIO
from .lookup import PRODUCT_INVENTORY


logger = logging.getLogger(__name__)


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


def generate_vehicle(weight: float) -> (str, str):
    """
    Function to choose the vehicle of delivery from the orders based on weight and destination
    Args:
        weight (float): Total weight of the package
    Returns:
        vehicle_id, vehicle_type (tuple): Vehicle Id and Type of the vehicle either Drone or Cyclist
    """
    vehicle_type = "Cyclist" if weight > 5 else "Drone"
    vehicle_id = "".join(
        random.choice(string.ascii_letters).capitalize() for _ in range(2)
    ) + "".join([str(random.randint(1, 9)) for _ in range(4)])
    return vehicle_id, vehicle_type


def schedule_orders(orders: dict) -> None:
    """
    Function to schedule orders
    Args:
        orders (dict): Complete list of orders
    """
    print("Vehicle_Id", "           ", "Vehicle_Type")
    for order in orders:
        vehicle_id, vehicle_type = generate_vehicle(
            get_total_weight(order["packages"])
        )
        print(vehicle_id, "                ", vehicle_type)


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
