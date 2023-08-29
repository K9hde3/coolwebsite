import os
from flask import Flask
import json as js_object_notation

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_PATH = os.path.join(CURRENT_DIR, "blog.json")

class json:
    def load(file_name: str) -> Union[list, dir]: # FIXME: Default value
        if not os.path.isfile(file_name):
            raise FileNotFoundError("File '" + file_name + "' not found.")
        iterations = 0
        while True:
            try:
                with open(file_name, "r") as file:
                    return js_object_notation.load(file)
            except:
                iterations += 1
                if iterations >= 30:
                    raise Exception("JSON file could not be loaded")
            else:
                break
    
    def dump(content: Union[list, dir], file_name: str):
        if not os.path.isfile(file_name):
            raise FileNotFoundError("File '" + file_name + "' not found.")
        with open(file_name, "w") as file:
            js_object_notation.dump(content, file)

class Blog:
    def __init__(self, topic: Optional[str] = None):
        blog = json.load(BLOG_PATH)
        current_topic = None
        if not topic is None:
            for blog_topic in blog["topics"]:
                if blog_topic["name"] == topic:
                    current_topic = blog_topic

        self.topic_name = topic
        self.topic = current_topic
        self.blog = blog

    def _reload(self):
        blog = json.load(BLOG_PATH)
        current_topic = None
        if not topic is None:
            for blog_topic in blog["topics"]:
                if blog_topic["name"] == self.topic_name:
                    current_topic = blog_topic
                    
        self.topic = current_topic
        self.blog = blog

    def __getitem__(self, key: str):
        self._reload()
        if not self.topic is None:
            return self.topic["articles"][key]
        else:
            return self.blog["articles"][key]

    def __setitem__ (self, key: str, value):
        self._reload()
        if not self.topic is None:
            self.topic["articles"][key] = value
        else:
            self.blog["articles"][key] = value
        # FIXME: dump
        

    def get(self, key):
        self._reload()
        try:
            if not self.topic is None:
                return self.topic["articles"][key]
            else:
                return self.blog["articles"][key]
        except:
            return None
            

app = Flask("coolwebsite")

@app.route("/")
def index():
    return "Hello World, this is a cool website."

if __name__ == "__main__":
    app.run(host = "localhost", port = 8080)
