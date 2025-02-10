import requests

BASE_URL="http://127.0.0.1:5000/"
header={"Content-Type":"application/json"}

#add products
for i in range(2,100):
    payload={
    "name":f"product {i}",
    "price":i* 50.39,
    "category": f"category {i}",
    "manufacturer":f"manufacturer {i}"
    }
    requests.post(BASE_URL+"api/products/add",headers=header,json=payload)


#add stocks to products
for i in range(2,100):
    payload={
    "quantity":100
    }
    res=requests.post(f"{BASE_URL}/api/stocks/add/{i}",headers=header,json=payload)
    res= requests.get(f"{BASE_URL}/{i}",headers=header)
    print(res.json())