from rest_framework.renderers import JSONRenderer



class CustomBaseRenderer(JSONRenderer):
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = renderer_context.get('response')
        
        response = {
            'status_code': response_data.status_code,
            'message': response_data.status_text,
            'data': data 
        }
        
        return super(CustomBaseRenderer, self).render(response, accepted_media_type, renderer_context)