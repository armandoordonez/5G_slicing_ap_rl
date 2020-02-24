# Monitor

Extract stats and act as a middle man between the IA and the docker containers. The system send the order to the osm NorthBoundInterface to scale up/down a given vnf. This software is able to modify the haproxy loadbalancer and add or reduce the number of instances to distribute the load.

# Requirements 

- You must have up and running cAdvisor in the OSM machine.

- You must have instantiated sometype of NS(network service) from OSM before execute this software.

- You must execute this script in the  OSM machine if you want to see the load balancer reflected.

# First Steps

Execute vnf_manager_cleaned.py --dst_ip osm_ip --sdm_ip  reinforcement_learning_ip --sdm_port reinforcement_learning_port to enable the monitoring over the osm, the script is in charge of send parsed data to the reinforcement learning algorithm.

# Warnings
- Dont  use "-" in the vnf-names


# Clone into another virtual machine from another account.
 - Pull automate
 - Delete This...
 - After get all GCloud permisions execute: gcloud compute disks create vm-prod-disk --source-snapshot \
 https://www.googleapis.com/compute/v1/projects/<source-\
 project>/global/snapshots/<source-vm-snapshot> --project target-project
  like this: gcloud compute disks create vm-prod-disk --source-snapshot https://www.googleapis.com/compute/v1/projects/golden-ego-255515/global/snapshots/osmsnapshot --project osmscaling-269020
  check: https://www.edureka.co/community/58337/recreating-different-transfer-snapshot-projects-projects
