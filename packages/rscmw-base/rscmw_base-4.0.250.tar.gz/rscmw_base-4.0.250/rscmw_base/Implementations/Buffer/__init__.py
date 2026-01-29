from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Types import DataType
from ...Internal.Utilities import trim_str_response
from ...Internal.ArgSingleList import ArgSingleList
from ...Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BufferCls:
	"""Buffer commands group definition. 6 total commands, 1 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("buffer", core, parent)

	@property
	def lineCount(self):
		"""lineCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lineCount'):
			from .LineCount import LineCountCls
			self._lineCount = LineCountCls(self._core, self._cmd_group)
		return self._lineCount

	def start(self, buffer: str) -> None:
		"""STARt:BASE:BUFFer \n
		Snippet: driver.buffer.start(buffer = 'abc') \n
		Creates and activates a buffer. If the buffer exists already, it is cleared (equivalent to method RsCmwBase.buffer.clear)
		. \n
			:param buffer: string The buffer is identified via this label in all buffer commands.
		"""
		param = Conversions.value_to_quoted_str(buffer)
		self._core.io.write(f'STARt:BASE:BUFFer {param}')

	def stop(self) -> None:
		"""STOP:BASE:BUFFer \n
		Snippet: driver.buffer.stop() \n
		Deactivates the active buffer. Only one buffer can be active at a time. The buffer and its contents are maintained, but
		recording is paused. Use method RsCmwBase.continuePy.buffer to reactivate a buffer. \n
		"""
		self._core.io.write(f'STOP:BASE:BUFFer')

	def stop_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""STOP:BASE:BUFFer \n
		Snippet: driver.buffer.stop_with_opc() \n
		Deactivates the active buffer. Only one buffer can be active at a time. The buffer and its contents are maintained, but
		recording is paused. Use method RsCmwBase.continuePy.buffer to reactivate a buffer. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCmwBase.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'STOP:BASE:BUFFer', opc_timeout_ms)

	def delete(self, buffer: str) -> None:
		"""DELete:BASE:BUFFer \n
		Snippet: driver.buffer.delete(buffer = 'abc') \n
		Deletes a buffer. \n
			:param buffer: string
		"""
		param = Conversions.value_to_quoted_str(buffer)
		self._core.io.write(f'DELete:BASE:BUFFer {param}')

	def clear(self, buffer: str) -> None:
		"""CLEar:BASE:BUFFer \n
		Snippet: driver.buffer.clear(buffer = 'abc') \n
		Clears the contents of a buffer. You get an empty buffer that you can fill with new commands. \n
			:param buffer: string
		"""
		param = Conversions.value_to_quoted_str(buffer)
		self._core.io.write(f'CLEar:BASE:BUFFer {param}')

	def fetch(self, buffer: str, line_number: int) -> str:
		"""FETCh:BASE:BUFFer \n
		Snippet: value: str = driver.buffer.fetch(buffer = 'abc', line_number = 1) \n
		Reads the contents of a buffer line. Buffer contents are stored line by line. Every query generates a new buffer line.
		The queries are not stored together with the results. Reading buffer contents is non-destructive. The lines can be read
		in arbitrary order. \n
			:param buffer: No help available
			:param line_number: integer The line number selecting the line to be read.
			:return: line: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('buffer', buffer, DataType.String), ArgSingle('line_number', line_number, DataType.Integer))
		response = self._core.io.query_str(f'FETCh:BASE:BUFFer? {param}'.rstrip())
		return trim_str_response(response)

	def clone(self) -> 'BufferCls':
		"""Clones the group by creating new object from it and its whole existing subgroups.
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group."""
		new_group = BufferCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
