from django.db import models
from enum import Enum


class BaseChoiceEnum(Enum):
    """The base class for choices enumeration.

    This enumeration is often uses with Django fields.
    """

    @classmethod
    def values(cls) -> list[int]:
        """Get values of enum.

        Returns
        -------
            List[int]: List of values.

        """
        return [data.value for data in cls]

    @classmethod
    def choices(cls) -> list[tuple]:
        """Get choices of enum.

        Returns
        -------
            List[Tuple]: List of choice.

        """
        return [(data.value, data.name) for data in cls]


class JobCategory(models.TextChoices):
    FULL_TIME = "Full Time", "Full Time"
    PART_TIME = "Part Time", "Part Time"


class LeaveType(models.TextChoices):
    ANNUAL = "Annual", "Annual"
    SICK = "Sick", "Sick"
    CASUAL = "Casual", "Casual"
    MATERNITY = "Maternity", "Maternity"


class LeaveStatus(models.TextChoices):
    PENDING = "Pending", "Pending"
    APPROVED = "Approved", "Approved"
    REJECTED = "Rejected", "Rejected"


class EducationType(models.TextChoices):
    ACADEMIC = "Academic", "Academic Records"
    PROFESSIONAL = "Professional", "Professional Qualifications"


class DocumentType(models.TextChoices):
    OFFER_LETTER = 'offer_letter', 'Offer Letter'
    BIRTH_CERTIFICATE = 'birth_certificate', 'Birth Certificate'
    GUARANTOR_FORM = 'guarantor_form', 'Guarantor’s Form'
    DEGREE_CERTIFICATE = 'degree_certificate', 'Degree Certificate'

    @classmethod
    def has_value(cls, value):
        return value in cls.values


class RoleChoices(BaseChoiceEnum):
    """Enumeration for role choices of users."""

    ADMIN = "admin"
    EMPLOYEE = "employee"
    CANDIDATE = "candidate"
