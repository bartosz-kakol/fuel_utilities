# Fuel Utilities

A modular Python application for monitoring and displaying vehicle fuel information using an OBD-II connection.

> [!IMPORTANT]
> This project is currently in development and is not fully functional.

## Overview

Fuel Utilities is designed to help vehicle owners monitor their fuel consumption and levels in real-time. The application connects to a vehicle's OBD-II port to retrieve fuel data and displays it on a connected display device (such as an SH1107 OLED display) or in a mock environment for testing and development.

The application is built with a modular, component-based architecture that makes it easy to extend with new implementations for different display types or fuel data sources.

## Features

- Real-time fuel monitoring via OBD-II connection
- Support for SH1107 OLED displays
- Mock implementations for testing without hardware
- Configurable via YAML files
- Extensible architecture for adding new components

## Installation

### Prerequisites

- Python 3.10 or higher
- I2C-enabled device (for hardware display)
- OBD-II adapter (for connecting to vehicles)

### Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd fuel_utilities
   ```

2. Install dependencies:
   ```
   make deps
   ```
   
   Or manually:
   ```
   pip install -r requirements.txt
   ```

3. Create a configuration file:
   ```
   cp config.dist.yaml config.yaml
   ```

4. Edit the configuration file to match your setup (see Configuration section below).

## Running the Application

To run the application with the default configuration:

```
python main.py
```

To specify a different configuration file:

```
python main.py --config path/to/config.yaml
```

## Configuration

The application is configured using a YAML file. By default, it looks for `config.yaml` in the project root, but you can specify a different file using the `--config` command-line option.

### Configuration Options

The configuration file has two main sections:

1. `components`: Specifies which implementation to use for each component type
2. `settings`: Contains settings specific to each implementation

Example configuration:

```yaml
components:
  display: sh1107  # Use the SH1107 OLED display implementation
  fuel: obd        # Use the OBD-II implementation for fuel data

settings:
  sh1107:
    bus: 1         # I2C bus number
    address: 0x3C  # I2C device address
  obd:
    connection:
      portstr: /dev/ttyUSB0  # Serial port for OBD-II adapter
      baudrate: 38400        # Baud rate for communication
    fuel_tank_capacity: 45   # Fuel tank capacity in liters
```

For development or testing without hardware, you can use the mock implementations:

```yaml
components:
  display: mock
  fuel: mock
```

## Architecture

The application is built around a component-based architecture with clear interfaces and implementations:

### Components

1. **Fuel Component**: Responsible for reading fuel data from a source (e.g., OBD-II)
   - Interface: `base.Fuel`
   - Implementations:
     - `impl.fuel.mock`: A mock implementation for testing
     - `impl.fuel.obd`: An implementation that reads data from OBD-II

2. **Display Component**: Responsible for showing fuel data to the user
   - Interface: `base.Display`
   - Implementations:
     - `impl.display.mock`: A mock implementation that prints to the console
     - `impl.display.sh1107`: An implementation for SH1107 OLED displays

### Implementation Manager

The `ImplementationManager` class handles loading and instantiating component implementations based on the configuration. It uses Python's dynamic import capabilities to load the specified implementations at runtime.

## Extending the Application

The modular architecture makes it easy to extend the application with new implementations for existing components or entirely new component types.

### Adding a New Implementation

To add a new implementation for an existing component:

1. Create a new Python file in the appropriate directory (e.g., `impl/display/new_display.py` for a new display implementation)
2. Implement the required interface (e.g., `Display` for a display implementation)
3. Export the implementation class as `export` at the module level
4. Update your configuration to use the new implementation

Example implementation:

```python
from base import Display

class NewDisplayImpl(Display):
    def init(self, **properties):
        # Initialize your display with the provided properties
        pass

    def post_init(self):
        # Perform any post-initialization tasks
        pass

    def show(self, data: dict):
        # Show the data on your display
        pass

# Export the implementation class
export = NewDisplayImpl
```

### Adding a New Component Type

To add a new component type:

1. Create a new interface in the `base` directory (e.g., `base/new_component.py`)
2. Extend the `Component` base class and define the required methods
3. Create implementations in a new directory under `impl` (e.g., `impl/new_component/`)
4. Update the main application to use the new component

## Makefile Shortcuts

The project includes a Makefile with shortcuts for common operations:

- `make deps`: Install project dependencies from requirements.txt
- `make assets`: Compile assets for the application

## Assets

The application uses compiled assets for display purposes. To compile the assets:

```
make assets
```

This runs the asset compiler script at `./assets/compiler.py`, which processes the assets and generates the `compiled.assets` file used by the application.

## Troubleshooting

### Common Issues

1. **OBD-II Connection Failures**:
   - Ensure the OBD-II adapter is properly connected
   - Verify the correct port and baud rate in the configuration
   - Check that the vehicle's ignition is on

2. **Display Issues**:
   - Verify the I2C bus and address settings
   - Check the physical connections
   - Try running with the mock display to isolate the issue
