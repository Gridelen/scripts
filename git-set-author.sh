#!/bin/sh

# Credits: http://stackoverflow.com/a/750191

git filter-branch -f --env-filter "
    GIT_AUTHOR_NAME='mere-human'
    GIT_AUTHOR_EMAIL='9664141+mere-human@users.noreply.github.com'
    GIT_COMMITTER_NAME='mere-human'
    GIT_COMMITTER_EMAIL='9664141+mere-human@users.noreply.github.com'
  " HEAD