import subprocess
import os
import urllib2
import json

class TorrentHandler:
    instance = ""
    def start_from_magnet(self, uri):
        bin_path = os.path.abspath("bin/")
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = bin_path
        env["DYLD_LIBRARY_PATH"] = bin_path
        kwargs = {
            "cwd": bin_path,
            "env": env,
        }
        self.instance = subprocess.Popen([bin_path+"/torrent2http", "-magnet='"+uri+"'"], **kwargs)
        return self.instance
    
    def check_progress(self):
        response = urllib2.urlopen("http://localhost:5001/status")
        data = json.load(response)
        return data['progress']
        
    def get_biggest_file(self):
    	response = urllib2.urlopen("http://localhost:5001/ls")
    	data = json.load(response)
    	biggest_file = sorted(data['files'], key=lambda x: x["size"])[-1]
    	return biggest_file