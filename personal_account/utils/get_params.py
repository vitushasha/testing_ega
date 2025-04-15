from functools import wraps


def get_param(param_name, param_type):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            param = None
            if self.request.query_params.get(param_name):
                param = self.request.query_params.get(param_name).strip(' []').split(',')
            elif self.request.data.get(param_name):
                param = self.request.data.get(param_name)
            if param and isinstance(param, param_type):
                self.request.data[param_name] = param
            return func(self.request, *args, **kwargs)
        return wrapper
    return decorator
