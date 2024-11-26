from dataclasses import dataclass
from typing import List, Optional

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
    
    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}"
    
    def validate(self) -> tuple[bool, str]:
        if len(self.last_name) > 40:
            return False, "Фамилия не может быть длиннее 40 символов"
        if len(self.first_name) > 40:
            return False, "Имя не может быть длиннее 40 символов"
        if self.middle_name and len(self.middle_name) > 60:
            return False, "Отчество не может быть длиннее 60 символов"
        if not self.gender:
            return False, "Пол обязателен для заполнения"
        if not self.department_id:
            return False, "Необходимо выбрать кафедру"
        return True, "" 