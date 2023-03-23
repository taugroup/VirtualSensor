import sys
sys.path.append('../../lib')
from TAUVirtualSensor import VirtualSensor

broker_address = "datahub.geos.tamu.edu"
vs = VirtualSensor(broker=broker_address, topic="air_quality", filepath="air_quality.csv", interval=5, verbose=True, tls=False)
vs.connect()
vs.read_csv()
vs.publish(loop=True)
