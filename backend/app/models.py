import enum

class UserRole(str, enum.Enum):
    DEVELOPER = "developer"
    ADMIN = "admin"


class SubmissionStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
