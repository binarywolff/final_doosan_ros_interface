from flask import Blueprint, render_template
import os
from flask import request
import functions
import logging  
from flask import send_from_directory
from pathlib import Path
import json
import errors_handle.errors_functions as errors_functions
import requests

bp = Blueprint("pages", __name__)

#Se il robot è connesso, porre la seguente variabile al valore True, altrimenti lasciarlo a False.
robot_present = False

#Il funzionmento delle seguenti route/post è speigato nella guida.
#Le route direzionano alle pagine HTML o alla funzioni definite nel file:"functions.py"
#Le post direzionani alle funzioni ma prendendo in ingresse dei parametri passati dal javscript.

@bp.route("/")
def home():
    if (functions.ROS.errors_check()):
        return render_template("pages/errore.html")   
    else:
        if(robot_present):
            digital_input = functions.ROS.get_digital_input()
            joint_position = functions.ROS.get_joint_position()
            return render_template("pages/home.html",digital_input=digital_input,joint_position=joint_position)#,digital_input=digital_input,joint_position=joint_position
        elif(not robot_present):
            return render_template("pages/home.html")
@bp.route("/pallet")
def pallet():
    return render_template("pages/pallet.html")

@bp.route("/plc")
def plc():
    return render_template("pages/plc.html")

@bp.route("/pallettizzazione")
def esegui_pallettizzazione():
    functions.ROS.pallettizzazione("")
    return "Pallettizzazione in corso" 

@bp.route("/pausa")
def pausa():
    resp = functions.ROS.pauseMotion()
    return resp

@bp.route("/resume")
def resume():
    resp = functions.ROS.resumeMotion()
    return resp

@bp.route("/stop")
def stop():
    resp = functions.ROS.stopMotion()
    return resp

@bp.post("/go_home")
def go_home():
    #Chiama la funzione move to per muovere il robot
    if(request.method == 'POST'):
        json_position = request.json
        #json_position = json.loads(string_position)
        print(json_position)
        position = json.dumps(json_position)
        print(position)
        resp = functions.ROS.move_to_srv(json_position)
        return resp

@bp.route("/errore")
def errors():
    return render_template('pages/errore.html')

@bp.route("/jog")
def jog():
    if(robot_present):
        current_posj = functions.ROS.get_joint_position()
        for i in range(0,6):
            current_posj[i] = round(current_posj[i], 2)
        return render_template('pages/jog.html', current_posj = current_posj, robot_present = robot_present) 
    elif(not robot_present):
        return render_template('pages/jog.html', robot_present = robot_present)

#background process happening without any refreshing
@bp.route('/get_joint_position')
def get_joint_position():
    functions.ROS.get_joint_position()
    return "Joint position get"

@bp.post("/foo")
def foo_post():
    mytext = request.form["mytext"]
    return mytext

@bp.post("/jog_function")
def jog_user_function():

    if(request.method == 'POST'):
        logging.warning("Jooooooooint______1:")
        json_data = request.json
        axis = int(json_data["joint_axis"])
        frame = int(json_data["frame"])
        speed = int(json_data["speed"])
        
        jog_data = request.form
        
        response = functions.ROS.jog_go_stop(axis, frame, speed)
        return "response"
    
    else:
        return "Hello world"

@bp.route("/map")
def map():
    return render_template("pages/ros3djs.html")

@bp.route("/map2")
def map2():
    return render_template("pages/ur_map.html")

@bp.route("/urdf2")
def urdf2():
    return render_template("pages/urdf.html")

@bp.route("/static/model/h2017")
def serveArmModel():
    return send_from_directory('/home/dario/catkin_ws/src/doosan-robot/dsr_example/py/scripts/flask_project/static/m1013_white', "m1013.urdf")

@bp.route("/ros3djs_folder")
def serve_ros3djs_folder():
    return send_from_directory('/home/dario/catkin_ws/src/ros3djs/build', "ros3d.js")

@bp.route("/urdf")
def urdf():
    return render_template("pages/rosedjs/examples/urdf2.html")

@bp.route("/test")
def test():
    return render_template("pages/test.html")

@bp.route("/flex")
def flex():
    return render_template("pages/flex.html")

@bp.post("/set_digital_output")
def set_digital_output():
    if(request.method == 'POST'):
        body = request.json
        index = int(body["index"])
        value = bool(body["value"])
        # value = True if request.form('value') == "true" else False
        resp = functions.ROS.set_digital_output(index, value)
        return resp
    else:
        return resp
    
@bp.route("/ferma_programma")
def ferma_programma():
    resp = functions.ROS.pallettizzazione("stop")
    return resp

@bp.post("/connect_to_robot")
def connect_to_robot():
    if(request.method == 'POST'):
        body = request.json
        action = bool(body["action"])

        if(action):
            resp = functions.ROS.connect_to_robot(True)
            return resp
    
        else:
            resp = functions.ROS.connect_to_robot(False)
            return resp

@bp.post("/update_home_position")
def update_home_position():
    if(request.method == 'POST'):
        position_json = request.json
        path = Path('static/home_position.json')
        path.write_text(json.dumps(position_json))    
        return "T'apposto" 
    
@bp.route("/get_modbus_value")
def get_modbus_value1():
    functions.ROS.get_modbus_value2()
    return "Ok"

@bp.route("/errors_notification")
def errors_notifications():
    resp = errors_functions.send_error_indexes()
    return resp