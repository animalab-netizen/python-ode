from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from python_ode import ChainUseCase, ErrorOutput, ExecutionResult, GuardRejectedError, GuardResult, SequenceUseCase, UseCase, ValueOutput


class EchoUseCase(UseCase[str, str]):
    async def execute(self, param: str) -> ExecutionResult[str]:
        return ExecutionResult.from_value(f"echo:{param}")


class GuardedUseCase(UseCase[str, str]):
    async def guard(self, param: str) -> GuardResult:
        if not param:
            return GuardResult.deny(GuardRejectedError("missing param"))
        return GuardResult.allow()

    async def execute(self, param: str) -> ExecutionResult[str]:
        return ExecutionResult.from_value(param.upper())


class RuntimeTests(unittest.IsolatedAsyncioTestCase):
    async def test_direct_use_case_normalizes_raw_values(self) -> None:
        output = await EchoUseCase().process("pikachu")
        self.assertIsInstance(output, ValueOutput)
        self.assertEqual("echo:pikachu", output.value)

    async def test_guarded_use_case_blocks_invalid_requests(self) -> None:
        output = await GuardedUseCase().process("")
        self.assertIsInstance(output, ErrorOutput)
        self.assertIsInstance(output.error, GuardRejectedError)

    async def test_chain_use_case_maps_first_result_into_second_story(self) -> None:
        chained = ChainUseCase[str, str, str](
            EchoUseCase(),
            lambda value, _param: _return(ExecutionResult.from_value(f"{value}:story")),
        )

        output = await chained.process("bulbasaur")
        self.assertIsInstance(output, ValueOutput)
        self.assertEqual("echo:bulbasaur:story", output.value)

    async def test_sequence_use_case_preserves_ordered_entries(self) -> None:
        sequence = SequenceUseCase[str, str](lambda value: _return(value.upper()))
        output = await sequence.process(["bulbasaur", "charmander", "squirtle"])
        self.assertIsInstance(output, ValueOutput)
        self.assertEqual(["BULBASAUR", "CHARMANDER", "SQUIRTLE"], output.value)


async def _return(value):
    return value
