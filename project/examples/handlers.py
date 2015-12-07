import logging
from django.core.mail import EmailMessage
from members.handlers import BaseApplicationHandler, BaseMemberHandler
from creditor.handlers import BaseTransactionHandler
from creditor.models import Transaction
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger('example.handlers')


class ExampleBaseHandler(BaseMemberHandler):
    def on_saving(self, instance):
        msg = "on_saving called for %s %s" % (type(instance) , instance)
        logger.info(msg)
        print(msg)

    def on_saved(self, instance):
        msg = "on_saved called for %s %s" % (type(instance) , instance)
        logger.info(msg)
        print(msg)


class MemberHandler(ExampleBaseHandler):
    pass


class ApplicationHandler(ExampleBaseHandler):
    def on_approving(self, application, member):
        msg = "on_approving called for %s" % application
        logger.info(msg)
        print(msg)

    def on_approved(self, application, member):
        msg = "on_approved called for %s" % application
        logger.info(msg)
        print(msg)
        mail = EmailMessage()
        mail.to = [ member.email, ]
        mail.body = """Your membership has been approved, your member id is #%d""" % member.member_id
        mail.send()


class TransactionHandler(BaseTransactionHandler):
    def import_transaction(self, at):
        msg = "import_transaction called for %s" % at
        logger.info(msg)
        print(msg)
        # We only care about transactions with reference numbers
        if not at.reference:
            return None

        lt = at.get_local()
        if lt.pk:
            # TODO update ? though it should not change...
            return lt

        # TODO: figure out if we want to make a proper local transaction
        return at

    def __str__(self):
        return str(_("Example application transactions handler"))
