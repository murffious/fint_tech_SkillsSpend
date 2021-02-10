from aws_cdk.core import Stack, StackProps, Construct, SecretValue
from aws_cdk.pipelines import CdkPipeline, SimpleSynthAction

import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_codepipeline_actions as codepipeline_actions
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
AWS_ACCT = os.getenv("AWS_ACCT")


class MyPipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        pipeline = CdkPipeline(
            self,
            "Pipeline",
            pipeline_name="MyAppPipeline",
            cloud_assembly_artifact=cloud_assembly_artifact,
            source_action=codepipeline_actions.GitHubSourceAction(
                action_name="GitHub",
                output=source_artifact,
                oauth_token=GITHUB_TOKEN,
                trigger=codepipeline_actions.GitHubTrigger.POLL,
                # Replace these with your actual GitHub project info
                owner="murffious",
                repo="fin_tech_SkillsSpend",
            ),
            synth_action=SimpleSynthAction.standard_npm_synth(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                # Use this if you need a build step (if you're not using ts-node
                # or if you have TypeScript Lambdas that need to be compiled).
                build_command="npm run build",
            ),
        )