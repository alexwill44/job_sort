from tkinter.tix import Form
from pydantic import BaseModel

class CSVupload(BaseModel):
    skip_header: bool
    overwrite: bool

    @classmethod
    def form_data(
        cls, 
        skip_header: bool,
        overwrite: bool,
    ) -> Form:
        return cls(
            skip_header=skip_header,
            overwrite=overwrite
        )