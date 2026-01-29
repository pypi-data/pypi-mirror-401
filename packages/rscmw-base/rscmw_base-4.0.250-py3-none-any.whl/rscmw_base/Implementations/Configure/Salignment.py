from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SalignmentCls:
	"""Salignment commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("salignment", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AlignmentMode:
		"""CONFigure:BASE:SALignment:MODE \n
		Snippet: value: enums.AlignmentMode = driver.configure.salignment.get_mode() \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('CONFigure:BASE:SALignment:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AlignmentMode)

	def set_mode(self, mode: enums.AlignmentMode) -> None:
		"""CONFigure:BASE:SALignment:MODE \n
		Snippet: driver.configure.salignment.set_mode(mode = enums.AlignmentMode.IQ) \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AlignmentMode)
		self._core.io.write(f'CONFigure:BASE:SALignment:MODE {param}')

	def get_slot(self) -> str:
		"""CONFigure:BASE:SALignment:SLOT \n
		Snippet: value: str = driver.configure.salignment.get_slot() \n
		No command help available \n
			:return: slot: No help available
		"""
		response = self._core.io.query_str('CONFigure:BASE:SALignment:SLOT?')
		return trim_str_response(response)

	def set_slot(self, slot: str) -> None:
		"""CONFigure:BASE:SALignment:SLOT \n
		Snippet: driver.configure.salignment.set_slot(slot = 'abc') \n
		No command help available \n
			:param slot: No help available
		"""
		param = Conversions.value_to_quoted_str(slot)
		self._core.io.write(f'CONFigure:BASE:SALignment:SLOT {param}')
