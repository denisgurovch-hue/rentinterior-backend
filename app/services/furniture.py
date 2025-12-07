import json
import os
from typing import List, Dict

class FurnitureService:
    """
    Сервис для подбора мебели по параметрам
    """
    
    def __init__(self):
        # Загрузить каталог при инициализации
        catalog_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'furniture_catalog.json')
        with open(catalog_path, 'r', encoding='utf-8') as f:
            self.catalog = json.load(f)
    
    def select_furniture(self, room_type: str, style: str, budget: int) -> List[Dict]:
        """
        Подобрать мебель под комнату, стиль и бюджет
        """
        # 1. Фильтровать по типу комнаты и стилю
        filtered = [
            item for item in self.catalog
            if room_type in item["room_types"] and style in item["styles"]
        ]
        
        # 2. Определить обязательные категории для комнаты
        required_categories = self._get_required_categories(room_type)
        
        # 3. Подобрать обязательные предметы (самые дешевые)
        selected = []
        total_cost = 0
        
        for category in required_categories:
            items_in_category = [item for item in filtered if item["category"] == category]
            if items_in_category:
                # Выбрать самый дешевый
                cheapest = min(items_in_category, key=lambda x: x["price"])
                if total_cost + cheapest["price"] <= budget:
                    selected.append(cheapest)
                    total_cost += cheapest["price"]
                    # Убрать из списка, чтобы не выбрать дважды
                    filtered.remove(cheapest)
        
        # 4. Добавить декор и дополнительные предметы до бюджета
        remaining = [item for item in filtered if item not in selected]
        remaining.sort(key=lambda x: x["price"])  # От дешевых к дорогим
        
        for item in remaining:
            if total_cost + item["price"] <= budget:
                selected.append(item)
                total_cost += item["price"]
        
        return selected
    
    def _get_required_categories(self, room_type: str) -> List[str]:
        """
        Обязательные категории мебели для комнаты
        """
        required = {
            "living_room": ["sofa", "table"],
            "bedroom": ["bed", "wardrobe"],
            "kitchen": ["table", "chair"],
            "bathroom": []
        }
        return required.get(room_type, [])
