#!/bin/bash
models=(
    sites.site
    blog.category
    blog.post
    blog.tag
    blog.snippet
    blog.sitedetail
    blog.aboutsite
    blog.privacypolicy
    blog.image
    blog.link
    blog
)

target_dir=$(dirname "$(cd "$(dirname "${BASH_SOURCE:-$0}")" && pwd)")

cd /django

for model in ${models[@]} ; do
    python manage.py dumpdata ${model} --indent 4 --output ${target_dir}/${model}.json
done