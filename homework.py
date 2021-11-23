from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    TRAINING_STR: str = 'Тип тренировки: {name}; '
    DURATION_STR: str = 'Длительность: {name:.3f} ч.; '
    DISTANCE_STR: str = 'Дистанция: {name:.3f} км; '
    SPEED_STR: str = 'Ср. скорость: {name:.3f} км/ч; '
    CALORIE_STR: str = 'Потрачено ккал: {name:.3f}.'

    def get_message(self) -> str:
        return (self.TRAINING_STR.format(name=self.training_type)
                + self.DURATION_STR.format(name=self.duration)
                + self.DISTANCE_STR.format(name=self.distance)
                + self.SPEED_STR.format(name=self.speed)
                + self.CALORIE_STR.format(name=self.calories))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    MIN_IN_HOUR: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    CALORIE_RUN_1: ClassVar[int] = 18
    CALORIE_RUN_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        return ((self.CALORIE_RUN_1 * self.get_mean_speed()
                - self.CALORIE_RUN_2) * self.weight
                / self.M_IN_KM * self.duration * self.MIN_IN_HOUR)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    CALORIE_WALK_1: ClassVar[float] = 0.035
    CALORIE_WALK_2: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        return ((self.CALORIE_WALK_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.CALORIE_WALK_2 * self.weight)
                * self.duration * self.MIN_IN_HOUR)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: int
    count_pool: int

    LEN_STEP: ClassVar[float] = 1.38
    CALORIE_SWIMM: ClassVar[float] = 1.1

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + self.CALORIE_SWIMM) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return training_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
