import keyring

ServiceName="githubclitool"
AccountName="default"

def GetToken():
    return keyring.get_password(ServiceName, AccountName)

def SaveToken(Token):
    keyring.set_password(ServiceName, AccountName, Token)

def DeleteToken():
    keyring.delete_password(ServiceName, AccountName)