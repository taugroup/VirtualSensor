#!/usr/bin/env python

import os
import sys
import time
import csv
import json
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc_value):
    print(f"Connected with result code : {rc_value}")

def on_publish(client, userdata, mid):
    print("Message Published.")
    
def on_log(client, userdata, level, buf):
    print("log: ", buf)
    
class VirtualSensor:
    def __init__(self, broker, topic="taugroup", filepath=None, verbose=True,
                 port=1883, timeout=60, interval=5, delimiter=",",
                 connect_cb=on_connect, publish_cb=on_publish, log_cb=on_log):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = connect_cb
        self.mqtt_client.on_publish = publish_cb
        self.mqtt_client.on_log = log_cb
        self.mqtt_client.connect(broker, port, timeout)
        self.interval = interval
        self.delimiter = delimiter
#TODO insert more checks
        self.filepath = filepath
        self.topic = os.path.basename(filepath).split('.')[0]
        
        if verbose:
            print("broker   :", broker)
            print("topic    :", self.topic)
            print("file path:", self.filepath)
            print("interval :", self.interval)
            print("delimiter:", self.delimiter)

    def publish(self, loop=True):
        if not os.path.exists(self.filepath):
            print ("The file is not found!")
            return False
        data_value = {}
        key_values = []

        if self.filepath.lower().endswith(".csv"):
            with open(self.filepath, mode='r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=self.delimiter)
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        key_values = row
                        line_count += 1
                    else:
                        temp_val = {}
                        data_val = row
                        count = 0
                        for value in key_values:
                            temp_val[value] = data_val[count]
                            count += 1
                        data_value[line_count] = temp_val
                        line_count += 1
        elif self.filepath.lower().endswith(".json"):
            with open (self.filepath, mode='r') as json_file:
                data_value = json.loads(json_file.read())

        else:
            print("Only CSV and Json files are supported!")
            return False

# infinite loop
        if loop:
            while True:
                for value in data_value:
                    temp_data_val = str(data_value[value]).replace("'", '"')
                    try:
                        self.mqtt_client.publish(self.topic, temp_data_val)
                        time.sleep(self.interval)
                    except Exception as e:
                        print(f"Publish Failed. {e}")
        else:
            for value in data_value:
                temp_data_val = str(data_value[value]).replace("'", '"')
                try:
                    self.mqtt_client.publish(self.topic, temp_data_val)
                    time.sleep(self.interval)
                except Exception as e:
                    print(f"Publish Failed. {e}")            
        return True
