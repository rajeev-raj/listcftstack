import json
import boto3

def lambda_handler(event, context):
    # Initialize the CloudFormation client
    cloudformation = boto3.client('cloudformation')

    # List all CloudFormation stacks
    stack_response = cloudformation.list_stacks(StackStatusFilter=[])

    stack_info = []

    for stack in stack_response['StackSummaries']:
        # Get the ARN of the stack
        stack_arn = stack['StackId']

        # Get tags associated with the stack
        tags_response = cloudformation.list_stack_resources(StackName=stack['StackName'])

        # Find the tags associated with the stack by looking at the 'Tags' key in the response
        stack_tags = None
        for resource in tags_response.get('StackResourceSummaries', []):
            if resource['LogicalResourceId'] == stack['StackName']:
                stack_tags = resource.get('Tags', [])

        # Append stack information to the list, including Stack ID
        stack_info.append({
            'StackName': stack['StackName'],
            'StackId': stack['StackId'],  # Include Stack ID
            'StackArn': stack_arn,
            'Tags': stack_tags
        })

    # Convert the result to JSON
    result_json = json.dumps(stack_info, indent=2)

    return {
        'statusCode': 200,
        'body': result_json
    }
