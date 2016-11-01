from __future__ import print_function
import yaml
import boto3
import datetime
import pytz
import base64
import base64_util
from dateutil import parser


class Rec2(object):

    def __init__(self):
        self.autoscaling_client = None
        self.cloudwatch_client = None
        self.now = None
        self.vars = None
        self.alarms = None
        self.details = None
        self.config = None
        self.alarm_status = None
        self.execute = None
        self.result = None
        self.utc_launch_time = None
        self.launch_configurations = None
        self.pending_launch_configuration = None
        self.asg_details = None
        self.reason = None
        self.new_class = None

    def lambda_startup(self):
        self.set_vars(
            yaml.load(open('vars.yaml')), yaml.load(open('alarms.yaml')))

        self.autoscaling_client = boto3.client(
            'autoscaling', region_name=self.vars['region'])
        self.cloudwatch_client = boto3.client(
            'cloudwatch', region_name=self.vars['region'])

        self.now = datetime.datetime.utcnow()

        self.process(

            self.autoscaling_client.describe_auto_scaling_groups(
                AutoScalingGroupNames=[self.vars['asg_identifier']]
            )['AutoScalingGroups'][0],

            self.cloudwatch_client.describe_alarms(
                AlarmNames=[
                    self.alarms['alarm_low_cpu'],
                    self.alarms['alarm_credits'],
                    self.alarms['alarm_drag'],
                ]),

            self.autoscaling_client.describe_launch_configurations(
            )['LaunchConfigurations']
        )

    def testing_startup(self, _vars, _alarms, _asg_details, _alarm_status, _launch_configurations):
        self.now = datetime.datetime.utcnow()
        self.set_vars(_vars, _alarms)
        self.process(
            _asg_details, _alarm_status, _launch_configurations, False)
        self.lambda_apply_action()
        self.print_logs()

    def set_vars(self, _vars, _alarms):
        self.vars = _vars
        self.alarms = _alarms

    def abort(self, msg):
        self.result['Action'] = 'NO_ACTION'
        self.result['Message'] = msg
        self.result['Logs'].append(
            "{}: {}".format(self.result['Action'], self.result['Message']))
        return self.result

    def awsinfo(self, msg):
        self.result['AWS'].append("{}: {}".format("AWS", msg))
        self.info(msg)

    def info(self, msg):
        self.result['Logs'].append("{}: {}".format("INFO", msg))

    def success(self):
        self.result['Action'] = 'MODIFY'
        self.result['Message'] = self.reason
        self.result['Logs'].append(
            "{}: {}".format(self.result['Action'], self.result['Message']))
        return self.result

    def process(self, _asg_details, _alarm_status, _launch_configurations, _execute=True):
        self.utc_launch_time = datetime.datetime.utcnow().strftime(
            "%a %b %d %H:%M:%S UTC %Y")
        self.config = False
        self.alarm_status = {
            "ReC2LowCpu": None,
            "ReC2LowCredits": None,
            "ReC2DragCredits": None,
        }
        self.result = {
            "Action": None,
            "Message": None,
            "Logs": [],
            "AWS": []
        }

        for status in _alarm_status['MetricAlarms']:
            if 'ReC2LowCpu' in status['AlarmName']:
                self.alarm_status['ReC2LowCpu'] = status['StateValue']
            elif 'ReC2LowCredits' in status['AlarmName']:
                self.alarm_status['ReC2LowCredits'] = status['StateValue']
            elif 'ReC2DragCredits' in status['AlarmName']:
                self.alarm_status['ReC2DragCredits'] = status['StateValue']

        self.asg_details = _asg_details
        self.launch_configurations = _launch_configurations
        self.execute = _execute

        self.info("Startup Time: {}".format(self.now.utcnow()))
        self.info("Configured instance sizes: Credit: {}, Standard: {}".format(
            self.vars['credit_instance_size'], self.vars['standard_instance_size']))

        self.info("Querying ASG: {}".format(self.vars['asg_identifier']))

        for config in self.launch_configurations:
            if config['LaunchConfigurationName'] == self.asg_details['LaunchConfigurationName']:
                self.info("Found active Launch Config: {}".format(
                    self.asg_details['LaunchConfigurationName']))
                self.info(
                    "Config Instance Type: {}".format(config['InstanceType']))
                self.config = config
                break

        if not self.config:
            return self.abort('Config not found!')

        if self.config['InstanceType'] not in [self.vars['credit_instance_size'], self.vars['standard_instance_size']]:
            return self.abort("Current instance type not in allowed sizes! Current: {}, Credit: {}, Standard: {}".format(self.config['InstanceType'], self.vars['credit_instance_size'], self.vars['standard_instance_size']))

        try:
            if base64_util.is_base64(arg=self.config['UserData']):
                self.info("base64 Userdata detected.. attempting to decode")
                self.config['UserData'] = base64.b64decode(self.config['UserData'])
        except:
            self.info("unable to decode userdata")

        if self.config['InstanceType'] == self.vars['credit_instance_size']:
            self.info("Checking if need to INCREASE")
            return self.check_increase()
        else:
            self.info("Checking if need to DECREASE")
            return self.check_decrease()

    def check_increase(self):
        self.info("Checking low credit alarm status {}/{}".format(
            self.alarms['alarm_credits'], self.alarm_status['ReC2LowCredits']))
        if self.alarm_status['ReC2LowCredits'] == 'ALARM':
            self.info("Low Credit Alarm in ALARM!")
            return self.scale('to_standard')

        if self.vars['drag_enabled']:
            self.info("Checking drag alarm status {}/{}".format(
                self.alarms['alarm_drag'], self.alarm_status['ReC2DragCredits']))
            if self.alarm_status['ReC2DragCredits'] == 'ALARM':
                self.info("Credit Drag Alarm in ALARM!")
                return self.scale('to_standard')
        else:
            self.info("Skipping drag alarm check: disabled")
        return self.abort("Nothing to do")

    def check_decrease(self):
        self.info("Checking low cpu alarm status {}/{}".format(
            self.alarms['alarm_low_cpu'], self.alarm_status['ReC2LowCpu']))
        if self.alarm_status['ReC2LowCpu'] == 'ALARM':
            self.info("Low CPU Alarm in ALARM!")
            return self.scale('to_credit')
        return self.abort("Nothing to do")

    def assert_cooldown_expired(self):
        last_rec2_change = False
        if self.reason == 'to_standard':
            return True
        self.info("Checking for last to_standard modification event")
        for tag in self.asg_details['Tags']:
            if tag['Key'] == 'rec2-modify-to-standard':
                try:
                    last_rec2_change = parser.parse(tag['Value'])
                    break
                except:
                    self.info(
                        "Unable to parse value from tag! {}".format(tag['Value']))
                    return False
        if last_rec2_change:
            delta_time = self.now.replace(tzinfo=pytz.utc) - last_rec2_change
            delta_time_calculated = divmod(
                delta_time.days * 86400 + delta_time.seconds, 60)
            self.info("Last finished modification {} Diff: (Min, Sec): {}".format(
                last_rec2_change, delta_time_calculated))
            if delta_time_calculated[0] < self.vars['cooldown']:
                self.info("Not enough time has passed since last modification ({})".format(
                    self.vars['cooldown']))
                return False
        return True

    def scale(self, reason):
        self.reason = reason
        if not self.vars['enabled']:
            return self.abort("Launch Config Modification disabled")
        if not self.assert_cooldown_expired():
            return self.abort("Cooldown threshold invalidation")
        self.new_class = self.vars[str(self.reason[3:]+"_instance_size")]
        self.info("Modifying Launch Config to {}".format(self.new_class))
        self.info("Executing scale command")
        return self.success()

    def create_launch_configuration(self):
        # auto_cleanup=True is default option, if var not present will cleanup
        # set to False to disable
        if 'auto_cleanup' not in self.vars or self.vars['auto_cleanup']:
            self.cleanup()
        worked = False
        to_copy = self.config.copy()
        del to_copy['CreatedTime']
        del to_copy['LaunchConfigurationARN']
        to_copy['InstanceType'] = self.new_class
        if "-ReC2-" in to_copy['LaunchConfigurationName']:
            to_copy['LaunchConfigurationName'] = to_copy['LaunchConfigurationName'][
                0:to_copy['LaunchConfigurationName'].index("-ReC2-")]
        self.pending_launch_configuration = to_copy[
            'LaunchConfigurationName']+"-ReC2-"+self.utc_launch_time.replace(" ", "-").replace(":", ".")
        to_copy['LaunchConfigurationName'] = self.pending_launch_configuration
        for i in ['KeyName', 'KernelId', 'RamdiskId']:
            if to_copy[i] == '':
                del to_copy[i]
        if not self.execute:
            self.awsinfo("EXECUTE disabled - create_launch_config {}/{}".format(
                self.pending_launch_configuration, self.new_class))
            return True
        try:
            self.autoscaling_client.create_launch_configuration(**to_copy)
            worked = True
        except Exception, e:
            self.info("AMZ response {}".format(e))
            self.info("Launch Config creation failed!")
        return worked

    def add_action_tag(self):
        worked = False
        if not self.execute:
            self.awsinfo(
                "EXECUTE disabled - add_action_tag {}".format(self.utc_launch_time))
            return True
        try:
            self.autoscaling_client.create_or_update_tags(
                Tags=[{
                    "ResourceId": self.vars['asg_identifier'],
                    "ResourceType": "auto-scaling-group",
                    "Key": "rec2-modify-to-standard",
                    "Value": self.utc_launch_time,
                    "PropagateAtLaunch": False
                }])
            worked = True
        except Exception, e:
            self.info("AMZ response {}".format(e))
            self.info("Unable to add action tag")
        return worked

    def cleanup(self):
        current_name = self.config['LaunchConfigurationName']
        if '-ReC2-' in current_name:
            for lconfig in self.launch_configurations:
                if '-ReC2-' in lconfig['LaunchConfigurationName'] and lconfig['LaunchConfigurationName'] != self.config['LaunchConfigurationName']:
                    self.info("Cleaning UP old ReC2 launch config! {}".format(lconfig['LaunchConfigurationName']))
                    try:
                        self.autoscaling_client.delete_launch_configuration(LaunchConfigurationName=lconfig['LaunchConfigurationName'])
                    except Exception, e:
                        self.info("AMZ response {}".format(e))
                        self.info("Unable to delete launch config {}".format(lconfig['LaunchConfigurationName']))

    def apply_launch_config(self):
        desired_capacity = self.asg_details[
            'DesiredCapacity'] + 2
        asg_dict = {
            'AutoScalingGroupName': self.vars['asg_identifier'],
            'LaunchConfigurationName': self.pending_launch_configuration,
            'DesiredCapacity': desired_capacity
        }
        if desired_capacity > self.asg_details['MaxSize']:
            asg_dict['MaxSize'] = desired_capacity
        if not self.execute:
            self.awsinfo("EXECUTE disabled - apply launch config {}/{}".format(
                desired_capacity, self.pending_launch_configuration))
            return True
        try:
            self.autoscaling_client.update_auto_scaling_group(**asg_dict)
        except Exception, e:
            self.info("AMZ response {}".format(e))
            self.info("Unable to apply launch config")

    def lambda_apply_action(self):
        if self.result['Action'] == 'MODIFY':
            if self.reason == 'to_standard':
                if not self.add_action_tag():
                    return self.abort("Action tag write error!")
            if self.create_launch_configuration():
                return self.apply_launch_config()
            return self.abort("System Error!")

    def print_logs(self):
        for log in self.result['Logs']:
            print(log)


def lambda_handler(context, event):
    rec2lambda = Rec2()
    rec2lambda.lambda_startup()
    rec2lambda.lambda_apply_action()
    rec2lambda.print_logs()
