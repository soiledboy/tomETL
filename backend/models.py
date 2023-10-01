# external modules
import datetime
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import text, func
from typing import List, Dict, Tuple

# internal modules
from backend.extensions import db


class ModelMixin(object):
    """A mixin implementing a simple __repr__."""

    def __repr__(self):
        return "<{klass} @{id:x} {attrs}>".format(
            klass=self.__class__.__name__,
            id=id(self) & 0xFFFFFF,
            attrs=" ".join("{}={!r}".format(k, v) for k, v in self.__dict__.items()),
        )


class Product(ModelMixin, db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    number = db.Column(db.String)
    product_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=False), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=False), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint(id),
        UniqueConstraint(product_id),
    )

    group = db.relationship("Group", secondary="product_groups")

    def to_dict(self) -> Dict:
        return PydanticProduct.from_orm(self).dict()

    @classmethod
    def get_by_name(cls, name: str):
        return cls.query.filter(cls.name == name).first()


class DailyPrice(ModelMixin, db.Model):
    __tablename__ = "prices"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=False), default=datetime.datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    sub_type = db.Column(db.String(20))
    low = db.Column(db.Numeric(precision=19, scale=4))
    mid = db.Column(db.Numeric(precision=19, scale=4))
    high = db.Column(db.Numeric(precision=19, scale=4))
    market = db.Column(db.Numeric(precision=19, scale=4))
    quantity = db.Column(db.Numeric(precision=19, scale=4))
    listings = db.Column(db.Numeric(precision=19, scale=4))
    __table_args__ = (
        UniqueConstraint(date, product_id),
    )

    product = db.relationship("Product", foreign_keys=[product_id])

    def to_dict(self) -> Dict:
        return PydanticDailyPrice.from_orm(self).dict()

    @classmethod
    def price_values_for_card(cls, product, duration: int = 7):
        # @TODO
        #   - what changes do they need to make to the DB?
        #   - get data for 1 card and 1 set going back to August

        with db.engine.connect() as con:
            sql = text(
                """
                SELECT 
                    dp.mid
                    , dp.date
                    , IFNULL(dp.quantity, 0) AS quantity
                FROM products AS p
                JOIN daily_prices AS dp ON p.id = dp.product_id
                WHERE p.name = :name
                    AND c.number = :number
            """
            )
            params = dict(name=product.name, number=product.number)
            res = con.execute(sql, **params).fetchall()
            results = [dict(row) for row in res]
            return results


class ProductGroup(ModelMixin, db.Model):
    __tablename__ = "product_groups"
    # fields
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=False), server_default=func.now())
    updated_at = db.Column(
        db.DateTime(timezone=False),
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))


class Group(ModelMixin, db.Model):
    __tablename__ = "groups"
    # fields
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=False), server_default=func.now())
    updated_at = db.Column(
        db.DateTime(timezone=False),
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )
    name = db.Column(db.String(255))
    abbreviation = db.Column(db.String(20))
    __table_args__ = (
        UniqueConstraint(id),
        UniqueConstraint(abbreviation),
    )

    products = db.relationship("Product", secondary="product_groups")

    def to_dict(self) -> Dict:
        return PydanticCardSet.from_orm(self).dict()


PydanticProduct = sqlalchemy_to_pydantic(Product)
PydanticDailyPrice = sqlalchemy_to_pydantic(DailyPrice)
PydanticCardset = sqlalchemy_to_pydantic(Group)
