

def validate_request(request):
    if 'action' in request and 'time' in request:
        return True
    return False


def make_response(request, code, data=None):
    return {
        'action': request.get('action'),
        'time': request.get('time'),
        'data': data,
        'code': code
    }
