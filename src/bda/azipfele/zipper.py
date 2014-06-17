# -*- coding: utf-8 -*-
import logging
import urlparse
import uuid
import zipfile

from collective.zamqp.consumer import Consumer
from collective.zamqp.interfaces import IMessageArrivedEvent
from collective.zamqp.interfaces import IProducer
from collective.zamqp.producer import Producer
from plone import api
from plone.app.uuid.utils import uuidToObject
from plone.uuid.interfaces import IUUID
from Products.CMFPlone.utils import safe_unicode
from zope.component import adapter
from zope.component import getUtility
from zope.i18n import translate
from zope.i18nmessageid import Message
from zope.interface import Interface

from bda.azipfele import _
from email.Header import Header
from email.MIMEText import MIMEText
from email.Utils import formatdate
import os


logger = logging.getLogger('bda.azipfele zipper')

QUEUE_NAME = 'bda.azipfele.zip'
ZIPDIRKEY = "BDA_AZIPFELE_ZIPS"
ZIPNGINXKEY = "BDA_AZIPFELE_NGINX"

MAIL_SUBJECT = _('download_mail_subject', "Download is ready!")
MAIL_BODY = _('download_mail_body', u"""\
TODO: Write this text

Collected files are ready for download at:

${download_url}

You are receiving this e-mail because you or someone else collected media files
at Zumtobel Partner Portal.

If you have questions contact Willi or Maja.

TODO: This text needs to be written and translated!

best regards

Flip
--
Zumtobel AG
Dornbirn
""")


def make_zip_filename(target_site, userid, uid):
    return "zumtobel-{0}-{1}-{2}.zip".format(
        target_site,
        userid,
        uid
    )


class Zipit(object):
    # tmpdir is given because otherwise test wont run with my understanding :P
    def __init__(self, portal, email, portal_url, userid, uids, lang='en'):
        self.portal = portal
        self.email = email
        self.portal_url = portal_url
        self.userid = userid
        self.uids = uids
        self.lang = lang
        if ZIPDIRKEY not in os.environ:
            raise ValueError(
                'Expect environment variable "{0}: pointing to target '
                'directory for zip-files, shared with nginx in order to '
                'work with x-sendfile.'.format(ZIPDIRKEY)
            )
        self.dir = os.environ[ZIPDIRKEY]

        # get targetsite ie. lcp
        url = urlparse.urlparse(portal_url)
        subdomain = url.hostname.split('.')[0]
        self.target_site = subdomain[:3]
        self.uid = str(uuid.uuid4())

    def create(self):
        """creates a zipfile with data from the given uids
        """
        # generate nice zipname
        self.zf_name = make_zip_filename(
            self.target_site,
            self.userid,
            self.uid
        )
        logger.info('Creating ZIP File {0}'.format(self.zf_name))
        with zipfile.ZipFile(
                os.path.join(self.dir, self.zf_name),
                mode='w',
                compression=zipfile.ZIP_DEFLATED,
                allowZip64=True
        ) as zf:
            for uid in self.uids:
                mfile = uuidToObject(uid)
                filedata = mfile.file.data  # blobfile as string
                filename = os.path.basename(mfile.file.filename)
                zf.writestr(filename, filedata)

    def notify(self):
        logger.info('Notify User about created ZIP.')
        logger.info(self.target_site + ' ' + self.zf_name)
        url = "{0}/mediadb_zip/{1}".format(
            self.portal_url,
            self.uid
        )
        mailsubject = translate(MAIL_SUBJECT, target_language=self.lang)
        mailsubject = Header(mailsubject, 'utf-8')
        mailbody = Message(MAIL_BODY, mapping={'download_url': url})
        mailbody = translate(mailbody, target_language=self.lang)
        mailbody = mailbody.encode('utf8')
        mailhost = api.portal.get_tool('MailHost')
        mailfrom = api.portal.get().email_from_address
        mailfrom_name = api.portal.get().email_from_name
        if mailfrom_name:
            mailfrom = u"%s <%s>" % (safe_unicode(mailfrom_name), mailfrom)
        message = MIMEText(mailbody, _subtype='plain')
        message.set_charset('utf-8')
        message.add_header('Date', formatdate(localtime=True))
        message.add_header('From_', mailfrom)
        message.add_header('From', mailfrom)
        message.add_header('To', self.email)
        message['Subject'] = mailsubject
        mailhost.send(messageText=message, mto=self.email)


def queue_zip_job():
    producer = getUtility(IProducer, name=QUEUE_NAME)
    producer.register()
    # collect some data
    payload = dict(foo='bar')
    producer.publish(payload, correlation_id='SOMEUNIQUEID')


class IZipProcessingMessage(Interface):
    """ Marker interface for zip processing  message
    """


class ZipProcessingProducer(Producer):
    """ Produces ZIP processing tasks
    """
    connection_id = 'superuser'
    serializer = 'msgpack'
    queue = QUEUE_NAME
    routing_key = QUEUE_NAME

    durable = True
    auto_delete = True


class ZipProcessingConsumer(Consumer):
    """ Consumes Zip processing tasks
    """
    connection_id = 'superuser'
    marker = IZipProcessingMessage
    queue = QUEUE_NAME
    routing_key = QUEUE_NAME

    durable = True
    auto_delete = True


class Found(Exception):
    """for loop breakout helper
    """


@adapter(IZipProcessingMessage, IMessageArrivedEvent)
def process_message(message, event):
    """ Handle messages received through consumer.
    """
    cid = message.header_frame.correlation_id
    logger.info("process message {0}".format(cid))
    email = message.body.get('email')
    portal_url = message.body.get('portal_url')
    uids = message.body.get('uids')
    lang = message.body.get('lang')

    portal = api.portal.get()
    userid = api.user.get_current().getId()
    file_uids = []
    try:
        for uid in uids:
            mdb_folder = uuidToObject(uid)
            try:
                for prefix in ['tif', 'vid', 'jpg.p', 'jpg.w']:
                    for name in mdb_folder:
                        mdb_folder[name].media_type
                        if mdb_folder[name].media_type.startswith(prefix):
                            file_uids.append(IUUID(mdb_folder[name]))
                            raise Found()
            except Found:
                continue
        zipit = Zipit(portal, email, portal_url, userid, file_uids, lang)
        zipit.create()
        zipit.notify()

    except Exception as e:
        logger.error('{0:s}: {1:s}'.format(e.__class__, e))

    # Send ACK
    message.ack()
