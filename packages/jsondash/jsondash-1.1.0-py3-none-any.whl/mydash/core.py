def get(obj, path, default=None):
    path = path.replace("[", ".").replace("]", "")

    for key in path.split("."):
        if not key:
            continue
        try:
            if key in obj:
                obj = obj[key]
            else:
                obj = obj[int(key)]
        except Exception:
            return default
    return obj


