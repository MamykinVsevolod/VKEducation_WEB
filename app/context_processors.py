def sections_processor(request):
    is_authorized = False
    if request.get_full_path() == '/':
        is_authorized = True
    print(request.get_full_path())
    print(is_authorized)
    return {'is_authorized': is_authorized}
