import imp
import yaml
import datetime
import pytz
from freezegun import freeze_time

rec2 = imp.load_source('rec2', './rec2/rec2.py')
a = rec2.Rec2()

# details
asg_details = {
            "AutoScalingGroupARN": "arn:aws:autoscaling:us-west-2:761425999210:autoScalingGroup:f604b0bf-e970-45a2-87c0-9cb336dcaeda:autoScalingGroupName/WebAppASG",
            "HealthCheckGracePeriod": 300,
            "SuspendedProcesses": [],
            "DesiredCapacity": 1,
            "Tags": [
                {
                    "ResourceType": "auto-scaling-group",
                    "ResourceId": "WebAppASG",
                    "PropagateAtLaunch": True,
                    "Value": "Production",
                    "Key": "Environment"
                },
                {
                    "ResourceType": "auto-scaling-group",
                    "ResourceId": "WebAppASG",
                    "PropagateAtLaunch": True,
                    "Value": "WebAppASG",
                    "Key": "Name"
                }
            ],
            "EnabledMetrics": [],
            "LoadBalancerNames": [
                "PROD-ELB"
            ],
            "AutoScalingGroupName": "WebAppASG",
            "DefaultCooldown": 300,
            "MinSize": 1,
            "Instances": [
                {
                    "ProtectedFromScaleIn": False,
                    "AvailabilityZone": "us-west-2a",
                    "InstanceId": "i-d031f714",
                    "HealthStatus": "Healthy",
                    "LifecycleState": "InService",
                    "LaunchConfigurationName": "WebAppASGLaunchConfigC"
                }
            ],
            "MaxSize": 4,
            "VPCZoneIdentifier": "subnet-03b96f66",
            "TerminationPolicies": [
                "Default"
            ],
            "LaunchConfigurationName": "WebAppASGLaunchConfigC",
            "CreatedTime": "2015-06-03T23:34:14.159Z",
            "AvailabilityZones": [
                "us-west-2a"
            ],
            "HealthCheckType": "EC2",
            "NewInstancesProtectedFromScaleIn": False
        }
asg_details_cooldown_invalid = {
            "AutoScalingGroupARN": "arn:aws:autoscaling:us-west-2:761425999210:autoScalingGroup:f604b0bf-e970-45a2-87c0-9cb336dcaeda:autoScalingGroupName/WebAppASG",
            "HealthCheckGracePeriod": 300,
            "SuspendedProcesses": [],
            "DesiredCapacity": 1,
            "Tags": [
                {
                    "ResourceType": "auto-scaling-group",
                    "ResourceId": "WebAppASG",
                    "PropagateAtLaunch": True,
                    "Value": "Production",
                    "Key": "Environment"
                },
                {
                    "ResourceType": "auto-scaling-group",
                    "ResourceId": "WebAppASG",
                    "PropagateAtLaunch": True,
                    "Value": "WebAppASG",
                    "Key": "Name"
                },
                {
                    "ResourceType": "auto-scaling-group",
                    "ResourceId": "WebAppASG",
                    "Key": "rec2-modify-to-standard",
                    "Value": datetime.datetime(2016, 1, 1, 19, 0, 0, 0, tzinfo=pytz.utc),
                    "PropagateAtLaunch": False
                }
            ],
            "EnabledMetrics": [],
            "LoadBalancerNames": [
                "PROD-ELB"
            ],
            "AutoScalingGroupName": "WebAppASG",
            "DefaultCooldown": 300,
            "MinSize": 1,
            "Instances": [
                {
                    "ProtectedFromScaleIn": False,
                    "AvailabilityZone": "us-west-2a",
                    "InstanceId": "i-d031f714",
                    "HealthStatus": "Healthy",
                    "LifecycleState": "InService",
                    "LaunchConfigurationName": "WebAppASGLaunchConfigC"
                }
            ],
            "MaxSize": 4,
            "VPCZoneIdentifier": "subnet-03b96f66",
            "TerminationPolicies": [
                "Default"
            ],
            "LaunchConfigurationName": "WebAppASGLaunchConfigC",
            "CreatedTime": "2015-06-03T23:34:14.159Z",
            "AvailabilityZones": [
                "us-west-2a"
            ],
            "HealthCheckType": "EC2",
            "NewInstancesProtectedFromScaleIn": False
        }
