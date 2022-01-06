import pandas as pd
import numpy as np
from tqdm import tqdm


def transformChoTot(data,dataRow):
    print('add url')
    dataRow = dataRow[['url','description']]
    data['url'] =''
    for x in tqdm(range(dataRow.shape[0])):
        tmp = data[data['body']==dataRow.description.iloc[x]]
        if tmp.shape[0] ==0:
            continue
        else:
            index = tmp.index
            data.loc[index,'url'] = dataRow.url.iloc[x]
    cols= ['url','date','body','mfdate','region_name','price','carmodel','carbrand','carmodel_name','carseats',
      'condition_ad_name','mileage_v2','gearbox','fuel','carcolor','carorigin',
       'cartype','image']
    
    res = pd.DataFrame(data[cols])

    def to_string(colA,colB):
        print(f'process {colA}')
        res[colB] =''
        tmp_dict = pd.read_csv('../util/Data/{}.csv'.format(colB))
        for x in tqdm(range(res.shape[0])):
            key = res.loc[x,colA]
            if pd.notna(key):
                result = tmp_dict[tmp_dict[colA] == key]
                if result.shape[0] > 0:
                    value = result.iloc[0,2]
                else:
                    continue
                res.loc[x,colB] = value
    
    to_string('carbrand','brand_name')
    to_string('carmodel','car_model')
    to_string('fuel','car_fuel')
    to_string('gearbox','gear')
    to_string('carorigin','origin')
    to_string('cartype','style')
    to_string('carcolor','car_color')
    #color
    id1 = res[res['car_color']=='Xanh lá'].index
    id2 = res[res['car_color']=='Xanh dương'].index
    id = id1.append(id2)

    res.loc[id,'car_color'] = 'Xanh'
    cols= ['url','body','origin','condition_ad_name','mileage_v2','car_color','carseats','gear','mfdate','price',
       'style','date','car_model','car_fuel','brand_name','region_name','image']
    last_res = res[cols]
    last_res.columns = ['url','description', 'origin', 'status', 'car_mileage', 'car_color',
       'car_seats', 'gear', 'car_year', 'car_price', 'style', 'createdAt',
       'model', 'fuel_x', 'brand_name', 'region_name','url_image']

    return last_res


