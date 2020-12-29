import os, jinja2, webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

pointList = []
nextId=1

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_html(self, template, **params):
        html = jinja_env.get_template(template)
        return html.render(params)
    
    def display_html(self, template, **kw):
        self.write(self.render_html(template, **kw))
        
        
class MainPage(Handler):
    def get(self):
        self.display_html("index.html", points = pointList)

class SavePoint(webapp2.RequestHandler):
    def post(self):
        global nextId
        global pointList
        name = self.request.get('pointName')
        latitude = self.request.get('pointLatitude')
        longitude = self.request.get('pointLongitude')
        pointList.append(dict(pointId=nextId, pointName=name, pointLatitude=latitude, pointLongitude=longitude))
        nextId+=1
        self.redirect('/')

class DeletePoint(webapp2.RequestHandler):
    def post(self):
        global pointList
        pointId = self.request.get('pointId')        
        pointList=[i for i in pointList if (i.get('pointId') != int(pointId))]        
        self.redirect('/')

app = webapp2.WSGIApplication([('/', MainPage),('/save',SavePoint),('/delete',DeletePoint)], debug=True)