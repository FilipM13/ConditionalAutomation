from typing import Optional

class Kwargs:
    
    def __init__(self, kwargs: Optional[dict] = None) -> None:
        self.kwargs = kwargs
        pass
    
    def check_kwargs(self):
        _kwargs = dict()
        for k, v in self.kwargs.items():
            _kwargs[k] = v if not callable(v) else v()
        return _kwargs
