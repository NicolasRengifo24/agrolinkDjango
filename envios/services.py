
import requests

class UbicacionService:
    @staticmethod
    def obtener_ciudades_cundinamarca():
        url = "https://api-colombia.com/api/v1/Department/15/cities"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return []
