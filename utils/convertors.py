def group_list(list1,size=3):
    list_group=[]
    for i in range(0,len(list1),size):
        list_group.append(list1[i:i+size])
    return list_group
