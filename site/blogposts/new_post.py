#!/usr/bin/python

import datetime as dt, os, argparse as arse, tempfile
from subprocess import call

jetzt=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
filejetzt=dt.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

parser=arse.ArgumentParser()
parser.add_argument("--title", default=filejetzt, help="pass title of document", metavar="TITLE")
args = parser.parse_args()
blogpost=args.title.replace(" ","_")+".md"
cwd=os.getcwd()

content=("---\n"
"layout: post\n"
"title: "+args.title+"\n"
"categories: \n"
"date: "+jetzt+"\n"
"---\n")

f = open(os.path.join(cwd, blogpost), 'w')
f.write(content)
f.close()
