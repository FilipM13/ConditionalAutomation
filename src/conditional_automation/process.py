from typing import Optional

from .kwargs import Kwargs


class Process(Kwargs):
    
    def __init__(self, function, kwargs: Optional[dict] = None) -> None:
        super().__init__(kwargs)
        self.function = function
    
    def __call__(self):
        try:
            _kwargs = self.check_kwargs() if self.kwargs else None
            if _kwargs:
                self.function(**_kwargs)
            else:
                self.function()
            return True
        except:
            return False
