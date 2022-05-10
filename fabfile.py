import shlex, subprocess
import os
import shutil
import sys
import socketserver

from psutil import Popen

# from pelican.server import ComplexHTTPRequestHandler
def local(command):
    subprocess.Popen(command)

def gh_pages():
    """Publish to GitHub Pages"""
    # rebuild()
    # local("ghp-import -b {github_pages_branch} {deploy_path} -p".format(**env))
    local("hexo generate")
    # local("cd content && git add . && git commit -m 'update md' && git push origin master && cd ../")
    local("git pull && git add . && git commit -m 'update blog src' && git push origin master --force")
    local("cp -rf ./public/* ../visonforcoding.github.io/ && cd ../visonforcoding.github.io && git pull && git add . && git commit -m 'update blog' && git push origin master --force")
    local("pwd")
    # local("cd ../visonforcoding.github.io && git push gitee master --force")
if __name__ == "__main__":
    gh_pages()

