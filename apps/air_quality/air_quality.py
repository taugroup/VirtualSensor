import sys
sys.path.append('../../lib')
from TAUVirtualSensor import VirtualSensor

broker_address = "datahub.geos.tamu.edu"
vs = VirtualSensor(broker_address, filepath="air_quality.csv", delimiter=";", interval=1)
vs.publish()

