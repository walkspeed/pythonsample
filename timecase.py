# -*- coding:utf-8 -*-

import time

lt = time.localtime(time.time())

print 'not format localtime : ',lt

print 'format localtime : ',time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
