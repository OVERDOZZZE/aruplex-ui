def is_authenticated(request):
    return bool(request.session.get('refresh'))
