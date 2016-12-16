#!/usr/bin/env python

from troposphere import Template, iam, Ref, Output, GetAtt
from awacs.aws import Action, Allow, Policy, Principal, Statement

t = Template()

role = t.add_resource(iam.Role(
    "lambdarole",
    AssumeRolePolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow,
                Principal=Principal('Service', 'lambda.amazonaws.com'),
                Action=[Action('sts', 'AssumeRole')]
            ),
            Statement(
                Effect=Allow,
                Principal=Principal('Service', 'events.amazonaws.com'),
                Action=[Action('sts', 'AssumeRole')]
            )
        ]
    ),
    Path='/',
    Policies=[iam.Policy(
        'lambdapolicy',
        PolicyName='lambdapolicy',
        PolicyDocument=Policy(
            Statement=[
                Statement(
                    Effect=Allow,
                    Action=[
                        Action('autoscaling', 'CreateLaunchConfiguration'),
                        Action('autoscaling', 'DeleteLaunchConfiguration'),
                        Action('autoscaling', 'DescribeLaunchConfigurations'),
                        Action('autoscaling', 'DescribeAutoScalingGroups'),
                        Action('autoscaling', 'UpdateAutoScalingGroup'),
                        Action('autoscaling', 'CreateOrUpdateTags'),
                    ],
                    Resource=[
                        "*"
                    ]
                ),
                Statement(
                    Effect=Allow,
                    Action=[
                        Action('cloudwatch', 'DescribeAlarms'),
                    ],
                    Resource=[
                        "*"
                    ]
                ),
                Statement(
                    Effect=Allow,
                    Action=[
                        Action('iam', 'PassRole'),
                    ],
                    Resource=[
                        "*"
                    ]
                ),
                Statement(
                    Effect=Allow,
                    Action=[
                        Action('logs', 'CreateLogGroup'),
                        Action('logs', 'CreateLogStream'),
                        Action('logs', 'PutLogEvents'),
                    ],
                    Resource=["arn:aws:logs:*:*:*"]
                )
            ]
        )
    )]
))

t.add_output([
    Output(
        'LambdaRole',
        Description='ReC2 Lambda Role ID',
        Value=Ref(role),
    ),
    Output(
        'LambdaRoleArn',
        Description='ReC2 Lambda Role ARN',
        Value=GetAtt(role.title, 'Arn')
    )
])

if __name__ == '__main__':
    print t.to_json()