def extractDataBonBanh(data):
    for x in tqdm(range(data.shape[0])):
        data.loc[x,'description'] = ' '.join(data.loc[x,'description'])
    # car_mileage
    for x in tqdm(range(data.shape[0])):
        tmp = data.km_number.iloc[x].split()
        data.loc[x,'car_mileage'] = int(tmp[0].replace(',',''))
    # car_seat
    for x in tqdm(range(data.shape[0])):
        tmp = data.number_seat.iloc[x].split()
        data.loc[x,'car_seats'] = int(tmp[0].replace(',',''))
    # cname, ctype, car_price
    for x in tqdm(range(data.shape[0])):
        tmp = data.title.iloc[x].replace('-','').strip()
        tmp = tmp.split('\t')
        if(len(tmp) == 5):
            cname = tmp[1].strip()
            ctype = tmp[2].strip()
            car_year = tmp[3].strip()
            priceStr = tmp[4].strip().split()
        elif (len(tmp) == 4):
            cname = tmp[1].strip()
            ctype = ''
            car_year = tmp[2].strip()
            priceStr = tmp[3].strip().split()
            
        car_year = [int(s) for s in car_year.split() if s.isdigit()][0]
        data.loc[x,'cname'] = cname
        data.loc[x,'ctype'] = ctype
        data.loc[x,'car_year'] = car_year
        price = 0
        for i in range(0,len(priceStr),2):
            x1 = int(priceStr[i])
            x2 = priceStr[i+1]
            if x2 == 'Tỷ':
                price +=x1*1e9
            elif x2 =='Triệu':
                price += x1 *1e6
        data.loc[x,'car_price'] = price
    data['car_type'] = data['car_model']
    # seller_location
    listCity = ['Gia Lai', 'TP HCM', 'Thanh Hóa', 'Hà Nội', 'Đồng Nai',
       'Bình Dương', 'Lâm Đồng', 'An Giang', 'Hải Phòng', 'Cần Thơ',
       'Bắc Ninh', 'Tây Ninh', 'Bắc Giang', 'Tiền Giang', 'Đăk Lăk',
       'Đồng Tháp', 'Sóc Trăng', 'Bà Rịa Vũng Tàu', 'Đà Nẵng',
       'Vĩnh Phúc', 'Nghệ An', 'Phú Thọ', 'Hải Dương', 'Yên Bái',
       'Điện Biên', 'Nam Định', 'Khánh Hòa', 'Bình Thuận', 'Ninh Bình',
       'Bắc Kạn', 'Vĩnh Long', 'Sơn La', 'Thái Bình', 'Quảng Ninh',
       'Thái Nguyên', 'Hưng Yên', 'Cao Bằng', 'Quảng Trị', 'Bình Định',
       'Kon Tum', 'Hà Nam', 'Hà Tĩnh', 'Thừa Thiên Huế', 'Quảng Ngãi',
       'Bình Phước', 'Lạng Sơn', 'Quảng Bình', 'Đăk Nông', 'Phú Yên',
       'Hậu Giang', 'Long An', 'Quảng Nam', 'Bến Tre', 'Kiên Giang',
       'Lào Cai', 'Hòa Bình', 'Tuyên Quang', 'Bạc Liêu', 'Hà Giang',
       'Trà Vinh', 'Cà Mau', 'Ninh Thuận', 'Lai Châu']
    for x in listCity:
        id = data[data.seller_address.str.contains(x)].index
        data.loc[id,'seller_location'] = x
    
    # create at
    for x in tqdm(range(data.shape[0])):
        tmp = data.date.iloc[x].replace('Đăng ngày\t','')
        tmp = tmp.replace('Đăng ngày ','')
        tmp = tmp.split('\t')
        data.loc[x,'createdAt'] = tmp[0]

    # rename
    data['car_fuel'] = data['engine']
    data['car_origin'] = data['origin']
    data['car_condition'] = data['status']
    data['car_color'] = data['exterior_color']
    data['car_gearbox'] = data['gear']
    cols = ['url','description', 'car_origin', 'car_condition', 'car_mileage', 'car_color',
       'car_seats', 'car_gearbox', 'car_year', 'car_price', 'car_type', 'createdAt',
       'cname', 'car_fuel', 'seller_location','url_image']
    tmp = data[cols]
    return tmp


