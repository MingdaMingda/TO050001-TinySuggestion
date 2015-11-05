#!/usr/bin/env python
#coding=utf-8
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import sys

from tornado.options import define, options

define("port", default=8902, help="run on the given port", type=int)

from tiny_sugg import SuggServer

_sugg_server = SuggServer()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class SuggHandler(tornado.web.RequestHandler):
    def get(self):
        prefix = self.get_argument('q')
        if prefix is None:
            sys.stderr.write('[ERROR] no name')
            sys.write('error')
            return

	sugg_info = _sugg_server.get_sugg(prefix.encode('utf-8'))

        self.render("sugg.html", info=sugg_info)

def main():
    _sugg_server.init()

    tornado.options.parse_command_line()
    application = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/r/sugg/", SuggHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)

    sys.stderr.write('[trace] service started...\n')

    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()

