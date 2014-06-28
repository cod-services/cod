#!/bin/sh

usage() {
    echo "Usage: $0 <from> [to]"
}

retrieve() {
    git --no-pager log --oneline --pretty=format:" - %h %s" --no-merges --grep="$1" $FROM..$TO
}

subheading() {
    echo "#### $1\n"
    retrieve "$2"
    echo
    echo
}

FROM=$1
TO=${2:-"HEAD"}

if [ -z $1 ];
then
    usage
    exit 1
fi

echo "### $FROM -> $TO\n"

subheading "Protocol Adjustments" "protocol\/"
subheading "Other Files" "etc\/"
subheading "Documentation" "doc\/"
subheading "Bot Commands" "bot\/"
subheading "Core Improvements" "src\/"
subheading "Core Modules" "core\/"
subheading "Scrapers" "scrapers\/"
subheading "Announcers" "announcer\/"
subheading "Services" "services\/"
