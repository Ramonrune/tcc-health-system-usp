import os, boto3, uuid, hashlib, base64, hmac

cognito_client = boto3.client('cognito-idp', region_name='us-east-1', aws_access_key_id=os.environ['ACCESS_KEY_AWS'], aws_secret_access_key=os.environ['SECRET_KEY_AWS'])

class CognitoUtil():

    def __init__(self):
        self.user_pool_id = os.environ["COGNITO_USER_POOL_ID"]
        self.cli_id = os.environ["COGNITO_CLI_ID"]
        
    def get_secret_hash(self, username):
        msg = username + os.getenv('COGNITO_CLI_ID')
        dig = hmac.new(str(os.getenv('COGNITO_CLI_SECRET')).encode('utf-8'),
                    msg=str(msg).encode('utf-8'), 
                    digestmod=hashlib.sha256).digest()
        d2 = base64.b64encode(dig).decode()
        return d2

    def auth(self, username, password):

        response = cognito_client.initiate_auth(
            ClientId=self.cli_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
                "SECRET_HASH": self.get_secret_hash(username) 
            }
        )

        return response
      
    def user_exists(self, username):
        try:
            cognito_client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=username
            )
            return True
        except cognito_client.exceptions.UserNotFoundException:
            return False
        
    def admin_create_user(self, email, password):
        try:
            response = cognito_client.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=email,
                MessageAction='SUPPRESS',
                TemporaryPassword=password,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': email
                    },
                ]
            )

            return "Success", response
        except cognito_client.exceptions.UsernameExistsException:
            return "UsernameExistsException", False


    

    def forgot_password(self, email):
        response = cognito_client.forgot_password(
            ClientId=self.cli_id,
            Username=email,     
            SecretHash=self.get_secret_hash(email)   
            )
        
        return response
        
    def confirm_forgot_password(self, email, confirmation_code, new_password):
        response = None
        try:
            response = cognito_client.confirm_forgot_password(
                ClientId=self.cli_id,
                Username=email,
                ConfirmationCode=confirmation_code,
                Password=new_password,
                SecretHash=self.get_secret_hash(email) 
            )

            return "Success", response
        except Exception as ex:
            return type(ex).__name__, response

    def admin_reset_password(self, email, password):
        
        cognito_client.admin_set_user_password(
            UserPoolId=self.user_pool_id,
            Username=email,
            Password=password,
            Permanent=True
        )
    
    def admin_get_user(self, email):
        response = cognito_client.admin_get_user(
            UserPoolId=self.user_pool_id,
            Username=email,

    )
        return response

    def respond_to_auth_challenge(self, email, newPassword, session):
        cognito_client.respond_to_auth_challenge(
            ClientId=self.cli_id,
            Session = session,
            ChallengeName="NEW_PASSWORD_REQUIRED",
            ChallengeResponses={
                "NEW_PASSWORD":newPassword,
                "USERNAME":email
            }
        )

    def sign_up(self, email, password):
        try:
            response = cognito_client.sign_up(
                ClientId=self.cli_id,
                Username=email,
                Password=password,
                SecretHash=self.get_secret_hash(email)
            )

            return "Success", response
        except cognito_client.exceptions.UsernameExistsException:
            return "UsernameExistsException", False
        

    def confirm_sign_up(self, email, code):
        try:
            response = cognito_client.confirm_sign_up(
                    ClientId=self.cli_id,
                    Username=email,
                    ConfirmationCode=code,
                    SecretHash=self.get_secret_hash(email)
            )

            return "Success", response
        except cognito_client.exceptions.CodeMismatchException:
            return "CodeMismatchException", False
        except cognito_client.exceptions.ExpiredCodeException:
            return "ExpiredCodeException", False
        except Exception as ex:
            import traceback
            traceback.print_exc()
            return "Exception", False
        
    def resend_confirmation_code(self, email):
        response = None
        try:
            response = cognito_client.resend_confirmation_code(
                ClientId=self.cli_id,
                Username=email
            )

            return "Success", response
        except Exception as ex:
            return type(ex).__name__, response
        
    def change_password(self, previous_password, new_password, access_token):
        response = None
        try:
            response = cognito_client.change_password(
                PreviousPassword=previous_password,
                ProposedPassword=new_password,
                AccessToken=access_token
            )

            return "Success", response
        except Exception as ex:
            return type(ex).__name__, response
        
    def resend_invitation(self, email):
        response = cognito_client.admin_create_user(
            UserPoolId=self.user_pool_id,
            Username=email,
            MessageAction='RESEND',
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
            ]
        )
        return response
    

    def revoke_token(self, access_token):
        response = cognito_client.global_sign_out(
            AccessToken=access_token
        )
        return response