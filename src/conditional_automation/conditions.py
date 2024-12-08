from typing import Optional

from .kwargs import Kwargs


class Condition(Kwargs):
    
    def __init__(self, function, kwargs: Optional[dict] = None, name: Optional[str] = None) -> None:
        super().__init__(kwargs)
        self.function = function
        self.name = name
    
    def __call__(self):
        try:
            _kwargs = self.check_kwargs() if self.kwargs else None
            if _kwargs:
                rv = self.function(**_kwargs)
            else:
                rv = self.function()
            assert isinstance(rv, bool)
            return rv
        except:
            return False
