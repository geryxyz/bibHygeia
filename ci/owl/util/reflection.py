def get_descent_classes(cls):
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_descent_classes(subclass))

    return all_subclasses
