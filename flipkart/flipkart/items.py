from dataclasses import dataclass, field


@dataclass
class FlipkartItem():
    url: str = None
    name: str = None
    images: list = field(default_factory=list)
    offers: list = field(default_factory=list)
    improved_price: str = None
    old_price: str = None
    discount_rate: str = None
    rating: str = None
    reviews_rating_total: str = None
    services: list = field(default_factory=list)
    seller: dict = field(default_factory=dict)
    details: list = field(default_factory=list)
    specs: list = field(default_factory=list)
    reviews: list = field(default_factory=list)
    category: list = field(default_factory=list)
