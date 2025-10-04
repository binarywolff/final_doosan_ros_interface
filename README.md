# Flask-Doosan-ROS Web Interface

This project is a **web application built with Flask** that connects to a **Doosan robot** using the **Robot Operating System (ROS)**.  
It provides a browser-based interface to **control the robot's motion**, **write and execute Python programs**, and **visualize the robot in 3D** using [`ros3djs`](http://wiki.ros.org/ros3djs).

---

## 🚀 Features
- Control the Doosan robot’s motion (joint and Cartesian commands) directly from the browser.
- Write, save, and execute custom Python robot programs through the web UI.
- Visualize the robot in 3D in real time with `ros3djs`.
- Communicate with ROS topics, services, and actions via `rosbridge_server`.
- Flask backend manages communication, execution, and the web interface.

---


### Installation & Usage

#### 1. Prerequisites
- Ubuntu 20.04 / 22.04  
- ROS Noetic
- Doosan ROS driver installed and running  
- Python 3.x
- Flask
- rosbridge_server
- JavaScript libraries:
  - three.js
  - roslib.js
  - ROS3D.js


#### 2. Clone the Repository
```bash
git clone https://github.com/your-username/flask-doosan-ros.git
cd flask-doosan-ros

