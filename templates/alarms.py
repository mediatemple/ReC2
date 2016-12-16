#!/usr/bin/env python

from troposphere import Template, Parameter, Ref, Output
from troposphere.cloudwatch import Alarm, MetricDimension

t = Template()

asg_identifier = t.add_parameter(Parameter(
    'AsgIdentifier',
    Type='String',
    Description='Autoscaling Group to monitor'
))

down_threshold = t.add_parameter(
    Parameter(
        'DownThreshold',
        Type='String'
    )
)

down_evaluations = t.add_parameter(
    Parameter(
        'DownEvaluations',
        Type='String'
    )
)

credit_threshold = t.add_parameter(
    Parameter(
        'CreditThreshold',
        Type='String'
    )
)

credit_evaluations = t.add_parameter(
    Parameter(
        'CreditEvaluations',
        Type='String'
    )
)

drag_threshold = t.add_parameter(
    Parameter(
        'DragThreshold',
        Type='String'
    )
)

drag_evaluations = t.add_parameter(
    Parameter(
        'DragEvaluations',
        Type='String'
    )
)

low_cpu_alarm = t.add_resource(
    Alarm(
        "ReC2LowCpu",
        AlarmDescription="CPU Low Alarm",
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Statistic="Average",
        Period=300,
        Dimensions=[
            MetricDimension(
                Name="AutoScalingGroupName",
                Value=Ref(asg_identifier)
            )
        ],
        EvaluationPeriods=Ref(down_evaluations),
        Threshold=Ref(down_threshold),
        ComparisonOperator="LessThanOrEqualToThreshold",
        AlarmActions=[],
        InsufficientDataActions=[],
        OKActions=[],
    )
)

low_credit_alarm = t.add_resource(
    Alarm(
        "ReC2LowCredits",
        AlarmDescription="CPU Credits Exhausted Average Alarm",
        Namespace="AWS/EC2",
        MetricName="CPUCreditBalance",
        Statistic="Average",
        Period=300,
        Dimensions=[
            MetricDimension(
                Name="AutoScalingGroupName",
                Value=Ref(asg_identifier)
            )
        ],
        EvaluationPeriods=Ref(credit_evaluations),
        Threshold=Ref(credit_threshold),
        ComparisonOperator="LessThanOrEqualToThreshold",
        AlarmActions=[],
        InsufficientDataActions=[],
        OKActions=[],
    )
)

drag_credit_alarm = t.add_resource(
    Alarm(
        "ReC2DragCredits",
        AlarmDescription="CPU Credits Exhausted (at least one)",
        Namespace="AWS/EC2",
        MetricName="CPUCreditBalance",
        Statistic="Minimum",
        Period=300,
        Dimensions=[
            MetricDimension(
                Name="AutoScalingGroupName",
                Value=Ref(asg_identifier)
            )
        ],
        EvaluationPeriods=Ref(drag_evaluations),
        Threshold=Ref(drag_threshold),
        ComparisonOperator="LessThanOrEqualToThreshold",
        AlarmActions=[],
        InsufficientDataActions=[],
        OKActions=[],
    )
)

t.add_output([
    Output(
        'DragAlarm',
        Description='Alarm name for instance dragging',
        Value=Ref(drag_credit_alarm)
    ),
    Output(
        'CpuLowAlarm',
        Description='Alarm name for down/low',
        Value=Ref(low_cpu_alarm)
    ),
    Output(
        'CreditLowAlarm',
        Description='Alarm name for credits out',
        Value=Ref(low_credit_alarm)
    )
])

if __name__ == '__main__':
    print t.to_json()
