from abc import ABC, abstractmethod


class BaseAPIProvider(ABC):

    @abstractmethod
    def to_dict_params(self):
        pass

    @abstractmethod
    def api_request(self):
        pass

    # @abstractmethod
    # def attach_to_queue(self):
    #     pass

    @abstractmethod
    def create_transformer(self, request):
        pass

    @abstractmethod
    def cache_manager(self):
        pass

    @abstractmethod
    def read_all_keys_values_from_api(self):
        pass

    @abstractmethod
    def check_for_caches(self):
        pass

    @abstractmethod
    def read_caches(self):
        pass

    @abstractmethod
    def execute_full_request(self):
        pass
    


