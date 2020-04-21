def xuanzhuan(lat,lon,angle):
    nox=[]
    noxx=[]
    earth = 6371.004  # km
    ##lon一度的长度(与lat有关)
    def one_of_lon(lat):
        radius=earth*math.cos(math.radians(lat))
        return math.pi*radius/180
    ##lat一度的长度
    def one_of_lat():
        radius=earth
        return math.pi*radius/180
    for i in range(len(no2)):
        a=[]
        for j in range(len(no2[i])):
            a.append(no2[i][j])
        nox.append(a)
    for i in range(len(no2)):
        a = []
        for j in range(len(no2[i])):
            a.append(no2[i][j])
        noxx.append(a)
    def get_position(lat,lon):#可优化
        a = 0#a是lat的位置
        b = 0
        for i in range(len(lats)):
            a = i
            if a >= (len(lats)-1):
                a = -1
                break
            if abs(lats[i][0]-lat) <= (abs(lats[i][0]-lats[i+1][0]))/2:#abs(i[0]-lat)<=0.013168
                break
        if a == len(lats):
            print('lat查找失败')
            print(lat, lon)
            a = -1
            exit(-1)
        for i in range(len(lons[a])):
            b = i
            if b >= (len(lons[a])-1):
                b = -1
                break
            if abs(lons[a][i] - lon) <= (abs(lons[a][b]-lons[a][b+1]))/2:#abs(i - lon) <= 0.017201
                break
        if b == len(lons[a]):
            print('lon查找失败')
            print(lat,lon)
            b = -1
            exit(-1)
        return a,b
    # def get_position(lat,lon):#可优化
    #     a=0#a是lat的位置
    #     b=0
    #     for i in lats:
    #         if(abs(i[0]-lat)<=0.014):#abs(i[0]-lat)<=0.013168
    #             break
    #         a=a+1
    #     if a==len(lats):
    #         print('查找失败')
    #         print(lat, lon)
    #         exit(-1)
    #         if (abs(i - lon) <=0.018 ):#abs(i - lon) <= 0.017201
    #             break
    #         b = b + 1
    #     if a==len(lats) or b==len(lons[a]):
    #         print('查找失败')
    #         print(lat,lon)
    #         exit(-1)
    #     return a,b
    def get_coordinate(lat,lon,distance,identifier):#输入坐标和距离lv：为经纬度标志，1代表lat，其它代表lon；输入距离返回经纬度
        if(identifier==1):#右
            result = lon + distance / one_of_lon(lat)
            return result
        elif(identifier==2):#下
            result = lat - distance / one_of_lat()
            return result
        elif (identifier == 3):#左
            result = lon - distance / one_of_lon(lat)
            return result
        elif (identifier == 4):#上
            result = lat + distance / one_of_lat()
            return result
        else:
            print('获取坐标函数输入错误')
            exit(-1)
    ###横向处理
    def fangxiang(lat,lon,angle,identifier,weight,accuracy):#lat,lon:坐标 angle：角度，获取上、下直线上的坐标值数组
        a=[]
        b=[]
        if(angle<180and angle>-180):
            newangle = 90 - angle
            if(identifier>0):
                for i in range(0,weight,accuracy):
                    c = get_coordinate(lat, lon,  i * math.sin(math.radians(newangle)),4)
                    d = get_coordinate(lat, lon,  i * math.cos(math.radians(newangle)),3)
                    a.append(c)
                    b.append(d)
            elif (identifier<0):
                for i in range(0, weight, accuracy):
                    c = get_coordinate(lat, lon,  i * math.sin(math.radians(newangle)),2)
                    d = get_coordinate(lat, lon,  i * math.cos(math.radians(newangle)),1)
                    a.append(c)
                    b.append(d)
            else:
                print('错误')
                return a,b
        else:
            if (identifier > 0):
                for i in range(0, weight, accuracy):
                    c = get_coordinate(lat, lon, i , 4)
                    a.append(c)
                    b.append(lon)
            elif (identifier < 0):
                for i in range(0, weight, accuracy):
                    c = get_coordinate(lat, lon, i , 2)
                    a.append(c)
                    b.append(lon)
            else:
                print('错误')
                return a, b
        return a,b#返回两个数组，垂直相距3km的位置
    demo1=[]
    demo2=[]
    demo3=[]
    demo4=[]
    def chuixian(old_lat,old_lon,new_position_one,new_position_two,angle,weight,accuracy):#处理横向数据;old为实际坐标,new为目的坐标
        local_lat_group,local_lon_group=fangxiang(old_lat,old_lon,angle,1,weight,accuracy)#生成上方坐标数组
        new_local_lat_group,new_local_lon_group=fangxiang(new_position_one, new_position_two,360,1,weight,accuracy)
        for i,j,k,l in zip(local_lat_group,local_lon_group,new_local_lat_group,new_local_lon_group):
            p, n = get_position(i,j)
            new_one,new_two= get_position(k,l)
            no2[new_one][new_two] = nox[p][n]
            demo1.append(p)
            demo2.append(n)
            demo3.append(new_one)
            demo4.append(new_two)

        local_lat_group, local_lon_group = fangxiang(old_lat, old_lon, angle, -1,weight,accuracy)  # 生成下方坐标数组
        new_local_lat_group, new_local_lon_group = fangxiang(new_position_one, new_position_two, 360, -1, weight,accuracy)
        for i, j,k,l in zip(local_lat_group,local_lon_group,new_local_lat_group,new_local_lon_group):
            p, n = get_position(i, j)
            new_one,new_two= get_position(k,l)
            no2[new_one][new_two] = nox[p][n]
            demo1.append(p)
            demo2.append(n)
            demo3.append(new_one)
            demo4.append(new_two)
    def zhixian(lat,lon,angle,lenth,weight,accuracy):#输入初始坐标、角度（顺时针旋转为正，逆时针为负，范围：0-90）
        local_lat_group=[]#纬度数组
        local_lon_group=[]#经度数组
        new_lat_group = []  # 纬度数组
        new_lon_group = []  # 经度数组
        for i in range(0, lenth, accuracy):#生成弯曲前的直线上的坐标数组
            c = get_coordinate(lat, lon,  i * math.sin(math.radians(angle)),4)
            d = get_coordinate(lat, lon,  i * math.cos(math.radians(angle)),1)
            local_lat_group.append(c)
            local_lon_group.append(d)
        for i in range(0, lenth, accuracy):#生成弯曲后的直线经纬度数组
            new_lon=get_coordinate(lat,lon,i,1)
            new_lat=lat
            new_lat_group.append(new_lat)
            new_lon_group.append(new_lon)
        for i,j,k,l in zip(local_lat_group,local_lon_group,new_lat_group,new_lon_group):#循环获取坐标数组中每个坐标，依据此坐标调用垂线处理函数
            #调用垂线处理
            chuixian(i,j,k,l,angle,weight,accuracy)
            #直线上数据赋值
            c,d=get_position(i,j)
            position_one,position_two=get_position(k,l)
            no2[position_one][position_two]=nox[c][d]
            demo1.append(c)
            demo2.append(d)
            demo3.append(position_one)
            demo4.append(position_two)
        return 0
    ###处理圆心部分
    #原理：以拐点为圆心分为上下两部分，分别索引旧圆对应新圆
    def yuan(lat,lon,angle,radius,unit,accuracy):
        # a=0#调试用
        # #上半部分
        for localangle,newangle in zip(np.arange(0,180-angle,(180-angle)/unit),np.arange(0,180,180/unit)):
            for distance in np.arange(0,radius,accuracy):
                local_lon=get_coordinate(lat,lon,distance*math.cos(math.radians(localangle)),3)
                local_lat=get_coordinate(lat, lon, distance * math.sin(math.radians(localangle)), 4)
                loop1,loop2=get_position(local_lat,local_lon)
                local_lon = get_coordinate(lat, lon, distance * math.cos(math.radians(newangle)), 3)
                local_lat = get_coordinate(lat, lon, distance * math.sin(math.radians(newangle)), 4)
                loop3, loop4 = get_position(local_lat, local_lon)
                no2[loop3][loop4] = nox[loop1][loop2]
                noxx[loop3][loop4]=1
            #     no2[loop3][loop4] = a#调试用
            # a=a+0.0000005#调试用
        #下半部分
        for localangle,newangle in zip(np.arange(0,180+angle,(180+angle)/unit),np.arange(0,180,180/unit)):
            for distance in np.arange(0,radius,accuracy):
                local_lon=get_coordinate(lat,lon,distance*math.cos(math.radians(localangle)),3)
                local_lat=get_coordinate(lat, lon, distance * math.sin(math.radians(localangle)), 2)
                loop1,loop2=get_position(local_lat,local_lon)
                local_lon = get_coordinate(lat, lon, distance * math.cos(math.radians(newangle)), 3)
                local_lat = get_coordinate(lat, lon, distance * math.sin(math.radians(newangle)), 2)
                loop3, loop4 = get_position(local_lat, local_lon)
                no2[loop3][loop4] = nox[loop1][loop2]
                noxx[loop3][loop4] = 1
            #     no2[loop3][loop4]=a#调试用
            # a = a - 0.0000005#调试用
    def main(lat,lon,angle):
        lenth=100#长度
        weight=40#单面宽度
        accuracy=2#km,精度，采样距离,整数
        radius = weight  # km,半径
        unit = 180  ##角度划分数量
        print('开始处理直线数据')
        zhixian(lat,lon,angle,lenth,weight,accuracy)
        print('直线处理完成')
        print('开始处理弯曲处圆形部分数据')
        for loop1,loop2 in zip(demo1,demo2):
            noxx[loop1][loop2]=0
        for loop3, loop4 in zip(demo3, demo4):
            noxx[loop3][loop4] = 1
        yuan(lat,lon,angle,radius,unit,accuracy)
        for num1 in range(len(noxx)):
            for num2 in range(len(noxx[num1])):
                if(noxx[num1][num2]==0):
                    no2[num1][num2]=0
    main(lat,lon,angle)#纬度、经度、角度(顺时针为正)