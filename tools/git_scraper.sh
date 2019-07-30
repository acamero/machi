#!/usr/bin/bash

# Execture this script in a git project context to obtain files changed related to issues.
git log --no-merges --grep="[Cc]lose[ds]* #" --grep="[Ff]ix[ds]* #" --grep="[Ss]olve[ds]* #" --until="2018-12-31" --patch --stat > commits.txt
grep "[Cc]lose[ds]* #" commits.txt > issues-ref.txt
grep "[Ff]ix[ds]* #" commits.txt >> issues-ref.txt
grep "[Ss]olve[ds]* #" commits.txt >> issues-ref.txt
grep -o "#[0-9][0-9]*" issues-ref.txt > issues-id.txt
sed -i s/#//g issues-id.txt
cat issues-id.txt | while read LINE; do
    hub issue show $LINE >> issue-$LINE.txt
done
rm issues-ref.txt
rm issues-id.txt
git log --pretty=oneline --until="2018-12-31" > all-commits.txt
grep -o "^[0-9A-Za-z]* " all-commits.txt > all-commits-hash.txt
sed -n -e 's/^commit //p' commits.txt > commits-hash.txt
cat commits-hash.txt | while read LINE; do
    grep --after-context=1 $LINE all-commits-hash.txt | sed -z 's/\n//g' >> commits-hash-previous.txt
    echo  >> commits-hash-previous.txt
done
rm commits-hash.txt
rm all-commits-hash.txt
mkdir src
cat commits-hash-previous.txt | while read -a IDS; do
    FILES=$(git diff-tree --no-commit-id --name-only -r ${IDS[0]})
    for FILE in ${FILES[@]}; do
        FILENAME=${FILE//"/"/"."}
        git show ${IDS[0]}:$FILE > src/${IDS[0]}.$FILENAME
        git show ${IDS[1]}:$FILE > src/${IDS[1]}.$FILENAME
    done
done
mkdir machi_scraper
mv src/ machi_scraper/
mv issue-*.txt machi_scraper/
mv all-commits.txt machi_scraper/
mv commits-hash-previous.txt machi_scraper/
rm commits.txt
