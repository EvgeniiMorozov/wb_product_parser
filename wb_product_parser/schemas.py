from pydantic import BaseModel


class Specification(BaseModel):
    operating_system: str
    model: str
    guarantee: str
    display_type: str
    screen_diagonal: str
    screen_resolution: str
    cpu: str
    ROM_size: str
    RAM_size: str
    battery_capacity: str
    main_camera_resolution: str
