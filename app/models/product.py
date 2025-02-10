from app.extentions import db

class Product(db.Model):
    __tablename__="products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    manufacturer  = db.Column(db.String(50), nullable=False)
    min_stock_threshold = db.Column(db.Integer, default=10)
    created_at= db.Column(db.DateTime(),nullable=False,server_default=db.func.now())
    updated_at= db.Column(db.DateTime(),nullable=False,server_default=db.func.now(),onupdate=db.func.now())
    stock = db.relationship('Stock', uselist=False, back_populates='product', cascade='all, delete-orphan')

    @property
    def data(self):
        return {
            'name':self.name,
            'price':self.price,
            'category':self.category,
            'manufacturer':self.manufacturer,
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        products = cls.query.all()
        res = []
        for product in products:
            res.append(product.data)
        return res
    
    @classmethod
    def get_by_id(cls,id):
        return cls.query.filter(cls.id==id).first()




