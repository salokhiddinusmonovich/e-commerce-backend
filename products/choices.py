from django.db import models

class CategoryType(models.IntegerChoices):
    NON_TYPE = 0, 'Non_type'
    CLOTHES = 1, 'Clothes'
    FOOD = 2, 'Food'
    GAME = 3, 'Game'
    DATA = 4, 'Data'