# python_mikhadarov
Проект "Генератор лабиринтов"
Целью проекта является написание приложения, с помощью которого можно генерировать лабиринты различного размера, проходить его и визуализировать путь прохождения из одной точки в другую.
Приложение позволяет генерировать лабиринты с помощью 3-х алгоритмов - 
1) Построение минимального остовного дерева 
2) Обход в глубину
3) модифицированный Алгоритм Крускала  
Модифицированный алгоритм Крускала представляет собой построение множеств клеток, содержащих тупики (клетки, из которых нельзя выйти не возвратясь обратно) и соединение их методом обхода в глубину.   
Построение пути также осуществляется методом обхода в глубину.  
При генерации лабиринта можно выбрать указать необходимый размер (но размер окна ограничен и при больших значениях клетки не будет видно).  
Графический интерфейс написан с помощью библиотеки pygame.  
Можно загрузить файл лабиринта, представляющий собой модель лабиринта в виде такстогого файла (с именем maze.txt), в котором стенки обозначены символом '█', а проходы - '_'.  
Есть возможность передвигаться по лабиринту с помощью стрелочных клавиш (передвижение происходит по 2 клетки, т.к. толщина стен равна толшине проходов и из промежуточных клеток нельзя перейди в другой проход).  
Мультиплеер осуществлен через peer-to-peer, максимум 2 игрока, кто быстрее дошел до правой нижней клетки, тот победил, второму игроку необходимо ввести IP и номер порта для поделючения.
Скачивание проекта:  
git clone https://github.com/mihaleksandr/python_mikhadarov.git  
cd dev  
git checkout dev  
pip install -r requirements.txt  
python3 InterfaceServer.py (запуск на основном компьютере или для одиночной игры)   
python3 InterfaceClient.py (если запуск на втором компьютере)   


