import asyncio
from datetime import datetime
from typing import List, Optional

from loguru import logger

import optrabot.config as optrabotcfg
from optrabot.broker.brokerfactory import BrokerFactory
from optrabot.exceptions import FatalTradeException, RetryableTradeException
from optrabot.managedtrade import ManagedTrade
from optrabot.signaldata import SignalData
from optrabot.trademanager import TradeManager
from optrabot.tradetemplate.processor.ironcondorprocessor import \
    IronCondorProcessor
from optrabot.tradetemplate.processor.ironflyprocessor import IronFlyProcessor
from optrabot.tradetemplate.processor.longcallprocessor import \
    LongCallProcessor
from optrabot.tradetemplate.processor.longputprocessor import LongPutProcessor
from optrabot.tradetemplate.processor.putspreadprocessor import \
    PutSpreadProcessor
from optrabot.tradetemplate.processor.templateprocessorbase import \
    TemplateProcessorBase
from optrabot.tradetemplate.templatefactory import Template, TemplateType
from optrabot.tradetemplate.templatetrigger import TriggerType
from optrabot.util.singletonmeta import SingletonMeta


class TemplateProcessor(metaclass=SingletonMeta):
	def __init__(self):
		pass

	async def processTemplate(self, template: Template, signalData: SignalData = None):
		"""
		Processes the signal and generates the appropriate orders.
		
		OTB-269: Implements entry retry mechanism with configurable max_retries and delay.
		- On RetryableTradeException: Wait for entry result and retry up to max_retries times
		- On FatalTradeException: Stop immediately without retry
		- Telegram notification only sent on final failure
		"""
		logger.info('Processing triggered template {}', template.name)
		
		if signalData.timestamp == None or self._isSignalOutdated(signalData.timestamp):
			logger.warning('Signal is outdated already or Signal timestamp is invalid!')
			return
		
		templateTrigger = template.getTrigger()
		if templateTrigger.type is None:
			raise ValueError('Template got no trigger type defined.')
		else:
			if templateTrigger.type == TriggerType.External:
				logger.debug(f'Processing triggered by external trigger')
			elif templateTrigger.type == TriggerType.Time:
				logger.debug(f'Processing triggered by time trigger')
			elif templateTrigger.type == TriggerType.Flow:
				logger.debug(f'Processing triggered by Flow Engine action')
		
		if templateTrigger.type == TriggerType.External:
			if templateTrigger.fromTimeUTC != None:
				today = datetime.today().date()
				fromDateTimeUTC = datetime.combine(today, templateTrigger.fromTimeUTC.time())
				signalDateTimeUTC = datetime.combine(today, signalData.timestamp.time())
				deltaInSeconds = (signalDateTimeUTC - fromDateTimeUTC).total_seconds()
				if deltaInSeconds <= 0:
					logger.info('Signal time is before "from time" of the template. Ignoring signal.')
					return
				
			if templateTrigger.toTimeUTC != None:
				today = datetime.today().date()
				toDateTimeUTC = datetime.combine(today, templateTrigger.toTimeUTC.time())
				signalDateTimeUTC = datetime.combine(today, signalData.timestamp.time())
				deltaInSeconds = (signalDateTimeUTC - toDateTimeUTC).total_seconds()
				if deltaInSeconds >= 0:
					logger.info('Signal time is after "to time" of the template. Ignoring signal.')
					return
				
			if templateTrigger.excludeFromTimeUTC != None and templateTrigger.excludeToTimeUTC != None:
				today = datetime.today().date()
				excludeFromDateTimeUTC = datetime.combine(today, templateTrigger.excludeFromTimeUTC.time())
				excludeToDateTimeUTC = datetime.combine(today, templateTrigger.excludeToTimeUTC.time())
				signalDateTimeUTC = datetime.combine(today, signalData.timestamp.time())
				deltaFromInSeconds = (signalDateTimeUTC - excludeFromDateTimeUTC).total_seconds()
				deltaToInSeconds = (signalDateTimeUTC - excludeToDateTimeUTC).total_seconds()
				if deltaFromInSeconds >= 0 and deltaToInSeconds <= 0:
					logger.info('Signal time is excluded the template. Ignoring signal.')
					return

		# OTB-269: Retry configuration
		max_retries = template.get_entry_max_retries()
		retry_delay = template.get_entry_retry_delay()
		attempt = 0
		last_error: Optional[str] = None
		
		while attempt <= max_retries:
			attempt += 1
			if attempt > 1:
				logger.info(f'Entry retry attempt {attempt}/{max_retries + 1} for template {template.name} after {retry_delay}s delay')
				await asyncio.sleep(retry_delay)
			
			try:
				# Create template processor fresh each attempt (recalculates strikes, etc.)
				templateProcessor = self.createTemplateProcessor(template)
			except ValueError as e:
				error_msg = f'Error creating a Template Processor: {e}'
				logger.error(error_msg)
				raise ValueError(error_msg) from e
			
			if templateProcessor.check_conditions() == False:
				logger.info('Template conditions are not met. Ignoring signal.')
				return

			try:
				# Compose entry order fresh each attempt (uses current market data)
				entryOrder = templateProcessor.composeEntryOrder(signalData)
				if entryOrder == None:
					error_msg = 'Error creating entry order.'
					logger.error(error_msg)
					raise ValueError(error_msg)
			except ValueError as e:
				# OTB-269: Treat entry order composition errors as retryable
				# Market conditions may change between retries
				last_error = str(e)
				logger.warning(f'Error creating entry order (attempt {attempt}/{max_retries + 1}): {e}')
				if attempt <= max_retries:
					continue  # Try again with next attempt
				else:
					# All retries exhausted for entry order composition
					break

			try:
				managedTrade = await TradeManager().openTrade(entryOrder, template)
				
				if managedTrade is not None:
					# Wait for entry completion (order fill or cancellation)
					entry_result = await managedTrade.wait_for_entry_complete()
					
					if entry_result.success:
						logger.info(f'Entry order for template {template.name} filled successfully')
						return  # Success - exit the retry loop
					else:
						last_error = entry_result.reason
						if not entry_result.retryable:
							logger.error(f'Entry failed (not retryable): {entry_result.reason}')
							# OTB-269: Send notification for non-retryable failures
							# (e.g., user cancellation, margin issues, broker rejection)
							await self._send_entry_failure_notification(template, entry_result.reason, 1, 1)
							# OTB-269: Raise exception so FlowEngine knows the action failed
							raise ValueError(f'Entry failed: {entry_result.reason}')
						else:
							logger.warning(f'Entry failed (retryable): {entry_result.reason}')
							# Continue to next retry attempt
				else:
					# openTrade returned None - shouldn't happen with new exception handling
					logger.warning(f'openTrade returned None for template {template.name}')
					raise ValueError(f'Failed to open trade for template {template.name}')
					
			except FatalTradeException as e:
				# Fatal error - don't retry, send notification immediately
				logger.error(f'Fatal error opening trade for template {template.name}: {e}')
				await self._send_entry_failure_notification(template, str(e), attempt, max_retries + 1)
				raise ValueError(f'Fatal trade error: {e}') from e
				
			except RetryableTradeException as e:
				# Retryable error during openTrade (before order was placed)
				last_error = str(e)
				logger.warning(f'Retryable error opening trade (attempt {attempt}/{max_retries + 1}): {e}')
				# Continue to next retry attempt
		
		# All retries exhausted
		logger.error(f'All {max_retries + 1} entry attempts failed for template {template.name}. Last error: {last_error}')
		await self._send_entry_failure_notification(template, last_error, attempt, max_retries + 1)
		# OTB-269: Raise exception so FlowEngine knows the action failed
		raise ValueError(f'All {max_retries + 1} entry attempts failed: {last_error}')
	
	async def _send_entry_failure_notification(self, template: Template, error_reason: str, attempt: int, total_attempts: int):
		"""
		Send Telegram notification about entry failure.
		OTB-269: Only called on final failure (after all retries exhausted or fatal error).
		"""
		from optrabot.tradinghubclient import NotificationType, TradinghubClient
		
		if total_attempts > 1:
			message = (
				f'❌ Entry failed for template *{template.name}*\n'
				f'*Strategy:* {template.strategy}\n'
				f'*Account:* {template.account}\n'
				f'*Attempts:* {attempt}/{total_attempts}\n'
				f'*Reason:* {error_reason}'
			)
		else:
			message = (
				f'❌ Entry failed for template *{template.name}*\n'
				f'*Strategy:* {template.strategy}\n'
				f'*Account:* {template.account}\n'
				f'*Reason:* {error_reason}'
			)
		
		await TradinghubClient().send_notification(NotificationType.ERROR, message)

	def createTemplateProcessor(self, template: Template) -> TemplateProcessorBase:
		"""
		Creates a new template processor for the given template
		"""
		match template.getType():
			case TemplateType.LongCall:
				return LongCallProcessor(template)
			case TemplateType.LongPut:
				return LongPutProcessor(template)
			case TemplateType.PutSpread:
				return PutSpreadProcessor(template)
			case TemplateType.IronFly:
				return IronFlyProcessor(template)
			case TemplateType.IronCondor:
				return IronCondorProcessor(template)
			case _:
				raise ValueError('Unsupported template type: {}'.format(template.getType()))

	def determineTemplates(self, signalStrategy: str) -> List[Template]:
		"""
		Determines a list of Templates which match the given external signal strategy
		"""
		config :optrabotcfg.Config = optrabotcfg.appConfig
		matching_templates = []
		for template in config.getTemplates():
			if template.is_enabled() == False:
				continue
			trigger = template.getTrigger()
			if trigger is not None and trigger.type == TriggerType.External and trigger.value == signalStrategy:
				matching_templates.append(template)
		return matching_templates
	
	def _isSignalOutdated(self, signalTimeStamp: datetime):
		""" Checks if the time stamp of the signal is older than 10 minutes which means it's outdated.
		
		Parameters
		----------
		signalTimeStamp : datetime
    		Timestamp of the signal.

		Returns
		-------
		bool
			Returns True, if the signal is outdated
		"""
		if signalTimeStamp == None:
			return True
		currentTime = datetime.now().astimezone()
		timeDelta = currentTime - signalTimeStamp
		if (timeDelta.total_seconds() / 60) > 10:
			return True
		return False
				