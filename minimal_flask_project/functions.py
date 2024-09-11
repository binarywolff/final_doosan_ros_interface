#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import numpy as np
import rospy
import sys
import subprocess
import time
import json
from std_msgs.msg import String
from tf2_msgs.msg import TFMessage
import std_msgs.msg 
import requests

# Le seguenti righe (fino alla classe ROS) servono a importare le librerie necessarie al funzionamento del Doosan
sys.dont_write_bytecode = True
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(__file__),"../../../../common/imp")) ) # get import path : DSR_ROBOT.py 

#Le seguenti due righe indicano il modello utilizzato, se non sono corrette il robot non funziona.
ROBOT_ID     = "dsr01"
ROBOT_MODEL  = "h2017"
import DR_init
DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL
from DSR_ROBOT import *

#La seguente riga importa tutti i servizi disponibili della Doosan.
from dsr_msgs.srv import * 

global stop_pallettization 
stop_pallettization = False

class ROS():
    def __init__(self):
        self.stop_pallettization = False
        
    #creazione del nodo principale, forse non serve ma lo lascio 
    def create_flask_node():
        if not rospy.is_shutdown():
            rospy.init_node('flask_ros_node', anonymous=True)
   
    #Questa funzione è stata pensata per attivarsi quando un digital input attivo di default viene staccato
    def  errors_check():
        #if(get_digital_input(1) != 1): return "la pompa dell'aria"
        #elif(get_digital_input(2) != 1): return "la presa della pinza"
        return False
    
    #Qui va il programa che il robot deve fare quando è accesso. Dipende ovviamente dall'applicazione.
    @classmethod
    def pallettizzazione(self, stop):    
        #Definizione posizioni notevoli
        sopra_scatola = posj(34.7, 49.4, 37.8, -0.0, 92.8, -79.5)
        presa_scatola = posj(34.8, 57.1, 42.6, -0.0, 80.3, -71.7)
        evita_ostacolo_1 = posj(139.3, 43.9, 58.8, -0.0, 77.3, -61.9)
        sopra_rilascio_1 =posj(155.9, 29.1, 84.2, -0.0, 66.7, -45.3)
        sopra_rilascio_2 =posj(188.9, 24.5, 91.5, -0.0, 64.0, -12.3)
        rilascio_pallet = posj(156.4, 47.1, 97.6, 0.0, 35.2, -46.2)
        rilascio_pallet_2 = posj(189.7, 43.8, 105.9, -0.1, 30.3, -12.8)

        posizioni_ordinate = [sopra_scatola, presa_scatola, sopra_scatola, evita_ostacolo_1, sopra_rilascio_1, rilascio_pallet,
                        sopra_scatola, presa_scatola, sopra_scatola, evita_ostacolo_1, sopra_rilascio_2, rilascio_pallet_2]
        
        #Per stoppare il programma. Non funziona ancora correttamente
        # if(stop == "stop"):
        #     self.stop_pallettization = True
            
        #Sorta di while(true) per tenere il robot in funzione finchè non viene fermato manualmente.
        #Il programma da fare in loop potrebbe anche essere scaricato sul PLC del robot, e quando l'operatore
        #vuole avviarlo, si scrive un valore (scelto per convenzione) su un registro MODBUS del robot.
        #while (not self.stop_pallettization):
        for i in range(0,12):
            if (i == 1 or i == 2 or i == 5 or i == 7 or i == 8 or i == 11):
                movej(posizioni_ordinate[i], vel = 30, acc = 5)
                force = get_tool_force(ref=DR_BASE)
                fz = float(force[2])
                if(fz >= -20):
                    set_digital_output(1, ON)
                    wait(0.5)
                if (i == 5 or i == 11):
                    set_digital_output(1, OFF)
            else:
                movej(posizioni_ordinate[i], vel = 30, acc = 15)
    
        return "Programma stoppato"
                    
            
            
            
    def move_home():
        with open('static/home_position.json') as f:
            position_json = json.load(f)
            print(position_json)
        
        position_temp = posj(float(position_json["j1"]), float(position_json["j2"]), float(position_json["j3"]), float(position_json["j4"]), float(position_json["j5"]), float(position_json["j6"]))
        movej(position_temp, vel = 30, acc = 5)
        
    #Funzione per movimentare il robot dando in ingresso una posizione di tipo json
    def move_to(position):
        #Modificare il json position in un'istanza della classe posj(definita dalla Doosan)
        position_temp = posj(float(position["j0"]), float(position["j1"]), float(position["j2"]), float(position["j3"]), float(position["j4"]), float(position["j5"]))
        #position_temp = posj(1,1,1,1,1,1)
        movej(position_temp, vel = 30, acc = 5) #Si posson scegliere velocità e accelerazioni differenti
        return "Movimentazione effettuata corretamente"
   
    def move_to_srv(position):
        move_client = rospy.ServiceProxy('/dsr01h2017/motion/move_joint', MoveJoint)
        
        print(position)
        position_float = [float(position["j1"]),float(position["j2"]),float(position["j3"]),float(position["j4"]),float(position["j5"]),float(position["j6"])]
        # position_float = [] * 6
        # position_float[0] = float(position["j1"])
        # position_float[1] = float(position["j2"])
        # position_float[2] = float(position["j3"])
        # position_float[3] = float(position["j4"])
        # position_float[4] = float(position["j5"])
        # position_float[5] = float(position["j6"])
        
        # position_float = [] * 6
        # position_float.append(float(position["j1"]))
        # position_float.append(float(position["j2"]))
        # position_float.append(float(position["j3"]))
        # position_float.append(float(position["j4"]))
        # position_float.append(float(position["j5"]))
        # position_float.append(float(position["j6"]))
        
        print(position_float)
        req = MoveJointRequest(position_float, 30, 5, 0, 0, 0, 0, 0)
        resp = move_client(req)
        rospy.spin() #May be commmented?
        return resp   
        
    #Funzione adibita per mettere in pausa il programma(servizio fornito dalla Doosan)                
    def pauseMotion():
        #Per usare un servizio, per prima cosa bisogna connettersi con esso.
        #La stringa: "/dsr01h2017/motion/move_pause" è il nome univico dato dall Doosan(vedi elenco servizi sullo Sharepoint)
        #La stringa: "MovePause", invece, è la classe del servizio. Per sapere quale sia, basta cercare la cartella dsr_msgs/srv
        #(in questo caso in: "/home/dario/catkin_ws/src/doosan-robot/dsr_msgs/srv") e al suo interno si trovano le classi dei servizi(dai quali deve essere tolto:".srv")
        pause_client = rospy.ServiceProxy('/dsr01h2017/motion/move_pause', MovePause)
        req = MovePauseRequest()
        resp = pause_client(req)
        rospy.spin() #May be commmented?
        return resp    
    
    #Analogamente a prima sono scritte le seguenti funzioni che chiamano i servizi.
    def resumeMotion():
        resume_client = rospy.ServiceProxy('/dsr01h2017/motion/move_resume', MoveResume)
        #while not rospy.is_shutdown():
        req = MoveResumeRequest()
        resp = resume_client(req) 
        #rospy.spin()
        return resp
            
    def stopMotion():
        stop_client = rospy.ServiceProxy('/dsr01h2017/motion/move_stop', MoveStop)
        #while not rospy.is_shutdown():
        req = MoveStopRequest()
        #req.first = 2       #Parameters: 1 = quick, 2 = slow
        resp = stop_client(req)   
        time.sleep(500)
        pause_client = rospy.ServiceProxy('/dsr01h2017/motion/move_pause', MovePause)
        req = MovePauseRequest()
        resp2 = pause_client(req)
        # rospy.spin()
        return resp, resp2
    
    def get_joint_position():    #GetCurrentPosj.srv /dsr01h2017/joint_states
        #rospy.init_node('get_joint_position')
        #posj_client = rospy.ServiceProxy('/dsr01h2017/aux_control/get_current_posj', GetCurrentPosj)
        #while not rospy.is_shutdown():
        #req = GetCurrentPosjRequest()
        #resp = posj_client(req)   

        #Invece che utilizzare il servizio si può usare la funzione dedicata della libreria.
        current_posj = get_current_posj()
        return current_posj
        
    #La seguente funzione è stato il primo tentativo di movimentazione Jog del robot.
    #Con questa funzione il robot si muove nella direzione desiderata per 2 sec.
    def jog_go_2_sec(jog_axis, reference_frame, speed):
        #Vedere il manuale per la documentazione del servizio.
        jog_client = rospy.ServiceProxy('/dsr01h2017/motion/jog', Jog)
        i = 0
        print(str(jog_axis) + str(reference_frame) + str(speed))
        while (i < 20):
            req = JogRequest(jog_axis, reference_frame, speed) #jog_axis[0 ~ 5(joints); 6 ~ 11(task X,Y,Z,rx,ry,rz)] reference_frame[0 = base, 1 = tool]
            r = rospy.Rate(10) #Hz                                #speed[%, 0 = stop, <0 = backwards]
            # r.sleep()
            resp = jog_client(req)
            i+=1
            
        req = JogRequest(jog_axis, reference_frame, 0)
        resp = jog_client(req) 
        return print(resp)

    #Questa invece è la funzione attualmente utilizzata
    #Semplicemente chiama il servizio con i parametri voluti,
    #ed è il codice in javascript a decidere come implementarlo.
    def jog_go_stop(jog_axis, reference_frame, speed):
        jog_client = rospy.ServiceProxy('/dsr01h2017/motion/jog', Jog)
        req = JogRequest(jog_axis, reference_frame, speed)
        resp = jog_client(req)
        return resp               
    
    #Funzione dedita a leggere gli input attivi e disattivi del robot
    def get_digital_input():
        digital_input = [0] * 16
        for i in range(1,17):
            digital_input[i-1] = get_digital_input(i)
            if (digital_input[i-1] < 0):
                return "An error occured with the " + i + "th digital input"
        return digital_input
    
    #Funzione dedita a leggere gli output attivi e disattivi del robot
    def get_digital_output(): 
        digital_output = [0] * 16
        for i in range(1,17):
            digital_output[i-1] = get_digital_output(i)
            if (digital_output[i-1] < 0):
                return "An error occured with the " + i + "th digital input"
        return digital_output
    
    #Funzione di ritorno in Home del robot. Ancora non testata.
    # def go_home():
    #     move_home()
    #     return "Homing completed"
    
    #Funzione per leggere i messaggi scritti so un topic
    def listener2(topic_name):
        rospy.init_node("listener", anonymous = True)
        rospy.Subscriber(topic_name, String, callback)
        rospy.spin()
        
    #Funzione che legge un messaggio da un topic e l riscrive su un altro topic.
    #Era stato testato per un problema che è stato poi risolto in maniera diversa.
    #Lo si lascia per completezza.
    def sub_pub(node_to_sub, node_to_pub):
        #Init node
        rospy.init_node("listener_and_publisher", anonymous = True)
        #Subscriber
        message = rospy.Subscriber(node_to_sub, TFMessage)
        #Publisher
        pub = rospy.Publisher(node_to_pub, TFMessage, queue_size = 10)
        pub.publish(message)
        rate = rospy.Rate(10)
        rate.sleep
        rospy.spin()
      
    #Funzione che setta gli output a true o false a seconda della richiesta.
    def set_digital_output(index, value):
        if (value):
            set_digital_output(index, ON)
            return "Sent ON on " + str(index) 
        else:    
            set_digital_output(index, OFF)
            return "Sent OFF on " + str(index)
        
    #Funzione per la connessione col robot. Ancora non funziona correttamente, perchè la disconnessione avviene una volta sì e una no(?).
    def connect_to_robot(action):
        if (action):
            global proc
            command = "cd /home/dario/catkin_ws; source devel/setup.bash; roslaunch dsr_launcher single_robot_gazebo.launch mode:=real model:=h2017 host:=10.0.1.137"
            # os.chdir("/home/dario/catkin_ws")
            # os.system("source devel/setup.bash")
            # os.system("roslaunch dsr_launcher single_robot_gazebo.launch mode:=real model:=h2017 host:=10.0.1.137")
            proc = subprocess.Popen(command,stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid)
            return "Connection made succesfully!"
        else:    
            subprocess.Popen.kill(proc)
            # os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            return "Connection killed succesfully!"
            
    
    def get_modbus_value2():
        robot_state = get_output_register_int(259)
        print("\n\n\n\n\n\n" + "The robot state is:" + robot_state + "\n\n\n\n\n\n")
        
        
