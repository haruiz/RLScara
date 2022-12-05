## INFO

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![TensorFlow 2.2](https://img.shields.io/badge/TensorFlow-2.^-FF6F00?logo=tensorflow)](https://github.com/tensorflow/tensorflow/releases/tag/v2.2.0)


### Description

### Arduino based Arm Platform


### 2D simulated Arm Platform

### Project Layout

- `3D models/`: 3D models folder. contains all the artifacts generated to build the 3d printed based arm platform
- `docs/` : Documentation folder
- `arduino/` : Arduino sketch code to control the arm platform
- `py/` : Python code generated to build the arm platform.

    **core classes**

    - `arm_controller.py` : Arm controller, it contains the class to control the arm platform.
    - `arm_env.py` : RL environment, it contains the class to build the RL environment
    - `arm_rl_model.py` : Arm model, it contains the class to build the RL model. For this project we used and implementation of the DDPG algorithm
    - `main.py` : Application entry point, this script should be used to train, evaluate the model, and  for rendering the simulation environment.
    
    **utils**

    - `arduino_utils.py` : Arduino utils, it contains some functions and classes to control the Arduino board.
    - `math_utils.py` : Math utils, it contains some functions and classes to perform some math operations.
    - `plot_utils.py` : Plot utils, it contains some functions and classes to plot the results.

### Installation
- Using pip

For running the app, we recommend to create a virtual environment and install the dependencies running the command below.

```bash
pip install -r requirements.txt
```

- Using poetry

For poetry users, run the command `poetry install` within the `py` folder. All the dependecies are listed in the `py/pyproject.toml` file.

```
cd py
poetry install
```

## LOGS
### 09/28/22
- added repo
