from __future__ import annotations
import cv2
import numpy as np
import pyautogui
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class MatchResult:
    x: int
    y: int
    width: int
    height: int
    confidence: float

    @property
    def center(self) -> tuple[int, int]:
        """Возвращает координаты центра найденного объекта."""
        return int(self.x + self.width / 2), int(self.y + self.height / 2)

def find_image(
    template_path: str | Path,
    threshold: float = 0.8,
    match_index: int = 0
) -> List[MatchResult]:
    """
    Ищет изображение-шаблон на экране.
    """
    screenshot = pyautogui.screenshot()
    screen_np = np.array(screenshot)
    
    screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
    
    template_file = Path(template_path)
    if not template_file.exists():
        raise FileNotFoundError(f"Шаблон {template_path} не найден")
        
    template = cv2.imread(str(template_file))
    if template is None:
        raise ValueError("Неверный формат файла шаблона или ошибка чтения")
    
    h, w = template.shape[:2]
    
    try:
        res = cv2.matchTemplate(screen_bgr, template, cv2.TM_CCOEFF_NORMED)
    except cv2.error as e:
        raise RuntimeError("Ошибка обработки изображения OpenCV") from e
    
    # Находим точки, превышающие порог
    y_loc, x_loc = np.where(res >= threshold)
    
    matches: List[MatchResult] = []
    
    for x, y in zip(x_loc, y_loc):
        if matches:
            last_match = matches[-1]
            if abs(x - last_match.x) < 5 and abs(y - last_match.y) < 5:
                continue
                
        confidence = float(res[y, x])
        matches.append(MatchResult(int(x), int(y), w, h, confidence))
    
    return matches

def move_to_image(image_path: str | Path, click: bool = True) -> Optional[tuple[int, int]]:
    """
    Находит изображение и наводит курсор на его центр.
    Возвращает координаты центра или None.
    """
    try:
        matches = find_image(image_path, threshold=0.9)
    except Exception as e:
        print(f"Ошибка поиска изображения: {e}")
        return None

    if not matches:
        print("Совпадений не найдено")
        return None

    target = matches[0]
    center_x, center_y = target.center

    pyautogui.moveTo(center_x, center_y)
    
    if click:
        pyautogui.click()
        
    return center_x, center_y