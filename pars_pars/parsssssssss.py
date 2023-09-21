import requests
import json
from statements.pars_statements import Currency as Curr
from loggs.loggs import logger_pars_errors
from typing import List
from db.CRUD.currency import CRUDCurrency
from statements.bd_models import Currency


class ParsNBRB():

    @staticmethod
    def pars_with_offrate() -> List[Curr]:
        url = "https://api.nbrb.by/exrates/currencies"
        result = []
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for i in data:
                currency_model = Curr(**i)
                try:
                    url = f'https://api.nbrb.by/exrates/rates/{currency_model.cur_id}'
                    currency_model.offrate = requests.get(url).json()['Cur_OfficialRate']
                    result.append(currency_model)
                    instance = Currency(
                        Cur_Name=currency_model.name,
                        Cur_ID=currency_model.cur_id,
                        Cur_DateStart=currency_model.start_date,
                        Cur_DateEnd=currency_model.end_date,
                        Cur_Scale=currency_model.scale,
                        Cur_Offrate=currency_model.offrate
                    )
                    CRUDCurrency.add(instance=instance)
                    logger_pars_errors.info(f'Добавлена валюта {currency_model.cur_name}')
                    print('done')
                except Exception as e:
                    logger_pars_errors.error(f'404 error по адресу {url} {e}')

        except requests.exceptions.RequestException as e:
            logger_pars_errors.error(f'произошла ошибка при отправкой запроса к API {e}')

        except json.JSONDecodeError as e:
            ogger_pars_errors.error(f'произошла ошибка при парсинкованииб JSON {e}')

        return result
