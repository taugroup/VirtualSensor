import sys
sys.path.append('../../lib')
from TAUVirtualSensor import VirtualSensor

#broker_address = "datahub.geos.tamu.edu"
broker_address = "localhost"
vs = VirtualSensor(broker_address, filepath="air_quality.csv", delimiter=";", interval=5)
vs.publish()