def transformBonBanh(data):
    # gearbox
    print("process gearbox")
    id1 = data[data['car_gearbox'] =='Số tự động'].index
    id2 = data[data['car_gearbox'] =='Số tay'].index
    data.loc[id1,'gear'] = 'Tự động'
    data.loc[id2,'gear'] = 'Số sàn'

    print("process engine")
    idXeDien = data[data['car_fuel'].str.contains('Điện')].index
    data.drop(index=idXeDien,inplace=True)
    data.reset_index(drop=True, inplace=True)
    id1 = data[data.car_fuel.str[0:1] =='X'].index
    id2 = data[data.car_fuel.str[0:1] =='D'].index
    id3 = data[data.car_fuel.str[0:1] =='H'].index
    data.loc[id1,'fuel_x'] = 'Xăng'
    data.loc[id2,'fuel_x'] = 'Dầu'
    data.loc[id3,'fuel_x'] = 'Động cơ Hybrid'

    print("process car origin")
    id1 = data[data['car_origin'] =='Lắp ráp trong nước'].index
    id2 = data[data['car_origin'] =='Nhập khẩu'].index
    data['origin'] = ''
    data.loc[id1,'origin'] = 'Việt Nam'
    data.loc[id2,'origin'] = 'Nước khác'

    print("process car type")
    tmp_dict = {
        'Hatchback':'Hatchback',
        'Crossover':'SUV / Cross over',
        'SUV':'SUV / Cross over',
        'Bán tải / Pickup':'Pick-up (bán tải)',
        'Truck':'Kiểu dáng khác',
        'Sedan':'Sedan',
        'Van/Minivan':'Van',
        'Convertible/Cabriolet':'Kiểu dáng khác',
        'Coupe':'Coupe (2 cửa)',
        'Wagon':'Sedan'
    }
    data['style']=''
    for x in tmp_dict:
        id = data[data['car_type'] == x].index
        data.loc[id,'style'] = tmp_dict[x]

    print("process car brand")
    tmp_brand_name = ['Kia', 'Ford', 'Lexus', 'Thaco', 'Mitsubishi',
       'LandRover', 'Toyota', 'Honda', 'VinFast', 'Mazda', 'Infiniti',
       'Hyundai', 'BMW', 'Fiat', 'Vinaxuki', 'Maserati', 'Vinfast',
       'Nissan', 'Cadillac', 'Chevrolet', 'Porsche', 'Audi', 'Mini',
       'Suzuki', 'MG', 'JRD', 'Bentley', 'Daewoo', 'Peugeot', 'Haima',
       'Volvo', 'Volkswagen', 'Subaru', 'UAZ', 'Isuzu', 'Dongfeng',
       'Ferrari', 'Rolls Royce', 'Hino', 'Ssangyong', 'Lincoln',
       'Daihatsu', 'Dodge', 'Renault', 'Chrysler', 'Luxgen', 'McLaren',
       'Jeep', 'Jaguar', 'Acura', 'Alfa Romeo', 'Smart', 'Dongben', 'SYM',
       'Proton', 'Opel', 'Scion', 'RAM', 'Geely', 'GMC', 'Lamborghini',
       'Morgan', 'Baic', 'Tobe', 'Chery', 'Changan', 'Mekong', 'Zotye',
       'Samsung', 'Gaz', 'Martin Aston', 'Lifan', 'Asia', 'Lada', 'Mercedes Benz']
    for x in tmp_brand_name:
        id = data[data['cname'].str.contains(x)].index
        data.loc[id,'brand_name'] = x
    
    print("process car model")
    for x in tqdm(range(data.shape[0])):
        setA = str(data.loc[x,'cname']).split()
        setB = str(data.loc[x,'brand_name']).split()
        if len(setB)==0:
            continue
        df = []
        for item in setA:
            if item not in setB:
                df.append(item)
        res = ' '.join(df)
        data.loc[x,'model'] = res.title()

    print("process car model")
    tmp_brand_name = pd.read_csv('../util/Data/brand_name.csv')
    tmp_car_model = pd.read_csv('../util/Data/car_model.csv')
    tmp_dict = {
        'Cx3':'CX 3',
        'CX5':'CX 5',
        'CX8':'CX 8',
        'CX9':'CX 9',
        'I10':'Grand i10',
        'Lux A 2.0':'Lux',
        'Lux SA 2.0':'Lux',
        'MU-X':'Mu X',
        'VF E34':'VFe34'
    }
    for x in tmp_dict:
        id = data[data['model'] == x].index
        data.loc[id,'model'] = tmp_dict[x]
    
    print("process car region name")
    tmp_dict = {
        'Bà Rịa Vũng Tàu':'Bà Rịa - Vũng Tàu',
        'TP HCM':'Tp Hồ Chí Minh',
        'Đăk Lăk':'Đắk Lắk',
        'Đăk Nông':'Đắk Nông'
    }
    data['region_name'] = data['seller_location']
    for x in tmp_dict:
        id = data[data['seller_location'] == x].index
        data.loc[id,'region_name'] = tmp_dict[x]

    print("process car status")
    id1 = data[data.car_condition =='Xe đã dùng'].index
    id2 = data[data.car_condition =='Xe mới'].index
    data.loc[id1,'status'] = 'Đã sử dụng'
    data.loc[id2,'status'] = 'Mới'
    cols= ['url','description','origin','status','car_mileage','car_color','car_seats','gear',
      'car_year','car_price','style','createdAt','model','fuel_x',
       'brand_name','region_name','url_image']
    last_res = pd.DataFrame(data[cols])

    print("process car color")
    id = last_res[last_res['car_color']=='Ghi'].index
    last_res.loc[id,'car_color'] = 'Xám'
    id1 = last_res[last_res['car_color']=='Cát'].index
    id2 = last_res[last_res['car_color']=='Kem'].index
    id3 = last_res[last_res['car_color']=='Đồng'].index
    id = id1.append([id2,id3])
    last_res.loc[id,'car_color'] = 'Vàng'
    return last_res









    





