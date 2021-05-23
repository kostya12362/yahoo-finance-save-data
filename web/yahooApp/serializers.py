from flask_marshmallow import Marshmallow
from yahooApp.models import Symbol, HistoryInfo


ma = Marshmallow()


class HistorySchema(ma.Schema):
    class Meta:
        model = HistoryInfo
        ordered = True
        fields = ('date', 'open', 'high', 'high', 'low', 'close', 'adj_close', 'volume')


class SymbolSchema(ma.Schema):
    history = ma.Nested(HistorySchema, many=True)

    class Meta:
        model = Symbol
        ordered = True
        fields = ('symbol', 'history_count', 'history')
