from django.http import HttpResponsePermanentRedirect

class CleanURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Remove consecutive slashes and trailing slashes from the request path
        cleaned_path = self.clean_path(request.path)
        
        # If the cleaned path is different from the original path, perform a 301 redirect
        if cleaned_path != request.path:
            print("Previous:" + request.path)
            print("New:" + cleaned_path)
            redirect_url = f"{request.path_info.replace(request.path, cleaned_path)}{request.META.get('QUERY_STRING', '')}"
            return HttpResponsePermanentRedirect(redirect_url)

        response = self.get_response(request)
        return response

    @staticmethod
    def clean_path(path):
        # Iterate over characters to remove consecutive slashes
        cleaned = []
        prev_char = None

        for char in path:
            if char != '/' or prev_char != '/':
                cleaned.append(char)
            prev_char = char

        return ''.join(cleaned)