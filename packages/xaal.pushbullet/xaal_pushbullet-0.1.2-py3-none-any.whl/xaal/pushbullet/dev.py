from xaal.lib import tools,Device
import platform
import time
import atexit
import logging

from pushbullet import Pushbullet

PACKAGE_NAME = "xaal.pushbullet"
logger = logging.getLogger(PACKAGE_NAME)


push_bullets = []
def register_device(engine):
    global push_bullet
    cfg = tools.load_cfg(PACKAGE_NAME)
    if not cfg:
        logger.info('Missing config file, building a new one')
        cfg = tools.new_cfg(PACKAGE_NAME)
        cfg['config']['keys']=''
        cfg.write()

    keys = cfg['config'].get('keys',None)
    if not keys or type(keys)!=list:
        logger.info('Please setup the Pushbullet keys')
        return
    for k in keys:
        push_bullets.append(Pushbullet(k))
    info = "%s@%s" % (PACKAGE_NAME,platform.node())
    dev = Device("notification.pushbullet")
    dev.address     = tools.get_uuid(cfg['config']['addr'])
    dev.product_id = "Pushbullet Notification device"
    dev.vendor_id  = "IHSEV TEAM"
    dev.version    = 0.1
    dev.info       = info
    dev.add_method('notify',notify)
    engine.add_device(dev)
    notify(info,'started')
    atexit.register(notify,info,'shutdown..')
                
def notify(_title,_msg):
    global push_bullets
    if push_bullets != []:
        for pb in push_bullets:
            try:
                pb.push_note(_title,_msg)
            except Exception as err:
                print("Pushbullet exception: {0}".format(err))
                # some error can occur on a broken link, just try to resend
                time.sleep(0.5)
                pb.push_note(_title,_msg)


def setup(engine):
    register_device(engine)
    return True

