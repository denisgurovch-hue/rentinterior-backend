from typing import List, Dict

class FurnitureService:
    """
    Сервис для подбора мебели по параметрам
    """
    
    def select_furniture(self, room_type: str, style: str, budget: int) -> List[Dict]:
        """
        Подобрать мебель под комнату, стиль и бюджет
        
        Пока возвращаем mock-данные, в следующем шаге заменим на реальную логику
        """
        # Mock данные для тестирования API
        mock_items = [
            {
                "name": "Диван Клиппан (тестовый)",
                "category": "sofa",
                "price": 24999,
                "shop": "IKEA",
                "link": "https://www.ikea.com/ru/ru/",
                "image_url": None
            },
            {
                "name": "Журнальный столик Лакк (тестовый)",
                "category": "table",
                "price": 1999,
                "shop": "IKEA",
                "link": "https://www.ikea.com/ru/ru/",
                "image_url": None
            }
        ]
        
        return mock_items[:2]  # Пока возвращаем 2 предмета для теста

