from datetime import date
from typing import Any, Dict, List

# from boto3.resources.base import ServiceResource
from botocore.utils import ClientError
from mypy_boto3_dynamodb import ServiceResource
from letstayinn_package.models import bookings


class BookingRepository:
    def __init__(self, table_name: str, ddb_resource: ServiceResource) -> None:
        self.table = ddb_resource.Table(table_name)
        self.table_name = table_name
        self.ddb_client = ddb_resource.meta.client

    def scan_expired_bookings(self) -> List[Dict[str, Any]]:
        today = date.today().isoformat()

        response = self.ddb_client.scan(
            TableName=self.table_name,
            FilterExpression="#s = :booked AND check_out < :today",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={
                ":booked": bookings.BookingStatus.Booking_Status_Booked,
                ":today": today,
            },
        )
        return response.get("Items", [])

    def mark_booking_completed(self, booking_id: str, user_id: str):
        try:
            self.ddb_client.transact_write_items(
                TransactItems=[
                    {
                        "Update": {
                            "TableName": self.table_name,
                            "Key": {
                                "pk": f"Booking#{booking_id}",
                                "sk": "META",
                            },
                            "UpdateExpression": "SET #s = :completed",
                            "ConditionExpression": "#s = :booked",
                            "ExpressionAttributeNames": {
                                "#s": "status",
                            },
                            "ExpressionAttributeValues": {
                                ":completed": bookings.BookingStatus.Booking_Status_Completed.value,
                                ":booked": bookings.BookingStatus.Booking_Status_Booked.value,
                            },
                        }
                    },
                    {
                        "Update": {
                            "TableName": self.table_name,
                            "Key": {
                                "pk": f"User#{user_id}",
                                "sk": f"booking#{booking_id}",
                            },
                            "UpdateExpression": "SET #s = :completed",
                            "ExpressionAttributeNames": {
                                "#s": "status",
                            },
                            "ExpressionAttributeValues": {
                                ":completed": bookings.BookingStatus.Booking_Status_Completed.value,
                            },
                        }
                    },
                ]
            )
        except ClientError as e:
            raise e
