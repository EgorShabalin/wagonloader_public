from PIL import Image, ImageColor, ImageDraw  # Импортируем инструменты рисования

import copy  # Для создания копии
import os, shutil  # Управление файлами
import random

# Создаем класс кузова
class Wagon:
    def __init__(self, length, width, height, carry):
        self.length = length - 5
        self.width = width - 5
        self.height = height - 5
        self.carry = carry
        self.S = (self.length) * (self.width)
        self.V = (self.length) * (self.width) * (self.height)

    def __str__(self):
        return f"Wagon(L = {self.length}, W = {self.width}, H = {self.height}, M = {self.carry})"


# Создаем класс коробки
class Box:
    def __init__(self, name, length, width, height, mass):
        self.name = name
        self.length = length + 5
        self.width = width + 5
        self.height = height + 5
        self.mass = mass
        self.S = self.length * self.width
        self.V = self.length * self.width * self.height

    # Для читаемого отображения экземляра класса
    def __str__(self):
        return f"{self.name}(L = {self.length}, W = {self.width}, H = {self.height}, M = {self.mass})"

    # Для читаемого отображения экземпляра класса в списке
    def __repr__(self):
        return f"{self.name}"  # (L = {self.length}, W = {self.width}, H = {self.height}, M = {self.mass})'


# Ввод параметров кузова:
def init_wagon():
    wagon_length = int(input("Wagon length(enter 0 to automate): "))
    if (
        wagon_length == 0
    ):  # Для упрощения ввода параметров заданы параметры по умолчанию
        global wagon
        wagon = Wagon(1000, 300, 260, 17000)
    else:
        wagon_width = int(input("Wagon width: "))
        wagon_height = int(input("Wagon height: "))
        wagon_carry = int(input("Wagon carry load: "))
        wagon = Wagon(wagon_length, wagon_width, wagon_height, wagon_carry)
    print(wagon)
    return wagon


# Ввод параметров коробки:
def init_boxes():
    num_boxes = int(input("Number of boxes(enter 0 to automate): "))
    global boxes
    boxes = []
    for i in range(num_boxes):
        i = Box(
            str(
                input("Box name: ")
            ),  # Ввод имени только английскими буквами из-за ограничений PIL
            int(input("Box length: ")),
            int(input("Box width: ")),
            int(input("Box height: ")),
            int(input("Box mass: ")),
        )
        boxes.append(i)

    # Для упрощения ввода параметров заданы параметры по умолчанию или random
    if num_boxes == 0:
        bname = ""
        c = 0
        for r in range(50):
            c += 1
            bname = "box" + str(c)
            boxes.append(
                Box(
                    bname,
                    random.randint(50, 100),
                    random.randint(50, 100),
                    200,
                    random.randint(5, 1000),
                )
            )
    for b in boxes:
        print(b)
    return boxes


"""
		box1 = Box('box1', 14, 113, 205, 1000)
		box2 = Box('box2', 210, 222, 205, 1000)
		box3 = Box('box3', 175, 233, 205, 1000)
		box4 = Box('box4', 195, 58, 205, 1000)
		box5 = Box('box5', 23, 189, 205, 1000)
		box6 = Box('box6', 230, 43, 205, 1000)
		box7 = Box('box7', 127, 112, 205, 1000)
		box8 = Box('box8', 273, 29, 205, 1000)
		box9 = Box('box9', 12, 19, 205, 1000)
		box10 = Box('box10', 230, 92, 205, 1000)
		box11 = Box('box11', 229, 180, 205, 1000)
		box12 = Box('box12', 132, 89, 205, 1000)
		box13 = Box('box13', 169, 134, 205, 1000)
		box14 = Box('box14', 141, 174, 205, 1000)
		box15 = Box('box15', 205, 201, 205, 1000)
		box16 = Box('box16', 192, 138, 205, 1000)
		box17 = Box('box17', 241, 57, 205, 1000)
		box18 = Box('box18', 47, 185, 205, 1000)
		box19 = Box('box19', 146, 126, 205, 1000)
		box20 = Box('box20', 199, 83, 205, 1000)
		boxes = [box1, box2, box3, box4, box5, box6, box7, box8, box9, box10, box11, box12, box13, box14, box15, box16, box17, box18, box19, box20]
"""


# Создание экземпляров классов кузова и коробок
wagon = init_wagon()
input_boxes = init_boxes()
boxes = copy.deepcopy(input_boxes)


# Здесь собирается список всех коробок, которые не поедут
not_to_go_box_list = []


# Проверяем Каждую коробку по размерам и массе
def box_fit(boxes):
    box_list = []
    for b in boxes:
        if b.mass > wagon.carry:
            box_list.append(b)
        if b.height > (wagon.height):
            box_list.append(b)
        if b.V > wagon.V:
            box_list.append(b)
        if b.S > wagon.S:
            box_list.append(b)
    return set(box_list)


boxes_dont_fit = box_fit(boxes)
for b in boxes_dont_fit:
    not_to_go_box_list.append(b.name)


