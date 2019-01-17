import boto3
def lambda_handler(context,event):
   
   #declare iam & sns clients
    client                  = boto3.client('iam')
    sns                     = boto3.client('sns')
    response                = client.list_users()
    userVirtualMfa          = client.list_virtual_mfa_devices()
    mfaNotEnabled           = []
    mfaEnabled              = []
    physicalString          = ''
  
           
    # loop through users to find MFA
    for user in response['Users']:
        userMfa  = client.list_mfa_devices(UserName=user['UserName'])
        
        if len(userMfa['MFADevices']) == 0:
            if user['UserName'] not in mfaEnabled:
                mfaNotEnabled.append(user['UserName']) 
    
    if len(mfaNotEnabled) > 0:
        physicalString = 'Physical & Virtual MFA is not enabled for the following users: \n\n' + '\n'.join(mfaNotEnabled)
    else:
        physicalString = 'All Users have Physical and Virtual MFA enabled'
    
    # output result to SNS topic
    response = sns.publish(
        TopicArn='arn:aws:sns:ap-southeast-1:857006248477:TestLambda',
        Message= physicalString,
        Subject='Report for IAM Users Not Having MFA Enabled',
    )
    
    return mfaNotEnabled
