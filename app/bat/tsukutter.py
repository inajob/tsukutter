#! /usr/bin/python
# -*- coding: utf-8 -*-
from ctypes import *
import urllib
import socket,time
import json as simplejson
#import simplejson
from datetime import datetime,timedelta
import re,random
import realurl
import os

import sqlite3
baseURI="http://twitter.com/statuses/"
basePath = "/app/db/"

import twoauth
#################################
## initialize oauth
#################################
twitterapi = twoauth.api(
	os.environ["TWITTER_CONSUMER_KEY"],
	os.environ["TWITTER_CONSUMER_SECRET"],
	os.environ["TWITTER_ACCESS_KEY"],
	os.environ["TWITTER_ACCESS_SECRET"]);


def post_twit(par):
		dto= socket.getdefaulttimeout();
		socket.setdefaulttimeout(6);
		url=baseURI;
		postData={};
		postData["status"]=par
		postData["source"]="tsukutter"
		params = "status="+urllib.quote(postData["status"].encode("utf-8"))+"&"
		params = params+("source="+postData["source"])
		#print params
		#print url
		try:
				try:
					#f =urllib.urlopen(url+"update.json",params)
                                        twitterapi.status_update(postData["status"].encode("utf-8"));
					#print f.read();
				except :
                                    import traceback
                                    print sys.exc_info()[0]
                                    print sys.exc_info()[1]
                                    print "post time out ?"
		finally:
			socket.setdefaulttimeout(dto)

def gets_reply():
		dto= socket.getdefaulttimeout();
		socket.setdefaulttimeout(32);
		url=baseURI;
		params=""
		obj=[];
		s=""
		try:
				try:
					#only support 20 request
					#f =urllib.urlopen(url+"replies.json")
					#s=f.read();
					#print s
					#obj=simplejson.loads(s);
                                        obj= twitterapi.mentions();
				except :
					import traceback
					print sys.exc_info()[0]
					print sys.exc_info()[1]

					print "mentions time out ?"
					#print (s);
		finally:
			socket.setdefaulttimeout(dto)
		ret=[];
		#for x in obj:
		#	if(x.has_key("text")):
		#		ret.append(x["text"])
		return obj;

bans = ['ks_ad123','siri_jp','SPOPPY_INFO'];
def make_reply():
	ngword=re.compile("@tsukutter")
	jap_data=[];
	jap_url=[];
	all_data=gets_reply();
        ret = [];
        for x in all_data:
            blk = False;
            # bot filter
            for u in bans:
                if x["user"]["screen_name"]==u:
                    blk = True;
            if x == ["retweeted"]:
              print "retweeted";
              blk = true
            if blk == True:
                continue;
            if x["user"]["screen_name"]!="tsukutter" and x["user"]["screen_name"]!="douyo" and x["user"]["screen_name"]!="Mai_iaM" and x["user"]["screen_name"]!="tnd" and re.search(r"t:\d+",x["text"])==None and re.search(r"^@tsukutter",x["text"])!=None:
                ret.append(x);
	for x in ret:
		x["text"]=ngword.sub("",x["text"]);
	return ret


def load_last_req():
	f=None;
	obj=None;
	try:
		f=open(basePath + "req.dat","r")
		str=f.read().decode("utf8")
		obj=simplejson.loads(str);
	except:
		print "load setting error";
		if f!=None:
			f.close();
		obj=None;
	return obj
def save_last_req(str):
	f=open(basePath + "req.dat","w")
	f.write(simplejson.dumps(str))
	f.close();

"""
create table tsukutter (
	tid int primary key,
	text text,
	text_org text,
	id text,
	profile_image_url text,
	name text,
	screen_name text,
        user text,
	created_at text
);

"""

def insert_line(obj):
	text = realurl.conv(obj['text']);
	db.execute('insert into tsukutter(tid,text,text_org,id,profile_image_url,name,screen_name,user,created_at) '+
		"values (?,?,?,?,?,?,?,?,datetime('now', 'localtime'))",
		(obj['tid'],text ,obj['text_org'],obj['id'],obj['profile_image_url'],obj['name'],obj['screen_name'],obj['user']));
def write_json(): # ope
	global db;
	db = sqlite3.connect('../db/tsukutter.db');
	write_cache()
        import mkrss
        mkrss.writeXML()
def write_cache():
	line = db.execute("select * from tsukutter order by created_at desc limit 40");
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
        f=open(basePath + "current.json","w");
	dat=simplejson.dumps({"data":objs});
	f.write(dat);
	f.close();

def dump_assoc(obj):
        for k,v in obj.items():
                print k,":",v
def save_log(addobj):
        if len(addobj)==0:
                return
        for x in addobj:
                insert_line(x);
        write_cache();
	return;
#DEBUGO = None
if __name__ == "__main__":
	import random, sys, os,time,codecs
       
	last_request=load_last_req();  # last_request {id:...,count:...}
	print last_request

	while True:
		print "-- test --"
		if last_request==None:
			last_request={"id":[],"count":0};
			print "SETTING ERROR";
			#sys.exit(-1);
		sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
		rep=make_reply();

	        new_mes=[];
		new_id=last_request["id"]
		flag_break=False;
		for x in (rep):
                        print x
			#print x["id"], x["text"]
                        print last_request["id"]
                        print x["id"]
			for y in last_request["id"]:
				if x["id"] == y:
					flag_break=True;
					print "hit",x["id"],y
					break;
			if flag_break:
				break;
			else:
				print "ok add new message",x["id"]
			#print x["id"]
			#print x["text"]
			#print x["user"]["screen_name"]
			#print x["user"]["profile_image_url"]
			#print
			ttext = "t:"+str(last_request["count"])+" "+x["text"]+" from @"+x["user"]["screen_name"];
			if len(ttext)>140:
				ttext = x["text"];

                        # db record
			text={"text":ttext,
                                "tid":str(last_request["count"]),
                                "id":x["id"],
                                "text_org":x["text"],
                                "profile_image_url":x["user"]["profile_image_url"],
                                "screen_name":x["user"]["screen_name"],
                                "name":x["user"]["name"],
                                "user":simplejson.dumps(x["user"])  # original
                                }

                        #continue
			post_twit(ttext)
			last_request["count"]=last_request["count"]+1
			#print text,x[u"id"]
			#print text['text']
			new_mes.append(text);
			new_id.append(x["id"]);
			new_id=new_id[-100:]
		#sys.exit(0)
		if len(rep)>0:
                        ## db setup
                        db = sqlite3.connect('../db/tsukutter.db');
                        save_log(new_mes);
                        db.commit();
                        db.close();
			last_request={"id":new_id,"count":last_request["count"]}
			save_last_req(last_request);
		print "wait..."
		db = sqlite3.connect('../db/tsukutter.db');
		write_cache();
		#db.commit();
		db.close();
		time.sleep(60*5);		#10min
print "tarminate."

