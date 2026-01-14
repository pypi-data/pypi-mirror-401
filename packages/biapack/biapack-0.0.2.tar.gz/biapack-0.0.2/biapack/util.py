from mcp.server.fastmcp import FastMCP
from .schema.header import Header

import boto3
import os

class Util():

    HEADER_PREFIX = "x-amzn-bedrock-agentcore-runtime-custom"

    def __init__(self, mcp: FastMCP):
        self.mcp = mcp

    def __get_from_ssm(self, parameter_name: str) -> str:
        """Busca o parâmetro no AWS SSM Parameter Store"""
        ctx = self.mcp.get_context()
        headers = ctx.request_context.request.headers
        prefix = headers.get(f"{self.HEADER_PREFIX}-prefix", None)
        client = boto3.client('ssm', region_name="sa-east-1")
        try:
            response = client.get_parameter(
                Name=f"{prefix}/{parameter_name}",
                WithDecryption=True
            )
        except client.exceptions.ParameterNotFound:
            return None
        return response.get('Parameter').get('Value')

    def get_header(self) -> Header:
        """Retorna os parâmetros padrão contidos no header da requisição"""
        ctx = self.mcp.get_context()
        headers = ctx.request_context.request.headers
        return Header(
            current_host=headers.get(f"{self.HEADER_PREFIX}-current-host", None),
            user_email=headers.get(f"{self.HEADER_PREFIX}-user-email", None),
            jwt_token=headers.get(f"{self.HEADER_PREFIX}-jwt-token", None),
            jsessionid=headers.get(f"{self.HEADER_PREFIX}-jsessionid", None),
            organization_id=int(headers.get(f"{self.HEADER_PREFIX}-organization-id", 0)),
            codparc=int(headers.get(f"{self.HEADER_PREFIX}-codparc", 0)),
            iam_user_id=int(headers.get(f"{self.HEADER_PREFIX}-iam-user-id", 0)),
            gateway_token=headers.get(f"{self.HEADER_PREFIX}-gateway-token", None)
        )
    
    def get_parameter(self, parameter_name: str) -> str:
        """
            Retorna o valor do parâmetro, buscando primeiro na variável de
            ambiente e depois no AWS SSM Parameter Store.
        """
        return os.getenv(
            parameter_name,
            self.__get_from_ssm(parameter_name)
        )