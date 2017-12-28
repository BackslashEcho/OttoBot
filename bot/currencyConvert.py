from webWrapper import RestWrapper

import json
import logging

_logger = logging.getLogger()

class CurrencyConverter():
    def __init__(self, webWrapper):
        self.rest = RestWrapper(webWrapper,
            "https://api.fixer.io/latest", {})

    async def get_symbols(self):
        #best way I can think of doing this is to hardcode USD, and get all possible conversion from USD
        #not ideal (USD still hardcoded) but honestly should be fine
        #unless trump changes USD to TD
        result = ['USD']
        response = await self.rest.request('', {'base':'USD'})
        data = json.loads(await response.text())

        for i in data['rates']:
            result.append(i)

        return sorted(result)

    async def convert(self, base_type, target_types):
        result = {}
        response = await self.rest.request('', {'base':base_type, 'symbols':','.join(target_types)})
        data = json.loads(await response.text())
        for i in data['rates']:
            if i not in target_types:
                _logger.error("unexpected value in conversion response: " + i)
            else:
                result[i] = data['rates'][i]
        return result