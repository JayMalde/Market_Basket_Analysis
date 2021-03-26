import pandas as pd
from apriori import apriori
from flask import (Flask, render_template, redirect, request)

dataset = pd.read_csv('Market_Basket_Optimisation.csv',  header = None )

transactions = []
list_of_products=[]
basket=[]
app=Flask(__name__)

totalrows = len(dataset)
totalcol =int( dataset.size /len(dataset) )

for i in range(0, len(dataset)):
    cart = []
    for j in range(0,totalcol):
        if str( dataset.values[i,j] ) != "nan":
            cart.append( str( dataset.values[i,j]  ))            
        if str(dataset.values[i,j]) not in list_of_products:
            list_of_products.append(str(dataset.values[i,j]))  
    transactions.append(cart)


rules = apriori( transactions, min_support = 0.003, min_confidence = 0.04, min_lift = 3)
results = list(rules)

def recommendation(basket):    
    recommendations=[]
    for item in results:
        pair = item[0] 
        items = [x for x in pair]
        for product in basket:
            if items[0]==product:
                # print("Rule: " + items[0] + " -> " + items[1])       
                # print("Support: " + str(item[1]))
                # print("Confidence: " + str(item[2][0][2]))
                # print("Lift: " + str(item[2][0][3]))
                # print("=====================================")
                if items[1] not in recommendations:
                    recommendations.append(items[1])
    return recommendations

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_items = request.form.getlist('items')
        for item in form_items:
            basket.append(item)
    context = {
        'itemset_count': len(list_of_products),
        'rules_count': len(results),
        'items': list_of_products,
        'basket':basket,
        'recommendations': recommendation(basket),
    }
    return render_template('main.html', **context)

@app.route('/reset-basket/', methods=['POST'])
def reset_basket():
    global basket
    basket = []
    return redirect('/')

if __name__ == '__main__':
    app.run()
    debug=True