# Скорректированный список коробок на погрузку
def new_boxes(boxes):
    bxs = []
    for b in boxes:
        if b not in box_fit(boxes):
            bxs.append(b)
    return bxs


boxes = new_boxes(boxes)

# Сортируем коробки по массе
"""
def boxes_by_mass(boxes):
	box_dict = {}
	for b in boxes:
		box_dict[b.name] = b.mass
	sorted_boxes = sorted(box_dict.items(), key=lambda kv: kv[1])
	#print('sorted_boxes', sorted_boxes)
	sorted_names = [k[0] for k in sorted_boxes]
	lst = []
	for n in sorted_names:
		for b in boxes:
			if n == b.name:
				lst.append(b)
	return lst[::-1]
# Коробки отсортированны по массе по убыванию
#boxes = boxes_by_mass(boxes)
#print(boxes)"""

# Поворачиваем коробки


def rotate(boxes):
    lst = []
    for b in boxes:
        if b.length > b.width and b.length <= wagon.width:
            b.length, b.width = b.width, b.length
            lst.append(b)
    for l in lst:
        for bx in boxes:
            if l.name == bx.name:
                bx = l
                bx.name = bx.name + "(r)"
    return boxes


"""
def rotate(boxes):
	lst = []
	for b in boxes:
		if b.length < b.width and b.width <= wagon.width:
			b.length, b.width = b.width, b.length
			lst.append(b)
	for l in lst:
		for bx in boxes:
			if l.name == bx.name:
				bx = l
				bx.name = bx.name + '(r)'
	return boxes
"""

boxes = rotate(boxes)

# Создаем очередь коробок на погрузку, исходя из массы
def av_mass(boxes):
    mass_all = 0
    for b in boxes:
        mass_all += b.mass
    mass = mass_all / len(boxes)
    return mass


def light_boxes(boxes):
    avM = av_mass(boxes)
    mass_list = []
    for b in boxes:
        if b.mass <= avM:
            mass_list.append(b)
    return mass_list


def heavy_boxes(boxes):
    avM = av_mass(boxes)
    mass_list = []
    for b in boxes:
        if b.mass > avM:
            mass_list.append(b)
    return mass_list


l_boxes = light_boxes(boxes)
# print('l_boxes', l_boxes)

h_boxes = heavy_boxes(boxes)
# print("h_boxes", h_boxes)


def loading_queue():
    idx = int(len(h_boxes) / 2)
    hb1 = h_boxes[0:idx]
    # print('hb1', hb1)
    hb2 = h_boxes[idx:]
    # hb2.reverse()
    # print('hb2', hb2)

    idx2 = int(len(l_boxes) / 2)
    ls1 = l_boxes[0:idx2]
    ls2 = l_boxes[idx2:]
    # ls2.reverse()

    queue = list(hb1 + ls1 + ls2 + hb2)

    return queue


loading_list = loading_queue()


# print('loading_list', loading_list)

