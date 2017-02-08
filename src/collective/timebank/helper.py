from plone import api

import logging

logger = logging.getLogger(__name__)


class JobTimeItem:
    def __init__(self, title, description, job_type, details, minutes_amount):
        self.title = title
        self.description = description
        self.job_type = job_type
        self.details = details
        self.minutes_amount = minutes_amount

    def register(self):

        bank = api.content.find(portal_type='JobTimeBank')

        if not bank or len(bank) > 1:
            raise ValueError("No time bank present or too many banks")
        else:
            bank = bank[0]

        try:
            obj = api.content.create(
                    type='JobTime',
                    title=self.title,
                    description=self.description,
                    job_type=self.job_type,
                    details=self.details,
                    minutes_amount=int(self.minutes_amount),
                    container=bank.getObject())
        except Exception, e:
            raise Exception(e)

        api.content.transition(obj=obj, transition='submit')

        return obj


class JobTimeBalanceItem:
    def __init__(self, user):
        self.user = user

    def open(self):

        bank = api.content.find(portal_type='JobTimeBank')

        if not bank or len(bank) > 1:
            raise ValueError("No time bank present or too many banks")
        else:
            bank = bank[0]

        obj = api.content.create(
                type='JobTimeBalance',
                title='Balance for %s' % self.user.id,
                minutes_balance=60,
                container=bank.getObject()
        )

        api.content.transition(obj=obj, transition='submit')

        return obj


class JobTimeBidItem:
    def __init__(self, title, job):
        self.title = title
        self.container = api.content.get(path="/".join(job.getPhysicalPath()))

    def register(self):
        obj = api.content.create(
                type='JobTimeBid',
                title=self.title,
                container=self.container.getObject()
        )

        api.content.transition(obj=obj, transition='submit')

        return obj
