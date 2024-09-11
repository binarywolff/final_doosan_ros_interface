#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Controller_digital_input:        
    def __init__(self):
        #Inserire i valori del controller digital input, quando il robot è in funzione
        #Controller digital inputs
        self.cdi_array = [1,0,0,0, 0,0,0,0, 0,0,0,0 ,0,0,0,0]
        
class Flange_digital_input:
    def __init__(self):
        #Inserire i valori del controller digital output, quando il robot è in funzione
        #Controller digital input
        self.fdi_array = [0,0,0, 0,0,0]
                
class Controller_digital_output:        
    def __init__(self):
        #Inserire i valori del controller digital output, quando il robot è in funzione
        #Controller digital output
        self.cdo_array = [0,0,0,0, 0,0,0,0, 0,0,0,0 ,0,0,0,0]
        
        