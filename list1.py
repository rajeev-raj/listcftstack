import boto3
import json

def lambda_handler(event, context):
    """Lists all CloudFormation stacks and their corresponding tags."""

    cfn = boto3.client('cloudformation')

    stacks = cfn.list_stacks()

    stacks_json = []
    for stack in stacks['StackSummaries']:
        stack_name = stack['StackName']
        stack_id = stack['StackId']

        # Get the stack ARN
        stack_arn = cfn.describe_stacks(StackName=stack_name)['Stacks'][0]['StackArn']

        # Get the stack tags
        stack_tags = cfn.describe_stacks(StackName=stack_name)['Stacks'][0]['Tags']

        # Create a JSON object for the stack
        stack_json = {
            'StackName': stack_name,
            'StackId': stack_id,
            'StackArn': stack_arn,
            'Tags': stack_tags
        }

        # Add the stack JSON object to the list
        stacks_json.append(stack_json)

    return {
        'statusCode': 200,
        'body': json.dumps(stacks_json)
    }
