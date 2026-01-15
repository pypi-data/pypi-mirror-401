from amsdal.contrib.crm.models.activity import ActivityRelatedTo as ActivityRelatedTo, ActivityType as ActivityType, EmailActivity as EmailActivity
from amsdal_data.transactions.decorators import async_transaction, transaction

class EmailService:
    """Service for email integration and logging."""
    @classmethod
    @transaction
    def log_email(cls, subject: str, body: str, from_address: str, to_addresses: list[str], cc_addresses: list[str] | None, related_to_type: ActivityRelatedTo, related_to_id: str, owner_email: str, *, is_outbound: bool = True) -> EmailActivity:
        """Log an email as an activity.

        This can be called when:
        - User sends email from CRM
        - Incoming email is parsed and associated with CRM record

        Args:
            subject: Email subject
            body: Email body
            from_address: Sender email address
            to_addresses: List of recipient email addresses
            cc_addresses: List of CC email addresses
            related_to_type: Type of related record (Contact, Account, Deal)
            related_to_id: ID of related record
            owner_email: Email of user who owns this activity
            is_outbound: True if sent from CRM, False if received

        Returns:
            The created EmailActivity
        """
    @classmethod
    @async_transaction
    async def alog_email(cls, subject: str, body: str, from_address: str, to_addresses: list[str], cc_addresses: list[str] | None, related_to_type: ActivityRelatedTo, related_to_id: str, owner_email: str, *, is_outbound: bool = True) -> EmailActivity:
        """Async version of log_email.

        Args:
            subject: Email subject
            body: Email body
            from_address: Sender email address
            to_addresses: List of recipient email addresses
            cc_addresses: List of CC email addresses
            related_to_type: Type of related record (Contact, Account, Deal)
            related_to_id: ID of related record
            owner_email: Email of user who owns this activity
            is_outbound: True if sent from CRM, False if received

        Returns:
            The created EmailActivity
        """
