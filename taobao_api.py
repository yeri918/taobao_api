from flask import Flask, redirect, url_for,request, render_template,redirect
from bs4 import BeautifulSoup
import requests

app=Flask(__name__)

@app.route('/productid/<int:pid>',methods=['POST','GET'])
def product_info(pid):
    if request.method=='POST':
        return redirect(url_for('product_id'))
    else:
        URL = f"https://item.taobao.com/item.htm?id={pid}"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        link="https://item.taobao.com/item.htm?id="+str(pid)
        title = soup.find(id="J_Title").find(class_="tb-main-title").text.strip()
        price = soup.find(id="J_StrPrice").find(class_="tb-rmb-num").text.strip()
        dict ={'Product URL': link, 'Product Name': title,'Price':price}

        for find_ul in soup.find_all('dd'):
            try:
                sub=find_ul.find('ul')['data-property']
                list=[]
                dict.update({sub:list})
                for detail in find_ul.find_all('span'):
                    try:
                        list.append(detail.text.strip())
                    except Exception as e:
                        pass
                if not list:
                    list.append("Could not find")
            except Exception as e:
                pass
    return render_template('result.html',result=dict)

@app.route('/',methods=['POST','GET'])
def product_id():
    if request.method=='POST':
        number=request.form['nm']
        return redirect(url_for('product_info',pid=number))
    else:
        return render_template('enter_id.html')
    

if __name__ == '__main__':
    app.run(debug=True)

#enter_id.html
#result.html