from typing import Type
import time
import argparse
import logging

import yaml

from impl import ImplementationManager
from base import Component, Display, Fuel

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str, default="config.yaml", help="Path to the configuration file.")
args = parser.parse_args()

# Load configuration
with open(args.config, "r") as stream:
    config = yaml.load(stream, Loader=Loader)

components_config: dict = config["components"]
settings_config: dict = config["settings"]

# Initialize the implementation manager
implementations = ImplementationManager()

def setup_component[T: Component](component: Type[T]) -> T:
    component_name = component.get_component_name()
    implementation_name = components_config[component_name]
    implementation_settings = settings_config.get(implementation_name, {})

    implementations.use_implementation(component, implementation_name, implementation_settings)

    return implementations.get_component(component)

# Initialize components
fuel = setup_component(Fuel)
display = setup_component(Display)

# Post-init routines
fuel.post_init()
display.post_init()

# Main loop
try:
    while True:
        data = fuel.read()
        display.show(data)

        # Wait for 1 second
        time.sleep(1)

except KeyboardInterrupt:
    logging.info("Program terminated by user (KeyboardInterrupt).")
