from flask import Flask
from flask_cors import CORS
import pages
from flask_apscheduler import APScheduler
import rospy
from flask import Flask, render_template, request, jsonify
import errors_handle.errors_functions as errors_functions
from std_msgs.msg import String 
import functions
import os
import datetime
import socketio

#Questo è il file lanciato per avviare il software.
#La funzione create_app() deve essere scritta come nella documentazione relativa di Flask.
def create_app():
    app = Flask(__name__)
    #Il CORS serve per poter mostrare su un riquadro di una pagina html, ciò che viene mostrato su un'altra pagina html.
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.register_blueprint(pages.bp)
    return app

def  errors_check():
    #if(get_digital_input(1) != 1): return "la pompa dell'aria"
    #elif(get_digital_input(2) != 1): return "la presa della pinza"
    #print("1 sec is passed")
    #errors_functions
    return False
    
def exit_handler():
    #close node
    pass

#Viene inizializzato il nodo dell'interfaccia per poter comunicare con il nodo master di roscore.
    


#os.system("rosrun rosbridge_server rosbridge_websocket")


#Il seguente codice serve a lanciare una certa funzione ogni n secondi.
# scheduler = APScheduler()
# scheduler.add_job(func=errors_check, trigger='interval', id='job', seconds=1)
# scheduler.start()


