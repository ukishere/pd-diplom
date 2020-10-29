

def input_validation(request):
    try:
        request.data['shop']
        request.data['categories']
        request.data['goods']

        if request.content_type != 'application/yaml':
            return False
    except KeyError:
        return False
    else:
        return True