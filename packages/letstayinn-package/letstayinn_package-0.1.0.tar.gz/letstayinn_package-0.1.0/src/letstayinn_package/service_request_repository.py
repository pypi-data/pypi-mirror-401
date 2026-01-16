import boto3
from typing import List, Dict, Any

from mypy_boto3_dynamodb import ServiceResource
from botocore.utils import ClientError


def getddbresource():
    return boto3.resource("dynamodb", region_name="ap-south-1")


class ServiceRequestRepository:
    def __init__(
        self,
        table_name: str,
        ddb_resource: ServiceResource | None = None,
    ) -> None:
        if ddb_resource is None:
            ddb_resource = getddbresource()

        self.table = ddb_resource.Table(table_name)
        self.table_name = table_name
        self.ddb_client = ddb_resource.meta.client

    def get_service_requests_by_booking(self, booking_id: str) -> List[Dict[str, Any]]:
        try:
            response = self.ddb_client.query(
                TableName=self.table_name,
                KeyConditionExpression="pk = :pk AND begins_with(sk, :sk)",
                ExpressionAttributeValues={
                    ":pk": f"Booking#{booking_id}",
                    ":sk": "Service#",
                },
            )
            return response.get("Items", [])
        except ClientError as e:
            raise e

    def delete_service_requests_by_booking(self, booking_id: str):
        service_requests = self.get_service_requests_by_booking(booking_id)

        if not service_requests:
            return

        transact_items = []

        for sr in service_requests:
            service_request_id = sr["service_request_id"]
            user_id = sr["user_id"]
            status_value = sr["status"]

            # 1️⃣ Global service request
            transact_items.append(
                {
                    "Delete": {
                        "TableName": self.table_name,
                        "Key": {
                            "pk": "ServiceRequests",
                            "sk": f"Service#{status_value}#{service_request_id}",
                        },
                    }
                }
            )

            # 2️⃣ User who created request
            transact_items.append(
                {
                    "Delete": {
                        "TableName": self.table_name,
                        "Key": {
                            "pk": f"User#{user_id}",
                            "sk": f"Made#{status_value}#{service_request_id}",
                        },
                    }
                }
            )

            # 3️⃣ Booking mapping
            transact_items.append(
                {
                    "Delete": {
                        "TableName": self.table_name,
                        "Key": {
                            "pk": f"Booking#{booking_id}",
                            "sk": f"Service#{service_request_id}",
                        },
                    }
                }
            )

            # 4️⃣ Assigned employee (ONLY if assigned)
            if sr.get("is_assigned") and sr.get("assigned_to"):
                transact_items.append(
                    {
                        "Delete": {
                            "TableName": self.table_name,
                            "Key": {
                                "pk": f"User#{sr['assigned_to']}",
                                "sk": f"Service#{status_value}#{service_request_id}",
                            },
                        }
                    }
                )

        # DynamoDB limit: 25 operations per transaction
        for i in range(0, len(transact_items), 25):
            try:
                self.ddb_client.transact_write_items(
                    TransactItems=transact_items[i: i + 25]
                )
            except ClientError as e:
                raise e
