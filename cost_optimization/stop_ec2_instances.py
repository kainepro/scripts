
# Script to stop running EC2 Instances when not required; must tag instances you want to stop with 'prostop'
# In EC2 Tags, use Key: prostop Value: stop, then run './prostop.py' in CLI.
# Todo: Improve automation to include scheduling (stop at evenings to save cost), mark running instances and stop unknown instances
# Script for starting instances in during office hours, set different actions for weekdays and weekends
#  Tag to identify how many hours you want an instance to run (ideal for prototyping)

#!/usr/bin/env python

import boto3

# Connect to the Amazon EC2 service
ec2 = boto3.resource('ec2')

# Loop through each instance
for instance in ec2.instances.all():
  state = instance.state['Name']
  for tag in instance.tags:

    # Check for the 'prostop' tag
    if tag['Key'] == 'prostop':
      action = tag['Value'].lower()
      
      # Stop?
      if action == 'stop' and state == 'running':
        print "Stopping instance", instance.id
        instance.stop()
      
      # Terminate?
      elif action == 'terminate' and state != 'terminated':
        print "Terminating instance", instance.id
        instance.terminate()