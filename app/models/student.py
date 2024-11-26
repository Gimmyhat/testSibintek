import re
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Student:
    id: Optional[int]
    gender: str
    last_name: str
    first_name: str
    middle_name: Optional[str]
    department_id: int
    department_name: Optional[str] = None
    teachers: List[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    photo_path: Optional[str] = None
    modified_at: Optional[datetime] = None
    
    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}"
    
    def validate(self) -> tuple[bool, str]:
        # Проверка обязательных полей
        if not self.gender:
            return False, "Поле 'Пол' обязательно для заполнения"
        if self.gender not in ['Мужской', 'Женский']:
            return False, "Некорректное значение поля 'Пол'"
            
        if not self.last_name or not self.last_name.strip():
            return False, "Поле 'Фамилия' обязательно для заполнения"
        if len(self.last_name) > 40:
            return False, "Фамилия не может быть длиннее 40 символов"
            
        if not self.first_name or not self.first_name.strip():
            return False, "Поле 'Имя' обязательно для заполнения"
        if len(self.first_name) > 40:
            return False, "Имя не может быть длиннее 40 символов"
            
        if self.middle_name and len(self.middle_name) > 60:
            return False, "Отчество не может быть длиннее 60 символов"
            
        if not self.department_id:
            return False, "Необходимо выбрать кафедру"
            
        # Проверка email если он указан
        if self.email:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.email):
                return False, "Некорректный формат email"
                
        # Проверка телефона если он указан
        if self.phone:
            phone_pattern = r'^\+?[1-9]\d{10,11}$'
            if not re.match(phone_pattern, self.phone):
                return False, "Некорректный формат телефона"
        
        return True, "" 