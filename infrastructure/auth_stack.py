"""CDK Stack: Amazon Cognito Authentication for the Teaching Agent.

Creates a Cognito User Pool with:
- Email-only sign-in (no self-service signup — instructors create accounts)
- Custom attributes: cohort, enrollment_date
- Instructor and Student Cognito groups
- App client configured for authorization code flow with PKCE
- Cognito Hosted UI domain
"""

import aws_cdk as cdk
from aws_cdk import (
    CfnOutput,
    Stack,
    aws_cognito as cognito,
)
from constructs import Construct


class TeachingAgentAuthStack(Stack):
    """Cognito User Pool, App Client, Hosted UI, and user groups."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        frontend_origin: str = "https://d32yz1ssnunfr5.cloudfront.net",
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ── User Pool ─────────────────────────────────────────────────────────
        self.user_pool = cognito.UserPool(
            self,
            "TeachingAgentUserPool",
            user_pool_name="teaching-agent-user-pool",
            # Disable self-service signup — instructors create all accounts
            self_sign_up_enabled=False,
            # Sign-in via email only
            sign_in_aliases=cognito.SignInAliases(email=True, username=False),
            sign_in_case_sensitive=False,
            # Auto-verify email on admin-created accounts
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            # Required standard attributes
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True, mutable=True),
                given_name=cognito.StandardAttribute(required=True, mutable=True),
                family_name=cognito.StandardAttribute(required=True, mutable=True),
            ),
            # Custom attributes for course tracking
            custom_attributes={
                "cohort": cognito.StringAttribute(
                    min_len=1,
                    max_len=50,
                    mutable=True,
                ),
                "enrollment_date": cognito.StringAttribute(
                    min_len=10,
                    max_len=10,  # ISO date: YYYY-MM-DD
                    mutable=True,
                ),
            },
            # Password policy — strong defaults
            password_policy=cognito.PasswordPolicy(
                min_length=10,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=True,
                temp_password_validity=cdk.Duration.days(7),
            ),
            # Account recovery via email
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            # MFA optional for now (can be upgraded to REQUIRED per cohort)
            mfa=cognito.Mfa.OPTIONAL,
            mfa_second_factor=cognito.MfaSecondFactor(sms=False, otp=True),
            # Email configuration — use Cognito default for dev; SES for prod
            email=cognito.UserPoolEmail.with_cognito(),
            # Keep users across pool deletion in dev (set to RETAIN in prod)
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        # Apply project tags
        cdk.Tags.of(self.user_pool).add("project", "teaching-agent")
        cdk.Tags.of(self.user_pool).add("environment", "dev")

        # ── User Groups ───────────────────────────────────────────────────────
        cognito.CfnUserPoolGroup(
            self,
            "InstructorsGroup",
            user_pool_id=self.user_pool.user_pool_id,
            group_name="instructors",
            description="Instructors with full admin access to the Teaching Agent",
            precedence=1,  # Lower number = higher precedence
        )

        cognito.CfnUserPoolGroup(
            self,
            "StudentsGroup",
            user_pool_id=self.user_pool.user_pool_id,
            group_name="students",
            description="Enrolled students with read/chat access",
            precedence=10,
        )

        # ── App Client ────────────────────────────────────────────────────────
        # Auth code flow with PKCE — tokens never exposed in URL fragments
        self.app_client = self.user_pool.add_client(
            "TeachingAgentAppClient",
            user_pool_client_name="teaching-agent-web-client",
            # Disable client secret — public PKCE client
            generate_secret=False,
            # Authorization code flow only (PKCE enforced on frontend)
            auth_flows=cognito.AuthFlow(
                user_password=False,  # Disable direct password flow
                user_srp=False,       # Disable SRP; use hosted UI only
                admin_user_password=True,  # Allow admin SDK calls for seeding
            ),
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(
                    authorization_code_grant=True,
                    implicit_code_grant=False,
                ),
                scopes=[
                    cognito.OAuthScope.OPENID,
                    cognito.OAuthScope.EMAIL,
                    cognito.OAuthScope.PROFILE,
                ],
                # Callback URLs — localhost for dev plus the public frontend
                # origin (CloudFront by default, overridable via the
                # ``frontend_origin`` prop / ``-c frontend_domain`` context).
                callback_urls=[
                    "http://localhost:5173/auth/callback",
                    f"{frontend_origin}/auth/callback",
                ],
                logout_urls=[
                    "http://localhost:5173/",
                    f"{frontend_origin}/",
                ],
            ),
            # Token validity windows
            access_token_validity=cdk.Duration.hours(1),
            id_token_validity=cdk.Duration.hours(1),
            refresh_token_validity=cdk.Duration.days(30),
            # Enable token revocation (logout invalidates refresh tokens)
            enable_token_revocation=True,
            # Prevent user existence errors leaking in auth responses
            prevent_user_existence_errors=True,
        )

        # ── Hosted UI Domain ──────────────────────────────────────────────────
        # Prefix must be globally unique; append account ID suffix to avoid clashes
        self.domain = self.user_pool.add_domain(
            "TeachingAgentDomain",
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix="teaching-agent-auth",
            ),
        )

        # ── Outputs ───────────────────────────────────────────────────────────
        CfnOutput(
            self,
            "UserPoolId",
            value=self.user_pool.user_pool_id,
            description="Cognito User Pool ID",
            export_name="TeachingAgentUserPoolId",
        )

        CfnOutput(
            self,
            "UserPoolArn",
            value=self.user_pool.user_pool_arn,
            description="Cognito User Pool ARN",
            export_name="TeachingAgentUserPoolArn",
        )

        CfnOutput(
            self,
            "AppClientId",
            value=self.app_client.user_pool_client_id,
            description="Cognito App Client ID (public, no secret)",
            export_name="TeachingAgentAppClientId",
        )

        CfnOutput(
            self,
            "HostedUIDomain",
            value=self.domain.base_url(),
            description="Cognito Hosted UI base URL",
        )

        CfnOutput(
            self,
            "LoginUrl",
            value=self.domain.sign_in_url(
                self.app_client,
                redirect_uri="http://localhost:5173/auth/callback",
            ),
            description="Hosted UI sign-in URL (dev — localhost callback)",
        )
