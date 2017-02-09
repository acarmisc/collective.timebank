import logging
from Products.Five.browser import BrowserView
from collective.timebank.helper import JobTimeItem, JobTimeBalanceItem, JobTimeBidItem, JobTimeTransactionItem
from collective.timebank import _
from plone import api

logger = logging.getLogger(__name__)


class NewRequestView(BrowserView):
    def render(self):
        return self.index()

    def __call__(self):
        self.display_form = True

        self.messages = list()
        request = self.request
        data = request.form

        if request.method == 'POST':
            logger.debug("Creating new time request")

            # TODO: better time value management (ie: hours + minutes)
            minutes_amount = data.get('amount')

            item = JobTimeItem(title=data.get('title'),
                               description=data.get('description'),
                               job_type='REQUEST',
                               details=data.get('details'),
                               minutes_amount=minutes_amount)

            try:
                job = item.register()
            except Exception, e:
                logger.error("Unable to create Time Job Request %s" % e)
                raise Exception

            self.messages.append(_(u"Request created"))
            self.display_form = False

        return self.render()


class NewBidView(BrowserView):
    def render(self):
        return self.index()

    def __call__(self):
        title = "Bid from %s" % api.user.get_current()
        item = JobTimeBidItem(title=title, job=self.context)

        bid = item.register()

        return self.render()


class JobTime(BrowserView):

    def is_mine(self):
        # FIXME: check ownership
        return True

    def get_bids(self):
        res = list()

        items = api.content.find(portal_type='JobTimeBid', path='/'.join(self.context.getPhysicalPath()))

        for i in items:
            res.append(i.getObject())

        return res


class JobTimeBank(BrowserView):

    def format_minutes(self, min):
        h = str(min / 60).zfill(2)
        m = str(min % 60).zfill(2)

        return "%s:%s" % (h, m)

    def get_requests(self):
        res = list()
        objs = api.content.find(portal_type='JobTime')

        for o in objs:
            res.append(o.getObject())

        return res

    def get_my_requests(self):
        res = list()
        objs = api.content.find(portal_type='JobTime', Creator=api.user.get_current())

        for o in objs:
            res.append(o.getObject())

        return res

    def get_balance(self):
        balance = api.content.find(portal_type='JobTimeBalance', Creator=api.user.get_current())

        if len(balance) > 1:
            logger.warning("Too many balance account. Getting the first")

        if not balance:
            balance = JobTimeBalanceItem(user=api.user.get_current())
            balance = balance.open()
            return balance

        return balance[0].getObject()


class NewTransactionView(BrowserView):
    def format_minutes(self, min):
        h = str(min / 60).zfill(2)
        m = str(min % 60).zfill(2)

        return "%s:%s" % (h, m)

    def render(self):
        return self.index()

    def __call__(self):

        self.display_confirm = True
        self.transaction_done = False

        self.messages = list()
        request = self.request

        if request.form.get('confirm'):
            transaction = JobTimeTransactionItem(bid=self.context)
            transaction = transaction.register()
            self.display_confirm = False
            self.messages.append(_(u"Transaction completed!"))
            self.transaction_done = True

        return self.render()
