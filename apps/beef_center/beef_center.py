import sys
sys.path.append('../../lib')
from TAUVirtualSensor import VirtualSensor

broker_address = "datahub.geos.tamu.edu"
vs = VirtualSensor(broker_address, filepath="beef_center.csv", delimiter=",", interval=1)
vs.publish()

