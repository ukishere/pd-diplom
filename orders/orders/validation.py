import json

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

def basket_validation(request):
    try:
        all_data = json.loads(request.body)
        for data in all_data:
            data['good_id']
            data['shop_id']
            data['quantity']

        if request.content_type != 'application/json':
            return False
    except KeyError or TypeError:
        return False
    else:
        return True

def default_check(request):
    if not request.user.is_authenticated:
        return True, 'login'
    elif request.user.is_vendor:
        return True, 'orders'
    else:
        return False, None