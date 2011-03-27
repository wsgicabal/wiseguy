import webob
import webob.exc
import deform
import colander
from wiseguy.loader import AppLoader

@colander.deferred
def deferred_component_validator(node, kw):
    loader = kw['loader']
    components = loader.ep_parser.get_components()
    def validate(node, val):
        for component_name, component in components:
            if val == component_name:
                return
        raise colander.Invalid(node, 'No such component named %s' % val)
    return validate

@colander.deferred
def deferred_component_widget(node, kw):
    loader = kw['loader']
    components = loader.ep_parser.get_components()
    values = []
    for component_name, component in components:
        title = getattr(component, 'title', component_name)
        values.append((component_name, title))
    return deform.widget.RadioChoiceWidget(values=values)

class SectionSchema(colander.Schema):
    name = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=70)
        )
    component = colander.SchemaNode(
        colander.String(),
        validator = deferred_component_validator,
        widget = deferred_component_widget,
        )

def configurator(environ, start_response):
    request = webob.Request(environ)
    loader = AppLoader()
    rendering = ''
    if request.path_info == '/':
        schema = SectionSchema()
        schema = schema.bind(loader=loader)
        form = deform.Form(schema, buttons=('submit',))
        if request.POST.get('submit'):
            controls = request.POST.items()
            try:
                captured = form.validate(controls)
                response = webob.exc.HTTPFound(
                    location='/app?name=%(name)s&component=%(component)s' %
                    captured)
                return response(environ, start_response)
            except deform.ValidationFailure, e:
                rendering = e.render()
        else:
            rendering = form.render()
    elif request.path_info.startswith('/app'):
        component_name = request.GET['component']
        app_name = request.GET['name']
        component = loader.components[component_name]
        app_schema = colander.SchemaNode(
            colander.Mapping(),
            )
        app_schema.add(colander.SchemaNode(
            colander.String(),
            name = 'name',
            title = 'Name',
            default = app_name,
            ))
        app_schema.add(colander.SchemaNode(
            colander.String(),
            name = 'component',
            default = component_name,
            ))
        component_schema = component.schema.bind(loader=loader)
        component_schema.name = 'config'
        app_schema.add(component_schema)
        form = deform.Form(app_schema, buttons=('submit',))
        if request.POST.get('submit'):
            controls = request.POST.items()
            try:
                captured = form.validate(controls)
                rendering = str(captured)
            except deform.ValidationFailure, e:
                rendering = e.render()
        else:
            rendering = form.render()

    body = '<html><body>%s</body></html>' % rendering
    response = webob.Response(body=body)
    return response(environ, start_response)
    
