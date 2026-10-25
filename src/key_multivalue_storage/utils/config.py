class NextGen:
    """
    Boolean controlling whether NextGen features should be activated or not.
    """
    def __init__(self, value: bool) -> None:
        self.value = value

    def __bool__(self) -> bool:
        return self.value

    def __repr__(self) -> str:
        return f"nextgen({self.value})"

_nextgen = NextGen(False)
"Boolean controlling whether NextGen features should be activated or not."