first_list = loading_list[: len(loading_list) // 2]
# print('first_list', first_list)
second_list = loading_list[len(loading_list) // 2 :]
# print('second_list', second_list)


def boxes_by_W(boxes):
    box_dict = {}
    for b in boxes:
        box_dict[b.name] = b.width
    sorted_boxes = sorted(box_dict.items(), key=lambda kv: kv[1])
    # print('sorted_boxes', sorted_boxes)
    sorted_names = [k[0] for k in sorted_boxes]
    lst = []
    for n in sorted_names:
        for b in boxes:
            if n == b.name:
                lst.append(b)
    return lst[::-1]


first_list = boxes_by_W(first_list)
second_list = boxes_by_W(second_list)


def boxes_by_S(boxes):
    box_dict = {}
    for b in boxes:
        box_dict[b.name] = b.S
    sorted_boxes = sorted(box_dict.items(), key=lambda kv: kv[1])
    # print('sorted_boxes', sorted_boxes)
    sorted_names = [k[0] for k in sorted_boxes]
    lst = []
    for n in sorted_names:
        for b in boxes:
            if n == b.name:
                lst.append(b)
    return lst[::-1]


first_list = boxes_by_S(first_list)
second_list = boxes_by_S(second_list)


"""
def boxes_by_L(boxes):
	box_dict = {}
	for b in boxes:
		box_dict[b.name] = b.length
	sorted_boxes = sorted(box_dict.items(), key=lambda kv: kv[1])
	#print('sorted_boxes', sorted_boxes)
	sorted_names = [k[0] for k in sorted_boxes]
	lst = []
	for n in sorted_names:
		for b in boxes:
			if n == b.name:
				lst.append(b)
	return lst[::-1]
first_list = boxes_by_L(first_list)
second_list = boxes_by_L(second_list)
"""
# print('first_list_Sorted', first_list)
# print('second_list_Sorted', second_list)

# Поиск коробки с минимальной массой
def mass_min(lst):
    min_mass = {}
    for b in lst:
        min_mass[b.name] = b.mass
    sorted_min_mass = sorted(min_mass.items(), key=lambda kv: kv[1])
    min_mass_box = sorted_min_mass[0][0]
    return min_mass_box


# Если после складывания коробок в 2 ряда коробки все равно не влезают, удаляем самую легкую коробку
def check_llist(lst):
    def mass(lst):
        all_mass = 0
        for l in lst:
            all_mass += l.mass
        return all_mass

    not_go = []
    while mass(lst) >= wagon.carry:
        not_go.append(mass_min(lst))
        for l in lst:
            if l.name == mass_min(lst):
                lst.remove(l)
    return not_go


n_go = check_llist(first_list + second_list)

not_to_go_box_list = not_to_go_box_list + n_go

not_to_go_box_list = set(not_to_go_box_list)
not_to_go_box_list = list(not_to_go_box_list)

# print('NTG list', not_to_go_box_list)


def rem_boxes(lst):
    for b in lst:
        if b.name in not_to_go_box_list:
            lst.remove(b)
    return lst


first_list = rem_boxes(first_list)
second_list = rem_boxes(second_list)

# print('first_list', first_list)
# print('second_list', second_list)

# print('NTG list', not_to_go_box_list)

# Создаем изображение кузова
def draw_wagon(wagon):
    image_width = wagon.length
    image_height = wagon.width
    image = Image.new("RGB", (image_width, image_height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, wagon.length, wagon.width), fill=ImageColor.getrgb("blue"))
    return image.save("wagon.png", "PNG")


# Создаем изображение каждой коробки и сохраняем все изображения коробок в папку /boxes
def draw_boxes(boxes):
    if not os.path.exists("boxes"):
        os.mkdir("boxes")

    for b in boxes:
        image = Image.new("RGB", (b.length, b.width))
        draw = ImageDraw.Draw(image)
        draw.rectangle(
            (0, 0, b.length, b.width),
            fill=ImageColor.getrgb("green"),
            outline=ImageColor.getrgb("white"),
        )
        draw.text((5, 5), text=b.name, fill="white", anchor="mm")
        image.save("boxes/" + str((b.name) + ".png"), "PNG")


draw_wagon(wagon)

draw_boxes(first_list)


# Вставляем изображения коробок на изображение кузова
loaded_list = []


def paster(lst, name):
    wag = Image.open("wagon.png")

    box_imgs = []
    for b in lst:
        box_imgs.append(Image.open("boxes/" + str(b.name) + ".png"))
    x = 0
    y = 0
    width = wag.size[1]
    cnt = 0
    mX = 0
    eX = 0
    for i in box_imgs:
        if width >= i.size[1] and wag.size[0] >= x + i.size[0]:
            # print('X', x)
            wag.paste(i, (x, y))
            y += i.size[1]
            width -= i.size[1]
            # print(i.filename)
            # print(i.size)
            if i.size[0] > mX:
                mX = i.size[0]
            if (x + i.size[0]) > eX:
                eX = x + i.size[0]
            loaded_list.append(i.filename[6:-4])
        elif wag.size[0] >= x + mX + i.size[0]:
            x += mX
            # print('X', x)
            y = 0
            width = wag.size[1]
            wag.paste(i, (x, y))
            # wag.save(name + '.png')
            mX = 0
            if i.size[0] > mX:
                mX = i.size[0]
            eX += i.size[0]
            y += i.size[1]
            width -= i.size[1]
            # print(i.filename)
            # print(i.size)
            loaded_list.append(i.filename[6:-4])
        else:
            not_to_go_box_list.append(i.filename[6:-4])

    wag.save(name + ".png")

    x_end = eX
    # print(x_end)
    return x_end


first = paster(first_list, "wagon1")

# Удаляем папку /boxes
shutil.rmtree("boxes")

wagon.length = wagon.length - first
# print('wagon.length', wagon.length)

draw_wagon(wagon)

draw_boxes(second_list)

paster(second_list, "wagon2")

for q in not_to_go_box_list:
    if q in loaded_list:
        not_to_go_box_list.remove(q)

wag1 = Image.open("wagon1.png")

if os.path.exists("wagon2.png"):
    wag2 = Image.open("wagon2.png")

    wag2 = wag2.rotate(180, expand=True)

    wag1.paste(wag2, (first, 0))
    wag1.save("loaded_wagon.png")

    os.remove("wagon1.png")
    os.remove("wagon2.png")
    os.remove("wagon.png")
else:
    wag1.save("loaded_wagon.png")
    os.remove("wagon1.png")
    os.remove("wagon.png")

# print('not_to_go_box_list', not_to_go_box_list)

# Удаляем папку /boxes и лишние файлы
shutil.rmtree("boxes")

# Отображаем отчет о погруженных и не вошедших коробках
if len(not_to_go_box_list) > 0:
    print("\nList of boxes loaded: \n", [b for b in loaded_list])
    print("These boxes can not be loaded: \n", not_to_go_box_list)
else:
    print("\nAll boxes loaded!")
    print("List of boxes loaded: \n", [b for b in loaded_list])

im = Image.open("loaded_wagon.png")
im.show()
