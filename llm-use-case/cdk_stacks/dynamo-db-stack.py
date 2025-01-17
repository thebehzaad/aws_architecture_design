from aws_cdk import (
    aws_dynamodb as dynamodb,
    Stack,
    core
)
from constructs import Construct
import random


class DynamoDbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB Table
        self.dynamo_db_table = dynamodb.Table(self, "DynamoDBTable",
            table_name="auth-policy-store",
            partition_key=dynamodb.Attribute(name="group", type=dynamodb.AttributeType.STRING),
            provisioned_throughput=dynamodb.ProvisionedThroughput(read_capacity_units=5, write_capacity_units=5)
        )



random.seed(47)


class DynamoDBStack(Stack):

  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    DDB_TABLE_SUFFIX = ''.join(random.sample((string.ascii_lowercase + string.digits), k=7))
    DDB_TABLE_NAME = "Comments-{}".format(DDB_TABLE_SUFFIX)

    ddb_table = aws_dynamodb.Table(self, "DynamoDbTable",
      table_name=DDB_TABLE_NAME,
      removal_policy=cdk.RemovalPolicy.DESTROY,
      partition_key=aws_dynamodb.Attribute(name="commentId",
        type=aws_dynamodb.AttributeType.STRING),
      time_to_live_attribute="ttl",
      billing_mode=aws_dynamodb.BillingMode.PROVISIONED,
      read_capacity=15,
      write_capacity=5,
    )

    ddb_table.add_global_secondary_index(
      read_capacity=15,
      write_capacity=5,
      index_name="pageId-index",
      partition_key=aws_dynamodb.Attribute(name='pageId', type=aws_dynamodb.AttributeType.STRING),
      projection_type=aws_dynamodb.ProjectionType.ALL
    )

    self.dynamodb_table = ddb_table


    cdk.CfnOutput(self, 'DynamoDBTableName', value=ddb_table.table_name,
      export_name=f'{self.stack_name}-TableName')