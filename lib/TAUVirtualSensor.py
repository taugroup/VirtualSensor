#!/usr/bin/env python

import os
import sys
import time
import csv
import json
import paho.mqtt.client as mqtt
import logging
import pandas as pd

class VirtualSensor:
    def __init__(self, broker=None, topic=None, filepath=None, verbose=True,
                 published=False, user=None, password=None, tls=True, port=1883, 
                 timeout=600, interval=5):
        self.mqtt_user = user
        self.mqtt_password = password 
        self.tls = tls
        self.mqtt_broker = broker
        self.mqtt_port = port
        self.mqtt_timeout = timeout
        self.interval = interval
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

    def on_connect(client, userdata, flags, rc, properties=None):
        logging.debug("Connected flags " + str(flags) + "result code " + str(rc))
        if rc == 0:
            client.connected_flag = True
        else:
            client.bad_connection_flag = True
            print(f"Connected with result code : {rc}")

    def on_publish(client, userdata, mid, properties=None):
        print("Message Published.")

    def on_log(client, userdata, level, buf):
        print("log: ", buf)

    def connect(self):
        # Create an MQTT client instance
        self.mqtt_client = mqtt.Client(client_id="", userdata=None, protocol=mqtt.MQTTv5)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_log = self.on_log
        self.mqtt_client.on_publish = self.on_publish

        if self.tls:
            # Set TLS context
            self.mqtt_client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
            print("enable TLS")

        # set username and password
        if self.mqtt_user:
            self.mqtt_client.username_pw_set(self.mqtt_user, self.mqtt_password)
            print("set user and password for MQTT: ", self.mqtt_user)

        if self.verbose:
            self.mqtt_client.enable_logger()

        self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port)

    def read_csv(self):
        if not os.path.exists(self.filepath):
            print(self.filepath)
            print ("The file is not found!")
            return False

        if self.filepath.lower().endswith(".csv"):
            print("Start processing CSV file.")
            with open(self.filepath, mode='r') as csv_file:
                dialect = csv.Sniffer().sniff(csv_file.readline())
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
                        print (data_val)
                        count = 0
                        for value in key_values:
                            temp_val[value] = data_val[count]
                            count += 1
                        self.data_value.append(temp_val)
                        line_count += 1
            self.fields = key_values
            if self.verbose:
                print("The file is processed successfully")
                print("The keys are:", self.fields)

    def pandas_read(self):
        df = pd.read_csv(self.filepath)
        df = df.T
        df.drop(df.index[:10], inplace=True)
        df['json'] = df.apply(lambda x: x.to_json(), axis=1)
        self.key_values = df.columns
        self.data_value = df['json'].values.tolist()

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
# infinite loop
        if loop:
            while True:
                for value in self.data_value:
                    temp_data_val = str(value).replace("'", '"')
                    try:
                        self.mqtt_client.publish(self.topic, payload=temp_data_val, qos=0, retain=True)
                        if self.verbose:
                            print(self.topic, temp_data_val)
                        time.sleep(self.interval)
                    except Exception as e:
                        print(f"Publish Failed. {e}")
                        self.connect()
                        pass
        else:
            for value in self.data_value:
                temp_data_val = str(value).replace("'", '"')
                try:
                    if self.verbose:
                        print(self.topic, temp_data_val)
                    self.mqtt_client.publish(self.topic, payload=temp_data_val, qos=1)
                    time.sleep(self.interval)
                except Exception as e:
                    print(f"Publish Failed. {e}")            
                    self.connect()
                    pass
        return
