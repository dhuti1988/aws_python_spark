# Use boto3 to provision AWS resources using cloudformation.yml file

import time

import boto3

IN_PROGRESS_STATUSES = (
    "CREATE_IN_PROGRESS",
    "UPDATE_IN_PROGRESS",
    "ROLLBACK_IN_PROGRESS",
    "DELETE_IN_PROGRESS",
    "UPDATE_ROLLBACK_IN_PROGRESS",
)


def poll_stack_status(cloudformation, stack_name, poll_interval=30):
    """Poll stack status until it reaches a terminal state."""
    while True:
        response = cloudformation.describe_stacks(StackName=stack_name)
        stack = response["Stacks"][0]
        status = stack["StackStatus"]
        print(f"Stack status: {status}")

        if status in IN_PROGRESS_STATUSES:
            time.sleep(poll_interval)
        else:
            return stack


def provision_aws_resources(stack_name):
    cloudformation = boto3.client("cloudformation")
    with open("aws/cloud_formation.yml", "r") as file:
        cloudformation_template = file.read()

    cloudformation.create_stack(
        StackName=stack_name,
        TemplateBody=cloudformation_template,
    )
    print(f"Stack {stack_name} creation initiated, polling for status...")

    stack = poll_stack_status(cloudformation, stack_name)
    if stack["StackStatus"] == "CREATE_COMPLETE":
        print(f"Stack {stack_name} provisioned successfully")
    else:
        print(f"Stack {stack_name} ended with status: {stack['StackStatus']}")
    return stack


if __name__ == "__main__":
    stack_name = "customer-analytics-stack"
    provision_aws_resources(stack_name)