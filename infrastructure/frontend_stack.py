"""CDK Stack: S3 + CloudFront hosting for the Teaching Agent React SPA.

Serves the built Vite frontend from a private S3 bucket behind CloudFront on a
free ``<id>.cloudfront.net`` URL. A dedicated ``/api/*`` behavior proxies API
requests to the existing API Gateway origin, so the SPA and its API share the
same origin (no CORS, cookie SameSite works normally).

Layout:
- Default behavior  ``/*``      -> private S3 bucket (OAC), SPA index fallback.
- Cache behavior    ``/api/*``  -> API Gateway (HTTPS), no caching, forward all.
"""

import os

from aws_cdk import (
    Stack,
    CfnOutput,
    Duration,
    RemovalPolicy,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
)
from constructs import Construct


class TeachingAgentFrontendStack(Stack):
    """Private S3 bucket + CloudFront distribution for the React SPA."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        api_domain: str,
        api_stage: str = "prod",
        **kwargs,
    ) -> None:
        """
        Args:
            api_domain: API Gateway domain WITHOUT scheme or path, e.g.
                ``65nvz27oze.execute-api.eu-west-2.amazonaws.com``.
            api_stage: API Gateway stage name used as the origin path (``prod``),
                so ``/api/health`` -> ``https://<api_domain>/prod/api/health``.
        """
        super().__init__(scope, construct_id, **kwargs)

        # ── Private S3 bucket for the built SPA assets ────────────────────────
        self.site_bucket = s3.Bucket(
            self,
            "SiteBucket",
            bucket_name=f"teaching-agent-frontend-{self.account}",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            # Dev convenience: allow teardown. Flip to RETAIN for prod.
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # ── API Gateway origin (for /api/* passthrough) ───────────────────────
        api_origin = origins.HttpOrigin(
            api_domain,
            origin_path=f"/{api_stage}",
            protocol_policy=cloudfront.OriginProtocolPolicy.HTTPS_ONLY,
        )

        # Forward everything to the API and never cache it — the API is dynamic
        # and auth-cookie sensitive. AllViewerExceptHostHeader forwards headers,
        # cookies, and query strings but drops the Host header (API Gateway
        # rejects a CloudFront Host header).
        api_behavior = cloudfront.BehaviorOptions(
            origin=api_origin,
            viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
            cache_policy=cloudfront.CachePolicy.CACHING_DISABLED,
            origin_request_policy=cloudfront.OriginRequestPolicy.ALL_VIEWER_EXCEPT_HOST_HEADER,
        )

        # ── CloudFront distribution ───────────────────────────────────────────
        self.distribution = cloudfront.Distribution(
            self,
            "SiteDistribution",
            comment="Teaching Agent frontend (SPA + /api proxy)",
            default_root_object="index.html",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_control(
                    self.site_bucket
                ),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
            ),
            additional_behaviors={
                "/api/*": api_behavior,
            },
            # SPA client-side routing: serve index.html for unknown paths so
            # deep links like /admin and /auth/callback resolve in-app.
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.seconds(0),
                ),
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.seconds(0),
                ),
            ],
        )

        # ── Deploy built assets (if present) + invalidate ─────────────────────
        # The built SPA lives in frontend/dist after `npm run build`. Deploy it
        # only when it exists so `cdk synth` doesn't fail before the first build.
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dist_dir = os.path.join(project_root, "frontend", "dist")
        if os.path.isdir(dist_dir):
            s3deploy.BucketDeployment(
                self,
                "DeploySite",
                sources=[s3deploy.Source.asset(dist_dir)],
                destination_bucket=self.site_bucket,
                distribution=self.distribution,
                distribution_paths=["/*"],
                prune=True,
            )

        # ── Outputs ───────────────────────────────────────────────────────────
        self.distribution_domain = self.distribution.distribution_domain_name

        CfnOutput(
            self,
            "CloudFrontURL",
            value=f"https://{self.distribution_domain}",
            description="Public URL for the Teaching Agent frontend",
        )
        CfnOutput(
            self,
            "CloudFrontDomain",
            value=self.distribution_domain,
            description="CloudFront distribution domain (add to Cognito callback URLs)",
        )
        CfnOutput(
            self,
            "SiteBucketName",
            value=self.site_bucket.bucket_name,
            description="S3 bucket holding the built frontend assets",
        )
