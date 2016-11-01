# ReC2 - ReActive EC2
Modify ASG parameters to use lower cost instances (until it's a problem, then change them!)

###Save up to 50% on EC2 costs and save yourself headache during traffic spikes

Features:
- Can be dropped into any project
- Handles low credit balance on T2 instances to upgrade to M/R instances automatically if they run out of credits
- Outputs logs to CloudWatch logs for review
- Creates multiple CloudFormation stacks to encapsulate the pieces
- Built to AWS best practices in terms of security and IAM roles etc.
- Uses CloudWatch alarms (that it creates) to determine when it needs to scale

Requirements:
- run **make prep** to install dependencies
- Manually configure repeating source after install via Lambda console - there is no automated way to do this yet, unfortunately - but only one time (see below for instructions!)

Tests
- run **make test**
- Check ./htmlcov/index.html for coverage report

Instructions:
- Modify vars.yaml to meet your needs.
- After loading a profile from AWS CLI that has admin access, run from root folder:
    **make prod** to install
- This will create all the stacks, buckets, lambda, cloudwatch, IAM roles, event sources etc needed for this project

This runs approxmiately 300,000 sec/month of lambda, well below the free tier for 128MB functions (3.2M) so it's free

Logs:
Sample log output:

```
START RequestId: 15e84aae-dc44-11e5-a5b6-b58f401b95b3 Version: $LATEST
INFO: Startup Time: 2016-02-26 04:51:01.301149
```
