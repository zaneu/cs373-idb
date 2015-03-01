# -*- coding: utf-8 -*-

# Scrapy settings for free_spirits project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'free_spirits'

SPIDER_MODULES = ['free_spirits.spiders']
NEWSPIDER_MODULE = 'free_spirits.spiders'

LOG_ENABLED = True
DEPTH_LIMIT = 1

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'free_spirits (+http://www.yourdomain.com)'
