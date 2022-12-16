#!/usr/bin/env python

import os
import sys
import time
import csv
import json
import paho.mqtt.client as mqtt
import logging

def on_connect(client, userdata, flags, rc):
    logging.debug("Connected flags " + str(flags) + "result code " + str(rc))
    if rc == 0:
        client.connected_flag = True
    else:
        client.bad_connection_flag = True
        print(f"Connected with result code : {rc}")

def on_publish(client, userdata, mid):
    print("Message Published.")
    
def on_log(client, userdata, level, buf):
    print("log: ", buf)
    
class VirtualSensor:
    def __init__(self, broker=None, topic=None, filepath=None, verbose=True,
                 published=False, port=1883, timeout=60, interval=5, delimiter=",",
                 connect_cb=on_connect, publish_cb=on_publish, log_cb=on_log):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = connect_cb
        self.mqtt_client.on_publish = publish_cb
        self.mqtt_client.on_log = log_cb
        self.mqtt_broker = broker
        self.mqtt_port = port
        self.mqtt_timeout = timeout
        self.interval = interval
        self.delimiter = delimiter
        self.filepath = filepath
        if topic:
            self.topic = topic
        else:
            self.topic = os.path.basename(filepath).split('.')[0]
        self.verbose = verbose
        self.published = published
        self.data_value = []
        self.key_values = []
        self.fields = []

        if self.verbose:
            print("broker   :", broker)
            print("topic    :", self.topic)
            print("file path:", self.filepath)
            print("interval :", self.interval)
            print("delimiter:", self.delimiter)

    def read_csv(self):
        if not os.path.exists(self.filepath):
            print(self.filepath)
            print ("The file is not found!")
            return False

        if self.filepath.lower().endswith(".csv"):
            with open(self.filepath, mode='r') as csv_file:
                dialect = csv.Sniffer().sniff(csv_file.read(1024))
                csv_file.seek(0)
                csv_reader = csv.reader(csv_file, dialect)
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
                        self.data_value.append(temp_val)
                        line_count += 1
            self.fields = key_values

    def read_json(self):
        if not os.path.exists(self.filepath):
            print(self.filepath)
            print ("The file is not found!")
            return False

        if self.filepath.lower().endswith(".json"):
            with open (self.filepath, mode='r') as json_file:
                self.data_value = json.loads(json_file.read())

        else:
            print("Only CSV and Json files are supported!")
            return False


    def publish(self, loop=True):
        self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port, self.mqtt_timeout)
# infinite loop
        if loop:
            while True:
                for value in self.data_value:
                    temp_data_val = str(value).replace("'", '"')
                    try:
                        if self.verbose:
                            print(self.topic, temp_data_val)
                        self.mqtt_client.publish(self.topic, temp_data_val)
                        time.sleep(self.interval)
                    except Exception as e:
                        print(f"Publish Failed. {e}")
        else:
            for value in self.data_value:
                temp_data_val = str(value).replace("'", '"')
                try:
                    if self.verbose:
                        print(self.topic, temp_data_val)
                    self.mqtt_client.publish(self.topic, temp_data_val)
                    time.sleep(self.interval)
                except Exception as e:
                    print(f"Publish Failed. {e}")            
        return
