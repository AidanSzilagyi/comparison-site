
def profile(request):
    if request.user.is_authenticated:
        return {"active_profile": getattr(request.user, "profile", None)}
    return {"active_profile": None}