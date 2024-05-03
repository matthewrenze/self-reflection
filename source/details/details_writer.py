import pandas as pd
from details.details_row import DetailsRow

class DetailsWriter:

    def write(self, details: list[DetailsRow], file_path: str) -> None:
        table = pd.DataFrame(details)
        table.to_csv(file_path, index=False)
