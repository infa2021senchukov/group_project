def read_data_from_file(input_filename):
    '''
    считывает данные из файла
    '''
    walls_data=[]
    walls_number=0
    units_data=[]
    units_number=0
    with open(input_filename, 'r') as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            object_type = line.split()[0]
            if object_type == "unit":
                units_data.append([])
                parse_unit_parameters(line, units_data, units_number)
                units_number += 1
            if object_type == "wall":
                walls_data.append([])
                parse_wall_parameters(line, walls_data, walls_number)
                walls_number += 1
    return((walls_data,units_data))
                
def parse_wall_parameters(line, walls_data, walls_number):
    '''
    считывает данные класса стен
    '''
    split = line.split()
    for i in range(1,len(split)):
        split[i] = int(split[i])
        walls_data[walls_number].append([])
        walls_data[walls_number][i-1]=split[i]
        
def parse_unit_parameters(line, units_data, units_number):
    '''
    считывает данные класса юнитов
    '''   
    split = line.split()
    unit_points=[]
    for i in range(1,len(split)):
        split[i] = int(split[i])
    for i in range(6):
        units_data[units_number].append(split[i+1])
    unit_points.append(split[7])
    for i in range(9,len(split),2):
        unit_points.append((split[i-1],split[i]))            
    units_data[units_number].append(unit_points)
(walls_data,units_data) = read_data_from_file("level_1.txt")
