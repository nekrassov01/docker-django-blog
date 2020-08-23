#!/bin/bash
TARGET_DIR=$(dirname "$(cd "$(dirname "${BASH_SOURCE:-$0}")" && pwd)")
cd /django
python manage.py dumpdata sites.site --indent 4 --output ${TARGET_DIR}/sites.site.json
python manage.py dumpdata blog.category --indent 4 --output ${TARGET_DIR}/blog.category.json
python manage.py dumpdata blog.tag --indent 4 --output ${TARGET_DIR}/blog.tag.json
python manage.py dumpdata blog.snippet --indent 4 --output ${TARGET_DIR}/blog.snippet.json
python manage.py dumpdata blog.sitedetail --indent 4 --output ${TARGET_DIR}/blog.sitedetail.json
python manage.py dumpdata blog.aboutsite --indent 4 --output ${TARGET_DIR}/blog.aboutsite.json
python manage.py dumpdata blog.privacypolicy --indent 4 --output ${TARGET_DIR}/blog.privacypolicy.json
python manage.py dumpdata blog --indent 4 --output ${TARGET_DIR}/blog.json