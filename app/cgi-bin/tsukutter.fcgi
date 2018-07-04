#! /usr/bin/python
# -*- coding: utf8 -*-
# coding: utf8 

import cgi,re,os,time,sys,fcntl,glob
import time
import codecs
import json as simplejson
import jon
import sqlite3

import jon.cgi as cgi
import jon.fcgi as fcgi


class Handler(cgi.Handler):
	def process(self, req):
		req.set_header("Content-Type", "text/html")
		if req.params.has_key('n'):
			page = req.params["n"];
		else:
			page = "";
		if req.params.has_key('u'):
			user = req.params['u'];
		else:
			user = None;
		objs = proc(page,user)
		req.write(simplejson.dumps({"data":objs}));
def proc(page,user):
	if page==None or page=="":
	        page = "0";
	db = sqlite3.connect('/app/db/tsukutter.db');
	if user:
		line = db.execute("select * from tsukutter where screen_name=? order by created_at desc limit 10 offset ?", (user,int(page),));
	else:
		line = db.execute("select * from tsukutter order by created_at desc limit 10 offset ?", (int(page),));
	
	objs = [];
	for l in line:
	        obj = {'tid':l[0],
	               'text':l[1],
	               'text_org':l[2],
	               'id':l[3],
	               'profile_image_url':l[4],
	               'name':l[5],
	               'screen_name':l[6],
	               'user':l[7],
	               'created_at':l[8],
	                };
	        objs.append(obj);
	db.close();
	return objs
#print "Content-Type: text/html;charset=utf-8\n\n"
#print simplejson.dumps({"data":objs});

fcgi.Server({fcgi.FCGI_RESPONDER: Handler}).run()

