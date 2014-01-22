#!/usr/bin/env python
# inspired Github-Auto-Deploy by logsol
# https://github.com/logsol/Github-Auto-Deploy/blob/master/GitAutoDeploy.py

import urlparse
import sys
import os
import json

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import settings
import logging
import logging.handlers
import urllib2
from netaddr import IPNetwork, IPAddress
from fabfile import deploy
from fabric.tasks import execute

logger = logging.getLogger(__name__)


class GitAutoDeploy(BaseHTTPRequestHandler):
    """
    simple web server that receive post from github
    """
    config = None
    quiet = False
    daemon = False
    git_refs = None
    git_repo_name = None
    git_commit_url = None
    request_ip = None

    def getConfig(self):

        for repository in self.config['repositories']:
            if not os.path.isdir(repository['path']):
                sys.exit('Directory ' + repository['path'] + ' not found')
            if not os.path.isdir(repository['path'] + '/.git'):
                sys.exit('Directory ' + repository['path'] + ' is not a Git repository')

        return self.config

    def do_GET(self):
        """
        this shows test page.
        quick server up test
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("<html><head><title>Hello World</title>")
        self.wfile.write("<link rel='stylesheet' href='//cdn.jsdelivr.net/foundation/5.0.2/css/foundation.min.css'>")
        self.wfile.write("</head>")
        self.wfile.write("<body style='padding:10%;'><h1>Hello World</h1>")
        self.wfile.write("</body></html>")
        self.wfile.close()

    def do_POST(self):
        """
        receive post from github
        """
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        self.set_repo_info(post_body)
        logger.info("received post receive hook payload from github")
        self.request_ip = self.client_address[0]
        logger.info("repo url: %(url)s, ref: %(ref)s" %
                    {"url": self.git_repo_url, "ref": self.git_refs})

        if self.is_valid_request() and self.git_refs == "refs/heads/master":
            branch = self.git_refs.split("/")[-1]
            execute(deploy, repo_name=self.git_repo_name, branch=branch)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
        else:
            self.send_response(404)
        self.end_headers()

    def set_repo_info(self, post_body):
        """
        parse payload info
        """
        post = urlparse.parse_qs(post_body)
        for payload in post['payload']:
            item = json.loads(payload)
            self.git_repo_url = item['repository']['url']
            self.git_repo_name = item['repository']['name']
            self.git_refs = item['ref']
            self.git_commit_url = item['commits'][0]['url']

    def is_valid_request(self):
        """
        Security: for now, we will check ip to validate request
        later we should use HTTPS and basic authentication to verify
        ie: hook address to be: https://yourUser:yourSecret@yoursite.net/path
        """
        valid = False
        # get web hook ip
        response = urllib2.urlopen("https://api.github.com/meta")
        data = json.load(response)
        github_cdir = data['hooks']
        logging.info("request ip: %s" % self.request_ip)
        logging.info("github cdir: %s" % github_cdir)
        if IPAddress(self.request_ip) in IPNetwork(github_cdir[0]) or self.request_ip == '127.0.0.1':
            valid = True
        return valid


def main():
    try:
        server = None
        for arg in sys.argv: 
            if arg == '-d' or arg == '--daemon-mode':
                GitAutoDeploy.daemon = True
                GitAutoDeploy.quiet = True
            if arg == '-q' or arg == '--quiet':
                GitAutoDeploy.quiet = True
                
        if GitAutoDeploy.daemon:
            pid = os.fork()
            if pid != 0:
                sys.exit()
            os.setsid()

        if not GitAutoDeploy.quiet:
            msg = 'github auto deploy service v 0.1 started at port {!s}'.format(settings.PORT)
        else:
            msg = 'github auto deploy service v 0.1 started at port {!s} in daemon mode'.format(settings.PORT)
        print msg
        logger.info(msg)
        server = HTTPServer(('', settings.PORT), GitAutoDeploy)
        server.serve_forever()

    except (KeyboardInterrupt, SystemExit) as e:
        if e: # wtf, why is this creating a new line?
            print >> sys.stderr, e

        if not server is None:
            server.socket.close()

        if not GitAutoDeploy.quiet:
            print 'Goodbye'

if __name__ == '__main__':
    logging.basicConfig(format=settings.FORMAT,
                        level=logging.INFO,
                        filename=settings.LOG_FILE,
                        filemode='a')
    handler = logging.handlers.RotatingFileHandler(settings.LOG_FILE,
                                                   mode='a',
                                                   maxBytes=1000000,  # approx 1mb
                                                   backupCount=1)
    main()