asg_details_cooldown_not_met = {
            "AutoScalingGroupARN": "arn:aws:autoscaling:us-west-2:761425999210:autoScalingGroup:f604b0bf-e970-45a2-87c0-9cb336dcaeda:autoScalingGroupName/WebAppASG",
            "HealthCheckGracePeriod": 300,
            "SuspendedProcesses": [],
            "DesiredCapacity": 1,
            "Tags": [
                {
                    "ResourceType": "auto-scaling-group",
                    "ResourceId": "WebAppASG",
                    "PropagateAtLaunch": True,
                    "Value": "Production",
                    "Key": "Environment"
                },
                {
                    "ResourceType": "auto-scaling-group",
                    "ResourceId": "WebAppASG",
                    "PropagateAtLaunch": True,
                    "Value": "WebAppASG",
                    "Key": "Name"
                },
                {
                    "ResourceType": "auto-scaling-group",
                    "ResourceId": "WebAppASG",
                    "Key": "rec2-modify-to-standard",
                    "Value": "Fri Jan 01 19:15:00 UTC 2016",
                    "PropagateAtLaunch": False
                }
            ],
            "EnabledMetrics": [],
            "LoadBalancerNames": [
                "PROD-ELB"
            ],
            "AutoScalingGroupName": "WebAppASG",
            "DefaultCooldown": 300,
            "MinSize": 1,
            "Instances": [
                {
                    "ProtectedFromScaleIn": False,
                    "AvailabilityZone": "us-west-2a",
                    "InstanceId": "i-d031f714",
                    "HealthStatus": "Healthy",
                    "LifecycleState": "InService",
                    "LaunchConfigurationName": "WebAppASGLaunchConfigC"
                }
            ],
            "MaxSize": 4,
            "VPCZoneIdentifier": "subnet-03b96f66",
            "TerminationPolicies": [
                "Default"
            ],
            "LaunchConfigurationName": "WebAppASGLaunchConfigC",
            "CreatedTime": "2015-06-03T23:34:14.159Z",
            "AvailabilityZones": [
                "us-west-2a"
            ],
            "HealthCheckType": "EC2",
            "NewInstancesProtectedFromScaleIn": False
        }
asg_details_at_capacity = {
            "AutoScalingGroupARN": "arn:aws:autoscaling:us-west-2:761425999210:autoScalingGroup:f604b0bf-e970-45a2-87c0-9cb336dcaeda:autoScalingGroupName/WebAppASG",
            "HealthCheckGracePeriod": 300,
            "SuspendedProcesses": [],
            "DesiredCapacity": 1,
            "Tags": [
                {
                    "ResourceType": "auto-scaling-group",
                    "ResourceId": "WebAppASG",
                    "PropagateAtLaunch": True,
                    "Value": "Production",
                    "Key": "Environment"
                },
                {
                    "ResourceType": "auto-scaling-group",
                    "ResourceId": "WebAppASG",
                    "PropagateAtLaunch": True,
                    "Value": "WebAppASG",
                    "Key": "Name"
                }
            ],
            "EnabledMetrics": [],
            "LoadBalancerNames": [
                "PROD-ELB"
            ],
            "AutoScalingGroupName": "WebAppASG",
            "DefaultCooldown": 300,
            "MinSize": 1,
            "Instances": [
                {
                    "ProtectedFromScaleIn": False,
                    "AvailabilityZone": "us-west-2a",
                    "InstanceId": "i-d031f714",
                    "HealthStatus": "Healthy",
                    "LifecycleState": "InService",
                    "LaunchConfigurationName": "WebAppASGLaunchConfigC"
                }
            ],
            "MaxSize": 1,
            "VPCZoneIdentifier": "subnet-03b96f66",
            "TerminationPolicies": [
                "Default"
            ],
            "LaunchConfigurationName": "WebAppASGLaunchConfigC",
            "CreatedTime": "2015-06-03T23:34:14.159Z",
            "AvailabilityZones": [
                "us-west-2a"
            ],
            "HealthCheckType": "EC2",
            "NewInstancesProtectedFromScaleIn": False
        }

