#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import time
import errors_handle.i_o_classes
import sys
import os
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
        
def send_error_indexes():
    #array degli indici con errori
    digital_inputs_error_indexes = check_controller_digital_input_errors()
    flange_digital_inputs_error_indexes = check_flange_digital_input_errors()
    return digital_inputs_error_indexes, flange_digital_inputs_error_indexes
    
def check_controller_digital_input_errors():
    #creazione di un'istanza della calsse Controller_digital_input
    controller_digital_inputs = errors_handle.i_o_classes.Controller_digital_input()
    #creazione elenco digital input con error
    controller_digital_inputs_error_indexes = []
    #salvataggio valori misurati
    for i in range(1,17):
        if (get_digital_input(i) != controller_digital_inputs.cdi_array[i-1]):
            #salvataggio dell'input con errore nel relativo array
            controller_digital_inputs_error_indexes.append(i)
    return controller_digital_inputs_error_indexes

def check_flange_digital_input_errors():
    #creazione di un'istanza della calsse Controller_digital_input
    flange_digital_inputs = errors_handle.i_o_classes.Flange_digital_input()
    #creazione elenco digital input con error
    flange_digital_inputs_error_indexes = []
    #salvataggio valori misurati
    for i in range(1,7):
        if (get_tool_digital_input != flange_digital_inputs.fdi_array[i-1]):
            #salvataggio dell'input con errore nel relativo array
            flange_digital_inputs_error_indexes.append(i)
    return flange_digital_inputs_error_indexes

def check_controller_digital_put_errors():
    #creazione di un'istanza della calsse Controller_digital_input
    controller_digital_outputs = errors_handle.i_o_classes.Controller_digital_output()
    #creazione elenco digital output con error
    controller_digital_outputs_error_indexes = []
    #salvataggio valori misurati
    for i in range(1,17):
        if (get_digital_output(i) != controller_digital_outputs.cdo_array[i-1]):
            #salvataggio dell'output con errore nel relativo array
            controller_digital_outputs_error_indexes.append(i)
    return controller_digital_outputs_error_indexes



    