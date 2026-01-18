def binary_insertion_sort(data, sort_type):
    """Сортировка бинарными вставками для отчётов"""
    if not data:
        return []
    
    result = data[:1]  # начинаем с первого элемента
    
    for i in range(1, len(data)):
        current = data[i]
        left = 0
        right = len(result)
        
        while left < right:
            mid = (left + right) // 2
            cmp = 0
            
            if sort_type == 1:  # Отчёт 1: семестр + кафедра + часы
                #Семестр (по возрастанию)
                if current['start_semester'] < result[mid]['start_semester']:
                    cmp = -1
                elif current['start_semester'] > result[mid]['start_semester']:
                    cmp = 1
                else:
                    #Кафедра (по возрастанию)
                    if current['department'] < result[mid]['department']:
                        cmp = -1
                    elif current['department'] > result[mid]['department']:
                        cmp = 1
                    else:
                        #Часы (по убыванию)
                        if current['total_hours'] > result[mid]['total_hours']:
                            cmp = -1 
                        elif current['total_hours'] < result[mid]['total_hours']:
                            cmp = 1 
            
            elif sort_type == 2:  # Отчёт 2: длительность + часы
                #Длительность (по возрастанию)
                if current['duration'] < result[mid]['duration']:
                    cmp = -1
                elif current['duration'] > result[mid]['duration']:
                    cmp = 1
                else:
                    #Часы (по убыванию)
                    if current['total_hours'] > result[mid]['total_hours']:
                        cmp = -1
                    elif current['total_hours'] < result[mid]['total_hours']:
                        cmp = 1
            
            else:  # Отчёт 3: кафедра + часы
                #Кафедра (по возрастанию)
                if current['department'] < result[mid]['department']:
                    cmp = -1
                elif current['department'] > result[mid]['department']:
                    cmp = 1
                else:
                    #Часы (по убыванию)
                    if current['total_hours'] > result[mid]['total_hours']:
                        cmp = -1
                    elif current['total_hours'] < result[mid]['total_hours']:
                        cmp = 1
            
            if cmp < 0:
                right = mid
            else:
                left = mid + 1
        
        # Вставляем элемент на найденную позицию
        result.insert(left, current)
    
    return result
