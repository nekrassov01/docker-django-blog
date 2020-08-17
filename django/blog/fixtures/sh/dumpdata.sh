#!/bin/bash
TARGET_DIR=$(dirname "$(cd "$(dirname "${BASH_SOURCE:-$0}")" && pwd)")
cd /django
python manage.py dumpdata sites.site --indent 4 --output ${TARGET_DIR}/sites_site_.json
python manage.py dumpdata blog.category --indent 4 --output ${TARGET_DIR}/category.json
python manage.py dumpdata blog.tag --indent 4 --output ${TARGET_DIR}/tag.json
python manage.py dumpdata blog.snippet --indent 4 --output ${TARGET_DIR}/snippet.json
python manage.py dumpdata blog.sitedetail --indent 4 --output ${TARGET_DIR}/sitedetail.json
python manage.py dumpdata blog.aboutsite --indent 4 --output ${TARGET_DIR}/aboutsite.json
python manage.py dumpdata blog.privacypolicy --indent 4 --output ${TARGET_DIR}/privacypolicy.json
python manage.py dumpdata blog --indent 4 --output ${TARGET_DIR}/blog.json