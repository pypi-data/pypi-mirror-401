from bclearer_core.objects.registers.nf_verse_registers import (
    NfVerseRegisters,
)


class NfUniverseRegisters(
    NfVerseRegisters
):
    def __init__(self):
        super().__init__()

    def __enter__(self):
        return self

    def __exit__(
        self,
        exception_type,
        exception_value,
        traceback,
    ):
        pass
