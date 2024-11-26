class DataAnalyzer:
    def __init__(self, main_data):
        self.main_data = main_data
        
    def create_sum_order_items_df(self):
        sum_order_items_df = self.main_data.groupby(by="product_category_name_english")["product_id"].count().reset_index()
        sum_order_items_df = sum_order_items_df.rename(columns={"product_id": "products"})
        sum_order_items_df = sum_order_items_df.sort_values(by="products", ascending=False)
        
        return sum_order_items_df
    
    def create_product_price_df(self):
        product_price_df = self.main_data.groupby(by="product_category_name_english").agg({
            "order_id": "nunique",
            "price":  "max"
        }).sort_values(by="price", ascending=False)
        
        return product_price_df
    
    def create_monthly_orders_df(self):
        monthly_df = self.main_data.resample(rule='M', on='order_approved_at').agg({
            "order_id": "nunique",
        })
        monthly_df.index = monthly_df.index.strftime('%B')
        monthly_df = monthly_df.reset_index()
        monthly_df.rename(columns={
            "order_id": "order_count"
        }, inplace=True)
        monthly_df = monthly_df.sort_values("order_count").drop_duplicates('order_approved_at', keep='last')
        month_mapping = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }

        monthly_df["month_numeric"] = monthly_df["order_approved_at"].map(month_mapping)
        monthly_df = monthly_df.sort_values("month_numeric")
        monthly_df = monthly_df.drop("month_numeric", axis=1)
        
        return monthly_df
    
    def review_score_df(self):
        review_scores = self.main_data['review_score'].value_counts().sort_values(ascending=False)
        most_common_score = review_scores.idxmax()
        
        return review_scores, most_common_score
    
    
class BrazilMapPlotter:
    def __init__(self, data, plt, mpimg, urllib, st):
        self.data = data
        self.plt = plt
        self.mpimg = mpimg
        self.urllib = urllib
        self.st = st
        
    def plot(self):
        brazil = self.mpimg.imread(self.urllib.request.urlopen('https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'),'jpg')
        ax = self.data.plot(kind="scatter", x="geolocation_lng", y="geolocation_lat", figsize=(10,10), alpha=0.3,s=0.3,c='maroon')
        self.plt.axis('off')
        self.plt.imshow(brazil, extent=[-73.98283055, -33.8,-33.75116944,5.4])
        self.st.pyplot()
        
    
