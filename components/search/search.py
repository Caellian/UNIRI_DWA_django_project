from django_components import component

@component.register("search")
class Search(component.Component):
    template_name = "search/search.html"

    def get_context_data(self):
        return {}

    class Media:
        css = "search/search.css"
        js = "search/search.js"