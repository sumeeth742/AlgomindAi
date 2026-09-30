from pydantic import BaseModel


class CheatSheetItem(BaseModel):
    key: str
    title: str
    mnemonic: str | None = None
    key_takeaway: str


class CheatSheetGroup(BaseModel):
    group: str
    items: list[CheatSheetItem]
