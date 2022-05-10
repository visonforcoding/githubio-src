echo 'do pub'
hexo generate
git add . && git commit -m 'update blog src' && git push origin master --force
cp -rf ./public/* ../visonforcoding.github.io/ && cd ../visonforcoding.github.io && git add . && git commit -m 'update blog' && git push origin master --force
pwd