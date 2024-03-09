class RequestParse:
    def __init__(self, request):
        self.request = request

    def get_int(self, key: str) -> int:
        return int(self.request.POST.get(key, "0"))

    def get_float(self, key: str) -> float:
        return float(self.request.POST.get(key, "0.0"))

    def get_str(self, key: str) -> str:
        return self.request.POST.get(key, "")

    def get_radio(self, key: str) -> bool:
        return self.request.POST.get(key, "off").lower() == "on"

