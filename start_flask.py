#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
from concurrent.futures import ProcessPoolExecutor

def my_parallel_command(command):
    subprocess.run(command, shell=True)

def all_commands():
    cmd1 = "roscore"
    cmd2 = "cd /home/dario/catkin_ws/src/doosan-robot/dsr_example/py/scripts/minimal_flask_project; python -m flask --app __init__ run --port 8000 --debug"
    cmd3 = "cd /home/dario/catkin_ws; source devel/setup.bash; roslaunch dsr_launcher single_robot_gazebo.launch mode:=real model:=h2017 host:=10.0.1.137"
    #cmd4 = "cd /home/dario/catkin_ws; source devel/setup.bash; rosrun rosbridge_server rosbridge_wewbsocket"
    
     
    commands = [cmd1, cmd2, cmd3]
    cpus = 2
    with ProcessPoolExecutor(max_workers = cpus) as executor:
        futures = executor.map(my_parallel_command, commands)
    
if __name__ == '__main__':
    all_commands()
    
    
    
 #######################il seguente codice era utilizzato nella versione precedente, lo si lascia per completezza#######################   
# global proc1
# global proc2
# global proc3
# def activate_roscore():
#     command = "roscore"
#     # proc1 = subprocess.Popen(command,stdout=subprocess.PIPE, 
#     #                    shell=False, preexec_fn=os.setsid)   
#     subprocess.run([command])
    
# def run_app(value):
#     if (value == "b"):
#         #open bootstrap project
#         os.chdir("/home/dario/catkin_ws/src/doosan-robot/dsr_example/py/scripts/bootstrap_flask_project")
    
#     elif (value =="f"):
#         #open original flask project
#         os.chdir("/home/dario/catkin_ws/src/doosan-robot/dsr_example/py/scripts/flask_project")
    
#     elif (value =="m"):
#         #open minimal flask project
#         os.chdir("/home/dario/catkin_ws/src/doosan-robot/dsr_example/py/scripts/minimal_flask_project")
    
#     elif (value =="g"):
#         #open github project
#         os.chdir("/home/dario/github/doosan-flask-interface")

#     #run application
#     # os.system("python -m flask --app __init__ run --port 8000 --debug")
#     command = "python -m flask --app __init__ run --port 8000 --debug"
#     subprocess.run([command])
    
# def connect_robot():
#     command = "cd /home/dario/catkin_ws; source devel/setup.bash; roslaunch dsr_launcher single_robot_gazebo.launch mode:=real model:=h2017 host:=10.0.1.137"
#     # proc2 = subprocess.Popen(command,stdout=subprocess.PIPE, 
#     #                    shell=False, preexec_fn=os.setsid)
#     subprocess.run([command])
    
# def run_web_socket():
#     command = "cd /home/dario/catkin_ws; source devel/setup.bash; rosrun rosbridge_server rosbridge_wewbsocket"
#     # proc3 = subprocess.Popen(command,stdout=subprocess.PIPE, 
#     #                    shell=False, preexec_fn=os.setsid)    
#     subprocess.run([command])

# def activate():
#     activate_roscore()
#     run_app(value)
#     connect_robot()
#     run_web_socket()

# def exit_handler():
#     subprocess.Popen.kill(proc1)
#     subprocess.Popen.kill(proc2)
#     subprocess.Popen.kill(proc3)
    
    