# launch_configurations
launch_configs_credit = [
        {
            "UserData": "#!/bin/bash",
            "IamInstanceProfile": "LambdaWorker",
            "EbsOptimized": False,
            "LaunchConfigurationARN": "arn:aws:autoscaling:us-west-2:761425999210:launchConfiguration:d9521163-b772-4922-8c62-a814cc4aedf3:launchConfigurationName/WebAppASGLaunchConfigC",
            "InstanceMonitoring": {
                "Enabled": False
            },
            "ClassicLinkVPCSecurityGroups": [],
            "CreatedTime": "2015-10-14T17:16:37.491Z",
            "BlockDeviceMappings": [
                {
                    "DeviceName": "/dev/xvda",
                    "Ebs": {
                        "DeleteOnTermination": True,
                        "VolumeSize": 8,
                        "VolumeType": "gp2"
                    }
                }
            ],
            "KeyName": "DANNO1",
            "SecurityGroups": [
                "sg-5de76738",
                "sg-9ae262ff",
                "sg-afe262ca"
            ],
            "LaunchConfigurationName": "WebAppASGLaunchConfigC",
            "KernelId": "",
            "RamdiskId": "",
            "ImageId": "ami-8ce302bf",
            "InstanceType": "t2.medium",
            "AssociatePublicIpAddress": True
        }
    ]
launch_configs_standard = [
        {
            "UserData": "IyEvYmluL2Jhc2gNCg==",
            "IamInstanceProfile": "LambdaWorker",
            "EbsOptimized": False,
            "LaunchConfigurationARN": "arn:aws:autoscaling:us-west-2:761425999210:launchConfiguration:d9521163-b772-4922-8c62-a814cc4aedf3:launchConfigurationName/WebAppASGLaunchConfigC",
            "InstanceMonitoring": {
                "Enabled": False
            },
            "ClassicLinkVPCSecurityGroups": [],
            "CreatedTime": "2015-10-14T17:16:37.491Z",
            "BlockDeviceMappings": [
                {
                    "DeviceName": "/dev/xvda",
                    "Ebs": {
                        "DeleteOnTermination": True,
                        "VolumeSize": 8,
                        "VolumeType": "gp2"
                    }
                }
            ],
            "KeyName": "DANNO1",
            "SecurityGroups": [
                "sg-5de76738",
                "sg-9ae262ff",
                "sg-afe262ca"
            ],
            "LaunchConfigurationName": "WebAppASGLaunchConfigC",
            "KernelId": "",
            "RamdiskId": "",
            "ImageId": "ami-8ce302bf",
            "InstanceType": "c4.large",
            "AssociatePublicIpAddress": True
        }
    ]
launch_configs_missing = []

# alarm_status
no_alarm = {
    "MetricAlarms": [{
        "AlarmName": "ReC2LowCpu",
        "AlarmDescription": "ASG CPU Low alarm",
        "StateValue": "OK",
    }, {
        "AlarmName": "ReC2LowCredits",
        "AlarmDescription": "ASG CPU Credits Low Alarm",
        "StateValue": "OK",
    }, {
        "AlarmName": "ReC2DragCredits",
        "AlarmDescription": "CPU Credits Drag Alarm",
        "StateValue": "OK",
    }]
}
low_asg_cpu = {
    "MetricAlarms": [{
        "AlarmName": "ReC2LowCpu",
        "AlarmDescription": "ASG CPU Low alarm",
        "StateValue": "ALARM",
    }, {
        "AlarmName": "ReC2LowCredits",
        "AlarmDescription": "ASG CPU Credits Low Alarm",
        "StateValue": "OK",
    }, {
        "AlarmName": "ReC2DragCredits",
        "AlarmDescription": "CPU Credits Drag Alarm",
        "StateValue": "OK",
    }]
}
credit_low = {
    "MetricAlarms": [{
        "AlarmName": "ReC2LowCpu",
        "AlarmDescription": "ASG CPU Low alarm",
        "StateValue": "OK",
    }, {
        "AlarmName": "ReC2LowCredits",
        "AlarmDescription": "ASG CPU Credits Low Alarm",
        "StateValue": "ALARM",
    }, {
        "AlarmName": "ReC2DragCredits",
        "AlarmDescription": "CPU Credits Drag Alarm",
        "StateValue": "OK",
    }]
}
drag_alarm = {
    "MetricAlarms": [{
        "AlarmName": "ReC2LowCpu",
        "AlarmDescription": "ASG CPU Low alarm",
        "StateValue": "OK",
    }, {
        "AlarmName": "ReC2LowCredits",
        "AlarmDescription": "ASG CPU Credits Low Alarm",
        "StateValue": "OK",
    }, {
        "AlarmName": "ReC2DragCredits",
        "AlarmDescription": "CPU Credits Drag Alarm",
        "StateValue": "ALARM",
    }]
}


