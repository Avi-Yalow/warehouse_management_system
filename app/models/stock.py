from app.extentions import db

class Stock(db.Model):
    __tablename__="stocks"
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), unique=True, nullable=False)
    last_updated = db.Column(db.DateTime(), nullable=False,server_default=db.func.now(), onupdate=db.func.now())
    # One-to-One relationship with Product
    product = db.relationship('Product', back_populates='stock')
    
    @property
    def data(self):
        return {
            'product_id':self.product_id,
            'quantity':self.quantity,
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_product_id(cls,product_id):
        return cls.query.filter(cls.product_id==product_id).first()
    
    @classmethod
    def get_all(cls):
        stocks = cls.query.all()
        res = []
        for stock in stocks:
            res.append(stock.data)
        return res



