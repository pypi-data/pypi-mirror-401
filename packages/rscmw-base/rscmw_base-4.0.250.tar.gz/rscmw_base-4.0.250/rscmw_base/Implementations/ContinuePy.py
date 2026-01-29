from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ContinuePyCls:
	"""ContinuePy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("continuePy", core, parent)

	def set_buffer(self, buffer: str) -> None:
		"""CONTinue:BASE:BUFFer \n
		Snippet: driver.continuePy.set_buffer(buffer = 'abc') \n
		Reactivates a buffer that was deactivated via method RsCmwBase.buffer.stop) . The R&S CMW continues writing data to the
		buffer. \n
			:param buffer: string
		"""
		param = Conversions.value_to_quoted_str(buffer)
		self._core.io.write(f'CONTinue:BASE:BUFFer {param}')
