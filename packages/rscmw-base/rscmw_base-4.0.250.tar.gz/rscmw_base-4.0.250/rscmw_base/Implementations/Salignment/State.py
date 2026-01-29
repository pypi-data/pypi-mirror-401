from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	# noinspection PyTypeChecker
	def fetch(self) -> List[enums.AlignmentState]:
		"""FETCh:BASE:SALignment:STATe \n
		Snippet: value: List[enums.AlignmentState] = driver.salignment.state.fetch() \n
		No command help available \n
			:return: state: No help available"""
		response = self._core.io.query_str(f'FETCh:BASE:SALignment:STATe?')
		return Conversions.str_to_list_enum(response, enums.AlignmentState)
