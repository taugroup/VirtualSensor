#!/bin/bash
IMAGE=vsp
# to build
rm -f $IMAGE.tar
docker build -t $IMAGE .

# to save
#docker save -o $IMAGE.tar $IMAGE

# copy to datahub
# rsync -av $IMAGE.tar jtao@datahub.geos.tamu.edu:

# to import
#docker image load -i $IMAGE.tar

# to spin up the container
docker run -p 8989:8000 -d $IMAGE