def get_vars(extra=None):
    suffix = extra if extra else ""
    return [yaml.load(file("./tests/test_vars{}.yaml".format(suffix))), yaml.load(file('./tests/test_alarms.yaml'))]


@freeze_time("2016-01-01 19:30:00", tz_offset=0)
def test_noop():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
                      asg_details, no_alarm, launch_configs_credit)
    assert(a.result['Action'] == 'NO_ACTION')
    assert(a.result['Message'] == 'Nothing to do')

@freeze_time("2016-01-01 19:30:00", tz_offset=0)
def test_invalid_index():
    test_yaml = get_vars("_invalid_index")
    a.testing_startup(test_yaml[0], test_yaml[1],
                      asg_details, no_alarm, launch_configs_credit)
    assert(a.result['Action'] == 'NO_ACTION')
    assert(a.result['Message'] == 'Current instance type not in allowed sizes! Current: t2.medium, Credit: t2.large, Standard: c4.large')

@freeze_time("2016-01-01 19:30:00", tz_offset=0)
def test_missing_config():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
                      asg_details, no_alarm, launch_configs_missing)
    assert(a.result['Action'] == 'NO_ACTION')
    assert(a.result['Message'] == 'Config not found!')

@freeze_time("2016-01-01 19:30:00", tz_offset=0)
def test_decrease():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
                      asg_details, low_asg_cpu, launch_configs_standard)
    assert(a.result['Action'] == 'MODIFY')
    assert(a.result['Message'] == 'to_credit')

@freeze_time("2016-01-01 19:30:00", tz_offset=0)
def test_standard_nominal_no_change():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
                      asg_details, no_alarm, launch_configs_standard)
    assert(a.result['Action'] == 'NO_ACTION')
    assert(a.result['Message'] == 'Nothing to do')

@freeze_time("2016-01-01 19:30:00", tz_offset=0)
def test_increase():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
                      asg_details, credit_low, launch_configs_credit)
    assert(a.result['Action'] == 'MODIFY')
    assert(a.result['Message'] == 'to_standard')

@freeze_time("2016-01-01 19:30:00", tz_offset=0)
def test_increase_drag():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
                      asg_details, drag_alarm, launch_configs_credit)
    assert(a.result['Action'] == 'MODIFY')
    assert(a.result['Message'] == 'to_standard')

@freeze_time("2016-01-01 19:30:00", tz_offset=0)
def test_increase_drag_skipped_drag_disabled():
    test_yaml = get_vars('_drag_disabled')
    a.testing_startup(test_yaml[0], test_yaml[1],
                      asg_details, drag_alarm, launch_configs_credit)
    assert(a.result['Action'] == 'NO_ACTION')
    assert(a.result['Message'] == 'Nothing to do')

@freeze_time("2016-01-01 19:30:00", tz_offset=0)
def test_system_disabled():
    test_yaml = get_vars('_system_disabled')
    a.testing_startup(test_yaml[0], test_yaml[1],
                      asg_details, drag_alarm, launch_configs_credit)
    assert(a.result['Action'] == 'NO_ACTION')
    assert(a.result['Message'] == 'Launch Config Modification disabled')

@freeze_time("2016-01-01 19:30:00", tz_offset=0)
def test_decrease_cooldown_invalid():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
                      asg_details_cooldown_invalid, low_asg_cpu, launch_configs_standard)
    assert(a.result['Action'] == 'NO_ACTION')
    assert(a.result['Message'] == 'Cooldown threshold invalidation')

@freeze_time("2016-01-01 19:30:00", tz_offset=0)
def test_decrease_cooldown_not_met():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
                      asg_details_cooldown_not_met, low_asg_cpu, launch_configs_standard)
    assert(a.result['Action'] == 'NO_ACTION')
    assert(a.result['Message'] == 'Cooldown threshold invalidation')

@freeze_time("2016-01-01 19:30:00", tz_offset=0)
def test_increase_with_asg_size_bump():
    test_yaml = get_vars()
    a.testing_startup(test_yaml[0], test_yaml[1],
                      asg_details_at_capacity, credit_low, launch_configs_credit)
    assert(a.result['Action'] == 'MODIFY')
    assert(a.result['Message'] == 'to_standard')
    assert(a.result['AWS'][-1] == 'AWS: EXECUTE disabled - apply launch config 3/WebAppASGLaunchConfigC-ReC2-Fri-Jan-01-19.30.00-UTC-2016')
