from flask import Flask,request
import json
import logging
import os
from datetime import datetime
if os.path.isdir("logs")==False:
    os.mkdir("logs")
logging.basicConfig(level=logging.DEBUG,format='[%(asctime)s][%(levelname)s]%(message)s',datefmt='%Y-%m-%d %H:%M',handlers=[logging.StreamHandler(),logging.FileHandler('logs\\{}.log'.format(datetime.now().strftime("%Y-%m-%d-%H-%M")), 'w', 'utf-8')])
logging.info("SimpleWebServer 1.0")
logging.info("Loading configs")
try:
    configs=json.load(open('configs.json',encoding='utf-8'))
    app=Flask(__name__,static_url_path="",static_folder=configs["resourcePath"])
    configs["resourcePath"]=configs["resourcePath"].replace("\\","/")
    os.chdir(configs["resourcePath"])
    @app.before_request
    def before_request():
        reqURL=request.path
        reqURL=reqURL[1:]
        if os.path.isfile(os.path.join(reqURL,"index.html")):
            return open(os.path.join(reqURL,"index.html"),encoding='utf-8').read()
    logging.info("Starting server")
    if configs["useSSL"]:
        app.run(host=configs["host"],port=configs["port"],ssl_context=(configs["SSLCertPath"],configs["SSLKeyPath"]))
    else:
        app.run(host=configs["host"],port=configs["port"])
except Exception as e:
    print(e.with_traceback())
    logging.error("configs.json has broken")