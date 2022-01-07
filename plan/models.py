import uuid

from django.db import models

from user.models import TimeStamp, User


class Questionnaire(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questionnaires')
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    STATUS = (
        (1, 'Initializing questionnaire'),
        (2, 'Section one submitted'),
        (3, 'Section two submitted'),
        (4, 'Questionnaire submitted')
    )
    status = models.IntegerField(help_text='Questionnaire status', choices=STATUS, default=1)

    def __str__(self):
        return '%s %s' % (self.user.email, self.id)

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['uuid'])
        ]


class SectionOne(TimeStamp):
    questionnaire = models.OneToOneField(Questionnaire, on_delete=models.CASCADE, related_name='section_one')
    # Is your business model B2C or B2B or both?
    BUSINESS_TYPES = (
        (1, 'B2B'),
        (2, 'B2C'),
        (3, 'Both')
    )
    business_type = models.IntegerField(choices=BUSINESS_TYPES, null=False, blank=False,
                                        help_text='Is your business model B2C or B2B or both?')
    # Do you target all age brackets?
    BRACKETS = (
        (1, 'Yes'),
        (2, 'No')
    )
    bracket = models.IntegerField(choices=BRACKETS, null=False, blank=False,
                                  help_text='Do you target all age brackets?')
    # Do you target all industries?
    INDUSTRIES = (
        (1, 'Yes'),
        (2, 'No')
    )
    industry = models.IntegerField(choices=INDUSTRIES, null=False, blank=False,
                                   help_text='Do you target all industries?')


class SectionTwo(TimeStamp):
    questionnaire = models.OneToOneField(Questionnaire, on_delete=models.CASCADE, related_name='section_two')
    # Did you have an investment?
    INVESTMENT = (
        (1, 'Yes'),
        (2, 'No')
    )
    investment = models.IntegerField(choices=INVESTMENT, help_text='Did you have an investment?',
                                     null=False, blank=False)
    # how much was the investment?
    investment_size = models.PositiveIntegerField(help_text='how much was the investment?', null=False, blank=False)
