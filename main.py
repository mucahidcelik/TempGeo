import os, jinja2, webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

pointList = []

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
    
    def post(self):
        name = self.request.get('pointName')
        latitude = self.request.get('pointLatitude')
        longitude = self.request.get('pointLongitude')
        print('n:'+name+' Lat:'+latitude+' Lng:'+longitude)
        pointList.append(dict(pointName=name, pointLatitude=latitude, pointLongitude=longitude))
        self.redirect('/')


app = webapp2.WSGIApplication([('/', MainPage),('/save',MainPage)], debug=True)