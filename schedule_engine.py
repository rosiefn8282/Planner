# schedule_engine.py

import pandas as pd
import random
from datetime import time, timedelta

DAYS = ["شنبه", "یک‌شنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه"]
TIME_SLOTS = [
    ("07:30", "09:00"), ("09:00", "10:30"), ("10:30", "12:00"),
    ("12:00", "13:30"), ("13:30", "15:00"), ("15:00", "16:30"), ("16:30", "18:00")
]

def read_input():
    df_teachers = pd.read_excel("input_data.xlsx", sheet_name="اساتید")
    df_classes = pd.read_excel("input_data.xlsx", sheet_name="کلاس‌ها")
    df_lessons = pd.read_excel("input_data.xlsx", sheet_name="درس‌ها")
    return df_teachers, df_classes, df_lessons

def generate_initial_population(lessons, teachers, classes, size=50):
    population = []
    for _ in range(size):
        schedule = []
        for _, lesson in lessons.iterrows():
            teacher_row = teachers[teachers['درس'] == lesson['نام درس']].iloc[0]
            available_days = teacher_row['روزهای آزاد'].split(',')
            day = random.choice(available_days)
            slot = random.choice(TIME_SLOTS)
            room = random.choice(classes['شماره کلاس'].tolist())
            schedule.append({
                'درس': lesson['نام درس'],
                'استاد': teacher_row['نام استاد'],
                'روز': day,
                'ساعت شروع': slot[0],
                'ساعت پایان': slot[1],
                'کلاس': room
            })
        population.append(schedule)
    return population

def has_conflict(entry, schedule):
    for other in schedule:
        if (entry['روز'] == other['روز'] and
            not (entry['ساعت پایان'] <= other['ساعت شروع'] or entry['ساعت شروع'] >= other['ساعت پایان'])):
            if entry['استاد'] == other['استاد'] or entry['کلاس'] == other['کلاس']:
                return True
    return False

def fitness(schedule):
    conflicts = 0
    for i in range(len(schedule)):
        for j in range(i + 1, len(schedule)):
            if has_conflict(schedule[i], schedule[j]):
                conflicts += 1
    return -conflicts

def crossover(parent1, parent2):
    point = len(parent1) // 2
    child = parent1[:point] + parent2[point:]
    return child

def mutate(schedule, teachers, classes):
    i = random.randint(0, len(schedule) - 1)
    teacher_row = teachers[teachers['نام استاد'] == schedule[i]['استاد']].iloc[0]
    available_days = teacher_row['روزهای آزاد'].split(',')
    schedule[i]['روز'] = random.choice(available_days)
    schedule[i]['ساعت شروع'], schedule[i]['ساعت پایان'] = random.choice(TIME_SLOTS)
    schedule[i]['کلاس'] = random.choice(classes['شماره کلاس'].tolist())
    return schedule

def run_genetic_algorithm(generations=200, population_size=50):
    teachers, classes, lessons = read_input()
    population = generate_initial_population(lessons, teachers, classes, population_size)

    for _ in range(generations):
        population = sorted(population, key=fitness, reverse=True)
        new_population = population[:10]  # elitism

        while len(new_population) < population_size:
            p1, p2 = random.sample(population[:30], 2)
            child = crossover(p1, p2)
            if random.random() < 0.3:
                child = mutate(child, teachers, classes)
            new_population.append(child)

        population = new_population

    best = max(population, key=fitness)
    return best, fitness(best)
