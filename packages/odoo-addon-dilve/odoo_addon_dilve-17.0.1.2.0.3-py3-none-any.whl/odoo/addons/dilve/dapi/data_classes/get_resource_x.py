from dataclasses import dataclass, field

@dataclass
class GetResourceX:
    resource: bytes

    def __init__(self, response):
        self.resource = response
