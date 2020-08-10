from services.custom_search import CustomSearchService
from googleapiclient.errors import HttpError
import json


class GoogleAPIsService:

    CUSTOMSEARCH = "customsearch"

    SERVICES = {CUSTOMSEARCH: CustomSearchService}

    def __init__(self, api_key=None):
        self.__services = dict()
        self.register_apikey(api_key)

    def get_service(self, service_name):
        return self.__services.get(service_name)

    def __getitem__(self, key):
        return self.get_service(key)

    def __build_services(self, api_key):
        for api, service_class in GoogleAPIsService.SERVICES.items():
            service_instance = self.__services.get(api)
            if not service_instance:
                self.__services[api] = service_class(api_key)
            else:
                service_instance.update_apikey(api_key)

    def get_customsearch_service(self) -> CustomSearchService:
        return self.get_service(GoogleAPIsService.CUSTOMSEARCH)

    def register_apikey(self, api_key):
        try:
            self.__build_services(api_key)
        except HttpError as e:
            content = json.loads(e.content)
            raise Exception(f"Unable to configure APIKEY: {content['error']['message']}")
        except Exception as e:
            raise e
        else:
            self.__api_key = api_key

    def get_apikey(self):
        return self.__api_key
